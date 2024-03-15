import logging
import time

gunicorn_logger = logging.getLogger('gunicorn.error')

def deploy():
    """To be implemented"""
    pass

def health_check():
    return "ok"