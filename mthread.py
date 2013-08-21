#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from time import sleep, ctime
import subprocess

devs = ('4', '2')

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
    def run(self):
        apply(self.func, self.args)


def assigner(dev):
    print "run dev%s"%dev
    command = "python assigner.py dev%s" % dev
    subprocess.call(command.split(), shell=False)
    
def main():
    print 'stating at:', ctime()
    threads = []
    nloops = range(len(devs))

    for i in nloops:
        t = MyThread(assigner, (devs[i]),
                assigner.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()
    for i in nloops:
        threads[i].join()

    print 'all DONE at:', ctime()

if __name__ == '__main__':
    main()
