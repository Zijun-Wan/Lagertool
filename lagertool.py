# imports
from flask import Flask, redirect, url_for,render_template, request,flash
import smtplib
import sqlite3
import calendar
import random
import datetime
import threading
import time

# sector for User
class User:
    # define variables in object
    def __init__(self) -> None:
        self.catagory = ""

# initialize Flask app
app = Flask(__name__)
app.secret_key = 'what ever'

# create a user object
user01 = User()

# check user's username and password with database
def UserCheck(user, password):
    conn = sqlite3.connect("Lagertur.db")
    cur=conn.cursor()
    cur.execute("SELECT password, userID FROM login WHERE username='{}'".format(user))
    check=cur.fetchone()
    conn.close()

    if check==None:
        flash("sorry, username does not exist")
        return -1
    else:
        if password==check[0]:
            return check[1]
        else:
            flash("password incorect")
            return -1
        
# route for home page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('submit') == 'LOGIN':
            userN = request.form.get('username')
            passW = request.form.get('password')
            userID = UserCheck(userN, passW)
            if userID != -1:
                conn = sqlite3.connect("Lagertur.db")
                cur = conn.cursor()
                cur.execute("SELECT catagory FROM login WHERE userID='{}'".format(userID))
                user01.catagory = cur.fetchone()[0]
                conn.close()
                return redirect(url_for('myBorrow'))
    return render_template('login.html')

if __name__== "__main__":
    # run the Flask app
    app.run(debug=True)