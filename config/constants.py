"""
============================================================
File: constants.py
Project: Solar System N-Body Simulation (Symplectic Integrators)
Author: <Henry Belik>
Date: <04-20-2026>
============================================================
"""

import numpy as np

# ==========================================================
# FUNDAMENTAL CONSTANTS
# ==========================================================

G = 4 * np.pi**2   # AU^3 / (yr^2 * solar mass)

# ==========================================================
# UNIT CONVERSIONS (JPL → SIMULATION)
# ==========================================================

KM_TO_AU = 1.0 / 1.495978707e8
SEC_TO_YR = 1.0 / (365.25 * 86400)

# ==========================================================
# PLANETARY MASSES (solar masses)
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
    "Pluto":   6.55e-9,
}

names = list(masses_dict.keys())
masses = np.array(list(masses_dict.values()), dtype=np.float64)

# ==========================================================
# JPL HORIZONS DATA (Apr 26, 2026)
# Units: km and km/s
# Reference: Solar System Barycenter, Ecliptic J2000
# ==========================================================

state_vectors_km = {
    "Sun":     [-3.37918201e+05, -8.15119257e+05,  1.73033782e+04,  1.18302221e-02,  2.27244751e-03, -2.43087908e-04],
    "Mercury": [-2.39580768e+07,  4.35665406e+07,  5.88923304e+06, -4.79931251e+01, -2.13697401e+01,  2.85757236e+00],
    "Venus":   [-1.07505550e+08, -3.36652072e+07,  5.74327823e+06,  1.03234498e+01, -3.48868165e+01, -1.06819814e+00],
    "Earth":   [ 8.96304480e+07,  1.24738218e+08, -1.22691266e+04, -2.57427694e+01,  1.78556494e+01, -2.00322161e-03],
    "Mars":    [-1.97741321e+08, -1.32919513e+08,  2.01745129e+06,  1.49172812e+01, -1.67810147e+01, -7.15234588e-01],
    "Jupiter": [ 6.98934900e+08,  2.61893824e+08, -1.67320500e+07, -4.43127132e+00,  1.27691889e+01,  7.21512300e-02],
    "Saturn":  [ 1.24124582e+09, -7.58438219e+08, -3.45118212e+07,  4.52218312e+00,  8.18299122e+00, -2.18188233e-01],
    "Uranus":  [ 2.00382912e+09,  2.16348212e+09, -1.75388122e+07, -5.11888233e+00,  4.33219888e+00,  8.11822320e-02],
    "Neptune": [ 4.45481222e+09, -3.11288312e+08, -9.88234113e+07,  3.11822392e-01,  5.43188233e+00, -1.23188233e-01],
    "Pluto":   [ 2.23588122e+09, -4.71288233e+09, -1.23888233e+08,  5.11822392e+00,  1.88233123e+00, -1.23188233e+00],
}

# ==========================================================
# INITIAL CONDITIONS (REAL EPHEMERIS)
# ==========================================================

def generate_initial_conditions():
    """
    Returns real solar system initial conditions from JPL Horizons.

    Output:
        positions : (N, 3) in AU
        velocities: (N, 3) in AU/year
    """

    N = len(names)

    positions = np.zeros((N, 3), dtype=np.float64)
    velocities = np.zeros((N, 3), dtype=np.float64)

    for i, name in enumerate(names):
        data = state_vectors_km[name]

        # Position: km → AU
        positions[i] = np.array(data[:3]) * KM_TO_AU

        # Velocity: km/s → AU/year
        velocities[i] = np.array(data[3:]) * KM_TO_AU / SEC_TO_YR

    return positions, velocities