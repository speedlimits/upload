#!/usr/bin/python
import os, sys, time
from ftplib import FTP
from Tkinter import *
import random

tempfilename = "temp_" + str(random.randint(1,10000000))

WINDOWS = False             #cygwin is not windows!

## shedskin windows works in console, not cygwin!

if "win32" in sys.platform or "shedskin" in sys.platform:
    WINDOWS = True

nulldev = "NUL" if WINDOWS else "/dev/null"

def fixsysline(s):
    if WINDOWS:
        s=s.replace("/", "\\")
    return s

def system(s):
    ##print "cmd-->" + fixsysline(s) + "<--"
    return os.system(fixsysline(s))

def checkhttpfile(path):
    cmd = "wget -S --spider -o " + nulldev + " " + path
    ##print "os.cmd:", cmd
    err = os.system(cmd)
    if err:
        return 0
    return 1

error_msgs = []

def error(*args):
    s = ""
    for i in args:
        s += str(i) + " "
    print s
    upload_log.write(s + "\n")
    error_msgs.append(s)

def say(*args):
    s = ""
    for i in args:
        s += str(i) + " "
    print s
    upload_log.write(s + "\n")

hashes = set()
name2hash = {}

def main():
    try:
        if not os.listdir("tempSirikataUpload") == []:
            if WINDOWS:
                os.system("del /Q tempSirikataUpload\*")
            else:
                os.system("rm tempSirikataUpload/*")
    except:
        system("mkdir tempSirikataUpload")
    say( "----------------------------------------------------------")
    say( "populating temp directory with name files:")
    f = open("Staging/names.txt")
    for i in f.readlines():
        try:
            name, hash = i.strip().split()
        except:
            error( "that looks like crap, not a name/mesh pair")
            continue
        clean = hash[-64:]
        hashes.add(clean)
        name2hash[name]=clean
        fo = open("tempSirikataUpload/"+name, "w")
        fo.write(hash)
        fo.close()
        say(name, "=>", hash)
    f.close()

    ftp = FTP("sirikata.com")
    ftp.login("slartist", "V3sb4Dkb")
    say( "----------------------------------------------------------")
    say( "copying asset files:")
    assetlist = os.listdir("Cache")
    assetlist2 = os.listdir("Staging")
    for i in hashes:
        if i in assetlist+assetlist2:
            if checkhttpfile("http://www.sirikata.com/content/assets/" + i):
                say( i, "found on server, not copying")
            else:
                say( "copying", i)
                cachedir = "Staging/" if (i in assetlist2) else "Cache/"
                cmd = "STOR content3/assets/" + tempfilename
                try:
                    f = open(fixsysline(cachedir)+i, "rb")
                    ftp.storbinary(cmd, f)
                    f.close()
                    ftp.rename("content3/assets/" + tempfilename, "content3/assets/" + i)
                except:
                    error( "problem uploading asset file:", i)
        else:
            if checkhttpfile("http://www.sirikata.com/content/assets/" + i):
                say( i, "(missing local asset) found on server, not copying")
            else:
                error("missing asset file, not local OR on server:", i)
    say( "done")
    say( "----------------------------------------------------------")
    say( "copying name files:")
    files = os.listdir(fixsysline("tempSirikataUpload"))
    for fil in files:
        if not fil in name2hash:
            error( "SKIPPING name file, was this in tempSirikataUpload?", fil)
            print "FATAL ERROR"
            exit()
        say( "copying ", fil)
        cmd = "STOR content3/names/" + tempfilename
        try:
            f = open(fixsysline("tempSirikataUpload/")+fil)
            ftp.storbinary(cmd, f)
            f.close()
            ftp.rename("content3/names/" + tempfilename, "content3/names/" + fil)
        except:
            error( "problem uploading name file -- read only? skipping this one")
            raise
    say( "done")
    say( "----------------------------------------------------------")

    ftp.quit()


upload_log = open("upload.log", "w")
main()

def cb():
    exit()

t = Tk()
s = '+' + repr(300) + '+' + repr(300)
t.geometry(s)

if error_msgs:
    l = Label(t, text="UPLOAD ERRORS")
    l.pack()
    say( "***********************ERROR****************************")
    for i in error_msgs:
        l = Label(t, text=i)
        l.pack()
        say( i)
    say( "********************************************************")

else:
    l = Label(t, text="UPLOAD COMPLETED SUCCESSFULLY")
    l.pack()

b = Button(t, text="OK", command=cb)
b.pack()
upload_log.close()
mainloop()

