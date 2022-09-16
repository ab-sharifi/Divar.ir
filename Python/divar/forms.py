from flask_wtf import FlaskForm
from wtforms import(
     SubmitField,
     StringField,
     PasswordField,
     validators,
     EmailField,)

from wtforms.validators import DataRequired,InputRequired
from wtforms import validators

class Register(FlaskForm):
    username = StringField(validators=[InputRequired(),validators.Length(min=8, max=128)])
    password = PasswordField(validators=[InputRequired(),validators.Length(min=8,max=128)])
    password_re = PasswordField(validators=[InputRequired(),validators.Length(min=8,max=128)])
    submit = SubmitField()


class ActiveCode(FlaskForm):
    activate_code = StringField(validators=[InputRequired()])


class Login(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(),validators.length(min=8,max=128)])
    submit = SubmitField()