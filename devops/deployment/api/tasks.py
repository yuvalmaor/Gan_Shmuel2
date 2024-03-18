
import os
import subprocess
import urllib.request

import git
from api.util import (GIT_PATH, SERVICES_PORT, ServiceDown, client,
                      containers_health, gunicorn_logger, repeating_task, task)

repo = git.cmd.Git(GIT_PATH)
@repeating_task(10)
def monitor(service):
    """If responses is not Successful urlopen will raise HTTPError"""
    try:
         urllib.request.urlopen(f"http://ec2-13-200-131-223.ap-south-1.compute.amazonaws.com:{SERVICES_PORT[service]}/health", timeout=10)
    except:
         raise ServiceDown(f"{service} is down")

# def callback_task(a, *args, **kwargs):
#    pass

def git_pull(branch:str):
   # checkout branch
   # GitPython
   gunicorn_logger.info(f"checkout: {repo.checkout(branch)}")
   gunicorn_logger.info(f"pull: {repo.pull()}")
   pass

def build_docker_image(app:str, image_tag:str ="latest"):

   path= os.path.join(GIT_PATH,app)
   dockerfile= './Dockerfile'  # Name of your Dockerfile
   tag= f'{app}:{image_tag}'  # Tag for your Docker image

   gunicorn_logger.info(f"Building Docker image '{image_tag}' from '{app}'")
   client.images.build(path=path,dockerfile=dockerfile,tag=tag) 
   gunicorn_logger.info("Build completed successfully.")
   return True

def deploy_docker_compose(service):
      gunicorn_logger.info(f"Deploying Docker Compose for {service}...")
      subprocess.run( ["docker-compose", "-f", f"{GIT_PATH}/{service}/docker-compose.yml", "up", "-d"])

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

@task
def deploy(branch:str,merged:str):
   # branch the branch to deploy(main,billing,weight)
   # head the branch that was merged from(any branch)
   try:
      git_pull()
      build_docker_image(branch)
      deploy_docker_compose(branch)  
      monitor(branch)
   except:
      gunicorn_logger.error('error')
      return False
# end gal 

def health_check():
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
