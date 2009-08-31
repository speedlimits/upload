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
##        print i
        sum = sha256(i)
        if not i==sum:
            print "bad SHA file:", i
            badfiles.append((i, "SHA"))
        else:
            fil = i
            try:
                f = open(fil, "rb")
            except:
                continue
            s = f.read(18)
            f.close()
            if s[:5] == "DDS |":
                w = ord(s[12]) + ord(s[13])*256
                h = ord(s[16]) + ord(s[17])*256
                siz = os.path.getsize(fil)
                res = w*h
                est = int((siz-141)*1.5)
                if not est >= res and (est-50) < res:
                    print "BAD DDS file, resolution =", w, h, fil
                    badfiles.append((i, "DDS"))
                else:
                    print "GOOD DDS file, resolution =", w, h, fil
            else:
                print "good file:", i

if badfiles:
    print "************************ BAD FILES: ****************************"
    for i, err in badfiles:
        print i, err
    print "****************************************************************"
    for i, err in badfiles:
        print "remove bad file (y/n)", i, err
        r=raw_input()
        if r[0]=="y":
            cmd = "rm " + i
            print cmd
            os.system(cmd)
else:
    print "No bad files found"
