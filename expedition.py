# imports
from flask import Flask, redirect, url_for,render_template, request,flash
import smtplib
from email.message import EmailMessage
import sqlite3
import calendar
import random
import datetime
import threading
import time

# give sectors to user
class User:
    # define vaiables in the object
    def __init__(self) -> None:
        self.user_info=[]
        self.time=[-1,-1,-1]
        self.ex_choice=[]
        self.mon_list=[]
        self.cal_time=[-1,-1]
        self.type=-1
        self.other_info=[]
        self.other_info_index=-1
        self.temp=0

    # functions in the class for accessing the object

    # to initialize the user when logged in
    def initialize(self, member_id, t):
        self.user_info=[]
        self.time=[-1,-1,-1]
        self.ex_choice=[]
        self.mon_list=[]
        self.cal_time=[-1,-1]
        self.type=-1
        self.other_info=[]
        self.other_info_index=-1
        self.temp=0
        self.user_info.append(member_id)

        if(t=="student"):
            conn = sqlite3.connect("expedition_manager.db")
            cur=conn.cursor()
            cur.execute("SELECT student_ID, year, ski_group, group_leader FROM student WHERE member_ID='{}'".format(member_id))
            info_list=cur.fetchone()

            for i in range(4):
                self.user_info.append(info_list[i])

            conn.commit()
            self.type=0
        else:
            self.type=1

        today=datetime.date.today().timetuple()
        self.time[0]=today.tm_year
        self.time[1]=today.tm_mon
        self.time[2]=today.tm_mday
        self.cal_time[0]=today.tm_year
        self.cal_time[1]=today.tm_mon

    # store the day of selection when user used the calendars
    def save_time(self, year, month, day):
        if year!=-1:
            self.time[0]=year

        if month!=-1:
            self.time[1]=month

        if day!=-1:
            self.time[2]=day
    
    # temporary store for the expedition on selected time
    def exOfTheDay(self, ex_list):
        self.ex_choice=ex_list

    # temporary store for the current calendar for user
    def save_mon(self, mon_list):
        self.mon_list=mon_list
    
    # temporary store for the current time of calendar
    def save_cal_time(self, year, mon):
        self.cal_time[0]=year
        self.cal_time[1]=mon

    # temporary store for the other information that is needed
    def save_other(self, val):
        self.other_info.append(val)
        self.other_info_index+=1

# initialize flask
app = Flask(__name__)
app.secret_key = 'what ever'

# created email for email automation
uname="aiglonex2022@gmail.com"
pw="AbCd0512"

# manager email
manager="aiglonex2022@gmail.com"
now=datetime.datetime.today()

# creating the object
user01=User()

# login page
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":

        if request.form.get("submit") == "LOGIN":
            user = request.form['user']
            password = request.form['password']
            userName=-1
            userName=UserCheck(user, password)
            
            if userName!=-1:
                conn=sqlite3.connect("expedition_manager.db")
                cur=conn.cursor()
                cur.execute("SELECT type FROM login WHERE member_ID='{}'".format(userName))
                member_type=cur.fetchone()
                user01.initialize(userName, member_type[0])
                get_cal(user01.time[0], user01.time[1], user01.time[2])

                if(member_type[0]=="student"):
                    return redirect(url_for('main_student'))
                else:
                    return redirect(url_for('main_staff'))

    return render_template('login.html')

# check user's username and password with database
def UserCheck(user, password):
    conn = sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    cur.execute("SELECT password, member_ID FROM login WHERE username='{}'".format(user))
    check=cur.fetchone()

    if check==None:
        flash("sorry, username does not exist")
        return -1
    else:
        if password==check[0]:
            return check[1]
        else:
            flash("password incorect")
            return -1

