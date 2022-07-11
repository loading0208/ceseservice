from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import pymysql
from config import *
from songline import Sendline
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import notification
con = pymysql.connect(HOST,USER,PASS,DATABASE)


helpdesk = Blueprint('helpdesk',__name__)
@helpdesk.route("/helpdesk")
def Helpdesk():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_helpdesk ORDER BY db_id DESC "
        cur.execute(sql)
        rows = cur.fetchall()
        sql = "SELECT * FROM db_department "
        cur.execute(sql)
        dep = cur.fetchall()
        return render_template('helpdesk.html',datas = rows,dep = dep,sumnoti=notification.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@helpdesk.route("/walkietalkie")
def Walkietalkie():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_walkietalkie"
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template('walkietalkie.html',datas = rows)
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()



@helpdesk.route("/repair")
def repair():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("/addrepair.html")


@helpdesk.route("/addrepair", methods=["POST"])
def addrepair():
     if request.method == "POST":
# Save img ---------------------------------------------------------------------
         file = request.files['file']
         upload_folder = 'static/imghelpdesk'
         app_folder = os.path.dirname(__file__)
         img_folder = os.path.join(app_folder,upload_folder)
         try: ## เลือกรูป
             file.save(os.path.join(img_folder,file.filename))
             path = upload_folder + "/" + file.filename
         except:## ไม่เลือก รูป
             path = ""
         ##input
         fname = request.form["fname"]
         lname = request.form["lname"]
         department = request.form["depart"]
         email = request.form["email"]
         goods = request.form["goods"]
         goodsohter = request.form["goodsohter"]
         code = request.form["code"]
         detail = request.form["detail"]
         jobstatus = request.form["jobstatus"]
         telin = request.form["telin"]
         if goods == "other":
             try:
                 con.connect()
                 cur = con.cursor()
                 sql = "insert into db_helpdesk (db_fname,db_lname,db_department,db_email,db_goods,db_code,db_detail,db_pic,jobstatus,db_telin) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                 cur.execute(sql,(fname,lname,department,email,goodsohter,code,detail,path,jobstatus,telin))
                 con.commit()
                 #----แจ้งเตือนผ่านไลน์--------------------------------------------
                 token = '6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O'
                 messenger = Sendline(token)
                 messenger.sendtext('คุณ' + session['fname']+' '+ 'แจ้งว่า' + detail)
                #----สิ้นสุด----------------------------------------------------
                 return redirect(url_for('helpdesk.Helpdesk'))
             except Exception as e:
                 print(e)
             finally:
                 print("Close")
                 cur.close()
                 con.close()
         else:
            try:

                 con.connect()
                 cur = con.cursor()
                 sql = "insert into db_helpdesk (db_fname,db_lname,db_department,db_email,db_goods,db_code,db_detail,db_pic,jobstatus,db_telin) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                 cur.execute(sql,(fname,lname,department,email,goods,code,detail,path,jobstatus,telin))
                 con.commit()
                 #----แจ้งเตือนผ่านไลน์--------------------------------------------
                 token = '6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O'
                 messenger = Sendline(token)
                 messenger.sendtext('คุณ' + session['fname']+' '+ 'แจ้งว่า' + detail)
                #----สิ้นสุด----------------------------------------------------
                 return redirect(url_for('helpdesk.Helpdesk'))
            except Exception as e:
                print(e)
            finally:
                 print("Close")
                 cur.close()
                 con.close()


@helpdesk.route("/ithelpdesk",methods=["POST"])
def Ithelpdesk():
    if request.method == "POST":
        id = request.form["id"]
        report = request.form["report"]
        Dateaccept = request.form["Dateaccept"]
        ituser = request.form["ituser"]
        jobstatus = request.form["jobstatus"]
        email = request.form["email"]

        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE `db_helpdesk` SET `db_status` =%s,`dateacc` =%s,`db_it` =%s, `jobstatus` =%s, `db_email`=%s  WHERE `db_id`=%s"
            cur.execute(sql,(report,Dateaccept,ituser,jobstatus,email,id))
            con.commit()
            cur.close()
#----แจ้งผลผ่าน e-mail----------------------------------------------------------------------------------
            def sendthai(sendto,subj,detail):

            	myemail = 'ces-eservice@hotmail.com'
            	mypassword = '@support65@'
            	receiver = sendto

            	msg = MIMEMultipart('alternative')
            	msg['Subject'] = subj
            	msg['From'] = 'IT Support CES'
            	msg['To'] = receiver
            	html = detail

            	part1 = MIMEText(text, 'plain')
            	msg.attach(part1)

            	s = smtplib.SMTP('smtp-mail.outlook.com:587')
            	s.ehlo()
            	s.starttls()

            	s.login(myemail, mypassword)
            	s.sendmail(myemail, receiver.split(','), msg.as_string())
            	s.quit()

            subject = 'แจ้งผลการซ่อม'
            msg = report + ' ' + 'เจ้าหน้าที่รับงาน' + ' ' + session ['fname']

            sendthai(email,subject,msg)
#-----------------------------------------------------------------------------------------------------------
            return redirect(url_for('dashboard.Dashboard'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@helpdesk.route("/ithelpdeskwait",methods=["POST"])
def Ithelpdeskwait():
    if request.method == "POST":
        id = request.form["id"]
        report = request.form["report"]
        Dateaccept = request.form["Dateaccept"]
        ituser = request.form["ituser"]
        jobstatus = request.form["jobstatus"]
        email = request.form["email"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE `db_helpdesk` SET `db_status` =%s,`dateacc` =%s, `db_it` =%s, `jobstatus` =%s, `db_email`=%s WHERE `db_id`=%s"
            cur.execute(sql,(report,Dateaccept,ituser,jobstatus,email,id))
            con.commit()
            cur.close()
            def sendthai(sendto,subj,detail):

            	myemail = 'not.reply.ces@gmail.com'
            	mypassword = 'sr3sr4sr5sr6'
            	receiver = sendto

            	msg = MIMEMultipart('alternative')
            	msg['Subject'] = subj
            	msg['From'] = 'IT Support CES'
            	msg['To'] = receiver
            	text = detail

            	part1 = MIMEText(text, 'plain')
            	msg.attach(part1)

            	s = smtplib.SMTP('smtp.gmail.com:587')
            	s.ehlo()
            	s.starttls()

            	s.login(myemail, mypassword)
            	s.sendmail(myemail, receiver.split(','), msg.as_string())
            	s.quit()

            subject = 'แจ้งผลการซ่อม'
            msg = report + ' ' + 'ซ่อมโดย' + ' ' + session ['fname']

            sendthai(email,subject,msg)
            return redirect(url_for('dashboard.Dashboard'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()



@helpdesk.route("/myjob" ,methods=["POST"])
def Myjob():
    if "username" not in session:
        return render_template("/login.html")
    if request.method == "POST":
        fname = request.form["fname"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM db_helpdesk WHERE db_fname = %s"
            cur.execute(sql,(fname))
            rows = cur.fetchall()
            return render_template('helpdeskid.html',datas = rows)
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@helpdesk.route("/editjobid", methods=["POST"])
def Editjobid():
    if request.method == "POST":
        id = request.form["id"]
        goods = request.form["goods"]
        code = request.form["code"]
        detail = request.form["detail"]
        file = request.files['file']
        if file.filename == "":
            try:
                con.connect()
                cur = con.cursor()
                sql = "UPDATE db_helpdesk SET `db_goods`=%s,`db_code`=%s,`db_detail`=%s WHERE `db_id`=%s"
                cur.execute(sql,(goods,code,detail,id))
                con.commit()
                return redirect(url_for('helpdesk.Helpdesk'))
            except Exception as e:
                print(e)
            finally:
                print("Close")
                cur.close()
                con.close()
        else:
            # update with no pic:
            file = request.files['file']
            upload_folder = 'static/imghelpdesk'
            app_folder = os.path.dirname(__file__)
            img_folder = os.path.join(app_folder,upload_folder)
            try: ## เลือกรูป
                file.save(os.path.join(img_folder,file.filename))
                path = upload_folder + "/" + file.filename
            except:## ไม่เลือก รูป
                path = ""
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE db_helpdesk SET `db_goods`=%s,`db_code`=%s,`db_detail`=%s, `db_pic`= %s WHERE `db_id`=%s"
            cur.execute(sql,(goods,code,detail,path,id))
            con.commit()
            return redirect(url_for('helpdesk.Helpdesk'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()

@helpdesk.route("/delete",methods=["POST"])
def Deletejob():
    if request.method == "POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "delete from db_helpdesk where db_id = %s"
            cur.execute(sql,(id))
            con.commit()
            return redirect(url_for('helpdesk.Helpdesk'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()




@helpdesk.route("/form")
def Form():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("/form.html")
