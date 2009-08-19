#!/usr/bin/python
import os, sys, time
from ftplib import FTP
from Tkinter import *

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
    error_msgs.append(s)

hashes = {}
def main():
    try:
        if not os.listdir("tempSirikataUpload") == []:
            if WINDOWS:
                os.system("del /Q tempSirikataUpload\*")
            else:
                os.system("rm tempSirikataUpload/*")
    except:
        system("mkdir tempSirikataUpload")
    f = open("Staging/names.txt")
    for i in f.readlines():
        try:
            name, hash = i.strip().split()
        except:
            error( "that looks like crap, not a name/mesh pair")
            continue
        clean = hash[-64:]
        hashes[clean]=name
        fo = open("tempSirikataUpload/"+name, "w")
        fo.write(hash)
        fo.close()
    f.close()

    print "----------------------------------------------------------"
    print "copying name files:"
    ftp = FTP("sirikata.com")
    ftp.login("slartist", "V3sb4Dkb")
    files = os.listdir(fixsysline("tempSirikataUpload"))
    for fil in files:
        print "copying ", fil
        cmd = "STOR content/names/tempUploadNameFile"
        try:
            f = open(fixsysline("tempSirikataUpload/")+fil)
            ftp.storbinary(cmd, f)
            f.close()
            ftp.rename("content/names/tempUploadNameFile", "content/names/" + fil)
        except:
            error( "problem uploading name file -- read only? skipping this one")
    print "done"
    print "----------------------------------------------------------"
    print "copying asset files:"
    assetlist = os.listdir("Cache")
    assetlist2 = os.listdir("Staging")
    for i in hashes:
        if i in assetlist+assetlist2:
            if checkhttpfile("http://www.sirikata.com/content/assets/" + i):
                print i, "found on server, not copying"
            else:
                print "copying", i
                cachedir = "Staging/" if (i in assetlist2) else "Cache/"
##                cmd = "STOR content/assets/" + i
                cmd = "STOR content/assets/tempUploadAssetFile"
                try:
                    f = open(fixsysline(cachedir)+i)
                    ftp.storbinary(cmd, f)
                    f.close()
                    ftp.rename("content/assets/tempUploadAssetFile", "content/assets/" + i)
                except:
                    error( "problem uploading asset file:", i)
        else:
            error( hashes[i], " points to missing file", i)

    ftp.quit()
    print "done"

main()

def cb():
    exit()

f = open("upload_error.log", "w")
t = Tk()
s = '+' + repr(300) + '+' + repr(300)
t.geometry(s)

if error_msgs:
    l = Label(t, text="UPLOAD ERRORS")
    l.pack()
    print "***********************ERROR****************************"
    for i in error_msgs:
        l = Label(t, text=i)
        l.pack()
        print i
    f.write(i)
    f.write("\n")
    print "********************************************************"

else:
    l = Label(t, text="UPLOAD COMPLETED SUCCESSFULLY")
    l.pack()
    f.write("no errors\n")

f.close()

b = Button(t, text="OK", command=cb)
b.pack()
mainloop()