# student main page
@app.route('/main_student', methods=["POST", "GET"])
def main_student():
    if request.method == "POST":

        if request.form.get("submit") == "SIGNUP":
            flash(signup())
        elif request.form.get("submit") == "INDEPENDENT_EX":
            flash(independent_ex())
        elif request.form.get("submit") == "PREMON":
            if user01.cal_time[1]==1:
                get_cal(user01.cal_time[0]-1, 12, -1)
            else:
                get_cal(user01.cal_time[0], user01.cal_time[1]-1, -1)
        elif request.form.get("submit") == "NEXTMON":
            if user01.cal_time[1]==12:
                get_cal(user01.cal_time[0]+1, 1, -1)
            else:
                get_cal(user01.cal_time[0], user01.cal_time[1]+1, -1)
        else:
            value=int(request.form.get("submit"))
            date(value)
            show_expeditions()

        return redirect(url_for("main_student"))
    return render_template('main_student.html', day=user01.mon_list, year=user01.cal_time[0], mon=switch_month(user01.cal_time[1]), ex_choice=user01.ex_choice)

# functions to get the date clicked on the calendar
def date(value):
    week=int(value/7)
    day_of_week=value%7

    if(value-14>user01.mon_list[week][day_of_week]):
        if (user01.cal_time[1]==12):
            user01.save_time(user01.cal_time[0]+1, 1,user01.mon_list[week][day_of_week])
        else:
            user01.save_time(user01.cal_time[0],user01.cal_time[1]+1,user01.mon_list[week][day_of_week])
        return

    if(value+14<user01.mon_list[week][day_of_week]):
        if (user01.cal_time[1]==1):
            user01.save_time(user01.cal_time[0]-1, 12,user01.mon_list[week][day_of_week])
        else:
            user01.save_time(user01.cal_time[0],user01.cal_time[1]-1,user01.mon_list[week][day_of_week])
        return

    user01.save_time(user01.cal_time[0],user01.cal_time[1],user01.mon_list[week][day_of_week])
    return

# function to get the month name for the calendar
def switch_month(mon):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return switcher[mon]

# function to get the calendar of the month selected on the calendar
def get_cal(year, month, day):
    # pre&next
    if(day==-1):
        user01.save_time(year, month, 1)
    # initialize
    else:
        user01.save_time(year, month, day)
    
    user01.save_cal_time(year, month)
    curMonth=calendar.monthcalendar(year, month)
    
    if month==1:
        pre_mon=calendar.monthcalendar(year-1, 12)
    else:
        pre_mon=calendar.monthcalendar(year, month-1)

    for i in range(7):
        if curMonth[0][i]==0:
            curMonth[0][i]=pre_mon[-1][i]
        else:
            break

    if month==12:
        next_mon=calendar.monthcalendar(year+1, 1)
    else:
        next_mon=calendar.monthcalendar(year, month+1)

    filled=0

    # fill the gaps on the calendar with dates of previous month
    for i in range(7):
        if curMonth[-1][6-i]==0:
            curMonth[-1][6-i]=next_mon[0][6-i]
            filled=1
        else:
            break
    length=len(curMonth)

    # fill the gaps on the calendar with dates of next month
    if length<6:
        for i in range (6-length):
            curMonth.append(next_mon[0+filled+i])
    show_expeditions()
    user01.save_mon(curMonth)

# function for independent expedition
def independent_ex():

    #check if is group leader
    if user01.user_info[4]!=1:
        return "you are not a group leader"

    conn = sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    counter=1
    date_txt=str(user01.time[2])+'.'+str(user01.time[1])+'.'+str(user01.time[0])
    cur.execute("SELECT expedition_name FROM expedition_arrange WHERE date='{}'".format(date_txt))
    ex_list=cur.fetchall()
    ex_name="independent_group"+str(counter)
    
    while ex_name in ex_list:
        counter+=1
        ex_name="independent_group"+str(counter)
    
    cur.execute("INSERT INTO expedition_arrange (date, expedition_name, expedition_ID, max, min, year_group_max, year_group_min, ski_group_max, ski_group_min, status, informed) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}', '{}')".format(date_txt, ex_name, 3, 6, 3, -1,-1, -1, -1, 0, 0))
    cur.execute("SELECT arranging_ID, expedition_name FROM expedition_arrange WHERE date='{}'".format(date_txt))
    ex_list=cur.fetchall()
    arrange=-1

    for elm in ex_list:
        if(elm[1]==ex_name):
            arrange=elm[0]
            break

    student="student"+str(user01.user_info[1])
    cur.execute("INSERT INTO student_list (arranging_ID, total, '{}') VALUES ('{}', '{}', '{}')".format(student, arrange, 1, 1))
    conn.commit()
    ex_name="your group name is "+ex_name
    manage_amount_expedition()
    return ex_name

