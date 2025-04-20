
# Sol-view

Interactive 3D solar system visualization in Python using Plotly. Accurately displays the Sun, planets, some of their largest moons, and supports adding more celestial bodies.

## Installation

1. **Clone the Repository**  
```bash
git clone https://github.com/ZekNe/sol-view.git
```

---
2. **Set up virtual environment (Optional)**
   
```bash
python -m venv venv
```

 Activate it:
* On Windows:
```bash
venv/scripts/activate
```
* On macOS/Linux:
```bash
source venv/bin/activate
```

---

3. **Install Dependencies**
   
* Requires Python 3.6+ (python --version to check)

 Using requirements.txt:
```bash
pip install -r requirements.txt
```

 or manually:
```bash
pip install numpy plotly
```

---

4. **Launch**
```bash
python sol-view.py
```


## Usage

### Celestial Body Parameters

| Parameter       | Description                             | Units         |
|-----------------|-----------------------------------------|---------------|
| name            | Name of the celestial body              | String        |
| radius          | Scaled radius (Earth radius = 6371km)   | 1 = 6371 km   |
| color           | Using pyplot colors                     | String        |
| semimajor_axis  | Avg. distance from the Sun              | Million km    |
| eccentricity    | Orbit stretch (0 = circle)              | 0–1 scale     |
| inclination     | Tilt of orbit                           | Degrees       |
| orbit           | Orbital period                          | Earth days    |
| mean_longitude  | Position in orbit (J2000)               | Degrees       |
| periapsis       | Closest approach to the Sun             | Million km    |
| mean_motion     | Average movement per day                | Degrees/day   |

### Adding New Bodies
Make sure to use J2000 epoch for accurate position in the orbit.

Add new celestial objects to celestial_body.json in this format:
```json
[
    {
    ...
    },
    {
        "name": "Halley's Comet",
        "radius": 2.1,
        "color": "gray",
        "semimajor_axis": 2653.417,
        "eccentricity": 0.96658,
        "inclination": 161.96,
        "orbit": 27284.17,
        "mean_longitude": 174.356,
        "periapsis": 87.72,
        "mean_motion": 0.0131
    }
]

```


### Set a Custom Year
Change the year by modifying the base_date in sol-view.py:
```py
base_date = datetime.date(date.year, 1, 1)

#e.g.

base_date = datetime.date(2033, 1, 1)
```

### Saving Output
To save the visualization as an HTML file for later viewing, uncomment the following line in sol-view.py:
```py
fig.write_html("solar_system.html", include_plotlyjs="cdn")
```


## License


[MIT](https://choosealicense.com/licenses/mit/)
