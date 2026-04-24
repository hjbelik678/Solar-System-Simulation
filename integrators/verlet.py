"""
============================================================
File: verlet.py
Project: Solar System N-Body Simulation
============================================================

PURPOSE:
--------
Implements the velocity Verlet integrator

FEATURES:
---------
- 2nd order symplectic method
- time reversible
- stable for long temr orbital dynamics

INTERFACE:
state -> updated state

DEPENDENCIES:
-------------
- physics.gravity.compute_accelerations
- core.state.state
"""

import numpy as np
from physics.gravity import compute_accelerations

def verlet_step(state, dt, softening=0.0):
    """
    perform on veloctiy verlet timestep
    Parameters
    ----------
    state: state
        current system state
    dt : float
        timestep
    softening : float
        Optional gravitational softening
    
    Returns
    -------
    state : State
        Updated state
    """

    # step 1: compute current acceleration
    a_t = compute_accelerations(state.positions, state.masses, softening = softening)

    # step 2: update positions
    state.positions += (state.velocities * dt + 0.5 * a_t * dt**2)

    # step 3: compute new accelerations
    a_t_dt = compute_accelerations(state.positions, state.masses, softening=softening)

    # step 4: updat velocities
    state.velocities += 0.5 * (a_t + a_t_dt) * dt

    return state

