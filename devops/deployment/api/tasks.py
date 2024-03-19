
import os
import subprocess
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import git
from api.util import (GIT_PATH, SERVICES_PORT, ServiceDown, client,
                      containers_health, gunicorn_logger, insert_image,
                      repeating_task, task, update_image)
from mailjet_rest import Client

api_key=os.getenv("API_KEY")
api_secret=os.getenv("API_SECRET")
mailjet = Client(auth=(api_key, api_secret))
#: Class for performing git commands on local git repo
repo = git.cmd.Git(GIT_PATH)

class EmailException(Exception):
   pass

class GitException(Exception):
   pass

@repeating_task(10)
def monitor(service):
    """If responses is not Successful urlopen will raise HTTPError"""
    try:
         urllib.request.urlopen(f"http://ec2-13-200-131-223.ap-south-1.compute.amazonaws.com:{SERVICES_PORT[service]}/health", timeout=10)
    except:
         raise ServiceDown(f"{service} is down")

def git_pull(branch:str,merged_commit:str) -> str:
   """Switchs to the specified branch and pulls 
   the changes

   :param branch: The brance that needs to be updated
   :type branch: str
   :param merged_commit: The id of the commit that was merged
   :type merged_commit: str
   :raises GitException: When git fails to switch branchs
   :return: The email of the person that performed the merge
   :rtype: str
   """
   gunicorn_logger.info(f"checkout: {repo.checkout(branch)}")
   if not repo.branch("--show-current") == branch:
      raise GitException(f"Failed to checkout branch: {branch}")
   
   gunicorn_logger.info(f"pull: {repo.pull()}")
   return repo.log(f"--format=%ae", f"{merged_commit}^!")

def build_docker_image(service:str) -> str:

   """Builds the image for the specified service with 
   the requested tag.

   :param service: The service which requires a new image
   :type service: str
   :return: The image tag
   :rtype: str
   """
   image_tag=datetime.today().strftime("%F.%H-%M-%S")
   path= os.path.join(GIT_PATH,service)
   dockerfile= './Dockerfile'  # Name of your Dockerfile
   tag= f'{service}:{image_tag}'  # Tag for your Docker image

   gunicorn_logger.info(f"Building Docker image '{image_tag}' from '{service}'")
   image=client.images.build(path=path,dockerfile=dockerfile,tag=tag)
   image[0].tag(service,"new")
   gunicorn_logger.info("Build completed successfully.")

   return image_tag

def deploy_docker_compose(service:str) -> None:
   """Runs docker-compose for the specified service

   :param service: The service name
   :type service: str
   """
   gunicorn_logger.info(f"Deploying Docker Compose for {service}...")
   subprocess.run(["docker-compose", "-f", f"{GIT_PATH}/{service}/docker-compose.yml", "up", "-d"])


def testing():
   """Run tests on the new image on a testing envirment
   """
   gunicorn_logger.info(f"Deploying Docker Compose for testing...")
   result =subprocess.run( ["docker-compose", "-f", f"{GIT_PATH}/billing/test-docker-compose.yml", "up", "-d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
   if result.returncode != 0:

      gunicorn_logger.error(f"Errors or failures occurred during the compose tests.")
      gunicorn_logger.error(result.stdout+result.stderr)
      msg=result.stdout+result.stderr
      raise Exception(msg)

   else:
      gunicorn_logger.info(f"compose test billingsuccessfully.")
   result =subprocess.run( ["docker-compose", "-f", f"{GIT_PATH}/weight/test-docker-compose.yml", "up", "-d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
   if result.returncode != 0:

      gunicorn_logger.error(f"Errors or failures occurred during the compose tests.")
      gunicorn_logger.error(result.stdout+result.stderr)
      msg=result.stdout+result.stderr
      
      raise Exception(msg)

   else:
      gunicorn_logger.info(f"compose test weight successfully.")
   #run pytest
   command = ["pytest", f"{GIT_PATH}/billing/tests", f"{GIT_PATH}/weight/tests"]

   # Run the command and capture the output and errors
   result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

   # Check if the process had an error (non-zero exit code)
   if result.returncode != 0:
      
      gunicorn_logger.error(f"Errors or failures occurred during the tests.")
      msg=result.stdout+result.stderr
      raise Exception(msg)
      
   else:
      gunicorn_logger.info(f"All tests passed successfully.")

 
def production(service:str):
   """Moves new service version to production after the tests.

      #. Gives the new image the tag "latest"
      #. Runs compose up for the specified service

   :param service: The service which recived an update
   :type service: str
   """
   client.images.get(f'{service}:new').tag(service,'latest')
   deploy_docker_compose(service)  
   monitor(service)

@task
def deploy(branch:str,merged:str,merged_commit:str) -> None:
   """Performes the deployment process

   :param branch: The branch to deploy
   :type branch: str
   :param merged: The merged branch
   :type merged: str
   :param merged_commit: The id of the commit that was merged
   :type merged_commit: str
   """
   prod= any((branch=='main',))
   email=None
   try:
      email=git_pull(branch,merged_commit)
      image_tag=build_docker_image(merged if prod else branch)
      testing()
      if branch=='main':
         rowid=insert_image(merged,image_tag)
         production(merged)
         update_image(True,rowid)
      msg={"massage":"The deployment to the {} environment finished successfully".format(
         "production" if prod else "testing"
      ),"subject":"Deployment finished successfully","recipiant":email}
   except Exception as exc:
      msg={"massage":exc,"subject":"Deployment failure","recipiant":email}
      gunicorn_logger.error(exc)
   if email:
      gunicorn_logger.info('test')
      send_mail(**msg)

@task
def revert(service:str,image_tag,email):
   try:
      client.images.get(f"{service}:{image_tag}").tag(service,'latest')
      deploy_docker_compose(service)
      msg={"massage":f"Revert to {service}:{image_tag} finished successfully",
           "subject":"Revert finished successfully","recipiant":email}
   except Exception as exc:
      gunicorn_logger.error(exc)
      msg={"massage":f"Revert to {service}:{image_tag} failed",
           "subject":"Revert failure","recipiant":email}
   send_mail(**msg)

def send_mail(massage:str,subject:str,recipiant:str="yuvalproject305@gmail.com"):
   # gunicorn_logger.info("try to send email to "+str(recipiant))
   msg_data = {
   'Messages': [
      {
      "From": {
         "Email": "yuvalproject305@gmail.com",
         "Name": "yuval"
      },
      "To": [ 
         {
         "Email": recipiant,

         } ],
      "Subject": subject,
      "TextPart": massage,
      }
   ]
   }
   gunicorn_logger.info("1")  
   result = mailjet.send.create(data=msg_data)
   gunicorn_logger.info("2")  
   if result.status_code != 200:
      gunicorn_logger.error("Failed to send email to"+str(recipiant))
   else:
      gunicorn_logger.info("email has been sended to "+str(recipiant))
   gunicorn_logger.info("done")  

def health_check() -> dict:
   """Performs service health check

   :return: A dictionary with the services status
   :rtype: dict
   """
   services = containers_health()
   for name in services:
      try:
         urllib.request.urlopen(
               f"http://ec2-13-200-131-223.ap-south-1.compute.amazonaws.com:{SERVICES_PORT[name]}/health", timeout=10)
      except:
         services[name]['api'] = 'down'
   return services

if __name__ == '__main__':
    print(health_check())
    # with ProcessPoolExecutor(max_workers=1) as executor:
    #     future = executor.submit(health_check)
    #     future.add_done_callback(callback_task)
    # print(future.result())
    # future.add_done_callback(callback_task)
