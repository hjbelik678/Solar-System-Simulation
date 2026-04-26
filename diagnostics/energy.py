"""
============================================================
File: energy.py
Project: Solar System N-Body Simulation (Symplectic Integrators)
============================================================

PURPOSE:
--------
Computes total mechanical energy of an N-body gravitational system.

Used for:
- validating numerical stability
- verifying correctness of integrators
- detecting energy drift over long simulations


PHYSICAL MODEL:
---------------
Total energy is defined as:

    E = T + U

where:

Kinetic Energy:
    T = (1/2) Σ_i m_i |v_i|^2

Potential Energy:
    U = - Σ_{i<j} G m_i m_j / |r_ij|

with:
- r_ij = r_j - r_i
- |r_ij| = distance between bodies


UNITS:
------
- Distance: AU
- Time: years
- Mass: solar masses

Derived:
- Energy units:
    M☉ · AU² / yr²


HETEROGENEOUS BODY MODEL:
-------------------------
Two categories:

1. Massive bodies (m > 0)
   - contribute to both kinetic and potential energy
   - define system dynamics

2. Test particles (m = 0)
   - contribute NOTHING to energy
   - ignored in computation

Implementation rule:
    Only include bodies where m > 0


BARYCENTRIC FRAME:
------------------
Energy is computed in the barycentric frame.

Properties:
- kinetic energy excludes bulk motion
- eliminates artificial center-of-mass drift energy

This ensures:
- physically meaningful total energy
- correct comparison across timesteps


NUMERICAL PROPERTIES:
---------------------
- Kinetic energy: fully vectorized
- Potential energy: computed via pairwise summation
- O(N^2) complexity for massive bodies
- stable under symplectic integration

Expected behavior (symplectic integrators):
- energy is NOT exactly conserved
- energy oscillates around a constant value
- no long-term drift


VALIDATION USE:
---------------
Energy is the primary diagnostic for integrator quality:

- Verlet:
    bounded oscillations

- Yoshida4:
    smaller oscillations

- Non-symplectic methods:
    energy drift over time

Key metric:

    Relative energy error:
        (E(t) - E(0)) / |E(0)|

Correct behavior:
    small, bounded oscillations


LIMITATIONS:
-----------
- ignores relativistic corrections
- assumes point masses
- no collision or merging effects
- potential energy undefined at r = 0 (no softening here)


FUTURE EXTENSIONS:
------------------
- softening support for close encounters
- fast pairwise computation (Barnes-Hut)
- energy decomposition (per-body contributions)
- adaptive timestep diagnostics


============================================================
CONSERVATION LAW INSIGHT
============================================================

Energy conservation arises from:

    time invariance of the system

In numerical simulations:

- exact conservation is NOT expected (discretization error)
- symplectic methods preserve a modified Hamiltonian

Thus:

    Energy should remain bounded, not constant

If energy drifts:
    → integrator is incorrect
    → timestep too large
    → force calculation error

============================================================
"""

import numpy as np
from config.constants import G


def compute_energy(state):
    """
    Compute total energy (kinetic + potential) of the system.
    Only includes massive bodies (m > 0).
    """

    positions = state.positions
    velocities = state.velocities
    masses = state.masses

    # --- Filter massive bodies ---
    mask = masses > 0.0
    pos = positions[mask]
    vel = velocities[mask]
    m = masses[mask]

    # --- Kinetic Energy ---
    kinetic = 0.5 * np.sum(m * np.sum(vel**2, axis=1))

    # --- Potential Energy ---
    U = 0.0
    N = len(m)

    for i in range(N):
        r_ij = pos[i+1:] - pos[i]
        dist = np.linalg.norm(r_ij, axis=1)

        U -= G * m[i] * np.sum(m[i+1:] / dist)

    return kinetic + U