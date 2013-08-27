#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

cxn = sqlite3.connect('database.db')
cur = cxn.cursor()
def createTable():
    cur.execute("CREATE TABLE device (IMEI VARCHAR(20), sim TINYINT, sd TINYINT)")
    cur.execute("CREATE TABLE package (name VARCHAR(16), user VARCHAR(16), timestamp VARCHAR(12), status TINYINT)")
    print "tables created"
def addData():
    cur.execute("INSERT INTO device VALUES ('dev1', 0, 0)")
    cur.execute("INSERT INTO device VALUES ('dev2', 1, 0)")
    cur.execute("INSERT INTO device VALUES ('dev3', 0, 1)")
    cur.execute("INSERT INTO device VALUES ('dev4', 1, 1)")
    cur.execute("INSERT INTO device VALUES ('dev5', 1, 0)")
    cur.execute("INSERT INTO package VALUES ('Album', 'user', '201308161509', 0)")
    cur.execute("INSERT INTO package VALUES ('Alarm', 'user', '201308161510', 0)")
    cur.execute("INSERT INTO package VALUES ('Music', 'user', '201308161511', 0)")
    cur.execute("INSERT INTO package VALUES ('Home', 'user', '201308161512', 0)")
    cur.execute("INSERT INTO package VALUES ('Phone', 'user', '201308161515', 0)")
    cur.execute("INSERT INTO package VALUES ('FM', 'user', '201308161517', 0)")
    cur.execute("INSERT INTO package VALUES ('Message', 'user', '201308161516', 0)")
    cur.execute("INSERT INTO package VALUES ('Contact', 'user', '201308161519', 0)")
    cur.execute("INSERT INTO package VALUES ('Setting', 'user', '201308161519', 0)")
    cur.execute("INSERT INTO package VALUES ('Downloads', 'user', '201308171519', 0)")
    cur.execute("INSERT INTO package VALUES ('Movies', 'user', '201308171619', 0)")
    cur.execute("INSERT INTO package VALUES ('Walkman', 'user', '201308181519', 0)")
    print "data inserted"

def clear():
    try:
        cur.execute("DROP TABLE device")
        cur.execute("DROP TABLE package")
    except:
        pass
    finally:
        print "table clear"
    
def showTable(table):
    cur.execute("SELECT * FROM %s"%table)
    for i in cur.fetchall():
        print i
#showTable('package')
clear()
createTable()
addData()
showTable('device')
showTable('package')
cur.close()
cxn.commit()
cxn.close()
