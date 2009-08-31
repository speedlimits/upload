import os, sys

if len(sys.argv) > 1:
    fil = sys.argv[1]
    files = [fil]
else:
    files = os.listdir(".")

for fil in files:
    cmd = "file " + fil
    sin, sout = os.popen2(cmd)
    s = sout.read()
    if "(DDS)" in s:
        i = s.index("(DDS), ")+7
        j = i+s[i:].index("x")
        k = j+s[j:].index(",")
        w = int(s[i:j-1])
        h = int(s[j+1:k])
        siz = os.path.getsize(fil)
        res = w*h
        if not int((siz-141)*1.5) == res:
            print fil, "is a BAD DDS file, resolution =", w, h
        else:
            print fil, "is a GOOD DDS file, resolution =", w, h
    else:
        print fil, "is NOT a DDS file"
