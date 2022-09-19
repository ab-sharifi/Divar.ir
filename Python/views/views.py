import os
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
    g.user_status = {"login":False, 'phone':"","name":"کاربر دیوار"}
    # update variables



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


@app.route("/login",methods=["POST","GET"])
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
            return redirect(url_for("user_profile"))

@app.route("/register", methods=["POST","GET"])
def register():
    if session.get("user_id",None):
        session.delete("user_id")
    form = Register()
    if request.method == "GET":
        return render_template("register/index.html",user_status=g.user_status,form=form)
    

    if request.method == "POST":
        if not form.validate_on_submit(): 
            return render_template("register/index.html",user_status=g.user_status,form=form)

        if form.validate_on_submit():
            # check user duplicate in db
            db_duplicate = User.query.filter(User.email == form.email.data).first()
            if db_duplicate:
                flash("ایمیل قبلا ثبت شده است", "danger")
                return render_template("register/index.html",user_status=g.user_status, form=form)

            # add to user db 
            new_user = User(email =form.email.data,password =  generate_password_hash(form.password.data),username=form.username.data)
            db.session.add(new_user)

            code = helpers.code_generator()
            time_send = datetime.datetime.utcnow()
            exp_time = time_send + datetime.timedelta(minutes=3)

            new_user_mail = MailVerification(email=form.email.data,send_time=time_send,
            exp_time=exp_time,
            user_id=new_user.id,
            active_code=code)

            db.session.add(new_user_mail)

            if(send_email(form.email.data,code)):
                db.session.commit()
                session["user_id"] = new_user.id
                form_active_code = ActiveCode()
                return render_template("activate_code.html", user_status=g.user_status, user_id=new_user.id, form=form_active_code)
            else:
                flash("119 خطایی رخ داده است دوباره امتحان کنید !", "danger")
                db.session.rollback()
                return render_template("register/index.html", user_status=g.user_status, form=form)

@app.route("/register/v/", methods=["POST"])
@login_required
def verification_code():

    cs_us = request.form.get("cs_us",None)
    code_activation = request.form.get("activate_code",None)

    if cs_us == None or cs_us != str(session["user_id"]):
        flash("136 خطایی در ثبت نام شما رخ داده است دوباره سعی کنید","danger")
        return redirect(url_for("register"))


    # check code validation and time
    check_db = MailVerification.query.filter(MailVerification.user_id==session["user_id"]).first()
    if not check_db:
        flash("143 خطایی رخ داده است ", "warning")
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
            db.session.add(user_obj)
            db.session.add(check_db)
            db.session.commit()
            flash("حساب کاربری با موفقیت ساخته شد ", "success")
            return redirect(url_for("login"))

        else:
            flash("171 مدت اعتبار کد گذشته است دوباره امتحان کنید", "danger")
            return redirect(url_for("register"))




@app.route("/profile")
@login_required
def user_profile():
    form = UserUpload()

    return render_template("user/index.html",form=form)






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
