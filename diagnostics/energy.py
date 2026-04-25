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