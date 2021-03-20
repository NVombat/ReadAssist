import smtplib,ssl
import os
import sqlite3
import models.users

#backend_mail and backend_pwd are environt variables
#by importing os, backmail_add and backmail_pwd are accessing the environment variable values
def send_mail_summ(e : str, s : str):

    conn= sqlite3.connect("app.db")
    cur = conn.cursor()

    backemail_add = os.environ.get('backend_mail')
    backemail_pwd = os.environ.get('backend_pwd')
    
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(backemail_add,backemail_pwd)

    cmd = f"Select Name from user where Email='{e}'"
    cur.execute(cmd)
    n = cur.fetchone()
    user_name = n[0]
    
#user mail subject, body and format of the mail
    subject = 'Read Assist Summary:'
    body = f'Dear {user_name}\nThankyou for choosing Read Assist.\n\nTHIS IS THE SUMMARY OF THE UPLOADED DOCUMENT.\n\n{s}\n\nWe hope to see you again!\n\nThe Read Assist Team'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(backemail_add,e,msg)
    server.quit()

#send questions to the mail
def send_mail_ques(e : str, s : str):

    conn= sqlite3.connect("app.db")
    cur = conn.cursor()

    backemail_add = os.environ.get('backend_mail')
    backemail_pwd = os.environ.get('backend_pwd')
    
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(backemail_add,backemail_pwd)

    cmd = f"Select Name from user where Email='{e}'"
    cur.execute(cmd)
    n = cur.fetchone()
    user_name = n[0]
    
#user mail subject, body and format of the mail
    subject = 'Read Assist Questions:'
    body = f'Dear {user_name}\nThankyou for choosing Read Assist.\n\n THESE ARE THE QUESTIONS BASED ON THE UPLOADED FILE:\n\n{s}\n\nWe hope to see you again!\n\nThe Read Assist Team'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(backemail_add,e,msg)
    server.quit()


