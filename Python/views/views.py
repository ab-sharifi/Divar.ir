import os
from turtle import update
import uuid
import datetime 
from . import helpers
from .helpers import login_required 
from flask import(
    jsonify,
    render_template,
    url_for,
    session,
    request,
    abort,
    flash,
    g,
    redirect,
    jsonify
)
from werkzeug.security import(
    check_password_hash,
    generate_password_hash
    )
from werkzeug.utils import secure_filename

from divar import app,db
from divar.models import MailVerification,User
from divar.Email import send_email
from divar.forms import Register, ActiveCode, Login,UserUpload

# list of cities (hard coded)
static = ['کرج','تهران','قم','مشهد','گیلان','گلستان','شیراز','اصفهان','کرمانشاه','تبریز']


@app.before_request
def before_Request():
    """
    before each request we get user status and save it to g variable 
    """
    # set up user status and access
    g.user_status = {"login" : False, 'phone':" " ,"name":"کاربر دیوار"}
    
    if session.get('user_id', False):
        UserStatus = User.query.filter(User.id==session["user_id"]).first()
        if UserStatus:
            if UserStatus.is_active == 1:
                g.user_status["login"] = True
                g.user_status["name"] = UserStatus.username
                if not UserStatus.phone:
                    g.user_status['phone'] = "شماره تماس وارد نشده است"
    
    # set up user_profile information


@app.errorhandler(500)
def error_500():
    db.session.rollback()
    return "Error 500"



# index home route
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":
        if not session.get("city"):
            return render_template("first-index/index.html",cities=static)
        else:
            return render_template("home-index/index.html",user_status=g.user_status)
    
    if request.method == "POST":
        if request.form.get("email",None) != None:
            email = request.form.get("email")



@app.route("/s/<string:city>" ,methods=["GET"])
def index_city(city):
    if city in static:
        session["city"] = city
    return redirect(url_for("index"))


@app.route("/login/",methods=["POST","GET"])
def login():
    form = Login(request.form)
    
    if request.method == "GET":
        return render_template("login/index.html",user_status=g.user_status,form=form)
    
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("login/index.html",user_status=g.user_status,form=form)
        
        if form.validate_on_submit():
            # query to db to find user with email
            login_user = User.query.filter_by(email=form.email.data).first()
            if not login_user:
                flash("ایمیل کاربر یافت نشد","danger")
                return render_template("login/index.html",user_status=g.user_status,form=form)
            #check user password
            if (not check_password_hash(login_user.password ,form.password.data)):
                flash("پسورد وارد شده صحیح نمی باشد","warning")
                return render_template("login/index.html",user_status=g.user_status,form=form)
            if not session.get("user_id",None):
                session["user_id"] = login_user.id
            # check user account is activated or not
            if not login_user.is_active == 1:
                # delete user from database
                login_user_mail = MailVerification.query.filter(MailVerification.email==login_user.email).first()
                db.session.delete(login_user)
                db.session.delete(login_user_mail)
                db.session.commit()
                db.session.rollback()
                flash("اکانت کاربری شما فعال نمی باشد لطفا دوباره اقدام به ساخت اکانت و فعال سازی آن کنید","danger")
                
                return redirect(url_for("login"))
            return redirect(url_for("user_profile"))


