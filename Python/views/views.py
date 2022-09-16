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
from divar import app,db
from divar.forms import Register, ActiveCode
from divar.models import MailVerification,User
from divar.Email import send_email
from . import helpers
import datetime 

# list of cities (hard coded)
static = ['کرج','تهران','قم','مشهد','گیلان','گلستان','شیراز','اصفهان','کرمانشاه','تبریز']
user_status = {"login":False, 'phone':"","name":"کاربر دیوار"}



# index home route
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":
        if not session.get("city"):
            return render_template("first-index/index.html",cities=static)
        else:
            return render_template("index-home/index.html",user_status=user_status)
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
    return render_template("login/index.html",user_status=user_status)


@app.route("/register", methods=["POST","GET"])
def register():
    
    if request.method == "GET":
        form = Register()
        return render_template("register/index.html",user_status=user_status,form=form)
    
    if request.method == "POST":
        form = Register(request.form)
        if form.validate_on_submit():
            username = request.form.get("username", None)
            email = request.form.get("email", None)
            password = request.form.get("password", None)
            password_re = request.form.get("password_re", None)
            security_qu = request.form.get("security-question", None)
            security_ans = request.form.get("security-answer", None)

            if not username :
                flash("نام کاربری را واردنشده است", "danger")
                form.username = ""
                return render_template("register/index.html",user_status=user_status,form=form)
            if not email :
                form.email = ""
                flash("ایمیل وارد نشده است", "danger")
                return render_template("register/index.html",user_status=user_status,form=form)
            if helpers.check_email(email) == False:
                form.email = ""
                flash("ایمیل وارد شده صحیح نمی باشد", "danger")
                return render_template("register/index.html",user_status=user_status,form=form)
            if not password :
                form.password = ""
                flash(" رمز عبور وارد نشده است","danger")
                return render_template("register/index.html",user_status=user_status, form=form)
            if not password_re :
                form.password_re = ""
                flash("تکرار رمز عبور وارد نشده است", "danger")
                return render_template("register/index.html",user_status=user_status, form=form)
            if password != password_re :
                flash("رمز عبور و تکرار رمز عبور یکسان نمی باشد", "danger")
                return render_template("register/index.html",user_status=user_status, form=form)

            print("now here 1")

            # check user duplicate in db
            db_duplicate = User.query.filter(User.email == email).first()
            if db_duplicate:
                flash("ایمیل قبلا ثبت شده است", "danger")
                return render_template("register/index.html",user_status=user_status, form=form)

            print("now here 2")
            # add to user db 
            new_user = User(email = email,password = password,username=username)
            db.session.add(new_user)

            code = helpers.code_generator()
            time_send = datetime.datetime.utcnow()
            exp_time = time_send + datetime.timedelta(minutes=3)

            new_user_mail = MailVerification(email=email,send_time=time_send,
            exp_time=exp_time,
            user_id=new_user.id,
            active_code=code)

            db.session.add(new_user_mail)
            print("now here 3")

            if(send_email(email,code)):
                db.session.commit()
                session["user_id"] = new_user.id
                form_active_code = ActiveCode()
                return render_template("activate_code.html", user_status=user_status, user_id=new_user.id, form=form_active_code)
            else:
                flash("119 خطایی رخ داده است دوباره امتحان کنید !", "danger")
                db.session.rollback()
                return render_template("register/index.html", user_status=user_status, form=form)
        
        # if form not validate on submit
        else:
            form = Register(request.form)
            return render_template("register", user_status=user_status, form=form)


@app.route("/register/v/", methods=["POST"])
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
        mail_obj = MailVerification.query.filter(MailVerification.user_id == session["user_id"]).first()
        db.session.delete(mail_obj)
        user_obj = User.query.filter(User.id==session["user_id"])
        db.session.delete(user_obj)
        db.session.commit()
        flash("154 کد منقضی شده است دوباره تلاش کنید", "warning")
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
            return redirect(url_for("register"))

        else:
            flash("171 مدت اعتبار کد گذشته است دوباره امتحان کنید", "danger")
            return redirect(url_for("register"))


@app.route("/temp")
def temp():
    form=ActiveCode()
    return render_template("activate_code.html",user_status=user_status,form=form)


@app.route("/temp1")
def temp1():
    return render_template("post-page/index.html")