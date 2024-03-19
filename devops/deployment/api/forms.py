from wtforms import Form,SelectField,SubmitField,EmailField
from wtforms.validators import DataRequired

class VersionForm(Form):
   version= SelectField('version',validate_choice=False,validators=[DataRequired()])
   email=EmailField('Email for status notifications',validators=[DataRequired()])
   submit=SubmitField('Revert')