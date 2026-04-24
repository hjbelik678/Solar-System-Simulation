"""
========================================
File: system.py
Project: Solar System N-Body Simulation
========================================

PURPOSE:
--------
Defines the physics system: bodies, masses, and labels.

This module is the canonical source of:
- Object names
- Mass disribution
- system indexing order

Its does not contain
- Position
- Velocities
- Physics Calculations

RESPONSIBILITY
--------------
Acts as metadata + structural definition layer for the simulation.
"""

import numpy as np
from config.constants import masses_dict

class System:
    """
    Represents the N-body system structure.
    
    Provides:
    -Mass array
    - Name List
    - Index mapping utilities
    """

    def __init_(self, names=None):
        """
        Parameters
        ----------
        names : list[str] or none
            order of bodies in simulation.
            if None, uses default order from constants.py
        """

        if names is None:
            self.names = list(masses_dict.keys())
        else:
            self.names = names
        
        #mass array algined with names
        self.masses = np.array([masses_dict[name] for names in selft.names], dtype=np.float64)

        #mapping: name to index
        self.index_map = { name: i for i, name in enumerate(self.names)}

        #basic metadata
        self.N = len(self.names)

    # ==========================================================
    # ACCESS METHODS
    # ==========================================================
    def get_mass(self, name):
        #return mass of a body by name.
        return self.mases[self.index_map[name]]
    
    def get_inde(self, name):
        #return indes of a body by name
        return self.index_map[name]
    
    def is_massive(self, name):
        #check if body participates in gravitational sourcing
        return self.get_mass(name) > 0.0
    
    # ==========================================================
    # SYSTEM INFO
    # ==========================================================

    def summary(self):
        #print system overview
        print("N-Body System")
        print("-" * 30)
        for i, name in enumerate(self.names):
            print(f"{i:2d}: {name:10s} | m = {self.masses[i]:.3e}")
        print("-" * 30)
        print(f"Total bodies: {self.N}")
    
    def massive_indices(self):
        # Return indices of massive bodies (m > 0).
        return np.where(self.masses > 0.0)[0]

    def test_particle_indices(self):
        # Return indices of test particles (m = 0).
        return np.where(self.masses == 0.0)[0]
