#!/usr/bin/env python
import sys
import os
import time
import sqlite3
import redis

#cfgdir = 'config/'
basedir = os.getcwd()
start = time.clock()
cache = redis.StrictRedis(host = 'localhost', port = 6379)
#class Package:
#    def __init__(self, name, sim = 0, sd = 0):
#        self.name = name
#        self.sim = sim
#        self.sd = sd
#
#    def getName(self):
#        return self.name
#    def getAll(self):
#        print "name: %s, sim:%d, sd: %d" % (self.name, self.sim, self.sd)


def distribute(dev, pkglist):
    devinfo = list(getDeviceInfo(dev)[0])
    print devinfo
    for pkg in pkglist:
        if devinfo[1] >= int(cache.get("package:%s:sim"%pkg)) and devinfo[2] >= int(cache.get("package:%s:sd"%pkg)):
            print "run %s" % pkg
            cache.lrem('pkg', 1, pkg)
            add()
            break
    else:
        print "no match"

def add():
    while cache.llen('pkg') < 3:
        cur.execute("SELECT name FROM package WHERE status = 0 ORDER BY timestamp")
        try:
            pkg = cur.fetchone()[0]
            cache.rpush('pkg', pkg)
            getPkgInfo(pkg)
            cur.execute("UPDATE package SET status = 1 WHERE name = '%s'" % pkg)
        except TypeError:
            print "No more package waiting"
            break

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
    f = open(cfgdir+'/'+ pkg +'.cfg')
    info = f.read().split()
    cache.mset({
        "package:%s:name"%pkg : info[0],
        "package:%s:sim"%pkg : info[1],
        "package:%s:sd"%pkg : info[2]
        })

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python assigner.py device"
        exit()
    else:
        dev = sys.argv[1]
    (cxn, cur) = connectDB()
    add()
    pkglist = cache.lrange('pkg', 0, -1)
    print 'Current queue:', pkglist
    for pkg in pkglist:
        print cache.mget('package:%s:name' % pkg, 'package:%s:user' % pkg, 'package:%s:sim' % pkg, 'package:%s:sd' % pkg)
    distribute(dev,pkglist)
    print cache.lrange('pkg', 0, -1)
    closeDB(cxn, cur)

end = time.clock()
print "Total time: %g s" % (end - start)
