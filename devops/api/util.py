import time
import sched
import logging
import sqlite3
from uuid import uuid4
from functools import wraps
from threading import Thread
from datetime import datetime


import docker
from config import DEFAULT_STATUS, SERVICES_PORT

client = docker.from_env()
scheduler = sched.scheduler(time.time, time.sleep)
gunicorn_logger = logging.getLogger('gunicorn.error')
con = sqlite3.connect("test.sqlite", check_same_thread=False)
cur = con.cursor()


class ServiceDown(Exception):
    pass

def repeating_task(interval: int):
    """Decorator for repeating a tasks and running
    in a separate thread

    :param int interval: The interval in seconds
    """
    def decorator(func):
        def periodic(scheduler, action, actionargs=()):
            """Runs the function and than re-schedules 
            """
            scheduler.enter(interval, 1, periodic,
                            (scheduler, action, actionargs))
            try:
                action(*actionargs)
            except Exception as exc:
                scheduler.cancel(scheduler.queue[0])
                gunicorn_logger.error(exc.args[0])

        def start_scheduler(func, *args, **kwargs):
            scheduler = sched.scheduler(time.time, time.sleep)
            periodic(scheduler, func, args)
            scheduler.run()

        @wraps(func)
        def wrap(*args, **kwargs):
            print(2)
            func_hl = Thread(target=start_scheduler,
                             args=(func, *args), kwargs=kwargs)
            func_hl.start()
            return func_hl
        return wrap
    return decorator


def task(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        task_id = uuid4()
        cur.execute("INSERT INTO tasks VALUES(?, ?, ?)",
                    (str(task_id), f.__name__, datetime.today()))
        con.commit()
        gunicorn_logger.info(f"[{task_id}]Task {f.__name__} started.")
        result = f(*args, **kwds)
        gunicorn_logger.info(f"[{task_id}]Task {f.__name__} finished.")
        return result
    return wrapper


def init_db():
    cur.execute("""CREATE TABLE if not exists tasks(
    id TEXT PRIMARY KEY,
    name TEXT,
    created_at datetime DEFAULT CURRENT_TIMESTAMP)""")

def containers_health():
    services=DEFAULT_STATUS.copy()
    for container in client.containers.list(all=True):
        if "devops" not in container.name:
            services[container.labels["com.docker.compose.project"]].update(
                {container.labels['com.docker.compose.service']:container.status})
    return services
