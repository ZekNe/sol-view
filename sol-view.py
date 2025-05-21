

import json
import datetime
import numpy as np
import plotly.graph_objects as go

# Load celestial body data
with open("celestial_body.json", "r") as file:
    spheres = json.load(file)

# Initial date
date = datetime.date.today()
day_of_year = date.timetuple().tm_yday

def julian_date(date):
    """Calculate the Julian Date for the current day."""
    return (
        367 * date.year 
        - (7 * (date.year + (date.month + 9) // 12)) // 4
        + (275 * date.month) // 9 
        + date.day + 1721013.5
    )

def anomaly(mean_longitude, periapsis, mean_motion, eccentricity, date, tol=1e-6):
    """Calculate the true anomaly for a celestial body."""

    JD = julian_date(date)
  
    mean_anomaly_deg = (mean_longitude - periapsis + mean_motion * (JD - 2451545.0)) % 360
    mean_anomaly = np.radians(mean_anomaly_deg) # Mean anomaly in radians
    eccentric_anomaly = mean_anomaly # Initial guess for eccentric anomaly

    # Iteratively solve for eccentric anomaly using Newton-Raphson method
    while True:
        delta = eccentric_anomaly - eccentricity * np.sin(eccentric_anomaly) - mean_anomaly
        if abs(delta) < tol:
            break
        eccentric_anomaly -= delta / (1 - eccentricity * np.cos(eccentric_anomaly))

    # Calculate true anomaly
    true_anomaly = 2 * np.arctan2(np.sqrt(1 + eccentricity) * np.sin(eccentric_anomaly / 2),
                                  np.sqrt(1 - eccentricity) * np.cos(eccentric_anomaly / 2))
    
    return true_anomaly

# Set sphere position
def get_position(sphere, date):
    """Compute the 3D position of a sphere."""

    # Sun
    if "semimajor_axis" not in sphere:
        return 0, 0, 0
    
    # Orbital elements
    a = sphere["semimajor_axis"]
    e = sphere["eccentricity"]
    i = sphere["inclination"]
    l = sphere["mean_longitude"]
    p = sphere["periapsis"]
    m = sphere["mean_motion"]
 
    true_anomaly = anomaly(l, p, m, e, date) # True anomaly
    r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly)) # Radial distance   
    periapsis = np.radians(p) # Periapsis in radians
    inclination = np.radians(i)

    x = r * np.cos(true_anomaly)
    y = r * np.sin(true_anomaly)
    z = 0

    x_rot = x * np.cos(periapsis) - y * np.sin(periapsis)
    y_rot = x * np.sin(periapsis) + y * np.cos(periapsis)
    z_rot = 0

    x_final = x_rot
    y_final = y_rot * np.cos(inclination)
    z_final = y_rot * np.sin(inclination)

    # If the sphere has a parent body, adjust the position
    if sphere.get("parent_body") is not None:
        x_parent, y_parent, z_parent = get_parent_position(sphere["parent_body"], date)
        return x_final + x_parent, y_final + y_parent, z_final + z_parent
 
    return x_final, y_final, z_final


def get_parent_position(name, date):
    for sphere in spheres:
        if sphere["name"] == name:

            # Orbital elements
            a = sphere["semimajor_axis"]
            e = sphere["eccentricity"]
            i = sphere["inclination"]
            l = sphere["mean_longitude"]
            p = sphere["periapsis"]
            m = sphere["mean_motion"]

            true_anomaly = anomaly(l, p, m, e, date) # True anomaly
            r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly)) # Radial distance  
            periapsis = np.radians(p) # Periapsis in radians
            inclination = np.radians(i)
            
            x = r * np.cos(true_anomaly)
            y = r * np.sin(true_anomaly)
            z = 0

            x_rot = x * np.cos(periapsis) - y * np.sin(periapsis)
            y_rot = x * np.sin(periapsis) + y * np.cos(periapsis)
            z_rot = 0
    
            x_final = x_rot
            y_final = y_rot * np.cos(inclination)
            z_final = y_rot * np.sin(inclination)

            return x_final, y_final, z_final

# Create sphere
def create_sphere(radius=1, color = "white", name = "sphere", resolution=20):
    """Generate 3D coordinates for a sphere and draw it."""

    # Create a meshgrid
    u = np.linspace(0, 2 * np.pi, resolution) # Azimuthal angle  
    v = np.linspace(0, np.pi, resolution) # Polar angle
    U, V = np.meshgrid(u, v)
    
    # Spherical coordinates to Cartesian
    x = radius * np.cos(U) * np.sin(V)
    y = radius * np.sin(U) * np.sin(V)
    z = radius * np.cos(V)

    return x, y, z, color, name

