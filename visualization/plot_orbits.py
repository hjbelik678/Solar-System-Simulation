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

        energy_dev = energy - np.mean(energy)

        plt.figure()
        plt.plot(energy_dev, linewidth=1)

        plt.title("Energy Deviation from Mean vs Time")
        plt.xlabel("Sample Index")
        plt.ylabel("ΔE (E - ⟨E⟩)")
        plt.grid()

        # Robust scaling so tiny 1e-16 variations remain visible
        max_dev = np.max(np.abs(energy_dev))
        if max_dev > 0:
            plt.ylim(-10 * max_dev, 10 * max_dev)

    # ======================================================
    # ANGULAR MOMENTUM
    # ======================================================

    if angular_momentum is not None:
        L = np.asarray(angular_momentum)

        t = np.arange(len(L))

        Lx = L[:, 0]
        Ly = L[:, 1]
        Lz = L[:, 2]

        plt.figure()

        plt.plot(t, Lx, label="Lx", linewidth=1)
        plt.plot(t, Ly, label="Ly", linewidth=1)
        plt.plot(t, Lz, label="Lz", linewidth=1)

        plt.title("Angular Momentum Components vs Time")
        plt.xlabel("Sample Index")
        plt.ylabel("Angular Momentum")
        plt.grid()
        plt.legend()

        # Centered scaling around conservation value
        L_mean = np.mean(L, axis=0)
        L_fluct = L - L_mean
        max_fluct = np.max(np.abs(L_fluct))

        if max_fluct > 0:
            plt.ylim(np.min(L) - 5 * max_fluct, np.max(L) + 5 * max_fluct)

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