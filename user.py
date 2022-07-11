from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import pymysql
from config import *
from songline import Sendline
con = pymysql.connect(HOST,USER,PASS,DATABASE)

user = Blueprint('user',__name__)

@user.route("/login")
def Login():
    if "username" not in session:
        return render_template("/login.html",status="wait")
    else:
        return redirect(url_for('home.Home'))

@user.route("/sign-in")
def Signin():
    if "username" not in session:
        return render_template("/login.html")
    else:
        return redirect(url_for('home.Home'))

@user.route("/profile")
def Profile():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("profile.html")

@ user.route("/checklogin", methods=["POST"])
def Checklogin():
    username = request.form['username']
    password = request.form['password']
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM tb_user WHERE usr_username = %s AND usr_password = %s and usr_status = 1"
        cur.execute(sql, (username, password))
        rows = cur.fetchall()
        if len(rows) > 0:
            session['username'] = username
            session['id'] = rows[0][0]
            session['fname'] = rows[0][1]
            session['lname'] = rows[0][2]
            session['email'] = rows[0][6]
            session['department'] = rows[0][7]
            session['level'] = rows[0][9]
            session.permanent = True
            if session['level'] == "admin":
                return redirect(url_for('dashboard.Dashboard'))
            if session['level'] == "สมาชิกทั่วไป":
                return redirect(url_for('home.Home'))
            if session['level'] == "dev":
                return redirect(url_for('databaseproblem.Databaseproblem'))
            else:
                return redirect(url_for('user.logoff'))
        else:
            flash("ไม่พบข้อมูลในระบบ กรุณาลองใหม่อีกครั้ง")
            return redirect(url_for('user.Signin'))
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()

@user.route("/formforgetpassword")
def Formforgetpassword():
    return render_template("forgetpassword.html")


@user.route("/forgetpassword", methods=["POST"])
def Forgetpassword():
    if request.method == "POST":
        newpassforget = request.form["newpassforget"]
        confirenewpassforget = request.form["confirenewpassforget"]
        email = request.form["email"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM tb_user WHERE usr_email = %s "
            cur.execute(sql, (email))
            rows = cur.fetchall()
            if len(rows) <= 0:
                flash("กรุณากรอก E-Mail ที่เคยลงทะเบียน")
                return redirect(url_for("user.Formforgetpassword"))
            if newpassforget != confirenewpassforget:
                flash("Password ไม่ตรงกัน")
                return redirect(url_for("user.Formforgetpassword"))
            if len(rows) > 0:
                sql = "UPDATE tb_user SET `usr_password`=%s  WHERE `usr_email`=%s"
                cur.execute(sql, (newpassforget, email))
                flash("เปลี่ยน Password เรียบร้อยครับ")
                # return redirect(url_for("user.Login"),status = "ok")
                return render_template('login.html', status="ok")
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()



@user.route("/formregis")
def Formregis():
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_department "
        cur.execute(sql)
        dep = cur.fetchall()
        return render_template("/regisuser.html",dep = dep)
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()

@user.route("/alluser")
def Alluser():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM tb_user"
        cur.execute(sql)
        rowsalluser = cur.fetchall()
        return render_template("dashboard/alluser.html",rowsalluser = rowsalluser)
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()

@user.route("/edituser",methods=["POST"])
def Edituser():
    if request.method == "POST":
        id = request.form["id"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        depart = request.form["depart"]
    try:
        con.connect()
        cur = con.cursor()
        sql = "UPDATE tb_user SET `usr_fname`=%s,`usr_lname`=%s,`usr_email`=%s,`usr_depart`=%s  WHERE `usr_id`=%s"
        cur.execute(sql,(fname,lname,email,depart,id))
        rowsalluser = cur.fetchall()
        return redirect(url_for('user.Alluser'))
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()

@user.route("/deleteuser",methods=["POST"])
def Deleteuser():
    if request.method == "POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "delete from tb_user where usr_id = %s"
            cur.execute(sql,(id))
            con.commit()
            return redirect(url_for("dashboard.Dashboard"))
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()

@user.route("/regisuser", methods=["POST"])
def Regisuser():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        #เช็ค e-mail ซ้ำ ---------------------------------------------
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM tb_user WHERE usr_email = %s "
            cur.execute(sql,(email))
            rows = cur.fetchall()
            if len (rows) >0:
                flash("E-Mail นี้มีผู้ใช้งานแล้ว กรุณาลองใหม่ หรือ ติดต่อ 147")
                return redirect(url_for('user.Formregis'))
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()
        #----END-----------------------------------------------------
        depart = request.form["depart"]
        username = request.form["username"]
        password = request.form["password"]
        repassword = request.form["repassword"]
        level = request.form["level"]
        #--------------------เช็ค user ซ้ำ---------------------------------------------
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM tb_user WHERE usr_username = %s "
            cur.execute(sql,(username))
            rows = cur.fetchall()
            if len (rows) >0:
                flash("Username นี้มีผู้ใช้งานแล้ว กรุณากรอกใหม่")
                return redirect(url_for('user.Formregis'))
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()
        #------------------------สิ้นสุด-------------------------------------
        if password != repassword:
            flash("Password ไม่ตรงกัน")
            return redirect(url_for('user.Formregis'))
    try:
        con.connect()
        cur = con.cursor()
        sql = "insert into tb_user (usr_fname,usr_lname,usr_email,usr_depart,usr_username,usr_password,usr_level) values(%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,(fname,lname,email,depart,username,password,level))
        con.commit()
        flash("สมัครสมาชิกเรียบร้อย รอ E-Mail ยืนยันเพื่อเข้าสู่ระบบ")
        #----แจ้งเตือนผ่านไลน์--------------------------------------------
        token = '6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O'
        messenger = Sendline(token)
        messenger.sendtext('มี User ใหม่รอการอนุมัติ')
        #----สิ้นสุด----------------------------------------------------
        return redirect(url_for('user.Login'))
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()


@user.route("/logoff")
def logoff():
    session.clear()
    return redirect(url_for('user.Login'))
