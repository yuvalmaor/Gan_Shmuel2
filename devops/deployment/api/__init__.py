from pathlib import Path
from multiprocessing import Pool

from api.tasks import deploy, gunicorn_logger, health_check, monitor
from api.util import SERVICES_PORT, init_monitor_db, scheduler
from flask import Flask, jsonify, request
from swagger_ui import api_doc

pool=Pool(1)

def setup(app:Flask):
   """configuration and setup"""
   app.logger.handlers = gunicorn_logger.handlers
   app.logger.setLevel(gunicorn_logger.level)
   api_doc(app, config_path=Path(__file__).parent.joinpath("swagger","openapi.json"), 
           url_prefix='/api/doc', title='API doc')
   init_monitor_db()
   for service in SERVICES_PORT:
        monitor(service)

def create_app():

   app=Flask(__name__)
   setup(app)

   @app.get("/health")
   def health():
      """Route for services health status
      """
      result=health_check()
      return jsonify(result)

   @app.post("/trigger")
   def trigger():
      """Route for Github webhook to send a trigger when
      there is a change in a 'pull request'.
      
      The request must answer all of the follwoing 
      requirements in order porceeding to deploy:

      #. The "action" is 'closed'.
      #. ['pull_request']['merged'] is true
      #. The branch is in ['main','weight','billing']

      """
      data=request.get_json()

      branch=data['pull_request']['base']['ref']
      merged_from=data['pull_request']['head']['ref']
      merged_commit=data['pull_request']['head']['sha']

      if all((data['action'] =='closed',data['pull_request']['merged'], 
             branch in ('main','weight','billing'))):
         gunicorn_logger(f"Recived trigger for branch: {branch}, changes mergred from branch: {merged_from}")
         results=pool.apply_async(
               deploy,kwds={'branch':branch,'merged':merged_from,'merged_commit':merged_commit})         
      return "ok"
   
   return app
