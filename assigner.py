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

def distribute(dev, pkglist):
    """Match packages with device"""
    devinfo = list(getDeviceInfo(dev)[0])
    print devinfo
    for pkg in pkglist:
        if (devinfo[1] >= int(cache.get("package:%s:sim"%pkg))
                and devinfo[2] >= int(cache.get("package:%s:sd"%pkg))):
            user = cache.get('package:%s:user' % pkg)
#            t = MyThread(runs, (pkg, user), runs.__name__)    
            remove(pkg)
            add()    #补充队列
            closeDB(cxn, cur)
            sleep(1)
            print 'fin', cache.lrange('pkg', 0, -1)    #打印结束时队列
            runs(pkg, user)
#            t.start()    #子线程开启
            break
    else:
        print "no match"
    end = clock()
    print "Total time: %g s" % (end - start)

def remove(pkg):
    """Remove package info from Redis"""
    cache.lrem('pkg', 1, pkg)
    cache.delete("package:%s:name"%pkg)
    cache.delete("package:%s:sim"%pkg)
    cache.delete("package:%s:sd"%pkg)
    cache.delete("package:%s:user"%pkg)

def add():
    """Add package to queue in Redis from database"""
    while cache.llen('pkg') < MAXLEN:
        cur.execute("SELECT name FROM package WHERE status = 0 ORDER BY timestamp")    #读取数据库并按timestamp排序
        try:
            pkg = cur.fetchone()[0]
            cur.execute("UPDATE package SET status = 1 WHERE name = '%s'" % pkg)
            cache.rpush('pkg', pkg)
            getPkgInfo(pkg)
        except TypeError:
            print "No more package waiting"
            break

def runs(pkg, user):
    """Run automation test"""
    pkgdir = os.path.join(basedir, user, pkg)
    print "run %s at %s" % (pkg, pkgdir)
    print "--------------------------------------------------------------------------"
    sec = random.randint(25, 30)
#    sleep(sec)
    command = "python sleep.py"
    subprocess.call(command.split(), shell = False)
    print "%s finish" % pkg

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

def getDeviceInfo(dev):
    """Get device info from database"""
    cur.execute("SELECT * FROM device WHERE IMEI = '%s'" % dev)
    return cur.fetchall()
def getPkgInfo(pkg):
    """Get package config from config file"""
    cur.execute("SELECT * FROM package WHERE name = '%s'" % pkg)
    pkginfo = cur.fetchone()
    user = pkginfo[1]
    cfgdir = os.path.join(basedir, user, pkg)
    try:
        f = open(cfgdir+'/'+ pkg +'.cfg')
        info = f.read().split()
        cache.mset({    #将cfg信息存放在Redis中，便于调用
            "package:%s:name"%pkg : info[0],
            "package:%s:sim"%pkg : info[1],
            "package:%s:sd"%pkg : info[2],
            "package:%s:user"%pkg : user
            })
    except:
        "Could not open package config"
        cache.lrem('pkg', 1, pkg)

def getDeviceList():    #由list.txt文件读取当前空闲设备列表
    try:
        f = open('list.txt')
        devs = []
        for line in f:
            devs.append(line.strip())
        return devs
    except:
        print "Could not open list.txt"
        exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python assigner.py device"
        exit()
    else:
        dev =sys.argv[1]
#    devs = getDeviceList()
#    print devs
    cache = redis.StrictRedis(host = 'localhost', port = 6379)
    (cxn, cur) = connectDB()
    add()
    pkglist = cache.lrange('pkg', 0, -1)
    print 'Current queue:', pkglist
    for pkg in pkglist:
        print cache.mget('package:%s:name' % pkg, 'package:%s:user' % pkg, 'package:%s:sim' % pkg, 'package:%s:sd' % pkg)
    try:
        distribute(dev,pkglist)
    except:
       print "device not defined"

