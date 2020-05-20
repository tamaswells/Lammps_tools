import mdtraj
import numpy as np
import sys

if len(sys.argv) == 1:
    print("Run as 'python lammpstrj2xtc.py *.lammpstrj'")
    sys.exit(0)
frames = mdtraj.load_lammpstrj(sys.argv[1],"system.gro",unit_set="real")

if frames.xyz[0].mean(axis=0).mean() < 1:
    frames.xyz = np.einsum('ijk, ikl->ijl',frames.xyz,frames.unitcell_vectors)*10 #ultra-fast
    #for index,line in enumerate(frames.unitcell_vectors):
        #frames.xyz[index] = np.matmul(frames.xyz[index],frames.unitcell_vectors[index])*10

frames.save_xtc("system.xtc")
