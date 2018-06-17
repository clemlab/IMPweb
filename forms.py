from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

from wtforms import Form, BooleanField, StringField, TextAreaField, validators

class RegistrationForm(Form):
    email = StringField('Email Address', [validators.DataRequired(), validators.Length(min=6, max=35)])
    jobname = StringField('Job Name', [validators.DataRequired(), validators.Length(max=100)])
    sequence = TextAreaField('Sequence', [validators.DataRequired(), validators.Length(max=100)])
    method = TextField('Sequence', [validators.DataRequired(), validators.Length(max=100)])
    accept_tos = BooleanField('Display Publically?', [validators.DataRequired()])
