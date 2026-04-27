import numpy as np

# --- Config ---
from config.constants import masses, names, generate_initial_conditions

# --- State ---
from core.state import State

# --- Scenario ---
from scenarios.solar_system import create_solar_system

# --- Integrator ---
from integrators.yoshida4 import yoshida4_step

# --- Simulation ---
from simulation.runner import run_simulation

# --- Diagnostics ---
from diagnostics.energy import compute_energy
from diagnostics.angular_momentum import compute_angular_momentum

# --- Visualization ---
from visualization.plot_orbits import plot_results, plot_inner_outer
from visualization.interactive_3D import plot_3d_orbits

# --- Settings ---
from config.settings import dt, steps, softening


# ==========================================================
# INITIALIZE SYSTEM
# ==========================================================

positions, velocities = generate_initial_conditions()

state = State(
    positions=positions,
    velocities=velocities,
    masses=masses,
    names=names
)

# ==========================================================
# RUN SIMULATION
# ==========================================================

history, energy_history, L_history = run_simulation(
    state,
    yoshida4_step,   # pass as positional argument
    dt,
    steps,
    softening,
    save_interval=10,
    track_energy=compute_energy,
    track_angular_momentum=compute_angular_momentum
)

history = np.asarray(history)
energy_history = np.asarray(energy_history)
L_history = np.asarray(L_history)

# ==========================================================
# DIAGNOSTICS
# ==========================================================

# Angular momentum error (Lz conservation check)
Lz = L_history[:, 2]
rel_error = (Lz - Lz[0]) / abs(Lz[0])

print("Max relative angular momentum error:",
      np.max(np.abs(rel_error)))

# ==========================================================
# VISUALIZATION
# ==========================================================

# Inner + outer system view (your new feature)
plot_inner_outer(history, names)

# Optional detailed plots
"""plot_results(
    history=history,
    names=names,
    energy=energy_history,
    angular_momentum=L_history,
    show_earth=True,
    show_sun=True
)"""

plot_3d_orbits(history, names, step=20)