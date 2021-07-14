#Import Libraries & Functions
from flask import Flask, render_template, request, session, g, redirect
from PIL import Image
from ML import wrapper

from models.users import (
    checkpassword,
    getemail,
    make_user, 
    insert,
    getname
)

from models.savedtext import (
    insert_text,
    get_text,
    text_tbl
)

from models.summ import (
    getq, summary_tbl
)

from ML.OCR import get_text
import time
from gtts import gTTS 
import os
from ML.ptt import get_pdf
import sqlite3

app = Flask(__name__)
app.secret_key = 'somekey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

make_user()
text_tbl("app.db")
summary_tbl("app.db")

# transformer = wrapper.customwrapper()

#This decorator is what converts them to URLs
@app.before_request
def security():
    g.user = None
    for i in session:
        print(session[i])
    if 'user_email' in session:
        emails = getemail()
        try:
            useremail = [email for email in emails if email[0] == session['user_email']][0]
            g.user = useremail
        except Exception as e:
            print("failed")
 
 #LOGIN
@app.route("/", methods=["GET", 'POST'])
def login():
    print("IN LOGIN")
    session.pop("user_email", None)
    if request.method == "POST":
        email = request.form["email"]
        try:
            name = request.form['name']
        except Exception as e:
            name = None


        password = request.form['password']

        if name != None:

            insert("user", values=(email, name, password))
            session['user_email'] = email
            return redirect('upload')
       
        if name == None:
            if checkpassword(password, email):
               
                session['user_email'] = email ## session makes a cookie
                return redirect('upload')
        return redirect("/")

        # print(password, email, name)
    return render_template("login.html")

#Checks type of file and returns the extension type
def checkext(name):
    ext = name.split('.')[1]
    return ext

@app.route("/upload", methods = ["POST", "GET"])
def upload():
  
    if g.user != None:
        if request.method=="POST":
            
            img = request.files["image"]
            #If pdf then run pdf function
            if checkext(img.filename) == 'pdf':
                text = get_pdf(img.filename)
            #For images
            else:
                text = get_text(img.filename)

            #Insert text into database
            text = ' '.join(text)
            insert_text('Text', g.user[0], text, path='app.db')

        return render_template("upload.html")
    return redirect("/")

#DASHBOARD
@app.route('/dashboard', methods=['GET', 'POST'])
def dash():
    if g.user != None:
        name = getname(g.user)
        
        return render_template("temp.html", name=name, email=g.user[0])
    return redirect('/')

#DISPLAY
@app.route('/display', methods=['GET', 'POST'])
def disp():
    if g.user != None:
        summ = getq(g.user[0])[0]
        return render_template("display.html", name=getname(g.user),  text=summ)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5000)