@app.route("/register/", methods=["POST","GET"])
def register():
    """
    register users and if user login to his account and want to register another
    account he should logut from his last account

    """
    
    form = Register()
    form_active_code = ActiveCode()

    if request.method == "GET":
        # if user request resend code 
        if session.get("resend"):
            if session.get("resend") == True:
                session.pop("resend")
                return render_template("activate_code.html", user_status=g.user_status, user_id=session["user_id"], form=form_active_code )
        
        return render_template("register/index.html",user_status=g.user_status,form=form)
    

    if request.method == "POST":

        if not form.validate(): 
            return render_template("register/index.html",user_status=g.user_status,form=form)

        if form.validate():
            # check user duplicate in db
            db_duplicate = MailVerification.query.filter(MailVerification.email == form.email.data.strip()).first()

            if db_duplicate:
                if (db_duplicate.activated == 1): 
                    flash("ایمیل قبلا ثبت شده است", "danger")
                    return render_template("register/index.html",user_status=g.user_status, form=form)
                
                # delete user if it already exists and did not activate his account
                if (db_duplicate.activated == 0):
                    old_user = User.query.filter(User.email == form.email.data.strip()).first()
                    db.session.delete(db_duplicate)
                    db.session.delete(old_user)
                    db.session.commit()
                    db.session.rollback()
                    form.data.clear()
                    flash("لطفا اطلاعات را پر کنید", "info")
                    return render_template("register/index.html",user_status=g.user_status, form=form)

            # duplicate request handler
            if not db_duplicate:
                
                # add to user db 
                new_user = User(email =form.email.data.strip(),password=generate_password_hash(form.password.data.strip()),
                username=form.username.data.strip())

                # create time and code 
                code = helpers.code_generator()
                time_send = datetime.datetime.utcnow()
                exp_time = time_send + datetime.timedelta(minutes=3)

                new_user_mail = MailVerification(email=form.email.data.strip(),send_time=time_send,
                exp_time=exp_time,
                user_id=new_user.id,
                active_code=code)
                db.session.add_all([new_user_mail,new_user])


                if(send_email(form.email.data.strip(),code)):
                    # if email was succesfully send it we add users to db
                    # otherwise we rollback it 
                    
                    db.session.commit()
                    # commit for get user id
                    new_user_mail.user_id = new_user.id
                    db.session.add(new_user_mail)
                    db.session.commit()

                    if session.get("user_id",None):
                        session.pop("user_id")
                    session["user_id"] = new_user.id
                    # remove user login session if it have
                    form.data.clear()
                    return render_template("activate_code.html", user_status=g.user_status, user_id=new_user.id, form=form_active_code)
                else:
                    flash("119 خطایی رخ داده است دوباره امتحان کنید !", "danger")
                    db.session.rollback()
                    return render_template("register/index.html", user_status=g.user_status, form=form)

            else:
                return redirect(url_for("register"))


@app.route("/register/v/", methods=["POST", "GET"])
@login_required
def verification_code():
    if request.method == "GET":
        return redirect(url_for("index"))


    if request.method == "POST":
        uuid_user_value = request.form.get("uuid_user_value",None).strip()
        code_activation = request.form.get("activate_code", None).strip()
        
        if not code_activation or not uuid_user_value:
            flash("درخواست دارای اشکال است","warning")
            return redirect(url_for("register")) 

        if uuid_user_value == None or (uuid_user_value != str(session["user_id"])):
            flash("200 خطایی در ثبت نام شما رخ داده است دوباره سعی کنید","danger")
            return redirect(url_for("register"))


        # check code validation and time
        check_db = MailVerification.query.filter(MailVerification.user_id==session["user_id"]).first()
        if not check_db:
            flash("207 خطایی رخ داده است ", "warning")
            return redirect(url_for("register"))

        now_time = datetime.datetime.utcnow()

        if (now_time > check_db.exp_time):
            # if token is expired delete user and redirect it
            mail_obj = MailVerification.query.filter(MailVerification.user_id == session["user_id"]).first()
            db.session.delete(mail_obj)
            user_obj = User.query.filter(User.id==session["user_id"]).first()
            db.session.delete(user_obj)
            db.session.commit()
            flash("کد منقضی شده است دوباره تلاش کنید", "warning")
            return redirect(url_for("register"))    
        else:
            # check code
            if (check_db.active_code == int(code_activation)):
                user_obj = User.query.filter(User.id==session["user_id"]).first()
                user_obj.is_active = 1
                check_db.activated = 1
                db.session.add_all([user_obj,check_db])
                db.session.commit()
                flash("حساب کاربری با موفقیت ساخته شد ", "success")
                return redirect(url_for("login"))

            else:
                flash("233 مدت اعتبار کد گذشته است دوباره امتحان کنید", "danger")
                return redirect(url_for("register"))



