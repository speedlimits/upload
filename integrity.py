#!/usr/bin/python
#check integrity of CDN assets

import os, sys
##import hashlib
##from ftplib import FTP

def sha256(filename):
    cmd = "./sha256 -256 " + filename
    sin, sout = os.popen2(cmd)
    s = sout.read().split()[-1]
    return s

badfiles = []
files = os.listdir(".")
for i in files:
    if len(i)==64:
        sum = sha256(i)
        if not i==sum:
            print "remove bad file? (y/n)", i,
            r=raw_input()
            if r[0]=="y":
                cmd = "rm " + i
                print cmd
                os.system(cmd)
            badfiles.append(i)
        else:
            print "good file:", i
