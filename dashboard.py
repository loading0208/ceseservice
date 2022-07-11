from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import pymysql
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from songline import Sendline
import notification
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)

dashboard = Blueprint('dashboard',__name__)


@dashboard.route("/dashboard")
def Dashboard():
    if "username" not in session:
        return render_template("/login.html")
    if session['level'] != 'admin':
        return redirect(url_for('home.Home'))
    now = datetime.today()
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_helpdesk WHERE jobstatus = 0 ORDER BY db_id DESC"
        cur.execute(sql)
        newdesk = cur.fetchall()
        snewdesk = len(newdesk)

        sql = "SELECT * FROM db_helpdesk WHERE jobstatus = 2 ORDER BY db_id DESC"
        cur.execute(sql)
        waitdesk = cur.fetchall()
        swaitdesk = len(waitdesk)

        sql = "SELECT * FROM db_booking WHERE bk_status = 0 OR bk_status = 2 OR bk_status = 10 OR bk_status = 12 OR bk_status=20 OR bk_status = 22"
        cur.execute(sql)
        booking = cur.fetchall()
        sbooking = len(booking)

        sql = "SELECT * FROM tb_user WHERE usr_status = 0"
        cur.execute(sql)
        newuser = cur.fetchall()
        snewuser = len(newuser)

        sql = "SELECT * FROM db_department "
        cur.execute(sql)
        dep = cur.fetchall()

        sumnoti = snewdesk+swaitdesk+snewuser+sbooking
        return render_template('dashboard.html',now=now.strftime("%H:%M %d/%m/%Y"),newdesk = newdesk,dep=dep,tnewdesk=snewdesk , waitdesk = waitdesk, twaitdesk=swaitdesk,booking=booking,tbooking=sbooking, newuser = newuser,tnewuser=snewuser,sumnoti=sumnoti)
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@dashboard.route("/ithelpdesk",methods=["POST"])
def Ithelpdesk():
    if request.method == "POST":
        id = request.form["id"]
        feedback = request.form["feedback"]
        Dateaccept = request.form["Dateaccept"]
        ituser = request.form["ituser"]
        jobstatus = request.form["jobstatus"]
        email = request.form["email"]
        nameuser = request.form["nameuser"]
        detail = request.form["detail"]

        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE `db_helpdesk` SET `db_status` =%s,`dateacc` =%s,`db_it` =%s, `jobstatus` =%s, `db_email`=%s  WHERE `db_id`=%s"
            cur.execute(sql,(feedback,Dateaccept,ituser,jobstatus,email,id))
            con.commit()
            #----แจ้งเตือนผ่านไลน์--------------------------------------------
            token = '6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O'
            messenger = Sendline(token)
            messenger.sendtext(ituser+' '+'รับงานแล้ว')
        #----สิ้นสุด----------------------------------------------------
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

            	part1 = MIMEText(html, 'html')
            	msg.attach(part1)

            	s = smtplib.SMTP('smtp-mail.outlook.com:587')
            	s.ehlo()
            	s.starttls()

            	s.login(myemail, mypassword)
            	s.sendmail(myemail, receiver.split(','), msg.as_string())
            	s.quit()

            subject = 'แจ้งผลการซ่อม'
            msg = f"""
                        <html>

                            <head></head>
                            <body style="font-family:'Prompt', sans-serif;font-size:20px;color:#079992">
                                <h2>รายงานผลการซ่อม </h2>
                                <h3>เรียนคุณ {nameuser}</h3>
                                <h3>อ้างอิงใบแจ้งซ่อมที่ : {id}</h3>
                                <h3>แจ้งว่า : {detail}</h3>
                                <h3>ผลการซ่อม : {feedback}</h3>
                                <h3>ผู้ซ่อม : {ituser}</h3>
                                <hr style="color:#079992">
                                <h3>IT Support CES</h3>
                                <a href="http://ceseservice.dyndns.org:88/" style="color:#079992" >CES-ESERVICE</a>
                            </body>
                        </html>
                    """

            sendthai(email,subject,msg)
