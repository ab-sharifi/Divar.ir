# all views for all routes located in here


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

@app.route("/")
def index():
    print("Hellow")
    return render_template('index-home/index.html')


@app.route("/index")
def first_index():
    return render_template('first-index/index.html')

@app.route("/page")
def page():
    return render_template("post-page/index.html")