from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import Length

class InputText(FlaskForm):
    inputtext = TextAreaField('Input Text', validators=[Length(min=0, max=14000)])
    submit = SubmitField('Submit')


class InputTicker(FlaskForm):
    ticker = StringField('Enter 1 Stock Ticker', render_kw={"placeholder": "AAPL"}, validators=[Length(min=0, max=5)])
    submit = SubmitField('Submit')