@app.route("/resend/", methods=["POST", "GET"])
@login_required
def resend():
    """
    this view get uuid => user_id
    and if not activated user send agian code to user account
    """


    if request.method == "GET":
        return redirect(url_for("index"))
    
    if request.method == "POST":
        form_active_code = ActiveCode()
        uuid_user_value = request.form.get('uuid_user_value')
        
        if not uuid_user_value:
            flash("مشکلی در درخواست شما وحود دارد/ بعدا امتحان کنید","danger")
            return redirect(url_for("register"))
        
        # check user is activate or not
        validate_user_db = MailVerification.query.filter(MailVerification.user_id==uuid_user_value).first()
        if not validate_user_db:
            flash("مشکلی در درخواست شما وحود دارد/ بعدا امتحان کنید","danger")
            return redirect(url_for("register"))
        if validate_user_db.activated == 1:
            return redirect(url_for("profile"))
        
        if validate_user_db.activated == 0:
            # update activated code 
            new_code = helpers.code_generator()
            validate_user_db.active_code = new_code
            # update time
            exp_time = datetime.datetime.utcnow() +  datetime.timedelta(minutes=3)
            validate_user_db.exp_time = exp_time
            db.session.add(validate_user_db) 
            db.session.commit()
            if  (send_email(validate_user_db.email, new_code)):
                # set to true to route register
                session["resend"] = True
                flash("کد تایید جدید با موفقیت ارسال شد","success")
                return redirect(url_for("register",_method="POST"))
            else:
                flash("خطایی رخ داد دوباره امتحان کنید","danger")
                return redirect(url_for("register"))




@app.route("/profile/", methods=["GET"])
@login_required
def user_profile():
    form = UserUpload()

    if request.method == "GET":
        # emtyp user placeholder information 
        user={}
        
        if (session.get("user_id")):
            # query for user images in db
            user_in_dn = User.query.filter(User.id==session["user_id"]).first()
            if user_in_dn:
                img_profile = "/static/uploads/images/" + user_in_dn.profile_image
                
                user = {"image" : img_profile, "join_date" : user_in_dn.create_time}
                
                if user_in_dn.username:
                    user["username"] = user_in_dn.username
                
                if user_in_dn.phone:
                    user["phone"] = user_in_dn.phone
                
                if user_in_dn.email:
                    user["email"] = user_in_dn.email

                return render_template("user/index.html",form=form,user=user)
            else:
                return redirect(url_for("index"))
        else:
            return redirect(url_for("index"))


@app.route("/profile/" , methods=["POST"])
@login_required
def profile():
    form = UserUpload()

    if request.method == "POST":
        if form.validate():
            if request.files:
                img = request.files.get("file", None)
                image_name = str(uuid.uuid1()) + "-" + img.filename
                image_name = secure_filename(image_name)

                if len(image_name) > 50:
                    image_name = image_name[40::]

                check_user = User.query.filter(User.id == session["user_id"]).first()
                if (check_user):
                    # delete previous picture
                    pri_img = check_user.profile_image
                    if  pri_img != app.config["DEFAULT_PICTURE"]:
                        os.remove(os.path.join(app.config["UPLOAD_FOLDER"],pri_img))
                    # replace pictures
                    
                    check_user.profile_image = image_name
                    path = (os.path.join(app.config["UPLOAD_FOLDER"],image_name))
                    img.save(path)
                    db.session.add(check_user)
                    db.session.commit()
                    return redirect(url_for("user_profile"))
                else:
                    return redirect(url_for("user_profile"))
            else:
                return redirect(url_for("user_profile"))
        else:
            return redirect(url_for("user_profile"))





@app.route("/logout/", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))











@app.route("/temp")
def temp():
    form=ActiveCode()
    return render_template("activate_code.html",user_status=g.user_status,form=form)


@app.route("/temp1")
def temp1():
    return render_template("post-page/index.html",user_status=g.user_status)


@app.route("/temp2",methods=["POST","GET"])
def temp2():
    if request.method == "GET":
        form = UserUpload()
        return render_template("user/profile.html",user_status=g.user_status,form=form)
    if request.method == "POST":
        form = UserUpload(request.form)
        if form.validate_on_submit():
            pass
        else:
            return render_template("user/profile.html",user_status=g.user_status,form=form)


