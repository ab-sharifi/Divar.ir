from wtforms import validators
from flask_wtf import FlaskForm

from wtforms import(
     SubmitField,
     StringField,
     PasswordField,
     validators,
     EmailField,
     FileField,
     TextAreaField,
     )

from wtforms.validators import DataRequired,InputRequired,Email, EqualTo

class Register(FlaskForm):

    username = StringField(validators=[
        InputRequired("نام کاربری وارد نشده است"),
        DataRequired(message="ورود داده الزامی است"),
        validators.Length(min=8, max=128,message="حداقل طول نام کاربری 8 و حداکثر 128 کاراکتر است")])
    
    email = EmailField(validators=[
        InputRequired("ایمیل وارد نشده است"),
        DataRequired(message="ورود داده الزامی است"),
        Email("آدرس ایمیل وارد شده صحیح نمی باشد")])
    
    password = PasswordField(validators=[
        InputRequired("پسورد وارد نشده است"),
        DataRequired(message="داده ای وارد نشده است"),
        validators.Length(min=8,max=128)])
    
    password_re = PasswordField(validators=[
        InputRequired("تکرار پسورد وارد نشده است"),
        DataRequired(message="ورود داده الزامی است"),
        validators.Length(min=8,max=128),
        EqualTo('password',message="رمز عبور وارد شده یکسان نمی باشد")])
    
    submit = SubmitField()


class ActiveCode(FlaskForm):
    # This field does not have any validation methods
    # its handel it in js in frontend
    activate_code = StringField(validators=[])


class Login(FlaskForm):
    
    email = EmailField(validators=[
        DataRequired("ایمیل وارد نشده است"),
        InputRequired("ایمیل وارد نشده است"),
        Email("آدرس ایمیل وارد شده صحیح نمی باشد")])
    
    password = PasswordField(validators=[
        DataRequired(message="پسورد وارد نشده است"),
        InputRequired(message="پسورد وارد نشده است"),
        validators.length(min=8,max=128)])
    
    submit = SubmitField()


class UserUpload(FlaskForm):
    file = FileField(validators=[DataRequired(),InputRequired()])
    submit = SubmitField() 


class RegisterPost(FlaskForm):
    
    title_post = StringField(validators=[
        DataRequired(message="عنوان آگهی اجباری است"),
        InputRequired(message="داده ای در فیلد وارد نشده است"),
        validators.Length(min=2,max=128, message="حداقل کاراکتر های عنوان آگهی 2 و حداکثر 128 کاراکتر است")])
    
    caption_post = TextAreaField(validators=[
        DataRequired(message="توضیحات آگهی اجباری است"),
        InputRequired(message="داده ای در فیلد وارد نشده است"),
        validators.Length(min=2,max=256, message="حداقل کاراکتر های توضیحات آگهی 2 و حداکثر 256 کاراکتر است")])
    
    # a post can be sell or trade by users
    # so there is no validator for price field
    price_post = StringField()

    file_post = FileField()
    submit = SubmitField()