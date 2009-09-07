#!/usr/bin/python
#script to convert name directory into names.txt suitable for Staging

import os

files = os.listdir(".")

fn = open("names.txt","w")
for fil in files:
    f = open(fil)
    s = f.read()
    f.close()
    if len(s) != 73:
        print "skipping", fil
    else:
        print fil, s
        fn.write(fil + " " + s + "\n")
fn.close

