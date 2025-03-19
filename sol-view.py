import plotly.graph_objects as go
import numpy as np
import datetime
import json

spheres = json.load(open("celestial_body.json", "r"))

# Initial date
date = datetime.date.today()
day_of_year = date.timetuple().tm_yday

def julian_date(date):
    """Calculate the Julian Date for the current day."""
    jd = (367 * date.year - (7 * (date.year + (date.month + 9) // 12)) // 4 +
           (275 * date.month) // 9 + date.day + 1721013.5)
    return jd

def anomaly(mean_longitude, periapsis, mean_motion, eccentricity, date, tol=1e-6):
    """Calculate the true anomaly for a celestial body."""
    JD = julian_date(date)
    M_deg = (mean_longitude - periapsis + mean_motion * (JD - 2451545.0)) % 360
    M = np.radians(M_deg)
    E = M # Initial guess for eccentric anomaly

    while True:
        delta = E - eccentricity * np.sin(E) - M
        if abs(delta) < tol:
            break
        E -= delta / (1 - eccentricity * np.cos(E))

    v = 2 * np.arctan2(np.sqrt(1 + eccentricity) * np.sin(E / 2),
                       np.sqrt(1 - eccentricity) * np.cos(E / 2))
    return v

# Set sphere position
def get_position(sphere, date):
    """Compute the 3D position of a sphere."""
    if "semimajor_axis" not in sphere:
        return 0, 0, 0
    a = sphere["semimajor_axis"]
    e = sphere["eccentricity"]
    i = sphere["inclination"]
    l = sphere["mean_longitude"]
    p = sphere["periapsis"]
    m = sphere["mean_motion"]
 
    v = anomaly(l, p, m, e, date)
    r = a * (1 - e**2) / (1 + e * np.cos(v)) # Radial distance   
    x = r * np.cos(v)
    y = r * np.sin(v)
    z = 0

    omega = np.radians(p)
    x_rot = x * np.cos(omega) - y * np.sin(omega)
    y_rot = x * np.sin(omega) + y * np.cos(omega)
    z_rot = 0

    i = np.radians(i)
    x_final = x_rot
    y_final = y_rot * np.cos(i)
    z_final = y_rot * np.sin(i)

    if sphere.get("parent_body") is not None:
        x_parent, y_parent, z_parent = get_parent_position(sphere["parent_body"], date)

        return x_final + x_parent, y_final + y_parent, z_final + z_parent

    else:
        return x_final, y_final, z_final


def get_parent_position(name, date):

    for sphere in spheres:
        if sphere["name"] == name:
            a = sphere["semimajor_axis"]
            e = sphere["eccentricity"]
            i = sphere["inclination"]
            l = sphere["mean_longitude"]
            p = sphere["periapsis"]
            m = sphere["mean_motion"]

            v = anomaly(l, p, m, e, date)
            r = a * (1 - e**2) / (1 + e * np.cos(v)) # Radial distance   
            x = r * np.cos(v)
            y = r * np.sin(v)
            z = 0

            omega = np.radians(p)
            x_rot = x * np.cos(omega) - y * np.sin(omega)
            y_rot = x * np.sin(omega) + y * np.cos(omega)
            z_rot = 0

            i = np.radians(i)
            x_final = x_rot
            y_final = y_rot * np.cos(i)
            z_final = y_rot * np.sin(i)

            return x_final, y_final, z_final


# Create sphere
def create_sphere(radius=1, color = "white", name = "sphere", resolution=20):
    """Generate 3D coordinates for a sphere and draw it."""
    u = np.linspace(0, 2 * np.pi, resolution)  
    v = np.linspace(0, np.pi, resolution)
    U, V = np.meshgrid(u, v)
    color = color

    x = radius * np.cos(U) * np.sin(V)
    y = radius * np.sin(U) * np.sin(V)
    z = radius * np.cos(V)

    return x, y, z, color, name

# Create orbit
def create_orbit(sphere, current_date, resolution=100):
    """Generate 3D coordinates for a spheres orbit."""
    a = sphere["semimajor_axis"]
    e = sphere["eccentricity"]
    i = sphere["inclination"]
    p = sphere["periapsis"]

    x_parent = 0
    y_parent = 0
    z_parent = 0

    t = np.linspace(0, 2 * np.pi, resolution)
    b = a * np.sqrt(1 - e**2)
    i = np.radians(i)

    if sphere.get("parent_body") is not None:
        x_parent, y_parent, z_parent = get_parent_position(sphere["parent_body"], current_date)


    x_orbit = a * np.cos(t) - a * e 
    y_orbit = b * np.sin(t) 
    z_orbit = 0

    omega = np.radians(p)
    x_rot = x_orbit * np.cos(omega) - y_orbit * np.sin(omega)
    y_rot = x_orbit * np.sin(omega) + y_orbit * np.cos(omega)
    z_rot = 0

    
    x = x_rot + x_parent
    y = y_rot * np.cos(i) + y_parent
    z = y_rot * np.sin(i) + z_parent

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
    traces.append(go.Surface(x=x, y=y, z=z, colorscale=color, showscale=False, name = name))

# Draw initial orbits
for sphere in spheres[1:]: 
    x, y, z = create_orbit(sphere, date)
    traces.append(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color="white", width=1),
                                name=f"{sphere['name']} Orbit", showlegend=False ))

fig.add_traces(traces)

# Pre-calculate positions for each day
base_date = datetime.date(date.year, 1, 1)
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
        frame_data.append(go.Surface(x=x, y=y, z=z, colorscale=color, showscale=False, name = name))

    for sphere in spheres[1:]: 
        x, y, z = create_orbit(sphere, current_date)
        frame_data.append(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color="white", width=1),
                                    name=f"{sphere['name']} Orbit", showlegend=False ))

    frames.append(go.Frame(data=frame_data, name=str(day),
                       layout=dict(title=f"Solar System - {current_date}")))

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
    plot_bgcolor="rgb(30, 30, 30)",
    paper_bgcolor="rgb(3, 3, 3)", 
    margin=dict(l=0, r=0, b=0, t=35)
)

# fig.write_html("solar_system.html", include_plotlyjs="cdn") # Export as html file
fig.show()