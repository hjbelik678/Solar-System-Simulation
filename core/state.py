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

class State:
    """
    Core simulation state container for N-body system.

    Stores:
    - positions
    - velocities
    - masses
    - names

    Designed for:
    - symplectic integrators
    - vectorized physics
    - barycentric corrections
    """

    def __init__(self, positions, velocities, masses, names):
        self.positions = np.array(positions, dtype=np.float64)
        self.velocities = np.array(velocities, dtype=np.float64)
        self.masses = np.array(masses, dtype=np.float64)
        self.names = list(names)

        self.N = self.positions.shape[0]

    # ==========================================================
    # MASS CLASSIFICATION
    # ==========================================================

    @property
    def massive_mask(self):
        return self.masses > 0.0

    @property
    def test_mask(self):
        return self.masses == 0.0

    @property
    def massive_indices(self):
        return np.where(self.massive_mask)[0]

    # ==========================================================
    # BARYCENTER CORRECTION
    # ==========================================================

    def apply_barycentric_correction(self):
        """
        Shifts system into center-of-mass frame.
        """

        total_mass = np.sum(self.masses)

        r_cm = np.sum(self.positions * self.masses[:, None], axis=0) / total_mass
        v_cm = np.sum(self.velocities * self.masses[:, None], axis=0) / total_mass

        self.positions -= r_cm
        self.velocities -= v_cm

    # ==========================================================
    # BASIC UTILITIES
    # ==========================================================

    def copy(self):
        return State(
            self.positions.copy(),
            self.velocities.copy(),
            self.masses.copy(),
            self.names.copy()
        )

    def summary(self):
        print("N-Body State")
        print("-" * 30)
        for i, name in enumerate(self.names):
            print(f"{i:2d}: {name:10s} | m={self.masses[i]:.3e}")
        print("-" * 30)
        print(f"N = {self.N}")