# function for signup
def signup():
    arrange=int(request.form['expedition_choices'])
    conn = sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    student="student"+str(user01.user_info[1])
    txt="SELECT total, "+student+" FROM student_list WHERE arranging_ID='{}'"
    cur.execute(txt.format(arrange))
    t=cur.fetchone()

    # prevent a student booking the same expedition twice and sign up if the student is not yet in the expedition
    if(t[1]!=1):
        total=int(t[0])+1
        cur.execute("UPDATE student_list SET '{}' = '{}', total = '{}' WHERE arranging_ID ='{}'".format(student, 1, total, arrange))
        conn.commit()
        return "success"

    conn.commit()
    manage_amount_expedition()
    return "you're in already"

# manage database for the amount of expedition done
def manage_amount_expedition():
    conn = sqlite3.connect("expedition_manager.db")
    cur = conn.cursor()
    cur.execute("SELECT num_completed FROM student WHERE student_id = '{}'".format(user01.user_info[0]))
    num=cur.fetchone()
    new=num[0]+1
    cur.execute("UPDATE student SET num_completed = '{}' WHERE student_id = '{}'".format(new, user01.user_info[0]))
    conn.commit()

# get ex for the day
def show_expeditions():
    text = str(user01.time[2])+'.'+str(user01.time[1])+'.'+str(user01.time[0])
    conn = sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    
    # student
    if user01.type == 0:
        cur.execute("SELECT arranging_ID, expedition_name, max, min, year_group_max, year_group_min, ski_group_max, ski_group_min FROM expedition_arrange WHERE date='{}'".format(text))
        temp=cur.fetchall()
        expeditions=[]

        for i in range(len(temp)):
            expeditions.append([])

            for j in temp[i]:
                expeditions[i].append(j)

        delete_list=[]

        for i in range(len(expeditions)):
            cur.execute("SELECT total FROM student_list WHERE arranging_ID='{}'".format(expeditions[i][0]))
            total=cur.fetchone()
            conn.commit()

            if(not(expeditions[i][4]<=user01.user_info[1]<=expeditions[i][5] and expeditions[i][4]!=-1 or expeditions[i][4]==-1)):
                delete_list.append(i)

            if(not(expeditions[i][6]<=user01.user_info[2]<=expeditions[i][7] and expeditions[i][6]!=-1 or expeditions[i][6]==-1)):
                delete_list.append(i)

            if(total[0]>=expeditions[i][2]):
                delete_list.append(i)

        for i in range(len(delete_list)):
            expeditions.pop(delete_list[len(delete_list)-i-1])
    
    # staff
    else:
        cur.execute("SELECT arranging_ID, expedition_name FROM expedition_arrange WHERE date='{}'".format(text))
        expeditions=cur.fetchall()
        conn.commit()
        
    my_list=[]

    for i in range (len(expeditions)):
        my_list.append([expeditions[i][0], expeditions[i][1]])

    user01.exOfTheDay(my_list)
# no need to go to anther page for students

# staff main_page
@app.route('/main_staff', methods=["POST", "GET"])
def main_staff():
    if request.method == "POST":
        if request.form.get("submit") == "ARRANGE":
            return redirect(url_for('arrange1'))
        elif request.form.get("submit") == "RETURN":
            return redirect(url_for('ret'))
        elif request.form.get("submit") == "NEW_KIT":
            return redirect(url_for('addKits'))
        elif request.form.get("submit") == "NEW_EX":
            return redirect(url_for('new_ex'))
        elif request.form.get("submit") == "NEW_MEMBER":
            return redirect(url_for('addMember'))
        elif request.form.get("submit") == "reset":
            reset()

    return render_template('main_staff.html')

# resetting
def reset():
    conn= sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    cur.execute("SELECT student_id FROM student")
    l=cur.fetchall()

    for i in range(len(l)):
        cur.execute("UPDATE student SET num_completed = 0 WHERE student_id = '{}'".format(l[i][0]))


# managing database
def init_database():
    print("aaaaa")
    kitsManage()
    studentManage()

