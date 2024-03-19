from api.ui import ui_bp
from api.util import get_image_list
from forms import VersionForm

from flask import render_template

@ui_bp.get("/revert")
@ui_bp.get("/revert/<service>")
def revert(service=None):
   if service:
      form=VersionForm()
      versions,current=get_image_list(service)
      form.version.choices=versions
      return render_template('revert.html',service=service,form=form,
                             current=current)
   
   return render_template('revert.html',service=service)