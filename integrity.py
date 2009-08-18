#check integrity of CDN assets

import os
import hashlib
from ftplib import FTP

def cb(s):
    fname = s.split()[-1]
    print fname


ftp = FTP("sirikata.com")
ftp.login("slartist", "V3sb4Dkb")
ftp.dir("content/assets", cb)
ftp.quit()

"""
badfiles = []
files = os.listdir(".")
for i in files:
    if len(i)==64:
        f=open(i)
        s=f.read()
        f.close()
        sum = hashlib.sha256(s).hexdigest()
        if not i==sum:
##            print "BAD file:", i, "sum:", sum
            print "rm", i
            badfiles.append(i)
"""
