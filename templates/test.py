
import smtplib
import sqlite3

conn = sqlite3.connect("Lagertur.db")
cur = conn.cursor()
cur.execute("SELECT storageID, name FROM item WHERE storageID = 1")
var = cur.fetchall()
print(var)
conn.close()