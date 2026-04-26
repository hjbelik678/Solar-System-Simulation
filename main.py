import numpy as np

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
from visualization.plot_orbits import plot_results

# --- Settings ---
from config.settings import dt, steps, softening


# ==========================================================
# INITIALIZE SCENARIO
# ==========================================================

state = create_solar_system()

# Ensure true barycentric frame at t=0
state.apply_barycentric_correction()

names = state.names


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


# ==========================================================
# VALIDATION
# ==========================================================

L = np.asarray(L)
Lz = L[:, 2]

rel_error = (Lz - Lz[0]) / abs(Lz[0])
print("Max angular momentum relative error:", np.max(np.abs(rel_error)))


# ==========================================================
# VISUALIZATION
# ==========================================================

plot_results(
    history,
    names,
    energy=energy,
    angular_momentum=L,
    show_all=True,      # all planets
    show_sun=True,      # barycentric motion
)