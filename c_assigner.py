#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task Assigner

Feature:                                                                          
    Match packages with idle devices.Maintain task queue.
"""
import sys
import os
import sqlite3
import redis
import threading
import subprocess
import random
from time import clock, ctime, sleep

MAXLEN = 8    #队列长度
basedir = os.getcwd()   #根目录
start = clock()

class MyThread(threading.Thread):
    """Define thread"""
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args


    def run(self):
        print 'starting', self.name, 'at:', ctime()
        self.res = apply(self.func, self.args)
        print self.name, 'finished at:', ctime()

class Queue(object):
    def __init__(self):
        self.add()
        self.queue = rs.lrange('pkg', 0, -1)

    def add(self):
        """Add package to queue in Redis from database"""
        (cxn, cur) = connectDB()
        while rs.llen('pkg') < MAXLEN:
            cur.execute("SELECT name FROM package WHERE status = 0 ORDER BY timestamp")    #读取数据库并按timestamp排序
            try:
                self.pkg = cur.fetchone()[0]
                cur.execute("UPDATE package SET status = 1 WHERE name = '%s'" % self.pkg)
                rs.rpush('pkg', self.pkg)
                self.getPkgInfo(self.pkg)
            except TypeError:
                print "No more package waiting"
                break
        closeDB(cxn, cur)
    def remove(self, pkg):
        """Remove package info from Redis"""
        rs.lrem('pkg', 1, pkg)
        rs.delete("package:%s:name"%pkg)
        rs.delete("package:%s:sim"%pkg)
        rs.delete("package:%s:sd"%pkg)
        rs.delete("package:%s:user"%pkg)
    def show(self):
        pkglist = rs.lrange('pkg', 0, -1)
        print 'Current queue:', pkglist
        for pkg in self.queue:
            print rs.mget('package:%s:name' % pkg, 'package:%s:user' % pkg, 'package:%s:sim' % pkg, 'package:%s:sd' % pkg)

    def getPkgInfo(self, pkg):
        """Get package config from config file"""
        cur.execute("SELECT * FROM package WHERE name = '%s'" % pkg)
        pkginfo = cur.fetchone()
        self.user = pkginfo[1]
        cfgdir = os.path.join(basedir, self.user, pkg)
        try:
            f = open(cfgdir+'/'+ pkg +'.cfg')
            info = f.read().split()
            rs.mset({    #将cfg信息存放在Redis中，便于调用
                "package:%s:name"% pkg: info[0],
                "package:%s:sim"% pkg: info[1],
                "package:%s:sd"% pkg: info[2],
                "package:%s:user"% pkg: self.user
                })
        except:
            "Could not open package config"
            rs.lrem('pkg', 1, self.name)

class Assigner(object):
    def __init__(self, dev):
        self.dev = dev

    def distribute(self):
        """Match packages with device"""
        self.devinfo = list(self.getDeviceInfo()[0])
        print self.devinfo
        for pkg in queue.queue:
            if (self.devinfo[1] >= int(rs.get("package:%s:sim"%pkg))
                    and self.devinfo[2] >= int(rs.get("package:%s:sd"%pkg))):
                self.user = rs.get('package:%s:user' % pkg)
#                t = MyThread(runs, (pkg, user), runs.__name__)    
                queue.remove(pkg)
                queue.add()    #补充队列
                sleep(1)
                print 'fin', rs.lrange('pkg', 0, -1)    #打印结束时队列
                self.runs(pkg)
#                t.start()    #子线程开启
                break
        else:
            print "no match"
        end = clock()
        print "Total time: %g s" % (end - start)
        print "--------------------------------------------------------------------------"


    def runs(self, pkg):
        """Run automation test"""
        showThread()
        pkgdir = os.path.join(basedir, self.user, pkg)
        print "run %s at %s" % (pkg, pkgdir)
        print "--------------------------------------------------------------------------"
#        sec = random.randint(25, 30)
#        sleep(sec)
        command = "python sleep.py"
        subprocess.call(command.split(), shell = False)
        print "%s finish" % pkg
        showThread()

    def getDeviceInfo(self):
        """Get device info from database"""
        (cxn, cur) = connectDB()
        cur.execute("SELECT * FROM device WHERE IMEI = '%s'" % self.dev)
        info = cur.fetchall()
        closeDB(cxn, cur)
        return info

def connectDB():
    """Connect Database"""
    cxn = sqlite3.connect('database.db')
    cur = cxn.cursor()
    return (cxn, cur)
def closeDB(cxn, cur):
    """Close Database"""
    cur.close()
    cxn.commit()
    cxn.close()

def showThread():
    print "###############################################################################################"
    os.system("ps -efL | grep 'assigner.py'")
    print "###############################################################################################"

#def getDeviceList():    #由list.txt文件读取当前空闲设备列表
#    try:
#        f = open('list.txt')
#        devs = []
#        for line in f:
#            devs.append(line.strip())
#        return devs
#    except:
#        print "Could not open list.txt"
#        exit()
#
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python assigner.py device"
        exit()
    else:
        dev =sys.argv[1]
#    devs = getDeviceList()
#    print devs
    rs = redis.StrictRedis(host = 'localhost', port = 6379)
    (cxn, cur) = connectDB()
    ta = Assigner(dev)
    queue = Queue()
    queue.show()
    try:
        ta.distribute()
    except:
       print "device not defined"

