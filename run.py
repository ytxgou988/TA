#!/usr/bin/env python
from subprocess import call, Popen
from time import sleep
call(["python", "init.py"], shell = False)
command = "python assigner.py"
f = open("list.txt", 'w')
f.write("dev4\ndev2\ndev5\n")
f.close()
#call(command.split(), shell=False)
t1 = Popen(command.split(), shell=False)

print '-----------------------------------------------------------------------------------'
sleep(10)
f = open("list.txt", 'w')
f.write("dev1\ndev3\ndev4\n")
f.close()
#call(command.split(), shell=False)
t2 = Popen(command.split(), shell=False)
print '-----------------------------------------------------------------------------------'
print t1.wait()
print t2.wait()
