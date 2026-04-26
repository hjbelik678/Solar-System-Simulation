"""
============================================================
File: settings.py
Project: Solar System N-Body Simulation
============================================================

PURPOSE:
--------
Defines core simulation parameters controlling time evolution
and numerical behavior.
"""

# ==========================================================
# TIME PARAMETERS
# ==========================================================

dt = 0.001          # Time step (years)
t_end = 1000        # Total simulation time (years)
steps = int(t_end / dt)

# ==========================================================
# INTEGRATOR
# ==========================================================

integrator = "yoshida4"   # "verlet" or "yoshida4"

# ==========================================================
# OUTPUT CONTROL
# ==========================================================

save_interval = 10        # Save every N steps

# ==========================================================
# NUMERICAL PARAMETERS
# ==========================================================

softening = 0.0           # Gravitational softening (AU)

# ==========================================================
# NOTES
# ==========================================================

"""
- Smaller dt improves accuracy, not just stability
- Symplectic integrators conserve structure, not exact energy
- Long-term simulations require careful timestep choice
"""