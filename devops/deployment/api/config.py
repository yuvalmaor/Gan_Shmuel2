import os
SERVICES_PORT={"weight":8085,"billing":8090}
DEFAULT_STATUS={"weight": {"api":"down","db":"down"},
                     "billing":{"api":"down","db":"down"}}

GIT_PATH = os.getenv("GIT_PATH")