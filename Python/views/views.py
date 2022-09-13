from flask import(
    render_template,
    url_for,
    session,
    request,
    abort,
    flash,
    g,
    redirect,
)
from divar.app import app
from divar.models import db,User
from views import helpers

# list of cities
static = ['کرج','تهران','قم','مشهد','گیلان','گلستان','شیراز','اصفهان','کرمانشاه','تبریز']



# index home route
@app.route("/s/<string:city>", methods=["GET"])
def index(city):
    user_status = {'login':False, 'phone':""}
    print(session.items())

    if request.method == "GET":
            if city in static:
                return render_template('index-home/index.html',user_status=user_status)
            else:     
                if session.get('city'):
                    if session.get('city') in static:
                        # render template to user owen city in session
                        return redirect(url_for('index',city=session['city']))
                else:
                    # return user to select city
                    return redirect(url_for('first_index'))

        
@app.route('/register_user', methods=['POST'])
def register_user():
    if request.method == "POST":
        email = request.form.get("email")
        if not email or not helpers.check_email(email):
            flash("ایمیل نا معتبر می باشد", "info")
            return render_template("index-home/index.html")
        new_email = User()
        new_email.email = email
        db.session.add(new_email)
        db.session.commit()
        return "ok"

# first index route
@app.route("/", methods=["GET", "POST"])
def first_index():    
    print(session.items())
    if request.method == 'GET':
        if session.get('city', "") not in static:
            return render_template('first-index/index.html',cities=static)
        else:
            return redirect(url_for('index',city=session['city']) )


# each page route
@app.route("/v/")
def page():
    return render_template("post-page/index.html")