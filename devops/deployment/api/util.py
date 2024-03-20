import os
import time
import sched
import logging
import sqlite3
from uuid import uuid4
from functools import wraps
from threading import Thread
from datetime import datetime


import docker
from api.config import DEFAULT_STATUS, SERVICES_PORT

client = docker.from_env()

GIT_PATH = os.getenv("GIT_PATH")

gunicorn_logger = logging.getLogger('gunicorn.error')
scheduler = sched.scheduler(time.time, time.sleep)
con = sqlite3.connect("tasks.sqlite", check_same_thread=False)
cur = con.cursor()

class ServiceDown(Exception):
   pass
class EmailException(Exception):
   pass

def repeating_task(interval: int):
   """Decorator for repeating a tasks

    :param int interval: The interval in seconds
    """
   def decorator(func):
      def periodic(scheduler:sched.scheduler, action, aargs:tuple=(),akwarg:dict={}):
         """Runs the function and than re-schedules 
         """
         s=scheduler.enter(interval, 1, periodic,
                        (scheduler, action, aargs,akwarg))
         try:
               action(*aargs,**akwarg)
         except Exception as exc:
            scheduler.cancel(s)
            gunicorn_logger.error(exc.args[0])

      @wraps(func)
      def wrap(*args, **kwargs):
         periodic(scheduler, func, args,kwargs)
      return wrap
   return decorator

def task(f):
   @wraps(f)
   def wrapper(*args, **kwargs):
      task_id = uuid4()
      cur.execute("INSERT INTO tasks VALUES(?, ?, ? ,?)",
                  (str(task_id), f.__name__, "{}".format(str(kwargs)[1:-1]),datetime.today()))
      con.commit()
      gunicorn_logger.info(f"[{task_id}]Task {f.__name__} started.")
      result = f(*args, **kwargs)
      gunicorn_logger.info(f"[{task_id}]Task {f.__name__} finished.")
      return result
   return wrapper

def init_monitor_db():
   cur.execute("""CREATE TABLE if not exists tasks(
   id TEXT PRIMARY KEY,
   name TEXT,
   additional_info TEXT,
   created_at datetime DEFAULT CURRENT_TIMESTAMP)""")
   cur.execute("""CREATE TABLE if not exists images(
   service TEXT,
   tag TEXT UNIQUE,
   works Boolean)""")
   t=Thread(target=scheduler.run,args=())
   t.start()

def insert_image(service:str,tag:str):
      cur.execute("INSERT INTO images VALUES(?, ?, ?)",
               (service,tag,False))
      con.commit()
      return cur.lastrowid

def update_image(status:bool,rowid:int):
   cur.execute("UPDATE images set works= ? where rowid = ?",(status,rowid))
   con.commit()

def get_image_list(service:str)->tuple[list[str],str]:
   latest_tags = client.images.get(f"{service}:latest").tags
   latest_tags.remove(f"{service}:latest")
   latest_tag = next(i for i in latest_tags if 'new' not in i).removeprefix(f"{service}:")
   cur.execute("SELECT tag FROM images WHERE service = ? and works = 1",(service,))
   rows = [i[0] for i in cur]
   return rows,latest_tag
   

def containers_health():
   services=DEFAULT_STATUS.copy()
   container_list=client.containers.list(all=True)
   if container_list:
      for container in container_list:
         cname=container.name
         if "test" not in cname and ("billing" in cname or "weight" in cname):
            services[container.labels["com.docker.compose.project"]].update(
               {container.labels['com.docker.compose.service']:container.status})
   return services