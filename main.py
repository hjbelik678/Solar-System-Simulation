import numpy as np
import matplotlib.pyplot as plt

# --- Diagnostics ---
from diagnostics.energy import compute_energy
from diagnostics.angular_momentum import compute_angular_momentum

# --- Core ---
from config.constants import masses, names, generate_initial_conditions
from core.state import State

# --- Integrator ---
from integrators.yoshida4 import yoshida4_step

# --- Settings ---
from config.settings import dt, steps, softening

# --- Runner ---
from simulation.runner import run_simulation

# ---- Scenarios ---
from visualization.plot_orbits import plotting

# ==========================================================
# INITIALIZE SYSTEM
# ==========================================================

positions, velocities = generate_initial_conditions()
state = State(positions, velocities, masses, names)


# ==========================================================
# RUN SIMULATION
# ==========================================================

history, energy, L = run_simulation(
    state,
    yoshida4_step,
    dt,
    steps,
    softening=softening,
    save_interval=10,
    track_energy=compute_energy,
    track_angular_momentum=compute_angular_momentum,
)

plotting(history, energy, L)

# ==========================================================
# ANGULAR MOMENTUM VALIDATION
# ==========================================================
"""
Lz = L[:, 2]
rel_error = (Lz - Lz[0]) / abs(Lz[0])
print("Max angular momentum relative error:", np.max(np.abs(rel_error)))
"""

