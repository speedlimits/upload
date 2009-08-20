#!/usr/bin/python
#check integrity of CDN assets

import os, sys

badfiles = []
names = os.listdir(".")
assets = os.listdir("../assets")

for i in names:
    f = open(i)
    s = f.read()
    f.close()
    if len(s) != 73 and len(s) != 74:
        print i, "doesn't look like a name file", len(s)
    else:
        s = s[-64:]
        if not s in assets:
            print i, "points to", s, "which I can't find in ../assets"
            print "remove", i, "? (y/n)",
            r=raw_input()
            if r[0]=="y":
                cmd = "rm " + i
                print cmd
                os.system(cmd)
            badfiles.append(i)
        else:
            print "good file:", i
