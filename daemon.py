#!/usr/bin/python
# -*- coding:utf-8 -*-

from Queue import Queue  
import os
import threading  
import time  

#Producer thread  
class MyThread(threading.Thread):    #线程类的定义
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        print 'starting', self.name, 'at:', time.ctime()
        self.res = apply(self.func, self.args)
        print self.name, 'finished at:', time.ctime()

class Searcher(threading.Thread):  

    def __init__(self, t_name, queue):  

        threading.Thread.__init__(self, name=t_name)  

        self.data=queue  

    def run(self):  

        i=1
        while i < 6:  
            self.data.put(i)  
            i += 1 
            time.sleep(5)  

#        print "%s: %s finished!" %(time.ctime(), self.getName())  
#Consumer thread  

class Dispatcher(threading.Thread):  

    def __init__(self, t_name, queue):  

        threading.Thread.__init__(self, name=t_name)

        self.data=queue  

    def run(self):  

        while 1:  
#            os.remove("list.txt")
#            f = open("list.txt", 'w')
            val = str(self.data.get())
    
#            f.write("dev"+str(val)+'\n')
#            f.close()
#dispatch package
            t = MyThread(runs, (val,), runs.__name__)
            t.start()
            time.sleep(5)  

        print "%s: %s finished!" %(time.ctime(), self.getName())  

def runs(val):
    dev = "dev"+val
    os.system("python assigner.py %s"%dev)

#Main thread  

def main():  

    queue = Queue()  
    searcher = Searcher('Search.', queue)  
    dispatcher = Dispatcher('Dispatch.', queue)  
    searcher.start()  
    dispatcher.start()  
#    searcher.join()  

    dispatcher.join()  

    print 'All threads terminate!'  
  


if __name__ == '__main__':  

    main()  
