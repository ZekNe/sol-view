import json
from vpython import *
import math

with open("planets.json", "r") as file:
    data = json.load(file)

sun = sphere(pos=vector(0, 0, 0), radius=1, color=color.yellow)

planets_spheres = []
labels = []

for planet in data["planets"]:
    distance = planet["orbital_elements"]["semi_major_axis"] * 10

    planet_sphere = sphere(
        pos = vector(distance, 0, 0),
        radius = planet["physical_properties"]["radius"] * 0.0001,
        color = color.white,
        name=planet["name"]
    )

    label_text = f"{planet['name']} - {planet['physical_properties']['radius']} km"

    planet_label = label(
        pos = planet_sphere.pos + vector(0, 0.1, 0),
        text = label_text,
        height = 12 , 
        color = color.white
    )

    planets_spheres.append(planet_sphere)
    labels.append(planet_label)


orbits = []
for planet in data["planets"]:
    distance = planet["orbital_elements"]["semi_major_axis"] * 10
    inclination = math.radians(planet["orbital_elements"]["inclination"])
    
    orbit = curve(color=color.gray(0.5))

    for angle in range(0, 361, 2):
        radian_angle = math.radians(angle)
        x = distance * math.cos(radian_angle)
        y = distance * math.sin(radian_angle)
        z = 0 

        point = vector(x, y, z).rotate(axis=vector(1, 0, 0), angle=inclination)
        orbit.append(point)

    orbits.append(orbit)

t = 0
while True:
    rate(30)

    for i, planet in enumerate(data['planets']):
        distance =  planet["orbital_elements"]["semi_major_axis"] * 10

        orbital_angle = math.radians(360*t / 365)

        planets_spheres[i].pos = vector(
            distance * math.cos(orbital_angle),
            distance * math.sin(orbital_angle), 
            0
        )
        
        labels[i].pos = planets_spheres[i].pos + vector(0, 0.1, 0)
        
    t += 1


