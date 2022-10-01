import os
import uuid
import datetime
from divar import app,db
from . import helpers
from .helpers import login_required 
from werkzeug.utils import secure_filename


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

from divar.models import( 
    MailVerification,
    User,
    Post,
    State,
    City)
from divar.Email import send_email
from divar.forms import Register, ActiveCode, Login, UserUpload, RegisterPost

# list of cities (hard coded)
static = ['کرج','تهران','قم','مشهد','گیلان','گلستان','شیراز','اصفهان','کرمانشاه','تبریز']


#########################  Attention #################################
from views.add_CategoryDB import add_category
from views.add_StatesDB import add_state
from views.add_CitiesDB import add_city
# Before start project be sure you call above function to add categories and states and cities to db
# becarfull you sould call below function in order to work correctly
# 
# 01 ->  add_category()
# 02 ->  add_state()
# 03 ->  add_city()
#
#  add_category() add_state() add_city()
#####################################################################

@app.before_request
def before_Request():
    """
    before each request we get user status and save it to g variable 
    """
    # add_category()
    # add_state()
    # add_city()

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


@app.errorhandler(500)
def error_500():
    db.session.rollback()
    return "Error 500"



# index home route
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":
        
        if not session.get("member"):
            return render_template("first-index/index.html",cities=static)
        else:
            return render_template("home-index/index.html",
            user_status=g.user_status)



@app.route("/s/<string:city>" ,methods=["GET"])
def index_city(city):
    if city in static:
        session["member"] = True
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

                new_user_mail = MailVerification(
                    email=form.email.data.strip(),
                    send_time=time_send,
                    exp_time=exp_time,
                    active_code=code,
                    user_mails=new_user)
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
            try:
                code_activation = int(code_activation)
            except ValueError:
                flash("کد ارسال شده نامعتبر می باشد","danger")
                return redirect(url_for("register"))
            
            if (check_db.active_code == code_activation):
                user_obj = User.query.filter(User.id==session["user_id"]).first()
                user_obj.is_active = 1
                check_db.activated = 1
                db.session.add_all([user_obj,check_db])
                db.session.commit()
                session["email"] = check_db.email
                flash("حساب کاربری با موفقیت ساخته شد ", "success")
                return redirect(url_for("login"))

            else:
                flash("233 مدت اعتبار کد گذشته است دوباره امتحان کنید", "danger")
                return redirect(url_for("register"))



@app.route("/resend/", methods=["POST"])
@login_required
def resend():
    """
    this view get uuid => user_id
    and if not activated user send agian code to user account
    """

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
            validate_user_db.send_time = datetime.datetime.utcnow()
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
                img_profile = "/static/uploads/profiles/" + user_in_dn.profile_image
                
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
                        os.remove(os.path.join(app.config["UPLOAD_FOLDER"],"profiles",pri_img))
                    # replace pictures
                    
                    check_user.profile_image = image_name
                    path = (os.path.join(app.config["UPLOAD_FOLDER"],"profiles",image_name))
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
    """
    In Logout View First Delete All Session from user and redirect it to index
    """
    session.clear()
    return redirect(url_for("index"))


