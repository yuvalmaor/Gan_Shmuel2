from api.ui import ui_bp
from forms import VersionForm


@ui_bp.get("/revert")
def revert():
   return "ok"