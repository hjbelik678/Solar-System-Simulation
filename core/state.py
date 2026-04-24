"""
============================================================
File: state.py
Project: Solar System N-Body Simulation (Symplectic Integrators)
============================================================

PURPOSE:
--------
Core data container for an N-body gravitational system using:
- barycentric coordinates
- symplectic integration
- vectorized NumPy computation


UNIT SYSTEM:
-----------
- Distance: AU
- Time: years
- Mass: solar masses
- G = 4π²


STATE REPRESENTATION:
--------------------
positions : (N, 3) float64
    Cartesian positions in AU

velocities : (N, 3) float64
    Cartesian velocities in AU/year

masses : (N,) float64
    Masses in solar masses

names : list[str]
    Body identifiers (for plotting/debugging)


HETEROGENEOUS BODY MODEL:
-------------------------
Two categories:

1. Massive bodies (m > 0)
   - mutually interact via gravity
   - contribute to system barycenter

2. Test particles (m = 0)
   - affected by gravity
   - do NOT affect other bodies

Implementation rule:
    If masses[i] == 0:
        body contributes NO gravitational force
        but still receives acceleration


BARYCENTRIC FRAME:
------------------
System is centered on center of mass:

    R_cm = Σ(m_i r_i) / Σ m_i
    V_cm = Σ(m_i v_i) / Σ m_i

After every timestep:
    positions -= R_cm
    velocities -= V_cm


NUMERICAL ASSUMPTIONS:
----------------------
- float64 precision
- fixed timestep
- symplectic integration externally
- no collisions or merging


HISTORY STORAGE (FOR ANIMATION):
--------------------------------
Trajectory storage is handled externally:

Recommended format:
    history_x : (T, N, 3)
    history_v : (T, N, 3)

State object only stores CURRENT step.


DESIGN PRINCIPLES:
------------------
- array-first (NumPy)
- no object-per-body abstraction
- integrator-agnostic
- scalable to large N systems


LIMITATIONS:
-----------
- O(N^2) gravity scaling
- no adaptive timestep
- no relativistic corrections
- no collision dynamics


FUTURE EXTENSIONS:
------------------
- Barnes-Hut tree (O(N log N))
- GPU acceleration (CUDA/JAX)
- hierarchical systems (moon-planet coupling)
- softening for dense clusters
- ephemeris-based initial conditions

============================================================
STATE MODEL (HETEROGENEOUS N-BODY SYSTEM)
============================================================

TWO LAYERS OF PARTICLES:

1. MASSIVE BODIES
   - mutually interact gravitationally
   - contribute to barycenter
   - examples: Sun, planets, moons

2. TEST PARTICLES
   - influenced by gravity
   - do NOT exert gravity
   - examples: comets, spacecraft, asteroids


WHY THIS WORKS:
--------------
- avoids O(N^2) cost for tiny bodies
- preserves physical accuracy for dominant masses
- keeps system fully vectorized


IMPORTANT CONSERVATION NOTE:
---------------------------
Momentum conservation is preserved only for:
    massive bodies subsystem

Test particles do not violate conservation laws because:
    their mass contribution = 0


NUMERICAL REPRESENTATION:
------------------------
positions : (N, 3) float64
velocities: (N, 3) float64
masses    : (N,) float64

indices are NOT stored explicitly; derived via mask.
"""

import numpy as np

def split_bodies(masses):
    """
    Returns index masks for heterogeneous system.
    """
    massive = masses > 0.0
    return massive