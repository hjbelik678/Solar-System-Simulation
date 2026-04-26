"""
============================================================
File: runner.py
Project: Solar System N-Body Simulation
============================================================

PURPOSE:
--------
Executes the main simulation loop.

Handles:
- time integration
- barycentric correction
- history storage
- diagnostics tracking
"""

import numpy as np

def run_simulation(state, integrator_step, dt, steps, softening=0.0, save_interval=10, track_energy=None, track_angular_momentum=None):
    """
    Run N-body simulation.

    Parameters
    ----------
    state : State
    integrator_step : function
        verlet_step or yoshida4_step
    dt : float
    steps : int
    softening : float
    save_interval : int
    track_energy : function or None
    track_angular_momentum : function or None

    Returns
    -------
    history : ndarray (T, N, 3)
    energy_history : list
    L_history : list
    """

    history = []
    energy_history = []
    L_history = []

    for step in range(steps):

        # --- Integrate ---
        integrator_step(state, dt, softening)

        # --- Barycentric correction ---
        state.apply_barycentric_correction()

        # --- Save ---
        if step % save_interval == 0:
            history.append(state.positions.copy())

            if track_energy:
                energy_history.append(track_energy(state))

            if track_angular_momentum:
                L_history.append(track_angular_momentum(state))

    return (
        np.array(history),
        np.array(energy_history),
        np.array(L_history),
    )