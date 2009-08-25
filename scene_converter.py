import sys, time
from xml.dom import minidom
from Tkinter import *
import tkSimpleDialog
import tkMessageBox

def attFloats2list(el, *ats):
    ret = []
    for at in ats:
        ret.append(float(el.getAttribute(at)))
    return ret

row1 = 'objtype,subtype,name,pos_x,pos_y,pos_z,orient_x,orient_y,orient_z,orient_w,scale_x,scale_y,scale_z,hull_x,hull_y,hull_z,density,friction,bounce,colMask,colMsg,meshURI,diffuse_x,diffuse_y,diffuse_z,ambient,specular_x,specular_y,specular_z,shadowpower,range,constantfall,linearfall,quadfall,cone_in,cone_out,power,cone_fall,shadow'
row2 = 'light,directional,,-1.86,3515.99,3.32,22.45,-63.46,-164.4,,,,,,,,,,,,,,0.6,0.6,0.6,0.33,0.99,0.97,0.9,0.11,200000,0,0,0,30,40,0.9,1,0'
row3 = 'camera,,,76.95,4598.41,25.59,-8.81,81.34,1.34,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,'

errors = []

def say(*args):
    s = ""
    for i in args:
        s += str(i) + " "
    print s

def main(fname, outfile=sys.stdout):
    try:
        x = minidom.parse(fname)
    except:
        errors.append("minidom.parse failed on " + str(fname))
        raise
    try:
        scene = x.getElementsByTagName("scene")[0]              #should only be 1
    except:
        errors.append("scene not found -- is this a 3DMAX xml file?")
        raise
    nodes = scene.getElementsByTagName("nodes")[0]
    nodes = nodes.getElementsByTagName("node")

    print >> outfile, row1
    print >> outfile, row2
    print >> outfile, row3

    names = set()

    for node in nodes:
        name = node.getAttribute("name")
        scale = attFloats2list(node.getElementsByTagName("scale")[0], "x", "y", "z")
        pos = attFloats2list(node.getElementsByTagName("position")[0], "x", "y", "z")
        rot = attFloats2list(node.getElementsByTagName("rotation")[0], "qx", "qy", "qz", "qw")
        ent = node.getElementsByTagName("entity")[0]
        mesh = str(ent.getAttribute("meshFile"))
        if not mesh[-5:] == ".mesh":
            raise "expected .mesh file, got: " + mesh
        name = mesh[:-5]
        i=1
        while name in names:
            name = mesh[:-5] + "." + str(i)
            i +=1
        names.add(name)
        
        outfile.write("mesh,graphiconly," + name + ",")
        outfile.write(str(pos[0])+","+str(pos[1])+","+str(pos[2])+",")
        outfile.write(str(rot[0])+","+str(rot[1])+","+str(rot[2])+","+str(rot[3]))
        commas = row1.split(",").index('meshURI') - row1.split(',').index('orient_w')
        outfile.write(","*commas)
        outfile.write(mesh)
        outfile.write("\n")


try:
    if len(sys.argv)==1:
        t = Tk()
        s = '+' + repr(300) + '+' + repr(300)
        t.geometry(s)
        t.update()
        time.sleep(.1)
        t.update()
        filename = tkSimpleDialog.askstring("enter filename", "OK", parent=t)
        outname = filename[:-4]+".csv"
        outhan = open(outname, "w")
        print "converting", filename, "to", outname
    else:
        filename = sys.argv[1]
        if len(sys.argv)==2:
            outhan = sys.stdout
        else:
            outhan = open(sys.argv[2], "w")
            print "converting", filename, "to", sys.argv[2]

    main(filename, outhan)
except:
    errors.append("something went wrong")

if len(sys.argv)==1:
    def cb():
        outhan.close()
        exit()

    if errors:
        l = Label(t, text="UPLOAD ERRORS")
        l.pack()
        say( "***********************ERROR****************************")
        for i in errors:
            l = Label(t, text=i)
            l.pack()
            say( i)
        say( "********************************************************")

    else:
        l = Label(t, text="CONVERSION COMPLETED SUCCESSFULLY")
        l.pack()

    b = Button(t, text="OK", command=cb)
    b.pack()
    mainloop()
else:
    for e in errors:
        print e

outhan.close()
