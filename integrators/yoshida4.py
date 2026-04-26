"""
============================================================
File: yoshida4.py
Project: Solar System N-Body Simulation (Symplectic Integrators)
============================================================

PURPOSE:
--------
Implements the 4th-order Yoshida symplectic integrator.

This method composes multiple Velocity Verlet steps with
carefully chosen coefficients to achieve higher-order accuracy
while preserving symplectic structure.


THEORY:
-------
Constructed from Verlet (2nd-order symplectic integrator):

    Φ₄(dt) = Φ(w₁ dt) Φ(w₀ dt) Φ(w₁ dt)

where:
    w₁ = 1 / (2 - 2^(1/3))
    w₀ = -2^(1/3) / (2 - 2^(1/3))

This cancels lower-order error terms, resulting in:

    Global error: O(dt⁴)


FEATURES:
---------
- 4th-order accuracy
- symplectic (preserves phase-space structure)
- time-reversible
- significantly improved energy behavior vs Verlet


NUMERICAL PROPERTIES:
---------------------
- requires 3 force evaluations per timestep
- ~3x cost of Verlet
- dramatically reduced energy oscillations


LIMITATIONS:
-----------
- fixed timestep only
- negative substep (w₀ < 0) required
- still O(N²) force scaling


DEPENDENCIES:
-------------
- integrators.verlet.verlet_step
"""

import numpy as np
from integrators.verlet import verlet_step

# ==========================================================
# YOSHIDA COEFFICIENTS
# ==========================================================

w1 = 1.0 / (2.0 - 2.0**(1.0 / 3.0))
w0 = -2.0**(1.0 / 3.0) * w1


def yoshida4_step(state, dt, softening=0.0):
    """
    Perform one Yoshida 4th-order timestep.

    Parameters
    ----------
    state : State
        Current system state
    dt : float
        Timestep
    softening : float
        Optional gravitational softening

    Returns
    -------
    state : State
        Updated state (in-place)
    """

    for w in (w1, w0, w1):
        verlet_step(state, w * dt, softening)

    return state