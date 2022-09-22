from flask_wtf import FlaskForm
from wtforms import(
     SubmitField,
     StringField,
     PasswordField,
     validators,
     EmailField,
     FileField,
     )

from wtforms.validators import DataRequired,InputRequired,Email, EqualTo
from wtforms import validators

class Register(FlaskForm):
    username = StringField(validators=[InputRequired("نام کاربری وارد نشده است"),DataRequired(),validators.Length(min=8, max=128)])
    email = EmailField(validators=[InputRequired("ایمیل وارد نشده است"), DataRequired() ,Email("آدرس ایمیل وارد شده صحیح نمی باشد")])
    password = PasswordField(validators=[InputRequired("پسورد وارد نشده است"),DataRequired(),validators.Length(min=8,max=128)])
    password_re = PasswordField(validators=[InputRequired("تکرار پسورد وارد نشده است"),DataRequired(),validators.Length(min=8,max=128), EqualTo('password',message="رمز عبور وارد شده یکسان نمی باشد")])
    submit = SubmitField()


class ActiveCode(FlaskForm):
    # This field does not have any validation methods
    # its handel it in js in frontend
    activate_code = StringField(validators=[])


class Login(FlaskForm):
    email = EmailField(validators=[DataRequired("ایمیل وارد نشده است"),InputRequired("ایمیل وارد نشده است"),Email("آدرس ایمیل وارد شده صحیح نمی باشد")])
    password = PasswordField(validators=[DataRequired(),InputRequired("پسورد وارد نشده است"),validators.length(min=8,max=128)])
    submit = SubmitField()


class UserUpload(FlaskForm):
    file = FileField(validators=[DataRequired(),InputRequired()])
    submit = SubmitField() 