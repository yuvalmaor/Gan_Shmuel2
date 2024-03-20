from flask import Blueprint,send_file,render_template,request,url_for,redirect
import os
from api.tasks import revert
from api.util import get_image_list
from api.ui.forms import VersionForm
LOG_FILE=os.getenv("LOG_FILE")
web=Blueprint("web",__name__)

@web.get("/revert")
@web.get("/revert/<service>")
def request_revert(service=None):
   if service and service in ['weight','billing']:
      form=VersionForm()
      versions,current=get_image_list(service)
      form.version.choices=versions
      return render_template('revert.html',service=service,current=current,
                              form=form)
   
   return render_template('revert.html',service=service)

@web.post("/revert/<service>")
def revert_version(service):
   if service and service in ['weight','billing']:
      form=VersionForm(request.form)
      if form.validate():
         revert(service,form.version.data,form.email.data)
   return redirect(url_for('web.request_revert'))

@web.get("/logs")
def logs():
   return render_template('logs.html')

@web.get("/log-download")
def download_log():
   return send_file(LOG_FILE,mimetype="text/plain",as_attachment=True)

@web.get("/log-stream")
def log_stream():
   with open(LOG_FILE) as fp:
      text = fp.read()
   return text ,{'Content-Type':'text/plain'}