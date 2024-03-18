from flask import Flask,request,jsonify,g
from swagger_ui import api_doc
from multiprocessing import Pool
from pathlib import Path
from api.util import init_monitor_db,SERVICES_PORT,scheduler
from api.tasks import gunicorn_logger,deploy,health_check,monitor

pool=Pool(1)

def setup(app:Flask):
   """configuration and setup"""
   app.logger.handlers = gunicorn_logger.handlers
   app.logger.setLevel(gunicorn_logger.level)
   api_doc(app, config_path=Path(__file__).parent.joinpath("swagger","openapi.json"), url_prefix='/api/doc', title='API doc')
   init_monitor_db()
   for service in SERVICES_PORT:
        monitor(service)

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
      if data['action'] =='closed' and data['pull_request']['merged']:
         results=pool.apply_async(
            deploy,kwds={'branch':data['pull_request']['head']['ref']})
      return "ok"
   
   return app
