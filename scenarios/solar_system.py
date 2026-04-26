"""
============================================================
File: solar_system.py
Project: Solar System N-Body Simulation
============================================================

PURPOSE:
--------
Defines a standard solar system scenario.

Provides:
- Sun + planets (circular orbit approximation)
- ready-to-use State object

This acts as a reusable entry point for simulations.


PHYSICAL MODEL:
---------------
- Newtonian gravity
- circular, coplanar orbits
- Sun initially at origin (corrected to barycenter later)


FUTURE EXTENSIONS:
------------------
- ephemeris-based initial conditions (JPL)
- inclined orbits
- moons
- asteroid belts
- spacecraft trajectories
"""

import numpy as np

from core.state import State
from config.constants import masses, names, generate_initial_conditions


def create_solar_system():
    """
    Create baseline solar system state.

    Returns
    -------
    state : State
        Initialized system ready for simulation
    """

    positions, velocities = generate_initial_conditions()

    state = State(
        positions=positions,
        velocities=velocities,
        masses=masses,
        names=names,
    )

    return state