# Create orbit
def create_orbit(sphere, current_date, resolution=100):
    """Generate 3D coordinates for a spheres orbit."""

    # Orbital elements
    a = sphere["semimajor_axis"]
    e = sphere["eccentricity"]
    i = sphere["inclination"]
    p = sphere["periapsis"]

    # If no parent body
    x_parent = 0
    y_parent = 0
    z_parent = 0
 
    # If there is a parent body, get its position
    if sphere.get("parent_body") is not None:
        x_parent, y_parent, z_parent = get_parent_position(sphere["parent_body"], current_date)

    t = np.linspace(0, 2 * np.pi, resolution) # Time value for the orbital path
    semi_minor_axis = a * np.sqrt(1 - e**2)
    inclination = np.radians(i)
    periapsis = np.radians(p)

    x_orbit = a * np.cos(t) - a * e 
    y_orbit = semi_minor_axis * np.sin(t) 
    z_orbit = 0

    x_rot = x_orbit * np.cos(periapsis) - y_orbit * np.sin(periapsis)
    y_rot = x_orbit * np.sin(periapsis) + y_orbit * np.cos(periapsis)
    z_rot = 0

    x = x_rot + x_parent
    y = y_rot * np.cos(inclination) + y_parent
    z = y_rot * np.sin(inclination) + z_parent

    return x, y, z

# Create Figure
fig = go.Figure() 

# Initial traces
traces = []

# Draw initial spheres
for sphere in spheres:
    x_pos, y_pos, z_pos = get_position(sphere, date)
    x, y, z, color, name = create_sphere(sphere["radius"], sphere["color"], sphere["name"])
    x += x_pos
    y += y_pos
    z += z_pos
    traces.append(go.Surface(x=x, y=y, z=z,
                             colorscale=color, 
                             showscale=False, 
                             name = name,
                             hovertemplate=' '))

# Draw initial orbits
for sphere in spheres[1:]: 
    x, y, z = create_orbit(sphere, date)
    traces.append(go.Scatter3d(x=x, y=y, z=z,
                               mode="lines",
                               line=dict(color="white",
                               width=1),
                               name=f"{sphere['name']} Orbit", 
                               showlegend=False,
                               hovertemplate=' ' ))

fig.add_traces(traces)

# Pre-calculate positions for each day
base_date = datetime.date(date.year, 1, 1) # Change this to a custom year, e.g., (2033, 1, 1)
step_size = 1
steps = []
frames = []

for day in range(0, 365, step_size):
    current_date = base_date + datetime.timedelta(days=day)
    frame_data = []

    # Calculate positions for each sphere
    for sphere in spheres:
        x_pos, y_pos, z_pos = get_position(sphere, current_date)
        x, y, z, color, name = create_sphere(sphere["radius"], sphere["color"], sphere["name"])

        x += x_pos
        y += y_pos
        z += z_pos

        frame_data.append(go.Surface(
                            x=x, y=y, z=z, 
                            colorscale=color, 
                            showscale=False, 
                            name = name, 
                            hovertemplate=' ',
                        ))

    for sphere in spheres[1:]: 
        x, y, z = create_orbit(sphere, current_date)

        frame_data.append(go.Scatter3d(
                            x=x, y=y, z=z, 
                            mode="lines", 
                            line=dict(color="white", width=1),
                            name=f"{sphere['name']} Orbit",
                            showlegend=False,
                            hovertemplate=' ',
                        ))

    frames.append(go.Frame(
                    data=frame_data,
                    name=str(day),
                    layout=dict(title=f"Solar System - {current_date}")
                ))

    steps.append({
        "args": [[str(day)], {"frame": {"duration": 0, "redraw": True},
                             "mode": "immediate",
                             "transition": {"duration": 0}}],
        "label": current_date.strftime("%b %d"),
        "method": "animate"
    })

fig.frames = frames

# Layout
fig.update_layout(
    title=f"Solar System - {date}",
    scene=dict(
        xaxis=dict(title="X Axis", visible=False),
        yaxis=dict(title="Y Axis", visible=False),
        zaxis=dict(title="Z Axis", visible=False),
        aspectmode='data',  
    ),
    sliders=[{
        "active": day_of_year - 1,
        "currentvalue": {"prefix": "Date: "},
        "pad": {"b": 5, "l": 15, "r": 15},
        "steps": steps
    }],
    updatemenus=[{
        "type": "buttons",
        "x": 0.01,
        "xanchor": "left",
        "y": 0.025,
        "yanchor": "top",
        "direction": "left",
        "showactive": False,
        "pad": {'r': 0, 't': 0},
        "font": {"size": 20},
        "buttons": [
            {
            "label": "−",
            "method": "animate",
            "args": [
                None,
                {
                    "frame": {"duration": 99999, "redraw": True},
                    "mode": "immediate",
                    "fromcurrent": True,
                    "direction": "reverse",
                    "transition": {"duration": 0}
                }
            ]
            },
            {
            "label": "+",
            "method": "animate",
            "args": [
                None,
                {
                    "frame": {"duration": 99999, "redraw": True},
                    "mode": "immediate",
                    "fromcurrent": True,
                    "direction": "forward",
                    "transition": {"duration": 0}
                }
            ]
            }]
        }],
    
    plot_bgcolor="rgb(30, 30, 30)",
    paper_bgcolor="rgb(3, 3, 3)", 
    margin=dict(l=0, r=0, b=0, t=35)
)

# fig.write_html("solar_system.html", include_plotlyjs="cdn") # Export as html file
fig.show()
