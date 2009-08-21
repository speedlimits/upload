#!/usr/bin/python
#check integrity of CDN assets

import os, sys

badfiles = []
names = os.listdir(".")
assets = os.listdir("../assets")

for i in names:
    f = open(i)
    s = f.read().strip()
    f.close()
    if len(s) != 73:
        print i, "doesn't look like a name file", len(s)
        badfiles.append("not a name file: " + i)
    else:
        s = s[-64:]
        if not s in assets:
            badfiles.append("not in assets: " + i)
            print i, "points to", s, "which I can't find in ../assets"
            print "remove", i, "? (y/n)",
            r=raw_input()
            if r[0]=="y":
                badfiles[-1] += "--removed"
                cmd = "rm " + i
                print cmd
                os.system(cmd)
        else:
            print "good file:", i

print "--------------------------------------------------------------"
print "                          BAD FILES:"
for i in badfiles:
    print i
print "--------------------------------------------------------------"

