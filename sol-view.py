import plotly.graph_objects as go
import numpy as np
import datetime

def julian_date():
    date = datetime.date.today()
    jd = (367 * date.year - (7 * (date.year + (date.month + 9) // 12)) // 4 + (275 * date.month) // 9 + date.day + 1721013.5)
    return jd

JD = julian_date()


spheres = [
    {"name": "Sun", "radius": 110 / 10, "color": "YlOrRd"},  # 1:10 radius
    {"name": "Mercury", "radius": 0.383 * 3, "color": "Purp", "semimajor_axis": 57.90900, "eccentricity": 0.20560, "inclination": 7.0, "orbit": 87, "mean_longitude": 252.25084, "periapsis": 29.022, "mean_motion": 4.092},
    {"name": "Venus", "radius": 0.950 * 3, "color": "Oranges", "semimajor_axis": 108.20000, "eccentricity": 0.00699, "inclination": 3.4, "orbit": 224, "mean_longitude": 181.97973, "periapsis": 67.16, "mean_motion": 1.602},
    {"name": "Earth", "radius": 1 * 3, "color": "Earth", "semimajor_axis": 149.60000, "eccentricity": 0.01671, "inclination": 0.0, "orbit": 365, "mean_longitude": 100.46646, "periapsis": 147.10, "mean_motion": 0.985607},
    {"name": "Mars", "radius": 0.532 * 3, "color": "agsunset", "semimajor_axis": 227.93919, "eccentricity": 0.09340, "inclination": 1.85, "orbit": 687, "mean_longitude": 355.43300, "periapsis": 206.62, "mean_motion": 0.524},
    {"name": "Jupiter", "radius": 11.21 * 3, "color": "pubugn", "semimajor_axis": 778.57000, "eccentricity": 0.04839, "inclination": 1.30, "orbit": 4333, "mean_longitude": 34.40438, "periapsis": 740.52, "mean_motion": 0.083},
    {"name": "Saturn", "radius": 9.45 * 3, "color": "electric", "semimajor_axis": 1433.53000, "eccentricity": 0.05386, "inclination": 2.49, "orbit": 10759, "mean_longitude": 50.07508, "periapsis": 1352.55, "mean_motion": 0.033},
    {"name": "Uranus", "radius": 4.01 * 3, "color": "bluyl", "semimajor_axis": 2872.46000, "eccentricity": 0.04638, "inclination": 0.77, "orbit": 30687, "mean_longitude": 314.05501, "periapsis": 2741.30, "mean_motion": 0.011},
    {"name": "Neptune", "radius": 3.88 * 3, "color": "blues", "semimajor_axis": 4495.06000, "eccentricity": 0.01000, "inclination": 1.77, "orbit": 60190, "mean_longitude": 304.88003, "periapsis": 4444.45, "mean_motion": 0.006},
    # {"name": "Pluto", "radius": 0.186, "color": "purpor", "semimajor_axis": 5906.38000, "eccentricity": 0.24880, "inclination": 17.15, "orbit": 90560, "mean_longitude": 238.92903, "periapsis": 4436.82, "mean_motion": 0.003}
]

def anomaly(l = "mean_longitude", p = "periapsis", m = "mean_motion", e = "eccentricity", tol=1e-6):
    T = (JD - 2451545.0) / 36525 # Julian date to centuries since J2000.0
    M = np.radians(l - p) + np.radians(m) * (JD - 2451545.0)
    E = M

    #Kepler Eq.
    while True:
        delta = E - e * np.sin(E) - M
        if abs(delta) < tol:
            break
        E -= delta / (1 - e * np.cos(E)) # Eccentric anomaly

    v = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2)) # True anomaly
    return v

#Create sphere
def create_sphere(radius=1, color = "white", name = "sphere"):
    resolution=20
    u = np.linspace(0, 2 * np.pi, resolution)  
    v = np.linspace(0, np.pi, resolution)
    U, V = np.meshgrid(u, v)
    x = radius * np.cos(U) * np.sin(V)
    y = radius * np.sin(U) * np.sin(V)
    z = radius * np.cos(V)
    color = color
    return x, y, z, color, name



#Set sphere position
def get_position(a = "semimajor_axis", e = "eccentricity", i = "inclination", orbit=100): 
    v = anomaly(sphere["mean_longitude"], sphere["periapsis"], sphere["mean_motion"], sphere["eccentricity"])
    r = a * (1 - e**2) / (1 + e * np.cos(v)) # Radial distance

    x = r * np.cos(v)
    y = r * np.sin(v)
    z = 0

    i = np.radians(i)

    x_final = x
    y_final = y * np.cos(i) - z * np.sin(i)
    z_final = y * np.sin(i) + z * np.cos(i)

    return x_final, y_final, z_final

#Create orbit
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

#Draw Sphere
fig = go.Figure() 
for sphere in spheres:
    if "semimajor_axis" in sphere:  
        x_pos, y_pos, z_pos = get_position(sphere["semimajor_axis"], sphere["eccentricity"], sphere["inclination"], sphere["orbit"])
    else:
        x_pos, y_pos, z_pos = 0, 0, 0
    x, y, z, color, name = create_sphere(sphere["radius"], sphere["color"], sphere["name"])
    x += x_pos
    y += y_pos
    z += z_pos
    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale=color, showscale=False, name = name))

#Draw Orbit
for sphere in spheres[1:]: 
    x, y, z = create_orbit(sphere["semimajor_axis"], sphere["eccentricity"], sphere["inclination"], sphere["orbit"])
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color="white", width=1), name=f"{sphere['name']} Orbit", showlegend=False ))

# Layout
fig.update_layout(
    title="Solar System",
    scene=dict(
        # xaxis=dict(title="X Axis", range=[-200, 200], visible=False),
        # yaxis=dict(title="Y Axis", range=[-200, 200], visible=False),
        # zaxis=dict(title="Z Axis", range=[-200, 200], visible=False),
        xaxis=dict(title="X Axis", visible=False),
        yaxis=dict(title="Y Axis", visible=False),
        zaxis=dict(title="Z Axis", visible=False),
        aspectmode='data',  
        # aspectratio=dict(x=1, y=1, z=1) 
    ),
    plot_bgcolor="rgb(30, 30, 30)",
    paper_bgcolor="rgb(3, 3, 3)", 
    margin=dict(l=0, r=0, b=0, t=40) # Remove margins
)

fig.show()