import plotly.graph_objects as go
import numpy as np


def create_sphere(radius=1, center=(0, 0, 0), resolution=20): #Sphere
    u = np.linspace(0, 2 * np.pi, resolution)  
    v = np.linspace(0, np.pi, resolution)
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

x, y, z = create_sphere(radius=5, center=(0, 0, 0)) #Sun coordinates

sun = go.Surface(x=x, y=y, z=z, colorscale='YlorRd', showscale=False) #Creates Sun

fig = go.Figure(data=[sun],) # Creates figure

# Layout
fig.update_layout(
    title='Solar System',
    scene=dict(
        xaxis=dict(visible=False), # Hide axes
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode='cube', # Equal proportions
    ),
    plot_bgcolor='rgb(30, 30, 30)',
    paper_bgcolor='rgb(0, 0, 0)', 
    margin=dict(l=0, r=0, b=0, t=40) # Remove margins
)

fig.show()