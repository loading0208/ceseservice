from flask import Blueprint,render_template,session
import notification
home = Blueprint('home',__name__)
@home.route("/home")
def Home():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("index.html",sumnoti=notification.Notification())
