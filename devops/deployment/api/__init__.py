from flask import Flask,request,jsonify
from swagger_ui import api_doc
from multiprocessing import Pool
from api.util import init_db,SERVICES_PORT

from api.tasks import gunicorn_logger,deploy,health_check,monitor

pool=Pool(1)

def setup(app:Flask):
   """configuration and setup"""
   app.logger.handlers = gunicorn_logger.handlers
   app.logger.setLevel(gunicorn_logger.level)
   api_doc(app, config_path='./swagger/openapi.json', url_prefix='/api/doc', title='API doc')
   init_db()
   for service in SERVICES_PORT:
        monitor(port=SERVICES_PORT[service],service=service.capitalize())

def create_app():

   app=Flask(__name__)
   setup(app)

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
   return app


if __name__=="__main__":
    app=create_app()
    app.run(port=8000)