# manage kits in database
def kitsManage():
    conn=sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    new=[]
    columns=[i[1] for i in cur.execute("PRAGMA table_info(kit_lists)")]

    for row in cur.execute("SELECT kits_ID FROM kits"):
        new.append("kit"+str(row[0]))

    for i in range(len(new)):
        if new[i] not in columns:
            text2="ALTER TABLE kit_lists ADD COLUMN "+new[i]+" INTEGER"
            cur.execute(('{}').format(text2))

    conn.commit()

# manage students in database
def studentManage():
    conn=sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    new=[]
    columns=[i[1] for i in cur.execute("PRAGMA table_info(student_list)")]

    for row in cur.execute("SELECT student_ID FROM student"):
        new.append("student"+str(row[0]))

    for i in range(len(new)):
        if new[i] not in columns:
            text2="ALTER TABLE student_list ADD COLUMN "+new[i]+" INTEGER"
            cur.execute(('{}').format(text2))

    conn.commit()

# arrange1
@app.route('/arrange1', methods=["POST", "GET"])
def arrange1():
    if request.method == "POST":

        if request.form.get("submit") == "PREMON":
            if user01.cal_time[1]==1:
                get_cal(user01.cal_time[0]-1, 12, -1)
            else:
                get_cal(user01.cal_time[0], user01.cal_time[1]-1, -1)
        elif request.form.get("submit") == "NEXTMON":
            if user01.cal_time[1]==12:
                get_cal(user01.cal_time[0]+1, 1, -1)
            else:
                get_cal(user01.cal_time[0], user01.cal_time[1]+1, -1)
        elif request.form.get("submit") == "DELETE":
            delete(int(request.form['expedition_choices']))
        elif request.form.get("submit") == "ADD":
            user01.save_other(request.form['exName'])
            return redirect(url_for("arrange2"))
        elif request.form.get("submit") == "HOME":
            return redirect(url_for("main_staff"))
        else:
            value=int(request.form.get("submit"))
            date(value)
            show_expeditions()

        return redirect(url_for("arrange1"))

    return render_template('arrange1.html', day=user01.mon_list, year=user01.cal_time[0], mon=switch_month(user01.cal_time[1]), ex_choice=user01.ex_choice)

# delete expedition
def delete(arrange):
    # cancle_email(arrange)
    conn = sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM expedition_arrange WHERE arranging_ID='{}'".format(arrange))
    cur.execute("DELETE FROM student_list WHERE arranging_ID='{}'".format(arrange))
    conn.commit()

