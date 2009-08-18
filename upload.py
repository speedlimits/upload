#!/usr/bin/python
import os, sys
from ftplib import FTP

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

hashes = set()
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
            print "that looks like crap, not a name/mesh pair"
            continue
        clean = hash[-64:]
        hashes.add(clean)
        fo = open("tempSirikataUpload/"+name, "w")
        fo.write(hash)
        fo.close()
    f.close()

    print "----------------------------------------------------------"
    print "copying name files:"
##    cmd = SCP + fixsysline(" tempSirikataUpload/*") + " henrikbennetsen@delorean.dreamhost.com:sirikata.com/content/names/."
##    ##print "os.cmd:", cmd
##    os.system(cmd)
    ftp = FTP("sirikata.com")
    ftp.login("slartist", "V3sb4Dkb")
    files = os.listdir(fixsysline("tempSirikataUpload"))
    for fil in files:
        print "copying ", fil
        cmd = "STOR content/names/" + fil
        try:
            f = open(fixsysline("tempSirikataUpload/")+fil)
            ftp.storbinary(cmd, f)
            f.close()
        except:
            print "problem uploading -- read only? skipping this one"
    print "done"
    print "----------------------------------------------------------"
    print "copying asset files:"
    assetlist = os.listdir("Cache")
    assetlist2 = os.listdir("Staging")
    for i in assetlist+assetlist2:
        if i in hashes:
            if checkhttpfile("http://www.sirikata.com/content/assets/" + i):
                print i, "found on server, not copying"
            else:
                print "copying", i
                cachedir = "Staging/" if (i in assetlist2) else "Cache/"
##                cmd = fixsysline(SCP+" " + cachedir + i) + " henrikbennetsen@delorean.dreamhost.com:sirikata.com/content/assets/."
##                ##print "os.cmd:", cmd
##                os.system(cmd)
                cmd = "STOR content/assets/" + i
                f = open(fixsysline(cachedir)+i)
                ftp.storbinary(cmd, f)
                f.close()

    ftp.quit()
    print "done"

main()
