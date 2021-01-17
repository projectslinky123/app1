from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length

class InputText(FlaskForm):
    inputtext = TextAreaField('Input Text', validators=[Length(min=0, max=14000)])
    submit = SubmitField('Submit')