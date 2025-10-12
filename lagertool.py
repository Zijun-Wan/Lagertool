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

# route for register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form.get('submit') == 'REGISTER':
            # TODO: add register function here and delete flash
            # register function should add the new user to the database
            flash("registering...")
            return redirect(url_for('login'))
    return render_template('register.html')

# TODO:route for My Bookings and change to the same way as others
@app.route('/mybookings')
def mybookings():
    conn = sqlite3.connect("Lagertur.db")
    cur = conn.cursor()
    
    # TODO:Shouldn't this show only the bookings for the exact user? i.e WHERE systemLog.userID = user01.user_info[0]
    # I'm not familiar with JOIN statements, so I leave this for now we fix later
    # SELECT JOIN: Item-Name + Start + Ende
    cur.execute("""
        SELECT systemLog.logID, item.name, systemLog.startTime, systemLog.endTime 
        FROM item 
        JOIN systemLog ON item.itemID = systemLog.itemID
    """)
    
    rows = cur.fetchall()
    conn.close()
    if request.method == 'POST':
        if request.form.get('submit') == 'INVENTORY':
            return redirect(url_for('inventorycheck'))
        else:
            log_id = request.form.get('submit')
            # TODO: add cancle.html and cancle function
            return redirect(url_for('cancle', log_id=log_id))
    return render_template('mybookings.html', bookings=rows)

# route for Inventory Check
@app.route('/inventorycheck', methods=['GET', 'POST'])
def inventorycheck():
    conn = sqlite3.connect("Lagertur.db")
    cur = conn.cursor()
    
    # Fetch item lists
    # TODO: add an category part to the database
    cur.execute("SELECT itemID, name, catagory, total, borrow FROM item")
    items = cur.fetchall()
    conn.close()
    
    if request.method == 'POST':
        if request.form.get('submit') == 'Edit':
            return redirect(url_for('edit_inventory'))
        elif request.form.get('submit') == 'BACK':
            return redirect(url_for('back'))
        elif request.form.get('submit') == 'LOGOUT':
            user01.initialize(-1, -1)
            return redirect(url_for('login'))
        else:
            item_id = request.form.get('submit')
            return redirect(url_for('bookingaviability', item_id=item_id))
    return render_template('inventorycheck.html', kit_lists=items)

# TODO:route for Booking Aviability
@app.route('/bookingaviability', methods=['GET', 'POST'])
def bookingaviability():
    if request.method == 'POST':
        if request.form.get('submit') == 'CHECK':
            flash("checking aviability...")
    return render_template('bookingaviability.html')

# route for back (404)
@app.route('/back')
def back():
    return render_template('back.html')

# TODO:route for Edit Inventory
@app.route('/edit_inventory', methods=['GET', 'POST'])
def edit_inventory():
    return render_template('edit_inventory.html')

# TODO: route for cancle this is not even started
@app.route('/cancle/<log_id>', methods=['GET', 'POST'])
def cancle(log_id):
    if request.method == 'POST':
        if request.form.get('submit') == 'CANCLE':
            flash("cancelling booking...")

# ───────────── App starten ─────────────
if __name__== "__main__":
    app.run(debug=True)
