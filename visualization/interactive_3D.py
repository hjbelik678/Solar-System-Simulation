"""
============================================================
File: interactive_3d.py
Project: Solar System N-Body Simulation
============================================================

PURPOSE:
--------
Interactive 3D visualization using Plotly.

Features:
- Full 3D orbit rendering
- Zoom / rotate / pan
- Animation over time
- Works in browser
"""

import numpy as np
import plotly.graph_objects as go


def plot_3d_orbits(history, names, step=10):
    """
    Interactive 3D orbit visualization.

    Parameters:
        history : (T, N, 3)
        names   : list[str]
        step    : downsampling for performance
    """

    history = np.asarray(history)

    T, N, _ = history.shape

    # Downsample for performance
    history = history[::step]
    T = history.shape[0]

    fig = go.Figure()

    # ======================================================
    # STATIC ORBITS (full trajectory lines)
    # ======================================================

    for i, name in enumerate(names):
        fig.add_trace(go.Scatter3d(
            x=history[:, i, 0],
            y=history[:, i, 1],
            z=history[:, i, 2],
            mode='lines',
            name=name
        ))

    # ======================================================
    # CURRENT POSITION MARKERS (animated)
    # ======================================================

    frames = []

    for t in range(T):
        frame_data = []

        for i, name in enumerate(names):
            frame_data.append(go.Scatter3d(
                x=[history[t, i, 0]],
                y=[history[t, i, 1]],
                z=[history[t, i, 2]],
                mode='markers',
                marker=dict(size=4),
                name=name
            ))

        frames.append(go.Frame(data=frame_data, name=str(t)))

    fig.frames = frames

    # ======================================================
    # LAYOUT
    # ======================================================

    fig.update_layout(
        title="3D Solar System Simulation",
        scene=dict(
            xaxis_title="X [AU]",
            yaxis_title="Y [AU]",
            zaxis_title="Z [AU]",
            aspectmode='data'
        ),
        updatemenus=[{
            "type": "buttons",
            "buttons": [
                {
                    "label": "Play",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": 30, "redraw": True}}]
                }
            ]
        }]
    )

    fig.show()