@app.route("/new/", methods=["POST", "GET"])
def register_post():

    temp = City.query.all()
    all_city = [temp.city_name for temp in temp]

    if not session.get("user_id"):
        return render_template("register-posts/error_auth.html" ,
        user_status=g.user_status)

    form= RegisterPost()
    if request.method == "GET":

        return render_template("register-posts/index.html",
        user_status=g.user_status,
        form=form, cities=all_city)
    
    if request.method == "POST":

        if not form.validate():
            flash("برخی فیلد ها مقدار نشده است","warning")
            return render_template("register-posts/index.html",
            user_status=g.user_status, form=form, cities=all_city)


        if form.validate():
            # check for validate categories  
            categories = request.form.getlist("category")
            categury_answer = helpers.check_category(categories)
            if not categury_answer:
                flash("دسته ای برای آگهی مورد نظرانتخاب نشده است","info")
                return render_template("register-posts/index.html",
                 user_status=g.user_status, form=form, cities=all_city)

            # check user id
            user_db = User.query.filter(User.id == session["user_id"]).first()
            if not user_db:
                flash("خطایی رخ داد لطفا دوباره به حساب کاربری خود وارد شوید","danger")
                return redirect(url_for("register_post"))
            
            # check to user select price or trade option
            if not (form.price_post.data.strip()) and not (request.form.get("trade-option",None)):
                flash("لطفا وضعیت پست را تعیین کنید (فروش قیمت یا معاوضه)","info")
                return render_template("register-posts/index.html", 
                user_status=g.user_status, form=form, cities=all_city)

            # if both is selected
            if (form.price_post.data.strip()) and (request.form.get("trade-option", False)):
                flash("یک پست نمی تواند هم قیمت و هم قابل معاوضه باشد","danger")
                form.price_post.errors = ["خطا : پست باید دارای قیمت یا قابل معاوضه باشد"]
                return render_template("register-posts/index.html",
                 user_status=g.user_status, form=form, cities=all_city)

            # find value of post price  
            post_trade_option = None
            if request.form.get("trade-option"):
                post_trade_option = request.form.get("trade-option")
            else:
                # if user just type price for post
                # try to convert it to number(int)
                post_trade_option = form.price_post.data.strip()
                try:
                    post_trade_option = int(post_trade_option)
                except ValueError:
                    flash("مبلغ آگهی ناممعتبر است","danger")
                    return render_template("register-posts/index.html",
                     user_status=g.user_status, form=form, cities=all_city)



            # check user select a city
            if request.form.get("city"):
                # check city is in db
                city_db = City.query.filter(City.city_name == request.form.get("city")).first()
                if not city_db:
                    flash("شهر انتخاب شده نامعتبر است","danger")
                    return render_template("register-posts/index.html",
                     user_status=g.user_status, form=form, cities=all_city)
            else:
                    flash("شهری برای آگهی انتخاب نشده است","danger")
                    return render_template("register-posts/index.html",
                     user_status=g.user_status, form=form, cities=all_city)

                


            
            # check chat option
            chat_option = None
            if request.form.get("chat-option"):
                chat_option = True if request.form["chat-option"] else False
                

            # create user post object for db
            new_post = Post(post_title=form.title_post.data.strip(),
            post_caption = form.caption_post.data.strip(),
            post_price = str(post_trade_option),
            post_status = "موجود" , 
            created_date = datetime.datetime.utcnow(),
            post_categories = str(categury_answer),
            user_id = user_db.id,
            chat_available = chat_option
            )

            # save image
            images_list = []
            if request.files:
                # check number of images
                len_imgs = request.files.getlist("post_img")
                
                if len(len_imgs) > 3:
                    flash("تعداد عکس های انتخاب شده بیش از 3 عدد است","danger")
                    return render_template("register-posts/index.html",
                    user_status=g.user_status, form=form, cities = all_city) 

                imgs = request.files.getlist("post_img")
                for each in imgs:
                    each_filename = each.filename
                    each_filename = str(uuid.uuid1()) + (each_filename)
                    each_filename = secure_filename(each_filename)
                    path = os.path.join(app.config["UPLOAD_FOLDER"], "posts", each_filename)
                    
                    images_list.append(each_filename)
                    each.save(path)
                
                new_post.image_location = str(images_list)

            # add user post to db
            try:
                db.session.add(new_post)
                db.session.commit()
                flash("پست با موفقیت ثبت شد", "success")
                return redirect(url_for("register_post"))
            except Exception as e:
                print(e)
                flash("خطایی هنگام ثبت آگهی رخ داد دوباره امتحان کنید","danger")
                return redirect(url_for("register_post"))
                


@app.route("/my-divar/my-posts/")
@login_required
def my_posts():
    my_posts = True
    return render_template("user-dashboard/index.html",user_status=g.user_status,my_posts=my_posts)

@app.route("/my-divar/bookmarks/")
@login_required
def my_bookmarks():
    my_bookmarks = True
    return render_template("user-dashboard/index.html",user_status=g.user_status,my_bookmarks=my_bookmarks)

@app.route("/my-divar/my-notes/")
@login_required
def my_notes():
    my_notes = True
    return render_template("user-dashboard/index.html",user_status=g.user_status,my_notes=my_notes)

@app.route("/my-divar/resent-seen/")
@login_required
def my_resent_seen():
    resent_seen = True
    return render_template("user-dashboard/index.html",user_status=g.user_status, resent_seen=resent_seen)




@app.route("/state/cities/", methods=["POST"])
def get_cities():
    """
    This take a post request of a state id 
    and return all cities in that state
    """
    if (request.form.get("cities")):
        id_state="temp"
        try:
            id_state = int(request.form.get("cities"))
        except ValueError:
            return jsonify(), 400
        
        state_db = State.query.filter(State.id==id_state).first()
        if not state_db:
            return jsonify(), 400

        temp = [city.city_name for city in state_db.cities]
    return jsonify(temp), 200


@app.route("/states/", methods=["GET"])
def get_states():
    """
    This view take a request and return all states
    """
    temp = {}
    states = State.query.all()
    for each in states:
        temp[each.state_name] = each.id
    return jsonify(temp), 200


@app.route("/user/city/", methods=["POST"])
def set_city():
    """
    This view take a city form client side and set city for user in session
    """
    if request.form.get("user_selected_city"):
        session["city"] = request.form.get("user_selected_city")
        return jsonify(), 200
    else:
        return jsonify(), 400


@app.route("/api/divar/set_number/", methods=["POST"])
@login_required
def set_phone_number():
    """
    This view take ajax request from client side and set phonenumber for user
    """
    print(request.form)
    if request.form.get("phone_number"):
        user_db = User.query.filter(User.id == session["user_id"]).first()
        if not user_db:
            return jsonify("ERROR"), 404
        # make sure user send a phone number
        # first make sure user send number 
        user_phone = request.form["phone_number"]
        try:
            user_phone = int(user_phone)
        except ValueError:
            return jsonify("NAN"), 400

        # check len of number
        if len(str(user_phone)) != 10:
            return jsonify("SHORT"), 400
        
        user_phone = "0" + str(user_phone) 

        user_db.phone = user_phone

        try:
            db.session.add(user_db)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        
        return jsonify("OK"), 200
    else:
        return jsonify("missing phone number"), 400






@app.route("/temp/", methods=["GET"])
def tmep():
        new_post = Post(post_title="temp",
        post_caption = "temp",
        post_price = "temp",
        post_status = "موجود" , 
        created_date = datetime.datetime.utcnow(),
        post_categories = "temp",
        chat_available = 0
        )

        db.session.add(new_post)
        db.session.commit()
        return "OK"
