"""
============================================================
File: plot_orbits.py
Project: Solar System N-Body Simulation
============================================================

PURPOSE:
--------
Visualization utilities for N-body simulations.

Supports:
- orbit plotting
- energy diagnostics
- angular momentum diagnostics
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_results(
    history,
    names,
    energy=None,
    angular_momentum=None,
    show_earth=False,
    show_sun=False,
    show_all=False,
):
    """
    General plotting function for simulation results.
    """

    history = np.asarray(history)

    # ======================================================
    # ORBIT PLOTS
    # ======================================================

    if show_all:
        plt.figure()
        for i, name in enumerate(names):
            plt.plot(history[:, i, 0], history[:, i, 1], label=name)

        plt.gca().set_aspect("equal")
        plt.legend()
        plt.title("Solar System Orbits")
        plt.xlabel("x [AU]")
        plt.ylabel("y [AU]")
        plt.grid()

    if show_earth:
        earth_index = names.index("Earth")

        plt.figure()
        plt.plot(history[:, earth_index, 0], history[:, earth_index, 1])
        plt.gca().set_aspect("equal")
        plt.title("Earth Orbit")
        plt.xlabel("x [AU]")
        plt.ylabel("y [AU]")
        plt.grid()

    if show_sun:
        sun_index = names.index("Sun")

        plt.figure()
        plt.plot(history[:, sun_index, 0], history[:, sun_index, 1])
        plt.gca().set_aspect("equal")
        plt.title("Sun Motion (Barycentric Frame)")
        plt.xlabel("x [AU]")
        plt.ylabel("y [AU]")
        plt.grid()

    # ======================================================
    # ENERGY
    # ======================================================

    if energy is not None:
        energy = np.asarray(energy)

        plt.figure()
        plt.plot(energy)
        plt.title("Total Energy vs Time")
        plt.xlabel("Sample Index")
        plt.ylabel("Energy")
        plt.grid()

    # ======================================================
    # ANGULAR MOMENTUM
    # ======================================================

    if angular_momentum is not None:
        L = np.asarray(angular_momentum)

        plt.figure()
        plt.plot(L[:, 2])
        plt.title("Angular Momentum (Lz)")
        plt.xlabel("Sample Index")
        plt.ylabel("Lz")
        plt.grid()

    plt.show()

def plot_inner_outer(history, names):
    history = np.asarray(history)

    inner = ["Mercury", "Venus", "Earth", "Mars"]
    outer = ["Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

    # --- Inner Solar System ---
    plt.figure()
    for name in inner:
        i = names.index(name)
        plt.plot(history[:, i, 0], history[:, i, 1], label=name)

    plt.gca().set_aspect("equal")
    plt.legend()
    plt.title("Inner Solar System")
    plt.grid()

    # --- Outer Solar System ---
    plt.figure()
    for name in outer:
        i = names.index(name)
        plt.plot(history[:, i, 0], history[:, i, 1], label=name)

    plt.gca().set_aspect("equal")
    plt.legend()
    plt.title("Outer Solar System")
    plt.grid()

    plt.show()