# arramge2
@app.route('/arrange2', methods=["POST", "GET"])
def arrange2():
    if request.method == "POST":

        if request.form.get('submit') == "CONFIRM":
            conn=sqlite3.connect("expedition_manager.db")
            cur=conn.cursor()
            cur.execute("SELECT expedition_ID from expeditions WHERE expedition_title='{}'".format(request.form['name']))
            temp=cur.fetchone()
            conn.commit()

            if temp!=None:
                group=user01.other_info.pop()
                date_txt=str(user01.time[2])+'.'+str(user01.time[1])+'.'+str(user01.time[0])
                max=request.form['max']
                min=request.form['min']
                skiMax=request.form['skiMax']
                skiMin=request.form['skiMin']
                yearMax=request.form['yearMax']
                yearMin=request.form['yearMin']
                cur.execute("INSERT INTO expedition_arrange (date, expedition_ID, expedition_name, max, min, ski_group_max, ski_group_min, year_group_max, year_group_min, status) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(date_txt, temp[0], group, max, min, skiMax, skiMin, skiMin, yearMax, yearMin, 0))
                cur.execute("SELECT arranging_ID FROM expedition_arrange WHERE expedition_name = '{}'".format(group))
                ex_id=cur.fetchone()
                cur.execute("INSERT INTO student_list (arranging_ID, total) VALUES ('{}', '{}')".format(ex_id[0],0))
                conn.commit()
                return redirect('arrange1')
            else:
                flash("expedition does not exist")

    return render_template('arrange2.html')

# return
@app.route('/ret', methods=["POST", "GET"])
def ret():
    exList=getAll()

    if request.method == "POST":

        if request.form.get("submit") == "HOME":
            return redirect(url_for("main_staff"))
        else:
            user01.save_other(request.form.get("submit"))
            return redirect(url_for("confirm"))

    return render_template('ret.html', ex=exList)

# get all the expeditions that are not yet returned
def getAll():
    conn = sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    cur.execute("SELECT date, arranging_ID, expedition_name FROM expedition_arrange WHERE status='{}'".format(0))
    exList=cur.fetchall()
    conn.commit()
    return exList

# new_ex
@app.route('/new_ex', methods=["POST", "GET"])
def new_ex():
    all_kit=get_List()
    
    if request.method == "POST":
        
        if request.form.get("submit") == "HOME":
            return redirect(url_for("main_staff"))
        elif request.form.get("submit") == "CONFIRM":
            title=request.form["ex_title"]
            conn = sqlite3.connect("expedition_manager.db")
            cur=conn.cursor()
            cur.execute("SELECT kit_list1, kit_list2 FROM expeditions WHERE expedition_title='{}'".format(title))
            temp=cur.fetchone()
            
            if temp==None:
                cur.execute("SELECT kit_list_ID FROM kit_lists")
                list1=cur.fetchall()
                m=0
                
                for i in list1:
                    if i[0]>m:
                        m=i[0]
                
                id1=m+1
                id2=m+2
                
                for i in range(len(all_kit)):
                    txt1 = "list1"+str(all_kit[i][0])
                    txt2 = "list2"+str(all_kit[i][0])
                    txt3 = "kit"+str(all_kit[i][0])
                    list1_num=request.form[txt1]
                    list2_num=request.form[txt2]
                    
                    if i==0:
                        cur.execute("INSERT INTO kit_lists (kit_list_ID, '{}') VALUES ('{}','{}')". format(txt3, id1, list1_num))
                        cur.execute("INSERT INTO kit_lists (kit_list_ID, '{}') VALUES ('{}','{}')". format(txt3, id2, list2_num))
                    else:
                        cur.execute("UPDATE kit_lists SET '{}' = '{}' WHERE kit_list_ID='{}'". format(txt3, list1_num, id1))
                        cur.execute("UPDATE kit_lists SET '{}' = '{}' WHERE kit_list_ID='{}'". format(txt3, list2_num, id2))
                
                cur.execute("INSERT INTO expeditions (expedition_title,kit_list1, kit_list2) VALUES('{}', '{}', '{}')".format(title,id1,id2))
            
            else:
                id1=temp[0]
                id2=temp[1]
                
                for i in range(len(all_kit)):
                    txt1 = "list1"+str(all_kit[i][0])
                    txt2 = "list2"+str(all_kit[i][0])
                    cur.execute("UPDATE kit_lists SET '{}' = '{}' WHERE kit_list_ID='{}'". format(txt1, request.form[txt1], id1))
                    cur.execute("UPDATE kit_lists SET '{}' = '{}' WHERE kit_list_ID='{}'". format(txt2, request.form[txt2], id2))
            
            conn.commit()

    return render_template('new_ex.html', kit_lists=all_kit)

# get list of all the kits
def get_List():
    conn = sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    cur.execute("SELECT kits_ID, kits_name FROM kits")
    temp=cur.fetchall()
    l=[]
    
    for i in range(len(temp)):
        l.append([])
        txt1="list1"+str(temp[i][0])
        txt2="list2"+str(temp[i][0])
        l[i].append(temp[i][0])
        l[i].append(temp[i][1])
        l[i].append(txt1)
        l[i].append(txt2)
    
    conn.commit()
    return l

# confirm
@app.route('/confirm', methods=["POST", "GET"])
def confirm():
    details = getDetails()
    
    if request.method == "POST":
        
        if request.form.get('submit')=="CONFIRM":
            conn = sqlite3.connect("expedition_manager.db")
            cur=conn.cursor()
            
            for i in range(len(details)):
                cur.execute("SELECT usable_num, num_need_repair FROM kits_manage WHERE kits_ID = '{}'".format(details[i][1]))
                temp=cur.fetchone()
                kit_info=[]
                
                print(temp)

                for j in temp:
                    kit_info.append(j)
                
                change=request.form[str(details[i][1])]
                
                if kit_info[0]== None:
                    kit_info[0]=0
                
                if kit_info[1]== None:
                    kit_info[1]=0
                
                kit_info[0]-=int(change)
                kit_info[1]+=int(change)
                cur.execute("UPDATE kits_manage SET usable_num = '{}', num_need_repair = '{}' WHERE kits_ID = '{}'".format(kit_info[0], kit_info[1], details[i][0]))
            
            cur.execute("UPDATE expedition_arrange SET status = '{}' WHERE arranging_ID = '{}'".format(1, user01.other_info[-1]))
            conn.commit()
            user01.other_info.pop()
            return redirect(url_for("ret"))

    return render_template('confirm.html', ex=details)


# get details of kits used for changing in database

# kit list1 for staff kit list2 for students 
def getDetails():
    conn = sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    cur.execute("SELECT expedition_ID FROM expedition_arrange WHERE arranging_ID='{}'".format(user01.other_info[-1]))
    id=cur.fetchone()
    cur.execute("SELECT kit_list1 FROM expeditions WHERE expedition_ID='{}'".format(id[0]))
    lists=cur.fetchone()
    cur.execute("SELECT * FROM kit_lists WHERE kit_list_ID='{}'".format(lists[0]))
    temp=cur.fetchone()
    list1=[]
    
    for i in temp:
        list1.append(i)
    
    list1.pop(0)
    cur.execute("SELECT kits_name, kits_ID FROM kits")
    temp=cur.fetchall()
    list2=[]
    
    for i in range(len(list1)):
        list2.append([])
        list2[i].append(temp[i][0])
        list2[i].append(temp[i][1])
        list2[i].append(list1[i])
    
    return list2

# member
@app.route('/addMember', methods=["POST", "GET"])
def addMember():
    
    if request.method == "POST":
        
        if request.form.get("submit") == "ADDMEMBER":
            memberUsername = request.form['username']
            memberName = request.form['name']
            membertype = request.form['type']
            conn = sqlite3.connect("expedition_manager.db")
            cur=conn.cursor()
            cur.execute("SELECT member_ID FROM login WHERE username='{}'".format(memberUsername))
            member_ID=cur.fetchone()
            
            if(member_ID==None):
                memberpassword = str(random.randint(100000000000, 999999999999))
                cur.execute("INSERT INTO member (member_name) VALUES ('{}')".format(memberName))
                cur.execute("SELECT member_ID FROM member WHERE member_name='{}'".format(memberName))
                member_ID=cur.fetchone()
                cur.execute("INSERT INTO login (username, password, type, member_ID) VALUES ('{}', '{}', '{}', '{}')".format(memberUsername, memberpassword, membertype, member_ID[0]))
                flash(memberpassword)
                user01.save_other(0)
            else:
                cur.execute("UPDATE member SET member_name='{}' WHERE member_ID='{}'".format(memberName, member_ID[0]))
                cur.execute("UPDATE login SET type='{}' WHERE member_ID='{}'".format(membertype, member_ID[0]))
                user01.save_other(1)

            conn.commit() 

            if(membertype=="student"):
                user01.save_other(member_ID[0])
                return redirect(url_for("addStudent"))

        elif request.form.get("submit") == "HOME":
            return redirect(url_for("main_staff"))

    return render_template('addMember.html')
        
# kits
@app.route('/addKits', methods=["POST", "GET"])
def addKits():
    
    if request.method == "POST":
        
        if request.form.get("submit") == "ADDKITS":
            kitName = request.form['kitName']
            kitType = request.form['kitType']
            newNumber = int(request.form['kitNumber'])
            repaired = int(request.form['repaired'])
            conn = sqlite3.connect("expedition_manager.db")
            cur=conn.cursor()
            cur.execute("SELECT total_num, kits_ID FROM kits WHERE kits_name='{}'".format(kitName))
            check=cur.fetchone()
            
            try:
                total=check[0]+newNumber
                cur.execute("UPDATE kits SET total_num='{}' WHERE kits_name='{}'".format(total, kitName))
                cur.execute("SELECT usable_num, num_need_repair FROM kits_manage WHERE kits_ID='{}'".format(check[1]))
                temp=cur.fetchone()
                
                if temp[0]==None:
                    temp[0]=0
                
                if temp[1]==None:
                    temp[1]=0
                
                temp[0]=temp[0]+repaired+newNumber
                temp[1]-=repaired
                cur.execute("UPDATE kits_manage SET usable_num='{}', num_need_repair='{}' WHERE kit_ID='{}'".format(temp[0], temp[1], check[1]))
                conn.commit()
            except:
                cur.execute("INSERT INTO kits (kits_name, kits_type, total_num) VALUES ('{}', '{}', '{}')".format(kitName, kitType, newNumber))
                cur.execute("SELECT kits_ID FROM kits WHERE kits_name='{}'".format(kitName))
                id=cur.fetchone()
                cur.execute("INSERT INTO kits_manage (kits_ID, usable_num, num_need_repair) VALUES ('{}', '{}', '{}')".format(id[0], newNumber, 0))
                conn.commit()
                kitsManage()
            
        elif request.form.get("submit") == "HOME":
            return redirect(url_for("main_staff"))

    return render_template('addKits.html')

# student
@app.route('/addStudent', methods=["POST", "GET"])
def addStudent():
    
    if(request.method == "POST"):
        
        if request.form.get("submit") == "ADDSTUDENT":
            house = request.form['house']
            skiGroup = request.form['skiGroup']
            
            if(request.form['groupLeader'].upper() == 'Y' or request.form['groupLeader'].upper() == 'YES'):
                groupLeader=1
            else:
                groupLeader=0
            
            year = request.form['year']
            conn = sqlite3.connect("expedition_manager.db")
            cur=conn.cursor()
            
            if user01.other_info[-2]==0:
                cur.execute("INSERT INTO student (member_ID, house, ski_group, group_leader, year, num_completed) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(user01.other_info[-1], house, skiGroup, groupLeader, year, 0))
                conn.commit()
                studentManage()
            else:
                cur.execute("UPDATE student SET house = '{}', ski_group = '{}', group_leader = '{}', year = '{}', num_completed = '{}' WHERE user_ID = '{}'".format(house, skiGroup, groupLeader, year, user01.other_info[-1]))
                conn.commit()

            user01.other_info.pop()
            user01.other_info.pop()
            return redirect(url_for("addMember"))

    return render_template('addStudents.html')

# function for the final information email
def final_info_email(now):
    conn= sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    tmr=datetime.datetime(now.tm_year,now.tm_mon,now.tm_mday+1).timetuple()
    tmr_txt=str(tmr.tm_mday)+"."+str(tmr.tm_mon)+"."+str(tmr.tm_year)
    cur.execute("SELECT arranging_ID, expedition_ID, min, expedition_name FROM expedition_arrange WHERE date='{}', informed='{}'".format(tmr_txt, 0))
    temp=cur.fetchall()
    l=[]
    
    for i in range(len(temp)):
        l.append([])
        
        for j in range(len(temp[i])):
            l[i].append(temp[i][j])

    delete_list=[]
    
    for i in range(len(l)):
        cur.execute("SELECT total FROM student_list WHERE arranging_ID='{}'".format(l[i][0]))
        t=cur.fetchone()
        
        if t[0]<l[i][2]:
            delete_list.append(i)
            delete(l[i][0])
    
    for i in range(len(delete_list)):
        l.pop(delete_list[len(delete_list)-i-1])
    
    for i in range(len(l)):
        body="your ex, '{}' is on '{}'. please bring the following kits. ".format(l[i][3], tmr_txt)
        cur.execute("SELECT kit_list2 FROM expedition WHERE expedition_ID='{}'".format(l[i][1]))
        k_id=cur.fetchone()
        cur.execute("SELECT * FROM kit_list WHERE kit_list_ID = '{}'".format(k_id[0]))
        temp=cur.fetchone()
        k=[]

        for j in temp:
            k.append(j)
        k.pop(0)

        for j in range(len(k)):

            if k[j]!=0:
                cur.execute("SELECT kits_name FROM kits WHERE kit_id='{}'".format(j+1))
                n=cur.fetchone()
                body=body+n[0]+"*"+str(k[j])+", "

        cur.execute("SELECT * from student_list WHERE arranging_ID='{}'".format(l[i][0]))
        temp=cur.fetchone()
        student=[]

        for j in temp:
            student.append(j)

        student.pop(0)
        student.pop(0)
        
        for j in range (len(student)):
            
            if student(j)==1:
                student_id=j+1
                cur.execute("SELECT member_id FROM student WHERE student_id = '{}'".format(student_id))
                member=cur.fetchone()
                cur.execute("SELECT username FROM login WHERE member_id = '{}'".format(member))
                mail=cur.fetchone()
                msg = EmailMessage()
                subject="upcomming expedition"
                msg['Subject'] = (subject)
                msg['From'] = (uname)
                msg['To'] = (mail[0])
                msg.set_content(body)
                
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(uname,pw)
                    smtp.send_message(msg)
                    smtp.quit()

        conn.commit()

# function for cancle expedition email
def cancle_email(arrange_ID):
    conn = sqlite3.connect("expedition_manager.db")
    cur=conn.cursor()
    cur.execute("SELECT date, expedition_name FROM expedition_arrange WHERE arranging_ID='{}'".format(arrange_ID))
    ex_info=cur.fetchone()
    body="Your expedition, '{}' on '{}' has been cancled".format(ex_info[1], ex_info[0])
    cur.execute("SELECT * from student_list WHERE arranging_ID='{}'".format(arrange_ID))
    temp=cur.fetchone()
    student=[]
    
    for i in temp:
        student.append(i)
    
    student.pop(0)
    student.pop(0)
    
    for j in range (len(student)):
        
        if student[j]==1:
            student_id=j+1
            cur.execute("SELECT member_id FROM student WHERE student_id = '{}'".format(student_id))
            member=cur.fetchone()
            cur.execute("SELECT username FROM login WHERE member_id = '{}'".format(member))
            mail=cur.fetchone()
            msg = EmailMessage()
            subject="cancled expedition"
            msg['Subject'] = (subject)
            msg['From'] = (uname)
            msg['To'] = (mail[0])
            msg.set_content(body)
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(uname,pw)
                smtp.send_message(msg)
                smtp.quit()

# function for kits status email
def kits_email():
    body="The following kits needs to be repaired. "
    conn = sqlite3.connect("expedition_manager.db")
    cur = conn.cursor()
    cur.execute("SELECT kits_ID, num_need_repair FROM kits_manage WHERE num_need_repair > 0")
    l=cur.fetchall()
    
    for i in l:
        cur.execute("SELECT kits_name FROM kits WHERE kits_ID = '{}'".format(i[0]))
        kit_name=cur.fetchone()
        body=body+str(i[1])+" "+kit_name[0]+", "
    
    msg = EmailMessage()
    subject="kits need to be repaired"
    msg['Subject'] = (subject)
    msg['From'] = (uname)
    msg['To'] = (manager)
    msg.set_content(body)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(uname,pw)
        smtp.send_message(msg)
        smtp.quit()

# functions for noticing about student not meeting requirements email
def requirements_email():
    conn = sqlite3.connect("expedition_manager.db")
    cur = conn.cursor()
    cur.execute("SELECT year, student_ID, num_completed FROM student")
    l=cur.fetchall()
    cur.execute("SELECT num_needed FROM year_group")
    required=cur.fetchall()
    
    for i in l:
        body="You have not yes completed your requirements. You still need to complete "
        
        if l[i][2]<required[l[i][0]-1][1]:
            body= body+ str(int(required[l[i][0]-1][1])-int(l[i][2]))
            cur.execute("SELECT username FROM login WHERE member_id = '{}'".format(l[i][1]))
            mail=cur.fetchone()
            msg = EmailMessage()
            subject="have not completed your requirements yet"
            msg['Subject'] = (subject)
            msg['From'] = (uname)
            msg['To'] = (mail[0])
            msg.set_content(body)
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(uname,pw)
                smtp.send_message(msg)
                smtp.quit()

# email sending (use multi threading)
def running():
    today=datetime.datetime.today()
    
    while 1:
        print("bob")
        now=datetime.datetime.today()
        next_d=False
        
        if now.timetuple().tm_mday!=today.timetuple().tm_mday:
            next_d=True
            print("bob1")
        
        if next_d==True:
            print("bob2")
            final_info_email(now)
            
            if now.timetuple().tm_wday==6:
                requirements_email()
                kits_email()
            
            today=datetime.datetime.today()
            next_d=False
            print("bob3")
        
        time.sleep(1800)


# running the program
if __name__== "__main__":
    init_database()
    # multi threading for doing multiple tasks at once
    threading.Thread(target=lambda: app.run()).start()
    threading.Thread(target=running()).start()