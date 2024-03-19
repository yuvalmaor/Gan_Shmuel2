from wtforms import Form,SelectField

class VersionForm(Form):
   version= SelectField('version',validate_choice=False)