from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit_btn = SubmitField('Search')
    catch_btn = SubmitField('Catch me!')