#-----------------------------------------------------------------------------------------------------------
            return redirect(url_for('dashboard.Dashboard'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()



@dashboard.route("/ithelpdeskwait",methods=["POST"])
def Ithelpdeskwait():
    if request.method == "POST":
        id = request.form["id"]
        report = request.form["report"]
        Dateaccept = request.form["Dateaccept"]
        ituser = request.form["ituser"]
        jobstatus = request.form["jobstatus"]
        email = request.form["email"]
        detail = request.form["detail"]
        nameuser = request.form["nameuser"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE `db_helpdesk` SET `db_status` =%s,`dateacc` =%s, `db_it` =%s, `jobstatus` =%s, `db_email`=%s WHERE `db_id`=%s"
            cur.execute(sql,(report,Dateaccept,ituser,jobstatus,email,id))
            con.commit()
            cur.close()
            def sendthai(sendto,subj,detail):

            	myemail = 'ces-eservice@hotmail.com'
            	mypassword = '@support65@'
            	receiver = sendto

            	msg = MIMEMultipart('alternative')
            	msg['Subject'] = subj
            	msg['From'] = 'IT Support CES'
            	msg['To'] = receiver
            	html = detail

            	part1 = MIMEText(html, 'html')
            	msg.attach(part1)

            	s = smtplib.SMTP('smtp-mail.outlook.com:587')
            	s.ehlo()
            	s.starttls()

            	s.login(myemail, mypassword)
            	s.sendmail(myemail, receiver.split(','), msg.as_string())
            	s.quit()

            subject = 'แจ้งผลการซ่อม'
            msg = f"""
                        <html>

                            <head></head>
                            <body style="font-family:'Prompt', sans-serif;font-size:20px;color:#079992">
                                <h2>รายงานผลการซ่อม </h2>
                                <h3>เรียนคุณ {nameuser}</h3>
                                <h3>อ้างอิงใบแจ้งซ่อมที่ : {id}</h3>
                                <h3>แจ้งว่า : {detail}</h3>
                                <h3>ผลการซ่อม : {report}</h3>
                                <h3>ผู้ซ่อม : {ituser}</h3>
                                <hr style="color:#079992">
                                <h3>IT Support CES</h3>
                                <a href="http://ceseservice.dyndns.org:88/" style="color:#079992">CES-ESERVICE</a>
                            </body>
                        </html>
                    """

            sendthai(email,subject,msg)
            return redirect(url_for('dashboard.Dashboard'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()



@dashboard.route("/updateuser",methods=["POST"])
def Updateuser():
    if request.method == "POST":
        id = request.form["id"]
        status = request.form["status"]
        email = request.form["email"]
        possession = request.form["possession"]
        name = request.form["name"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE `tb_user` SET `usr_status` =%s , `usr_level`=%s WHERE `usr_id`=%s"
            cur.execute(sql,(status,possession,id))
            con.commit()
            cur.close()
            def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

            	myemail = 'ces-eservice@hotmail.com'
            	mypassword = '@support65@'
            	receiver = sendto

            	msg = MIMEMultipart('alternative')
            	msg['Subject'] = subj
            	msg['From'] = 'IT Support CES'
            	msg['To'] = receiver
            	html = detail

            	part1 = MIMEText(html, 'html')
            	msg.attach(part1)

            	s = smtplib.SMTP('smtp-mail.outlook.com:587')
            	s.ehlo()
            	s.starttls()

            	s.login(myemail, mypassword)
            	s.sendmail(myemail, receiver.split(','), msg.as_string())
            subject = 'สมาชิกได้รับการอนุมัติ'
            msg = f"""
                        <html>

                            <head></head>
                            <body style="font-family:'Prompt', sans-serif;font-size:20px;color:#079992">
                                <h2>เรียนคุณ {name}</h2>
                                <h3>คุณได้รับอนุญาติให้ใช้งานระบบ CES-ESERVICE ได้แล้ว</h3>
                                <h3>ขอบคุณครับ</h3>
                                <hr style="color:#079992;width:50%;" align="left">
                                <h3>IT Support CES</h3>
                                <a href="http://ceseservice.dyndns.org:88/" style="color:#079992">CES-ESERVICE</a>
                            </body>
                        </html>
                    """

            sendthai(email,subject,msg)
            return redirect(url_for('dashboard.Dashboard'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@dashboard.route("/adddepartment",methods=["POST"])
def Adddepartment():
        inputdep = request.form["inputdep"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "insert into db_department (dep_name) values(%s)"
            cur.execute(sql,(inputdep))
            con.commit()
            return redirect(url_for('dashboard.Dashboard'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@dashboard.route("/report",methods=['POST'])
def Report():
    if "username" not in session:
        return render_template("/login.html")
    if session['level'] != 'admin':
        return redirect(url_for('home.Home'))
    if request.method == "POST":
        months = request.form['months']
        dstart = request.form['dstart']
        dend = request.form['dend']
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM db_helpdesk where db_date between %s and %s"
            cur.execute(sql,(dstart,dend))
            rows = cur.fetchall()
            return render_template("report.html",datas = rows,months=months)
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
