from flask import Flask,render_template,url_for


app = Flask(__name__)



@app.route("/")
def inedx():
    return render_template('divar-index-home/index.html')