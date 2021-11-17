# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 10:54:51 2021

@author: Nan
"""

with open("503-2.data") as reader:
    content = reader.readlines()

numbers = 0
start = 0
x,y,z = 0,0,0
x_lo,y_lo,z_lo = 0,0,0
for index,i in enumerate(content):
    if "atoms" in i:
        numbers = int(i.split()[0])
    elif "xlo xhi" in i:
        x=float(i.split()[1])-float(i.split()[0])
        x_lo=float(i.split()[0])
    elif "ylo yhi" in i:
        y=float(i.split()[1])-float(i.split()[0])
        y_lo=float(i.split()[0])
    elif "zlo zhi" in i:
        z=float(i.split()[1])-float(i.split()[0])
        z_lo=float(i.split()[0])
    elif "Atoms" in i:
        start = index + 2
        break
atoms = []
for i in content[start:start+numbers]:
    atoms.append(list(map(float,i.strip("\r\n").strip("\n").split())))
atoms.sort(key=lambda x:x[0])
with open("PBS16.car") as reader:
    content = reader.readlines()
to_be_writen = []    
index_i = 0 
for index,i in enumerate(content):
    if len(i.split())!=9 and  "PBC" in i and "PBC=" not in i:
        to_be_writen.append("PBC  %f %f %f   90.0000   90.0000   90.0000 (P1)\n" %(x,y,z))    
    elif len(i.split())==9:
        tmp = "%-5s%15.9f%15.9f%15.9f" %(i.split()[0],atoms[index_i][4]-x_lo,atoms[index_i][5]-y_lo,atoms[index_i][6]-z_lo) + i[50:]
        to_be_writen.append(tmp)
        index_i+=1
    else:
        to_be_writen.append(i)

with open("pbs-16.car","w") as writer:
    writer.writelines(to_be_writen)