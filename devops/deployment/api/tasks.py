
import os
import subprocess
import urllib.request

import git
from mailjet_rest import Client
from api.util import (GIT_PATH, SERVICES_PORT, ServiceDown, client,
                      containers_health, gunicorn_logger, repeating_task, task)


api_key=os.getenv("API_KEY")
api_secret=os.getenv("API_SECRET")

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
   return repo.log(f"--format='%ae'", f"{merged_commit}^!")

def build_docker_image(service:str, image_tag:str ="latest") -> None:
   """Builds the image for the specified service with 
   the requested tag

   :param service: The service which requires a new image
   :type service: str
   :param image_tag: The image tag , defaults to "latest"
   :type image_tag: str, optional
   """

   path= os.path.join(GIT_PATH,service)
   dockerfile= './Dockerfile'  # Name of your Dockerfile
   tag= f'{service}:{image_tag}'  # Tag for your Docker image

   gunicorn_logger.info(f"Building Docker image '{image_tag}' from '{service}'")
   client.images.build(path=path,dockerfile=dockerfile,tag=tag) 
   gunicorn_logger.info("Build completed successfully.")

def deploy_docker_compose(service:str) -> None:
   """Runs docker-compose for the specified service

   :param service: The service name
   :type service: str
   """
   gunicorn_logger.info(f"Deploying Docker Compose for {service}...")
   subprocess.run( ["docker-compose", "-f", f"{GIT_PATH}/{service}/docker-compose.yml", "up", "-d"])

def send_mail(massage:str,subject:str,recipiants:list[str]):
   mailjet = Client(auth=(api_key, api_secret), version='v3.1')
   data = {
   'Messages': [
      {
      "From": {
         "Email": "yuvalproject305@gmail.com",
         "Name": "yuval"
      },
      "To": [ 
         {
         "Email": recipiant,
         } for recipiant in recipiants ],
      "Subject": subject,
      "HTMLPart": "<h3>"+massage+"</h3>",
      "CustomID": "AppGettingStartedTest"
      }
   ]
   }
   result = mailjet.send.create(data=data)
   if result.status_code != 200:
      raise EmailException("Failed to send email")   

# yuval
def testing():
   # to be implemented
   # * test compose up 
   # * run tests
   # return bool
   pass
# end yuval

# gal 
def production():
   # rename image tag to latest
   # compose up
   pass

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
   try:
      git_pull(branch,merged_commit)
      build_docker_image(branch)
      deploy_docker_compose(branch)  
      monitor(branch)
   except Exception as exc:
      gunicorn_logger.error(exc)

if __name__ == '__main__':
    print(health_check())
    # with ProcessPoolExecutor(max_workers=1) as executor:
    #     future = executor.submit(health_check)
    #     future.add_done_callback(callback_task)
    # print(future.result())
    # future.add_done_callback(callback_task)
