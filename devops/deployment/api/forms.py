from wtforms import Form,SelectField,SubmitField

class VersionForm(Form):
   version= SelectField('version',validate_choice=False)
   submit=SubmitField('revet')