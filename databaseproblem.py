from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import pymysql
from config import *
from datetime import datetime
from songline import Sendline
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
con = pymysql.connect(HOST,USER,PASS,DATABASE)

databaseproblem = Blueprint('databaseproblem',__name__)


@databaseproblem.route("/databaseproblem")
def Databaseproblem():
    if "username" not in session:
        return render_template("/login.html")
    now = datetime.today()
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM problem_db WHERE status = 0 "
        cur.execute(sql)
        status = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM problem_db ORDER by id DESC"
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template('databaseproblem.html',status=len(status),datas = rows,now=now.strftime("%d/%m/%Y %H:%M"))
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()

@databaseproblem.route("/adddatabaseproblem", methods=["POST"])
def Adddatabaseproblem():
     if request.method == "POST":
# Save img ---------------------------------------------------------------------
         file = request.files['file']
         upload_folder = 'static/databaseproblem'
         app_folder = os.path.dirname(__file__)
         img_folder = os.path.join(app_folder,upload_folder)
         try: ## เลือกรูป
             file.save(os.path.join(img_folder,file.filename))
             path = upload_folder + "/" + file.filename
         except:## ไม่เลือก รูป
             path = ""
         ##input
         problem = request.form["problem"]
         dateadd = request.form["dateadd"]
         user = request.form["user"]
         try:
             con.connect()
             cur = con.cursor()
             sql = "insert into problem_db (problem,date,pic,user) VALUES(%s,%s,%s,%s)"
             cur.execute(sql,(problem,dateadd,path,user))
             con.commit()
             #----แจ้งเตือนผ่านไลน์--------------------------------------------
             token = 'UJ2XqbZF55zjfqfAepLUb98IqET6EgbFZmg0jxEu7G0'
             messenger = Sendline(token)
             messenger.sendtext('แจังปัญหาการใช้งานโปรแกรม Database System'+ ' ' + '==>'+ ' ' +problem)
             #----สิ้นสุด----------------------------------------------------
             return redirect(url_for('databaseproblem.Databaseproblem'))
         except Exception as e:
             print(e)
         finally:
             print("Close")
             cur.close()
             con.close()


@databaseproblem.route("/databaseproblemedit",methods=["POST"])
def Databaseproblemedit():
    if request.method == "POST":
        id = request.form["id"]
        problem = request.form["problem"]
        status = request.form["status"]
        edituser = request.form["edituser"]
        dateedit = request.form["dateedit"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE  `problem_db` SET `status` =%s,`edituser` =%s,`problem_edit`=%s WHERE `id`=%s"
            cur.execute(sql,(status,edituser,dateedit,id))
            con.commit()
            cur.close()
             #----แจ้งเตือนผ่านไลน์--------------------------------------------
            token = 'UJ2XqbZF55zjfqfAepLUb98IqET6EgbFZmg0jxEu7G0'
            messenger = Sendline(token)
            messenger.sendtext('ลำดับที่'+' '+ id + ' '+ problem + ' ' + 'แก้ไขแล้วโดย' + ' ' + session['fname'])
             #----สิ้นสุด----------------------------------------------------
            return redirect(url_for('databaseproblem.Databaseproblem'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@databaseproblem.route("/databaseproblemcheck",methods=["POST"])
def Databaseproblemcheck():
    if request.method == "POST":
        id = request.form["id"]
        status = request.form["status"]
        checkuser = request.form["checkuser"]
        datecheck = request.form["datecheck"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE  `problem_db` SET `status` =%s,`checkuser` =%s,`date_check` =%s WHERE `id`=%s"
            cur.execute(sql,(status,checkuser,datecheck,id))
            con.commit()
            cur.close()
              #----แจ้งเตือนผ่านไลน์--------------------------------------------
            token = 'UJ2XqbZF55zjfqfAepLUb98IqET6EgbFZmg0jxEu7G0'
            messenger = Sendline(token)
            messenger.sendtext('ลำดับที่'+' '+ id +' '+ 'ผ่านครับ' + ' ' + session['fname'])
              #----สิ้นสุด----------------------------------------------------
            return redirect(url_for('databaseproblem.Databaseproblem'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@databaseproblem.route("/reject",methods=["POST"])
def Reject():
    if request.method == "POST":
        id = request.form["id"]
        status = request.form["status"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE  `problem_db` SET `status` =%s WHERE `id`=%s"
            cur.execute(sql,(status,id))
            con.commit()
            cur.close()
             #----แจ้งเตือนผ่านไลน์--------------------------------------------
            token = 'UJ2XqbZF55zjfqfAepLUb98IqET6EgbFZmg0jxEu7G0'
            messenger = Sendline(token)
            messenger.sendtext('ลำดับที่'+' '+ id +' '+ 'ยังไม่ผ่านครับ' + ' ' + session['fname'])
             #----สิ้นสุด----------------------------------------------------
            return redirect(url_for('databaseproblem.Databaseproblem'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
