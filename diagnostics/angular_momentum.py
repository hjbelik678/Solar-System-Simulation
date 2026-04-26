"""
============================================================
File: angular_momentum.py
Project: Solar System N-Body Simulation (Symplectic Integrators)
============================================================

PURPOSE:
--------
Computes total angular momentum of an N-body gravitational system.

Used for:
- validating conservation laws
- verifying physical correctness of force calculations
- detecting numerical torque or integration errors


PHYSICAL MODEL:
---------------
Total angular momentum is defined as:

    L = Σ_i m_i (r_i × v_i)

where:
- r_i is position vector
- v_i is velocity vector
- m_i is mass

For planar systems (xy-plane), the dominant component is:

    L_z = Σ_i m_i (x_i v_yi - y_i v_xi)


UNITS:
------
- Distance: AU
- Time: years
- Mass: solar masses

Derived:
- Angular momentum units:
    M☉ · AU² / yr


HETEROGENEOUS BODY MODEL:
-------------------------
Two categories:

1. Massive bodies (m > 0)
   - contribute to angular momentum
   - define physical system dynamics

2. Test particles (m = 0)
   - contribute NOTHING to angular momentum
   - ignored in computation

Implementation rule:
    Only include bodies where m > 0


BARYCENTRIC FRAME:
------------------
Angular momentum is computed in the barycentric frame.

Because:
- center of mass is fixed
- linear momentum is removed

This ensures:
- physically meaningful angular momentum
- no artificial drift from reference frame motion


NUMERICAL PROPERTIES:
---------------------
- Uses vectorized NumPy operations
- O(N) complexity after masking
- stable under symplectic integration

Expected behavior:
- angular momentum should remain constant
- deviations should be at floating-point precision level


VALIDATION USE:
---------------
Angular momentum is a stricter diagnostic than energy:

- Energy:
    oscillates slightly (symplectic behavior)

- Angular Momentum:
    should be conserved exactly (no oscillation)


LIMITATIONS:
-----------
- ignores relativistic corrections
- assumes point masses
- does not account for external torques


FUTURE EXTENSIONS:
------------------
- component-wise diagnostics (Lx, Ly, Lz tracking)
- per-body angular momentum analysis
- spin angular momentum (extended bodies)
- torque diagnostics


============================================================
CONSERVATION LAW INSIGHT
============================================================

Angular momentum conservation arises from:

    rotational symmetry of the system

If angular momentum drifts:
    → forces are asymmetric
    → integration is incorrect
    → numerical instability is present

Thus:

    Angular momentum is a direct test of physical correctness

============================================================
"""

import numpy as np


def compute_angular_momentum(state):
    """
    Compute total angular momentum vector of the system.
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

    # --- Compute L = sum m * (r x v) ---
    L = np.sum(m[:, None] * np.cross(pos, vel), axis=0)

    return L