#!/usr/bin/env python

import numpy as np
import MDAnalysis 
import mdtraj

class trj_reader(object):
    def __init__(self,lammps_data="init.data"):
        self.atom_style = {"full":'id resid type charge x y z','atomic':'id type x y z','charge':'id type charge x y z'}
        self.lammps_data_name = lammps_data

        self.masses= [1.00794,4.002602,6.941,9.012182,10.811,12.011,14.00674,\
            15.9994,18.9984032,20.1797,22.989768,24.3050,26.981539,28.0855,\
            30.97362,32.066,35.4527,39.948,39.0983,40.078,44.955910,47.88,\
            50.9415,51.9961,54.93085,55.847,58.93320,58.69,63.546,65.39,\
            69.723,72.61,74.92159,78.96,79.904,83.80,85.4678,87.62,88.90585,91.224,\
            92.90638,95.94,98,101.07,102.90550,106.42,107.8682,112.411,\
            114.82,118.710,121.75,127.60,126.90447,131.29,132.90543,137.327,138.9055,140.115,\
            140.90765,144.24,145,150.36,151.965,157.25,158.92534,162.50,\
            164.93032,167.26,168.93421,173.04,174.967,178.49,180.9479,\
            183.85,186.207,190.2,192.22,195.08,196.96654,200.59,204.3833,\
            207.2,208.98037,209,210.0,222,223,226.025,227.028,232.0381,\
            231.03588,238.0289,237.048,244.,243.,247.,247.,251.,252.,\
            257.,258.,259.,260.0]

        self.elements=['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg',\
            'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr',\
            'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', \
            'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', \
            'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', \
            'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', \
            'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', \
            'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', \
            'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr']

        self.lammps_data_reader()
        
    @staticmethod
    def judge_element(mass,masses):
        for index,i in enumerate(masses):
            if abs(mass-i)<0.1:
                return index
            
    def lammps_data_reader(self):
        self.topol = MDAnalysis.Universe(self.lammps_data_name, atom_style=self.atom_style['charge'])
        self.topol.add_TopologyAttr('names')
        self.topol.add_TopologyAttr('resnames')
        types = self.topol.atoms.types
        for index,i in enumerate(self.topol.atoms.masses):
            types[index] = self.elements[self.judge_element(i,self.masses)]
        self.topol.atoms.names = types
        self.topol.atoms.residues.resnames = np.array(['MOL'], dtype=object)
        self.topol.atoms.write('init.gro',reindex=False)
    
    def lammps_trj2xtc(self,lammpstrj_name):
        frames = mdtraj.load_lammpstrj(lammpstrj_name,"init.gro",unit_set="real") #unit is important
        frames.xyz = np.einsum('ijk, ikl->ijl',frames.xyz,frames.unitcell_vectors)*10 #ultra-fast
        frames.save_xtc("system.xtc")
        
    def read_xtc(self):
        self.traj = MDAnalysis.Universe('init.gro',"system.xtc")

    def xtc_to_arc(self):
        atom_names = self.traj.atoms.names
        with open("test.arc",'w') as writer:
            writer.write("!BIOSYM archive 3\nPBC=ON\n")
            for trajectory_ in self.traj.trajectory:
                writer.write("                                                                          0.0000\n!DATE Thu Jul 22 22:54:16 2021\n")
                a,b,c,alpha,beta,gamma=trajectory_.dimensions
                writer.write("PBC%9.4f%9.4f%9.4f%9.4f%9.4f%9.4f\n" %(a,b,c,alpha,beta,gamma))
                for i in range(trajectory_.n_atoms):
                    string = "%-5s%15.9f%15.9f%15.9f%5s%3d%7s%7s%8.3f\n" %(atom_names[i],\
                                   trajectory_.positions[i][0] ,trajectory_.positions[i][1] ,trajectory_.positions[i][2],"XXXX",\
                                              1, "XX", atom_names[i], 0)
                    writer.write(string)
                writer.write("end\n")            
                writer.write("end\n")   

if __name__ == "__main__":
    trj = trj_reader("final2.data")
    trj.lammps_trj2xtc("dump.reax2.lammpstrj")  
    trj.read_xtc()
    trj.xtc_to_arc()
