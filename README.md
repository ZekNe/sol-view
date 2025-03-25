
# Sol-view

Interactive 3D solar system in Python with Plotly.
Accurate visualization of our solar system for a given year,
showing the sun, planets and some of their largest moons,
and the ability to add more if desired.



## Installation

Clone or download repository

```bash
git clone https://github.com/ZekNe/sol-view.git
```
------------------------------------------------
*optional
Set up virtual environment

```bash
python -m venv venv
```

Launch the environment from main directory
```bash
venv/scripts/activate
```
------------------------------------------------
Install libraries

```bash
pip install numpy, plotly
```
or

```bash
pip install -r requirements.txt
```
------------------------------------------------

Launch from main directory

```bash
py sol-view.py
```

## Usage

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

Make sure to use J2000 epoch for accurate position in the orbit.

Add new celestial objects to celestial_body.json in this format
```bash
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

------------------------------------------------

Change this to a custom year, e.g., (2033, 1, 1)

```bash
base_date = datetime.date(date.year, 1, 1)
```
------------------------------------------------
Comment out if you wish to save as html for later viewing.

```bash
fig.write_html("solar_system.html", include_plotlyjs="cdn")
```


## License

[MIT](https://choosealicense.com/licenses/mit/)