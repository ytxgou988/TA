#!/usr/bin/env python
import os
import sqlite3
import redis
import threading
import random
from time import clock, ctime, sleep

MAXLEN = 5
basedir = os.getcwd()
start = clock()
cache = redis.StrictRedis(host = 'localhost', port = 6379)

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
        print 'starting', self.name, 'at:', ctime()
        self.res = apply(self.func, self.args)
        print self.name, 'finished at:', ctime()


def distribute(dev, pkglist):
    devinfo = list(getDeviceInfo(dev)[0])
    print devinfo
    for pkg in pkglist:
        if devinfo[1] >= int(cache.get("package:%s:sim"%pkg)) and devinfo[2] >= int(cache.get("package:%s:sd"%pkg)):
            t = MyThread(runs, (pkg,), runs.__name__)
            cache.lrem('pkg', 1, pkg)
            add()
            t.start()
#            t.join()
            break
    else:
        print "no match"

def add():
    while cache.llen('pkg') < MAXLEN:
        cur.execute("SELECT name FROM package WHERE status = 0 ORDER BY timestamp")
        try:
            pkg = cur.fetchone()[0]
            cur.execute("UPDATE package SET status = 1 WHERE name = '%s'" % pkg)
            cache.rpush('pkg', pkg)
            getPkgInfo(pkg)
        except TypeError:
            print "No more package waiting"
            break

def runs(pkg):
    print "run %s" % pkg
    sec = random.randint(25,30)
    sleep(sec)
    print "%s finish" % pkg

def connectDB():
    cxn = sqlite3.connect('database.db')
    cur = cxn.cursor()
    return (cxn, cur)

def closeDB(cxn, cur):
    cur.close()
    cxn.commit()
    cxn.close()
def getDeviceInfo(dev):
    cur.execute("SELECT * FROM device WHERE IMEI = '%s'" % dev)
    return cur.fetchall()
def getPkgInfo(pkg):
    cur.execute("SELECT * FROM package WHERE name = '%s'" % pkg)
    pkginfo = cur.fetchone()
    user = pkginfo[1]
    cfgdir = os.path.join(basedir, user, pkg)
    try:
        f = open(cfgdir+'/'+ pkg +'.cfg')
        info = f.read().split()
        cache.mset({
            "package:%s:name"%pkg : info[0],
            "package:%s:sim"%pkg : info[1],
            "package:%s:sd"%pkg : info[2],
            "package:%s:user"%pkg : user
            })
    except:
        "Could not open package config"
        cache.lrem('pkg', 1, pkg)

def getDeviceList():
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
#    if len(sys.argv) != 2:
#        print "Usage: python assigner.py device"
#        exit()
#    else:
#        dev = sys.argv[1]
#        pass
    devs = getDeviceList()
    print devs
    (cxn, cur) = connectDB()
    add()
    for dev in devs:
        pkglist = cache.lrange('pkg', 0, -1)
        print 'Current queue:', pkglist
        for pkg in pkglist:
            print cache.mget('package:%s:name' % pkg, 'package:%s:user' % pkg, 'package:%s:sim' % pkg, 'package:%s:sd' % pkg)
        try:
            distribute(dev,pkglist)
        except:
            print "device not defined"
            continue
        sleep(1)
        print 'fin', cache.lrange('pkg', 0, -1)
    closeDB(cxn, cur)

end = clock()
print "Total time: %g s" % (end - start)
