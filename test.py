#!/usr/bin/env python

class Package:
    def __init__(self, name, sim = 0, sd = 0):
        self.name = name
        self.sim = sim
        self.sd = sd

    def getName(self):
        return self.name
    def getAll(self):
        print "name: %s, sim:%d, sd: %d" % (self.name, self.sim, self.sd)
class Device:
    def __init__(self, id, sim = 0, sd = 0):
        self.id = id
        self.sim = sim
        self.sd = sd
    def getId(self):
        return self.id
    def getSim(self):
        return self.sim
    def getSd(self):
        return self.sd

def distribute(dev, pkg):
    if dev.sim == pkg.sim and dev.sd == pkg.sd:
        print "run %s" % pkg.name
        list.pop(list.index(pkg))
        return True
    else:
        return False

def add(pkg):
    list.append(pkg)

if __name__ == "__main__":
    pkg1 = Package('Album')
    pkg2 = Package('Home', sim = 1)
    pkg3 = Package('Music', sim = 1, sd = 1)
    pkg4 = Package('Test')
    dev1 = Device('123', sim = 1, sd = 1)

    list = [pkg1, pkg2, pkg3]
    print [x.name for x in list]
    
    for pkg in list:
        if distribute(dev1, pkg):
            add(pkg4)
            break;
    else:
        print "no match"
    print [x.name for x in list]

