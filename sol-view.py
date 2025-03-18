import plotly.graph_objects as go
import numpy as np
import datetime

spheres = [
    {"name": "Sun", "radius": 110 / 10, "color": "YlOrRd"},
    {"name": "Mercury", "radius": 0.383 * 5, "color": "Purp", "semimajor_axis": 57.90900, "eccentricity": 0.20560, "inclination": 7.0, "orbit": 87, "mean_longitude": 252.25084, "periapsis": 29.022, "mean_motion": 4.092},
    {"name": "Venus", "radius": 0.950 * 5, "color": "Oranges", "semimajor_axis": 108.20000, "eccentricity": 0.00699, "inclination": 3.4, "orbit": 224, "mean_longitude": 181.97973, "periapsis": 54.780, "mean_motion": 1.602},
    {"name": "Earth", "radius": 1 * 5, "color": "Earth", "semimajor_axis": 149.60000, "eccentricity": 0.01671, "inclination": 0.0, "orbit": 365, "mean_longitude": 100.46646, "periapsis": 85.901, "mean_motion": 0.985607},
    {"name": "Mars", "radius": 0.532 * 5, "color": "Oryel", "semimajor_axis": 227.93919, "eccentricity": 0.09340, "inclination": 1.85, "orbit": 687, "mean_longitude": 355.43300, "periapsis": 286.231, "mean_motion": 0.524},
    {"name": "Jupiter", "radius": 11.21 * 5, "color": "Peach", "semimajor_axis": 778.57000, "eccentricity": 0.04839, "inclination": 1.30, "orbit": 4333, "mean_longitude": 34.40438, "periapsis": 273.442, "mean_motion": 0.083},
    {"name": "Saturn", "radius": 9.45 * 5, "color": "Armyrose", "semimajor_axis": 1433.53000, "eccentricity": 0.05386, "inclination": 2.49, "orbit": 10759, "mean_longitude": 49.94432, "periapsis": 336.178, "mean_motion": 0.033},
    {"name": "Uranus", "radius": 4.01 * 5, "color": "bluyl", "semimajor_axis": 2872.46000, "eccentricity": 0.04638, "inclination": 0.77, "orbit": 30687, "mean_longitude": 314.05501, "periapsis": 98.862, "mean_motion": 0.011},
    {"name": "Neptune", "radius": 3.88 * 5, "color": "blues", "semimajor_axis": 4495.06000, "eccentricity": 0.01000, "inclination": 1.77, "orbit": 60190, "mean_longitude": 304.88003, "periapsis": 256.932, "mean_motion": 0.006},
    # {"name": "Pluto", "radius": 0.186, "color": "purpor", "semimajor_axis": 5906.38000, "eccentricity": 0.24880, "inclination": 17.15, "orbit": 90560, "mean_longitude": 238.92903, "periapsis": 4436.82, "mean_motion": 0.003},
     # Moons
    {"name": "Moon", "parent_body":"Earth", "radius": 0.273 * 5, "color": "gray", "semimajor_axis": 5 + 0.3844 * 20, "eccentricity": 0.0549, "inclination": 5.145, "orbit": 27.321582, "mean_longitude": 218.316, "periapsis": 356400, "mean_motion": 13.176358},
    #  # Moons of Jupiter
    {"name": "Io", "parent_body": "Jupiter", "radius": 0.287 * 5, "color": "gray", "semimajor_axis": 11.21 * 5 + 0.4217 * 20, "eccentricity": 0.0041, "inclination": 0.036, "orbit": 1.769, "mean_longitude": 122.572, "periapsis": 0.0, "mean_motion": 1.769},
    {"name": "Europa", "parent_body": "Jupiter", "radius": 0.245 * 5, "color": "gray", "semimajor_axis": 11.21 * 5 + 0.6709 * 20, "eccentricity": 0.009, "inclination": 0.470, "orbit": 3.551, "mean_longitude": 88.350, "periapsis": 0.0, "mean_motion": 101.38},
    {"name": "Ganymede", "parent_body": "Jupiter", "radius": 0.413 * 5, "color": "gray", "semimajor_axis": 11.21 * 5 + 1.0704 * 20, "eccentricity": 0.0013, "inclination": 0.204, "orbit": 7.155, "mean_longitude": 184.790, "periapsis": 0.0, "mean_motion": 50.32},
    {"name": "Callisto", "parent_body": "Jupiter", "radius": 0.378 * 5, "color": "gray", "semimajor_axis": 11.21 * 5 + 1.8827 * 20, "eccentricity": 0.0074, "inclination": 0.192, "orbit": 16.689, "mean_longitude": 269.000, "periapsis": 0.0, "mean_motion": 21.58},
    # Moons of Saturn
    {"name": "Titan", "parent_body": "Saturn", "radius": 0.404 * 5, "color": "gray", "semimajor_axis": 9.45 * 5 + 1.222 * 20, "eccentricity": 0.0288, "inclination": 0.348, "orbit": 15.945, "mean_longitude": 83.538, "periapsis": 0.0, "mean_motion": 22.58},
    {"name": "Rhea", "parent_body": "Saturn", "radius": 0.120 * 5, "color": "gray", "semimajor_axis": 9.45 * 5 + 1.527 * 20, "eccentricity": 0.0015, "inclination": 0.348, "orbit": 4.518, "mean_longitude": 276.204, "periapsis": 0.0, "mean_motion": 79.68},
    {"name": "Dione", "parent_body": "Saturn", "radius": 0.088 * 5, "color": "gray", "semimajor_axis": 0.377 * 30, "eccentricity": 0.0023, "inclination": 0.013, "orbit": 2.737, "mean_longitude": 181.898, "periapsis": 0.0, "mean_motion": 131.56},
    # Moons of Uranus
    {"name": "Titania", "parent_body": "Uranus", "radius": 0.124 * 5, "color": "gray", "semimajor_axis": 4.01 * 5 + 0.436 * 20, "eccentricity": 0.0014, "inclination": 0.002, "orbit": 8.706, "mean_longitude": 97.908, "periapsis": 0.0, "mean_motion": 41.36},
    {"name": "Oberon", "parent_body": "Uranus", "radius": 0.119 * 5, "color": "gray", "semimajor_axis": 4.01 * 5 + 0.583 * 20, "eccentricity": 0.0016, "inclination": 0.001, "orbit": 13.463, "mean_longitude": 0.0, "periapsis": 0.0, "mean_motion": 26.74},
    # Moons of Neptune
    {"name": "Triton", "parent_body": "Neptune", "radius": 0.212 * 5, "color": "gray", "semimajor_axis": 3.88 * 5 + 0.3545 * 20, "eccentricity": 0.0001, "inclination": 157.8 / 100, "orbit": 5.877, "mean_longitude": 10.9, "periapsis": 0.0, "mean_motion": 61.26},
]
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
        # z_parent = sphere["radius"] * 10
        i = 0

    x_orbit = a * np.cos(t) - a * e + x_parent
    y_orbit = b * np.sin(t) + y_parent
    z_orbit = 0

    omega = np.radians(p)
    x_rot = x_orbit * np.cos(omega) - y_orbit * np.sin(omega)
    y_rot = x_orbit * np.sin(omega) + y_orbit * np.cos(omega)
    z_rot = 0

    
    x = x_rot
    y = y_rot * np.cos(i)
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