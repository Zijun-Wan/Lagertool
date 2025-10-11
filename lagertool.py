from flask import Flask, redirect, url_for, render_template, request, flash
import sqlite3

# sector for User
class User:
    # define vaiables in the object
    def __init__(self) -> None:
        self.user_info=[]
        self.type=-1
        self.other_info=[]
        self.other_info_index=-1
        self.temp=0
    
    # functions in the class for accessing the object
    
    # to initialize the user when logged in
    def initialize(self, user_id, cat):
        self.user_info=[]
        self.type=-1
        self.other_info=[]
        self.other_info_index=-1
        self.temp=0
        self.user_info.append(user_id)

    # temporary store for the other information that is needed
    def save_other(self, val):
        self.other_info.append(val)
        self.other_info_index+=1

# initialize Flask app
app = Flask(__name__)
app.secret_key = 'what ever'

# create a user object
user01 = User()

# check user's username and password with database
def UserCheck(user, password):
    conn = sqlite3.connect("Lagertur.db")
    cur = conn.cursor()
    cur.execute("SELECT password, userID FROM login WHERE username='{}'".format(user))
    check = cur.fetchone()
    conn.close()

    if check is None:
        flash("sorry, username does not exist")
        return -1
    else:
        if password == check[0]:
            return check[1]
        else:
            flash("password incorrect")
            return -1

# route for home page (login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('submit') == 'LOGIN':
            userN = request.form.get('username')
            passW = request.form.get('password')
            userID = -1
            userID = UserCheck(userN, passW)
            if userID != -1:
                conn = sqlite3.connect("Lagertur.db")
                cur = conn.cursor()
                cur.execute("SELECT catagory FROM login WHERE userID='{}'".format(userID))
                cat=cur.fetchone()
                user01.initialize(userID, cat[0])
                conn.close()
                return redirect(url_for('mybookings'))
    return render_template('login.html')

# route for My Bookings
@app.route('/mybookings')
def mybookings():
    conn = sqlite3.connect("Lagertur.db")
    cur = conn.cursor()
    
    # SELECT JOIN: Item-Name + Start + Ende
    cur.execute("""
        SELECT item.name, systemLog.startTime, systemLog.endTime 
        FROM item 
        JOIN systemLog ON item.itemID = systemLog.itemID
    """)
    
    rows = cur.fetchall()
    conn.close()
    
    # Array von Dictionaries für Template
    bookings = []
    for row in rows:
        bookings.append({
            'name': row[0],
            'startTime': row[1],
            'endTime': row[2]
        })
    
    return render_template('mybookings.html', bookings=bookings)

# ───────────── App starten ─────────────
if __name__== "__main__":
    app.run(debug=True)
