"""
===============================================
FIle: gravity.py
Porject: Solar System N-Body Simulation
===============================================

PURPOSE:
--------
Computes gravitational accelerations for an N-body system suing 
-Newtonian gravity
-Barycentric coordinates
- support for heterogeneous bodies
    -massive
    -test particles

PHYSICAL MODEL:
---------------
- Force Law: F = G m_i m_j /r^2
- Acceleration: a_i = Σ_j G m_j r_ij / |r_ij|^3

Supports:
- Massive bodies (m>0): full interactions
- Test particles (m=0): feel gravity but does not exert it

UNITS:
------
- Distance: AU
- Time: years
- Mass: solar masses
- G = 4π^2

INPUTS:
-------
positions: ndarray (N, 3)
velocities: ndarray (N, 3)
masses: ndarray (N,)

OUTPUT:
-------
accelerations: ndarray (N,3)

NUMERICAL FEATURES:
-------------------
- fully vectoriezed
- O(N*M) complexity where M = number os massive bodies
- stabel for symplectic integration

LIMITATION:
-----------
- O(N^2) worst case for all massive systems
- No softening (can add later if needed)
- no relativistics corrections (for now)
"""

import numpy as np
from config.constants import G

def compute_accelerations(positions, masses, softening=0.0):
    """Compute gravitational accelerations for all bodies.

    Parameters
    ----------
    positions : ndarray (N, 3)
    masses    : ndarray (N,)
    softening : float (optional)
        Small value to avoid singularities (default = 0)

    Returns
    -------
    accelerations : ndarray (N, 3)
    """
    # ensure float64
    positions = positions.astype(np.float64, copy=False)
    masses = masses.astype(np.float64, copy=False)

    N = positions.shape[0]

    #identify massive bodies m>0
    massive_mask = masses > 0.0

    #extract massive bodies
    pos_massive = positions[massive_mask]
    massive_massive = masses[massive_mask]

    #compute pairwise displacements (N, M, 3)
    r_ij = pos_massive[None, :, :] - positions[:, None, :]

    #distance squared with optional softening
    dist_sq = np.sum(r_ij**2, axis=2) + softening**2

    #avoid division by zero
    inv_disti3 = np.zeros_like(dist_sq)
    mask = dist_sq>0
    inv_disti3[mask] = 1.0 / (dist_sq[mask] * np.sqrt(dist_sq[mask]))

    #multiply by masses of source bodies
    acc = G * np.sum(r_ij * inv_disti3[:, :, None] * massive_massive[None, :, None], axis = 1)

    return acc

