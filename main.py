import numpy as np
import matplotlib.pyplot as plt
from diagnostics.energy import compute_energy

from config.constants import masses, names, generate_initial_conditions
from core.state import State
from integrators.verlet import verlet_step
from config.settings import dt, steps, softening


#  Initialize system 
positions, velocities = generate_initial_conditions()
state = State(positions, velocities, masses, names)
energy_history = []

#  Storage (only store every few steps) 
history = []

#  Simulation loop 
for step in range(steps):
    verlet_step(state, dt, softening)

    # Keep system centered
    state.apply_barycentric_correction()

    # Save occasionally (reduce memory)
    if step % 10 == 0:
        history.append(state.positions.copy())
        energy_history.append(compute_energy(state))

history = np.array(history)

earth_index = names.index("Earth")
sun_index = names.index("Sun")

# plot sun position
plt.plot(history[:, sun_index, 0], history[:, sun_index, 1])

x = history[:, earth_index, 0]
y = history[:, earth_index, 1]

# plot earth position
plt.figure()
plt.plot(x, y)
plt.gca().set_aspect('equal')
plt.title("Earth Orbit (Verlet Test)")
plt.xlabel("x [AU]")
plt.ylabel("y [AU]")
plt.grid()
plt.show()

#plot energy
plt.figure()
plt.plot(energy_history)
plt.title("Total Energy vs Time")
plt.xlabel("Step (sampled)")
plt.ylabel("Energy")
plt.grid()
plt.show()