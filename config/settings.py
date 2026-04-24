"""
============================================================
File: settings.py
Project: Solar System N-Body Simulation (Symplectic Integrators)
Author: <Henry Belik>
Date: <04-20-2026>
============================================================

PURPOSE:
--------
Defines all simulation control parameters, numerical settings,
and runtime configuration for the N-body solar system model.

This file controls HOW the simulation runs, not the physics.


PHYSICAL MODEL (DEFINED ELSEWHERE):
------------------------------------
- Newtonian gravity (see gravity.py)
- Barycentric reference frame (center-of-mass fixed)
- Symplectic integration (see integrators/)


UNITS:
------
All values assume the global unit system:

- Distance: AU
- Time: years
- Mass: solar masses

(Defined in constants.py)


============================================================
NUMERICAL SETTINGS
============================================================
"""

# ==========================================================
# TIME PARAMETERS
# ==========================================================

dt = 0.001          # Time step (years)
                    # ~0.365 days

t_end = 100         # Total simulation time (years)

steps = int(t_end / dt)

# ==========================================================
# INTEGRATOR SELECTION
# ==========================================================

# Options:
# "verlet"   -> 2nd-order symplectic (stable baseline)
# "yoshida4" -> 4th-order symplectic (for accuracy)

integrator = "yoshida4"

# ==========================================================
# OUTPUT CONTROL
# ==========================================================

save_interval = 10
# Save every N steps (reduces memory usage)

enable_energy_tracking = True
enable_angular_momentum_tracking = True

# ==========================================================
# NUMERICAL STABILITY CONTROLS
# ==========================================================

softening = 0.0
# Optional gravitational softening factor
# (set >0 only if adding collision avoidance)

max_allowed_distance = None
# If set, can terminate simulation for escaping bodies

min_allowed_distance = 0.0
# For collision detection (optional future feature)

# ==========================================================
# SIMULATION MODE FLAGS
# ==========================================================

use_barycentric_frame = True
# MUST be True for correct momentum conservation

fixed_sun = False
# Deprecated: should always remain False

include_sun_motion = True
# Derived from barycentric formulation

# ==========================================================
# PERFORMANCE SETTINGS
# ==========================================================

use_vectorization = True
# Always True unless debugging

use_numba_acceleration = False
# Optional future optimization

parallelize_forces = False
# Future upgrade (O(N^2) parallelization)

# ==========================================================
# VISUALIZATION SETTINGS
# ==========================================================

plot_trajectories = True
trail_length = 5000

animate = True
fps = 30

show_real_time = False
# If True: slows simulation but shows live plotting

# ==========================================================
# EXPERIMENT CONTROL (IMPORTANT FOR YOU)
# ==========================================================

experiment_name = "solar_system_base_run"

run_id = None
# Can be auto-generated for batch experiments

record_state_vectors = True
# Saves full state history (memory intensive)

record_energy = True
record_momentum = True

# ==========================================================
# VALIDATION SETTINGS
# ==========================================================

check_energy_drift = True
energy_tolerance = 1e-3

check_momentum_conservation = True
momentum_tolerance = 1e-10

# ==========================================================
# NOTES
# ==========================================================

"""
- Smaller dt improves phase accuracy, not just stability
- Symplectic integrators will NOT conserve energy exactly
  but will keep it bounded
- Barycentric frame removes artificial momentum drift
- Increasing order (Verlet → Yoshida4) improves long-term fidelity
- N-body simulations are chaotic: small changes diverge exponentially

Recommended starting configuration:
    dt = 0.001
    integrator = "yoshida4"
    t_end = 50-200 years

"""