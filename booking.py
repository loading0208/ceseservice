from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import pymysql
from config import *
import os
import datetime
from songline import Sendline
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import notification

con = pymysql.connect(HOST,USER,PASS,DATABASE)



booking = Blueprint('booking',__name__)

@booking.route("/bookingroom")
def Booking():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_department "
        cur.execute(sql)
        dep = cur.fetchall()

        sql = "SELECT * FROM db_booking WHERE bk_room = 'Malakul' and bk_status = 1"
        cur.execute(sql)
        queuemalakul = cur.fetchall()

        sql = "SELECT * FROM db_booking WHERE bk_room = 'Chadjew' and bk_status = 21"
        cur.execute(sql)
        queuechadjew = cur.fetchall()

        sql = "SELECT * FROM db_booking WHERE bk_room = 'Thanasriporn' and bk_status = 11"
        cur.execute(sql)
        queuethanasriporn = cur.fetchall()

        return render_template('meetingroom/bookingroom.html',sumnoti=notification.Notification(),queuemalakul=len(queuemalakul),queuechadjew=len(queuechadjew),queuethanasriporn=len(queuethanasriporn))
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@booking.route("/howto")
def Howto():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("meetingroom/howto.html",sumnoti=notification.Notification())


@booking.route("/addbooking", methods=["POST"])
def addbooking():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        department = request.form["depart"]
        email = request.form["email"]
        room = request.form["room"]
        date = request.form["date"]
        dateend = request.form["dateend"]
        other = request.form["other"]
        status = request.form["status"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "insert into db_booking (bk_fname,bk_lname,bk_department,bk_email,bk_room,bk_dateuse,bk_dateend,bk_other,bk_status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(fname,lname,department,email,room,date,dateend,other,status))
            con.commit()
            #----แจ้งเตือนผ่านไลน์--------------------------------------------
            token = '6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O'
            messenger = Sendline(token)
            messenger.sendtext('คุณ' + session['fname']+' '+ 'จองห้องประชุม ห้อง' + room )
           #----สิ้นสุด----------------------------------------------------
            if room == 'Malakul':
                return redirect(url_for('booking.Malakul'))
            if room == 'Thanasriporn':
                return redirect(url_for('booking.Thanasriporn'))
            if room == 'Chadjew':
                return redirect(url_for('booking.Chadjew'))

        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()

@booking.route("/malakul")
def Malakul():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_booking WHERE bk_room = 'Malakul' ORDER BY bk_id DESC"
        cur.execute(sql)
        malakul = cur.fetchall()
        sql = "SELECT * FROM db_department "
        cur.execute(sql)
        dep = cur.fetchall()
        return render_template('meetingroom/malakul.html',malakul = malakul,dep=dep,sumnoti=notification.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()




@booking.route("/thanasriporn")
def Thanasriporn():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_booking WHERE bk_room = 'Thanasriporn' ORDER BY bk_id DESC"
        cur.execute(sql)
        thanasriporn = cur.fetchall()
        sql = "SELECT * FROM db_department "
        cur.execute(sql)
        dep = cur.fetchall()
        return render_template('meetingroom/thanasriporn.html',thanasriporn=thanasriporn,dep=dep,sumnoti=notification.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@booking.route("/chadjew")
def Chadjew():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_booking WHERE bk_room = 'Chadjew' ORDER BY bk_id DESC"
        cur.execute(sql)
        chadjew = cur.fetchall()
        sql = "SELECT * FROM db_department "
        cur.execute(sql)
        dep = cur.fetchall()
        return render_template('meetingroom/chadjew.html',chadjew=chadjew,dep=dep,sumnoti=notification.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@booking.route("/updatestatus",methods=["POST"])
def Updatestatus():
    if request.method == "POST":
        id = request.form["id"]
        status = request.form["status"]
        room = request.form["room"]
        email = request.form["email"]
        admin = request.form["admin"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE  `db_booking` SET `bk_status` =%s,`bk_admin` =%s WHERE `bk_id`=%s"
            cur.execute(sql,(status,admin,id))
            con.commit()
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

            if status == '1' or status=='11' or status == '21':
                subject = 'สถานะการจองห้องประชุม'
                msg = 'อนุญาตให้ใช้งานได้ เจ้าหน้าที่ทำรายการ'+' '+admin

                sendthai(email,subject,msg)
            if status=='3' or status=='13' or status=='23':
                subject = 'สถานะการจองห้องประชุม'
                msg = 'ห้องประชุมไม่ว่าง'+' '+admin

                sendthai(email,subject,msg)
#-----------------------------------------------------------------------------------------------------------
            return redirect(url_for('dashboard.Dashboard'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()




@booking.route("/closeroom",methods=["POST"])
def Closeroom():
    if request.method == "POST":
        id = request.form["id"]
        status = request.form["status"]
        room = request.form["room"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE  `db_booking` SET `bk_status` =%s WHERE `bk_id`=%s"
            cur.execute(sql,(status,id))
            con.commit()
            cur.close()
            #----แจ้งเตือนผ่านไลน์--------------------------------------------
            token = '6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O'
            messenger = Sendline(token)
            messenger.sendtext('คุณ' + session['fname']+' '+ 'ใช้งานห้องประชุมเสร็จแล้ว' + ' '+room)
            #----สิ้นสุด----------------------------------------------------

            if room == 'Malakul':
                return redirect(url_for('booking.Malakul'))
            if room == 'Thanasriporn':
                return redirect(url_for('booking.Thanasriporn'))
            if room == 'Chadjew':
                return redirect(url_for('booking.Chadjew'))
            return redirect(url_for('booking.Chadjew'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@booking.route("/cancelroom",methods=["POST"])
def Cancelroom():
    if request.method == "POST":
        id = request.form["id"]
        room = request.form["room"]
        status = request.form["status"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE  `db_booking` SET `bk_status` =%s WHERE `bk_id`=%s"
            cur.execute(sql,(status,id))
            con.commit()
            cur.close()
            if room == 'Malakul':
                return redirect(url_for('booking.Malakul'))
            if room == 'Thanasriporn':
                return redirect(url_for('booking.Thanasriporn'))
            if room == 'Chadjew':
                return redirect(url_for('booking.Chadjew'))
            return redirect(url_for('booking.Chadjew'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@booking.route("/deletebooking",methods=["POST"])
def Deletebooking():
    if request.method == "POST":
        id = request.form["id"]
        room = request.form["room"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "delete from db_booking where bk_id = %s"
            cur.execute(sql,(id))
            con.commit()
            if room == 'Malakul':
                return redirect(url_for('booking.Malakul'))
            if room == 'Thanasriporn':
                return redirect(url_for('booking.Thanasriporn'))
            if room == 'Chadjew':
                return redirect(url_for('booking.Chadjew'))
            return redirect(url_for('booking.Booking'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()



"""
    @booking.route("/updateroom",methods=["POST"])
    def Updateroom():
        if request.method == "POST":
            id = request.form["id"]
            status = request.form["status"]
            email = request.form["email"]
            try:
                con.connect()
                cur = con.cursor()
                sql = "UPDATE  `tb_user` SET `usr_status` =%s WHERE `usr_id`=%s"
                cur.execute(sql,(status,id))
                con.commit()
                cur.close()

                def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

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
                subject = 'สมาชิกได้รับการอนุมัติ'
                msg = '''เจ้าหน้าที่อนุมัติการสมัครสมาชิกเข้าสู่ระบบแจ้งซ่อมของแผนก IT Support แล้วโดย '''+ ' ' + session ['fname'] +' '+ '''ท่านสามารถเข้าสู่ระบบได้ทาง itsupport.dyndns-web.com:88 '''

                sendthai(email,subject,msg)

                return redirect(url_for('dashboard.Dashboard'))

        """
