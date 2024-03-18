
import urllib.request

import git
from api.util import (SERVICES_PORT, ServiceDown, build_docker_image,
                      containers_health, deploy_docker_compose,
                      gunicorn_logger, repeating_task, task)

repo = git.cmd.Git("/app")
@repeating_task(10)
def monitor(service):
    """If not Successful responses urlopen will raise HTTPError"""
    try:
         urllib.request.urlopen(f"http://localhost:{SERVICES_PORT[service]}/health", timeout=5)
    except:
         raise ServiceDown(f"{service} is down")

def callback_task(a, *args, **kwargs):
   pass

@task
def deploy(branch:str):
   try:
      repo.pull()
      build_docker_image(branch)
      deploy_docker_compose(branch)  
      monitor(branch)
   except:
      return False

def health_check():
   services = containers_health()
   for name in services:
      try:
         urllib.request.urlopen(
               f"http://localhost:{SERVICES_PORT[name]}/health", timeout=5)
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
