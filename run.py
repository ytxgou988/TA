#!/usr/bin/env python
from subprocess import call, Popen
from time import sleep
call(["python", "init.py"], shell = False)
command = "python assigner.py"
f = open("list.txt", 'w')
f.write("dev4\ndev2\n")
f.close()
#call(command.split(), shell=False)
t1 = Popen(command.split(), shell=False)
sleep(5)
f = open("list.txt", 'w')
f.write("dev1\ndev3\n")
f.close()
#call(command.split(), shell=False)
t2 = Popen(command.split(), shell=False)
print t1.wait()
print t2.wait()
