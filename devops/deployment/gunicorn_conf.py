from multiprocessing import cpu_count
from os import environ
from logging.handlers import TimedRotatingFileHandler


bind = '0.0.0.0:' + environ.get('PORT', '8000')
workers = 1

wsgi_app="app:create_app()"

# log to stream
accesslog = "-"  
errorlog = "-"

# logconfig_dict={
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'customFormatter': {
#             'format':'[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
#             'datefmt': '%d-%m-%Y %H:%M:%S'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             "class": "logging.handlers.TimedRotatingFileHandler",
#             'formatter': 'customFormatter',
#             "filename":"test.log",
#             "when": "midnight",
#             "backupCount": 2,
#             'interval': 1
#         }
#     },
#     'loggers': {
#         'gunicorn.error': {
#             'propagate': True,
#         },
#     },
#     'root': {
#         'level': 'INFO',
#         'handlers': ['console'],
#     }
# }