
import urllib.request

import git
from api.util import (SERVICES_PORT, ServiceDown, build_docker_image,
                      containers_health, deploy_docker_compose,
                      gunicorn_logger, repeating_task, task,GIT_PATH)

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
   e=repo.pull()
   gunicorn_logger.info(e)
   pass

def image():
   pass

def testing():
   # to be implemented
   # * test compose up 
   # * run tests
   # return bool
   pass

def production():
   # rename image tag to latest
   # compose up
   pass

@task
def deploy(base:str,head:str):
   # base the branch to deploy(main,billing,weight)
   # head the branch that it was merged from(any branch)
   try:
      git_pull()
      build_docker_image(branch)
      deploy_docker_compose(branch)  
      monitor(branch)
   except:
      gunicorn_logger.error('error')
      return False

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
