import logging
import time
from typing import Callable
from uuid import uuid4
from functools import wraps

gunicorn_logger = logging.getLogger('gunicorn.error')

def task(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        task_id=uuid4()
        # print(f"[{task_id}] Task {f.__name__} started.")
        gunicorn_logger.info(f"[{task_id}]Task {f.__name__} started.")
        result=f(*args, **kwds)
        # print(f"[{task_id}] Task {f.__name__} finished.")
        gunicorn_logger.info(f"[{task_id}]Task {f.__name__} finished.")
        return result
    return wrapper

def callback_task(a,*args, **kwargs):
    pass

@task
def deploy():
    """To be implemented"""
    pass

@task
def health_check():
    #docker compose ps --format "{{.Service}} {{.State}}"
    return {"sevices":{"Weight": {"api":"running","database":"running"},
                     "Billing":{"api":"running","database":"running"}}}

# pool=TaskManager()

if __name__ == '__main__':
    print(health_check())
    # with ProcessPoolExecutor(max_workers=1) as executor:
    #     future = executor.submit(health_check)
    #     future.add_done_callback(callback_task)
        # print(future.result())
    # future.add_done_callback(callback_task)

