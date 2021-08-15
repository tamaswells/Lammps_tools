#!/usr/bin/env python

import numpy as np
import MDAnalysis 

class trj_reader(object):
    def __init__(self,lammps_data="init.data",lammps_trj="file.xtc"):
        self.atom_style = {"full":'id resid type charge x y z','atomic':'id type x y z'}
        self.atom_element = {"1":"C","2":"H"}
        self.lammps_data_name = lammps_data
        self.lammps_trj_name = lammps_trj
        self.lammps_data_reader()
    
    def lammps_data_reader(self):
        self.topol = MDAnalysis.Universe(self.lammps_data_name, atom_style=self.atom_style['full'])
        self.topol.add_TopologyAttr('names')
        self.topol.add_TopologyAttr('resnames')
        types = self.topol.atoms.types
        for i in range(len(types)):
            types[i] = self.atom_element[types[i]]
        self.topol.atoms.names = types
        self.topol.atoms.residues.resnames = np.array(['MOL'], dtype=object)
        self.topol.atoms.write('init.gro',reindex=False)
    
    def load_lammps_trj(self):
        self.traj = MDAnalysis.Universe('init.gro',self.lammps_trj_name)
        
if __name__ == "__main__":
    trj = trj_reader("init.data","short.xtc")
    trj.load_lammps_trj()
