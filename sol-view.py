import plotly.graph_objects as go
import numpy as np

spheres = [
    {"name": "Sun", "radius": 5.5, "center": (0, 0, 0), "color": "YlOrRd"},
    {"name": "Mercury", "radius": 0.383, "center": (-46, 46, 6), "color": "Purp", "semimajor_axis": 57.909, "eccentricity": 0.2056, "inclination": 7.0},
    {"name": "Venus", "radius": 0.950, "center": (76, -76, -4), "color": "Oranges", "semimajor_axis": 108.2, "eccentricity": 0.007, "inclination": 3.4},   
    {"name": "Earth", "radius": 1, "center": (-107, -107, 0), "color": "Earth", "semimajor_axis": 149.6, "eccentricity": 0.017, "inclination": 0.0}   
]


def create_sphere(radius=1, center=(0, 0, 0), resolution=20, color = "white", name = "sphere", **kwargs): #Sphere
    u = np.linspace(0, 2 * np.pi, resolution)  
    v = np.linspace(0, np.pi, resolution)
    U, V = np.meshgrid(u, v)
    x = radius * np.cos(U) * np.sin(V) + center[0]
    y = radius * np.sin(U) * np.sin(V) + center[1]
    z = radius * np.cos(V) + center[2]
    color = color
    return x, y, z, color, name

def create_orbit(a = "semimajor_axis", e = "eccentricity", i = "inclination", resolution=100):
    t = np.linspace(0, 2 * np.pi, resolution)
    b = a * np.sqrt(1 - e**2)
    x = a * np.cos(t) - a * e 
    y1 = b * np.sin(t) 
    z1 = np.zeros_like(t)  
    i = np.radians(i)
    y = y1 * np.cos(i) - z1 * np.sin(i)
    z = y1 * np.sin(i) + z1 * np.cos(i)
    return x, y, z

fig = go.Figure()
for sphere in spheres:
    x, y, z, color, name = create_sphere(**sphere)
    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale=color, showscale=False, name = name))

for sphere in spheres[1:]:
    x, y, z = create_orbit(sphere["semimajor_axis"], sphere["eccentricity"], sphere["inclination"])
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color="white", width=1), name=f"{sphere['name']} Orbit" ))

# Layout
fig.update_layout(
    title="Solar System",
    scene=dict(
        xaxis=dict(title="X Axis", range=[-200, 200], visible=False),
        yaxis=dict(title="Y Axis", range=[-200, 200], visible=False),
        zaxis=dict(title="Z Axis", range=[-200, 200], visible=False),
        # aspectmode='manual',  
        # aspectratio=dict(x=1, y=1, z=1) 
    ),
    plot_bgcolor="rgb(30, 30, 30)",
    paper_bgcolor="rgb(3, 3, 3)", 
    margin=dict(l=0, r=0, b=0, t=40) # Remove margins
)

fig.show()