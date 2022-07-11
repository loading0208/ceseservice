from flask import Flask,render_template,session,redirect,send_from_directory
from datetime import timedelta
import time
import datetime

from dashboard import *
from user import *
from helpdesk import *
from contact import *
from home import *
from propertyregister import *
from booking import *
from landing import *
from notification import *
from databaseproblem import *

app = Flask(__name__)

app.secret_key = "ceseservice"
app.permanent_session_lifetime = timedelta(hours=1)

app.register_blueprint(dashboard)
app.register_blueprint(user)
app.register_blueprint(helpdesk)
app.register_blueprint(contact)
app.register_blueprint(home)
app.register_blueprint(propertyregister)
app.register_blueprint(booking)
app.register_blueprint(landing)
app.register_blueprint(notification)
app.register_blueprint(databaseproblem)



@app.route("/")
def wtf():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("/index.html")

@app.route("/static/imghelpdesk/<filename>")
def protect(filename):
    if "username" not in session:
        return redirect(url_for('user.Login'))
    return send_from_directory("static/imghelpdesk",filename)

#-------------Error page--------------------------------------------------------

#-------------------Error 404 --------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("Notfound"))

@app.route("/notfound")
def Notfound():
    return render_template("errorpage/errorpage404.html")
#-------------------end 404 ----------------------------------------------------

#-------------------Error 405 --------------------------------------------------
@app.errorhandler(405)
def not_found405(error):
    return redirect(url_for("Notfound405"))

@app.route("/notfound405")
def Notfound405():
    return render_template("errorpage/errorpage405.html")
#-------------------end 405 ----------------------------------------------------


#-------------------Error 500 --------------------------------------------------
@app.errorhandler(500)
def not_found500(error):
    return redirect(url_for("Notfound500"))

@app.route("/notfound500")
def Notfound500():
    return render_template("errorpage/errorpage500.html")
#-------------------end 500 ----------------------------------------------------




if __name__== '__main__':
    app.run(host = "0.0.0.0",port=88,debug = True )
