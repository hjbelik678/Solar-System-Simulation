# Solar System N-Body Simulation (Symplectic Integrators)

A high-precision, vectorized N-body gravitational simulation of the Solar System using symplectic integration methods and real JPL Horizons ephemeris data.

This project focuses on **numerical stability, long-term orbital fidelity, and physically consistent conservation laws** in chaotic gravitational systems.

---

# Overview

This simulator models the full Solar System as an N-body Newtonian system:

- Sun + 8 planets + Pluto
- Real initial conditions from **JPL Horizons (Apr 26, 2026)**
- Fully barycentric (center-of-mass frame)
- Designed for long-term orbital stability studies

The system is built to explore:

- Chaotic divergence in gravitational systems
- Energy conservation under symplectic integrators
- Angular momentum stability
- Real vs idealized orbital evolution
- Visualization of multi-body orbital structure

---

# Physical Model

## Governing Physics

The simulation uses **Newtonian gravity**:

\[
F_{ij} = G \frac{m_i m_j}{r_{ij}^2}
\]

with vectorized acceleration:

\[
\mathbf{a}_i = G \sum_{j \neq i} m_j \frac{\mathbf{r}_j - \mathbf{r}_i}{(|\mathbf{r}_j - \mathbf{r}_i|^2 + \epsilon^2)^{3/2}}
\]

---

## Units

All computations use a consistent astronomical unit system:

| Quantity | Unit |
|----------|------|
| Distance | AU |
| Time | years |
| Mass | Solar masses (M☉) |
| Gravitational constant | G = 4/pi^2 |

---

## Frame of Reference

- Barycentric (center-of-mass fixed)
- No artificial Sun pinning
- Momentum conserving system-wide

---

## Heterogeneous Bodies

Two particle types:

### Massive bodies
- Mutual gravitational interaction
- Contribute to barycenter

### Test particles (future extension)
- Feel gravity
- Do not exert force

---

# Numerical Methods

## Integrators

### Leapfrog (Verlet)
- 2nd order symplectic
- Stable baseline

### Yoshida 4th Order (primary)
- Higher-order symplectic scheme
- Improved long-term energy conservation
- Recommended default

---

## Why Symplectic Integration?

Unlike standard integrators:

- Energy is NOT exactly conserved
- BUT energy remains bounded over long timescales
- Preserves Hamiltonian structure
- Crucial for chaotic systems like N-body gravity

---

# Diagnostics

## Energy Conservation

Computed as:

- Kinetic energy
- Gravitational potential energy

Used to verify long-term numerical stability.

Expected behavior:
- Small oscillations around constant mean
- No secular drift

---

## Angular Momentum

Computed as:

L = Σ m_i (r_i × v_i)

Expected:
- Extremely stable (≈ 10⁻¹⁴ relative error observed)
- Strong validation of barycentric correctness

---

# Initial Conditions

## Data Source

Initial conditions are taken from:

- NASA JPL Horizons System
- Reference epoch: **April 26, 2026**
- Frame: Solar System Barycenter
- Coordinates: Ecliptic J2000

---

## Bodies Included

- Sun
- Mercury
- Venus
- Earth
- Mars
- Jupiter
- Saturn
- Uranus
- Neptune
- Pluto

---

## Units Conversion

Raw data:

- Positions: km → AU
- Velocities: km/s → AU/year

---

# Project Structure

## Project Structure

```text
solar_sim/
│
├── main.py
│
├── config/
│   ├── constants.py
│   └── settings.py
│
├── core/
│   ├── state.py
│   └── system.py
│
├── physics/
│   └── gravity.py
│
├── integrators/
│   ├── verlet.py
│   └── yoshida4.py
│
├── visualization/
│   └── interactive_3d.py
```
---

# Visualization

## Matplotlib (diagnostics)
Used for:
- energy plots
- angular momentum stability
- quick orbit validation

## Interactive 3D (Plotly)
Features:
- Full 3D orbital visualization
- Zoom / rotate / pan
- Time animation
- Multi-body tracking

Recommended for exploration and presentation.

---

# Simulation Configuration

Located in `config/settings.py`

Key parameters:

- `dt = 0.001` years (~0.365 days)
- `t_end = 1000` years (default long-run stability test)
- `integrator = "yoshida4"`
- `softening = 0.0` (optional numerical stabilization)

---

# Key Results

## Verified Properties

- ✔ Energy is bounded (no drift under Yoshida4)
- ✔ Angular momentum conserved to ~10⁻¹⁴ relative error
- ✔ Stable barycentric motion
- ✔ Real ephemeris initial conditions correctly integrated

---

## Observed Physics

- Inner planets show rapid chaotic divergence
- Outer planets remain smooth over long timescales
- Pluto exhibits high eccentricity orbital structure
- System is strongly sensitive to initial conditions (chaos confirmed)

---

# Known Limitations

- O(N²) gravitational complexity
- No relativistic corrections
- No collisions or mergers
- No adaptive timestep
- No GPU acceleration (yet)

---

# Future Improvements

## Performance
- Barnes–Hut O(N log N)
- GPU acceleration (CUDA / JAX)

## Physics
- Relativistic corrections
- Moon systems (Earth–Moon, Jovian moons)
- Asteroid belt population

## Modeling
- True ephemeris interpolation over time
- Non-planar orbital inclinations (partially included via JPL data)
- Collision and fragmentation physics

## Visualization
- Real-time streaming simulation
- Camera tracking (Sun/Earth/planet follow modes)
- Lighting and size scaling for realism

---

# Data Source

Initial conditions:

> NASA JPL Horizons System  
https://ssd.jpl.nasa.gov/horizons/

Ephemeris reference:
- DE441 planetary ephemeris
- Barycentric Solar System frame
- Ecliptic J2000 reference plane

---

# Author

Henry Belik  
Physics-based numerical simulation project  
computational astrophysics and dynamical systems
April 2026

---

# 🧭 Summary

This project is a fully functional, high-precision gravitational N-body simulator designed to:

- replicate real Solar System dynamics
- test numerical integrators
- study chaos in celestial mechanics
- provide an extensible physics research platform
