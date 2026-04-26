"""
============================================================
File: constants.py
Project: Solar System N-Body Simulation (Symplectic Integrators)
Author: <Henry Belik>
Date: <04-20-2026>
============================================================

PURPOSE:
--------
Defines all physical constants, planetary masses, and initial
conditions for the solar system simulation.

This module serves as the single source of truth for:
- Unit system
- Gravitational constant
- Planetary data (mass, position, velocity)


PHYSICAL MODEL:
---------------
- Newtonian N-body gravity
- Point masses
- No relativistic corrections
- Gravitational Forces Only


UNITS:
-----------------
- Distance: Astronomical Units (AU)
- Time: Years (yr)
- Mass: Solar Masses (M☉)

Derived:
- Gravitational constant:
    G = 4π² AU³ / (yr² M☉)

IMPORTANT:
----------
All modules MUST use these units consistently.


DATA DEFINITIONS:
-----------------
Each body is defined by:
- name
- mass (solar masses)
- initial position (AU)
- initial velocity (AU/yr)

Initial conditions assume:
- Circular orbits
- Motion in the xy-plane
- Sun at origin


NOTES:
------
- Circular velocity: v = sqrt(GM / r)
- Since M_sun = 1 → v = sqrt(4π² / r)
- Direction: +y for planets starting on +x axis


LIMITATIONS:
------------
- Real planetary orbits are elliptical and inclined
- No barycentric correction (Sun fixed at origin)
- Initial conditions are approximate


FUTURE IMPROVEMENTS:
--------------------
- Use NASA/JPL ephemerides
- Add orbital inclinations
- Switch to barycentric frame
- Include moons, asteroids, comets

============================================================
"""

import numpy as np

# ==========================================================
# FUNDAMENTAL CONSTANTS
# ==========================================================

G = 4 * np.pi**2   # AU^3 / (yr^2 * solar mass)

# ==========================================================
# PLANETARY MASSES (in solar masses)
# ==========================================================

masses_dict = {
    "Sun":     1.0,
    "Mercury": 1.651e-7,
    "Venus":   2.447e-6,
    "Earth":   3.003e-6,
    "Mars":    3.213e-7,
    "Jupiter": 9.545e-4,
    "Saturn":  2.857e-4,
    "Uranus":  4.365e-5,
    "Neptune": 5.149e-5,
    "Pluto": 6.55e-9,
}

# Order matters for simulation arrays
names = list(masses_dict.keys())
masses = np.array(list(masses_dict.values()))

# ==========================================================
# ORBITAL RADII (AU)
# Approximate semi-major axes
# ==========================================================

radii = {
    "Mercury": 0.39,
    "Venus":   0.72,
    "Earth":   1.00,
    "Mars":    1.52,
    "Jupiter": 5.20,
    "Saturn":  9.58,
    "Uranus":  19.2,
    "Neptune": 30.05,
    "Pluto": 39.48,
    
}

# ==========================================================
# INITIAL CONDITIONS
# Circular orbits in xy-plane
# ==========================================================

def generate_initial_conditions():
    """
    Returns:
        positions : ndarray (N, 3)
        velocities: ndarray (N, 3)
    """

    N = len(names)

    positions = np.zeros((N, 3))
    velocities = np.zeros((N, 3))

    # Sun at origin
    positions[0] = [0, 0, 0]
    velocities[0] = [0, 0, 0]

    # Planets
    for i, name in enumerate(names[1:], start=1):
        r = radii[name]

        # Position on x-axis
        positions[i] = [r, 0, 0]

        # Circular velocity magnitude
        v = np.sqrt(G / r)

        #pluto
        if name == "Pluto":
            v = np.sqrt(G / r) * 0.9

        # Velocity in +y direction
        velocities[i] = [0, v, 0]

    return positions, velocities