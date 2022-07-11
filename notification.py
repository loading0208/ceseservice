from flask import Blueprint
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)

notification = Blueprint('notification',__name__)

@notification.route("/notification")
def Notification():
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

        sql = "SELECT * FROM tb_user WHERE usr_status = 0"
        cur.execute(sql)
        newuser = cur.fetchall()
        snewuser = len(newuser)

        sql = "SELECT * FROM db_booking WHERE bk_status = 0 OR bk_status = 2 OR bk_status = 10 OR bk_status = 12 OR bk_status=20 OR bk_status = 22"
        cur.execute(sql)
        booking = cur.fetchall()
        sbooking = len(booking)

        sumnoti = snewdesk+swaitdesk+snewuser+sbooking
        sum=str(sumnoti)
        return sum
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
