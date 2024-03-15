from flask import Flask,request,jsonify
from flask.globals import g
from swagger_ui import api_doc
from multiprocessing import Pool,active_children,Process,Queue
from concurrent.futures import ProcessPoolExecutor
from tasks import gunicorn_logger,deploy


app=Flask(__name__)

app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
pool=Pool(1)
api_doc(app, config_path='./swagger/openapi.json', url_prefix='/api/doc', title='API doc')

# def callback_a():
#     pass

@app.get("/health")
def health():
    gunicorn_logger.info("health")
    pool.apply_async(deploy,())
    # gunicorn_logger.info(len(active_children()))
    #docker compose ps --format "{{.Service}} {{.State}}"
    temp={"sevices":{"Weight": {"api":"running","database":"running"},
                     "Billing":{"api":"running","database":"running"}}}
    return jsonify(temp)

@app.post("/trigger")
def trigger():
    data=request.get_json()
    print(data)
    return "ok"


if __name__=="__main__":
    app.run(port=8000)