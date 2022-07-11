from flask import Blueprint,render_template,session
import notification

landing = Blueprint('landing',__name__)

@landing.route("/0001")
def news0001():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("landing/0001.html",sumnoti=notification.Notification())

@landing.route("/0002")
def news0002():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("landing/0002.html",sumnoti=notification.Notification())

@landing.route("/0003")
def news0003():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("landing/0003.html",sumnoti=notification.Notification())


@landing.route("/pro")
def Pro():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("landing/pro.html")

@landing.route("/0004")
def news0004():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("landing/0004.html",sumnoti=notification.Notification())

@landing.route("/0005")
def news0005():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("landing/0005.html",sumnoti=notification.Notification())

@landing.route("/0006")
def news0006():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("landing/0006.html",sumnoti=notification.Notification())
