from flask import Flask,request,jsonify
from swagger_ui import api_doc
from multiprocessing import Pool,Process
from util import init_db,SERVICES_PORT

from tasks import gunicorn_logger,deploy,health_check,monitor

def setup():
   init_db()
   for service in SERVICES_PORT:
        monitor(port=SERVICES_PORT[service],service=service.capitalize())

app=Flask(__name__)
setup()
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

api_doc(app, config_path='./swagger/openapi.json', url_prefix='/api/doc', title='API doc')
pool=Pool(1)

@app.get("/health")
def health():
    gunicorn_logger.info("health")
    result=health_check()
    return jsonify(result)

@app.post("/trigger")
def trigger():
    data=request.get_json()
    results=pool.apply_async(deploy,())
    print(data)
    return "ok"


if __name__=="__main__":
    app.run(port=8000)