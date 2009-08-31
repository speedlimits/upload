#!/usr/bin/python
#check integrity of DDS files
import os, sys

if len(sys.argv) > 1:
    fil = sys.argv[1]
    files = [fil]
else:
    files = os.listdir(".")

for fil in files:
    try:
        f = open(fil, "rb")
    except:
##        print "Directory?"
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
        else:
            print "GOOD DDS file, resolution =", w, h, fil
