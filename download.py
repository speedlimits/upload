#!/usr/bin/python
#script to download names from CDN into Staging
#assumes it should be in build/cmake, YMMV

import os
from ftplib import FTP

if not os.path.exists("password"):
    print "password (I'm going to save it in plaintext!):",
    password = raw_input().strip()
    f = open("password", "w")
    f.write(password)
    f.close()

f = open("password")
password = f.read().strip()
f.close()

files = []
def cb(fil):
    global files
    files.append(fil.split()[-1])

ftp = FTP("sirikata.com")
ftp.login("slartist", password)
ftp.cwd("content3/names")
ftp.retrlines('LIST', cb)

print "files:"
for i in files:
    print i

data = None
def cb2(s):
    global data
    data = s.strip()

fn = open("names.txt","w")
for fil in files:
##    f = open(fil)
##    s = f.read()
##    f.close()

    ftp.retrlines('RETR ' + fil, cb2)
    s = data
    if len(s) != 73:
        print "skipping", fil
    else:
        print fil, s
        fn.write(fil + " " + s + "\n")
fn.close

if os.path.exists("build/cmake"):
    if not os.path.exists("build/cmake/Staging"):
        cmd = "mkdir build/cmake/Staging"
        os.system(cmd)
    cmd = "cp names.txt build/cmake/Staging"
    os.system(cmd)

