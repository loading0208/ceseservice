from flask import Blueprint,render_template,session,request,redirect,url_for
import pymysql
from config import *
import notification
con = pymysql.connect(HOST,USER,PASS,DATABASE)

contact = Blueprint('contact',__name__)
@contact.route("/contact")
def Contact():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_contact"
        cur.execute(sql)
        contact = cur.fetchall()
        sql = "SELECT * FROM db_department "
        cur.execute(sql)
        dep = cur.fetchall()
        return render_template('contact.html',contact = contact,dep = dep,msg = "All Department",sumnoti=notification.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()



@contact.route("/addcontact", methods=['POST'])
def Addcontact():
    name = request.form["name"]
    position = request.form["position"]
    tel = request.form["tel"]
    email = request.form["email"]
    ext = request.form["ext"]
    Dpart = request.form["Dpart"]
    try:
        con.connect()
        cur = con.cursor()
        sql = "insert into db_contact (con_name,con_position,con_tel,con_email,con_ext,con_depid) values(%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,(name,position,tel,email,ext,Dpart))
        con.commit()
        return redirect(url_for('contact.Contact'))
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()



@contact.route("/bydepart",methods=['POST'])
def Bydepart():
    if request.method == "POST":
        dep = request.form['dep']
        if dep == "All Department":
            return redirect(url_for('contact.Contact'))
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM db_contact where con_depid = %s "
            cur.execute(sql,(dep))
            rows = cur.fetchall()
            return render_template("contact.html",datas = rows,dep = dep)
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@contact.route("/editcontact",methods=["POST"])
def Editcontact():
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        position = request.form["position"]
        Dpart = request.form["Dpart"]
        tel = request.form["tel"]
        email = request.form["email"]
        ext = request.form["ext"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE db_contact SET `con_name`=%s,`con_position`=%s,`con_depid`=%s,`con_tel`=%s,`con_email`=%s,`con_ext`=%s  WHERE `id`=%s"
            cur.execute(sql,(name,position,Dpart,tel,email,ext,id))
            rows = cur.fetchall()
            con.commit()
            return redirect(url_for('contact.Contact'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@contact.route("/deletecontact",methods=["POST"])
def Deletecontact():
    if request.method == "POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "delete from db_contact where id = %s"
            cur.execute(sql,(id))
            con.commit()
            return redirect(url_for("contact.Contact"))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
