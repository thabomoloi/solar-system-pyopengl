# Graphics Assignment 1

## Setup

Setup assumes that you are using a UNIX-based OS with python3 and python3-venv installed.

To build the virtual environment and install necessary packages:

```bash
> make
```

To activate the virtual environment:

```bash
> source ./venv/bin/activate
```

To run the code:

```bash
> python ./src/main.py
```

or

```bash
make run
```

## Features

The solar system has the following components

### Models

All models are textured.

* **Sun:** Stationary at postion $(0,0,0)$ but rotates on its axis counterclockwise.
* **8 Planets:**
  * All planets orbiting around the sun in a counterclockwise direction.
  * Each planet axis is tilted at different angles.
  * The planets rotate and revolve at different speeds.
* **Moon:** Orbits around the earth. Also tilted and rotate on its own axis.
* **Stars:** To represent the surroundings using cubemap.

### Light

* The main light source is the sun.
* There is moving light on top of the models which rotates about the $y$-axis.

### Key Controls

* `SPACE`: Play or pause
* `KEY_UP`: Increase speed
* `KEY_DOWN`: Decrease speed
* `CTRL + KEY_UP`: Zoom in
* `CTRL + KEY_DOWN`: Zoom out
* `X`: Rotate camera about $x$-axis clockwise
* `CTRL + X`: Rotate camera about $x$-axis counterclockwise
* `Y`: Rotate camera about $y$-axis clockwise
* `CTRL + Y`: Rotate camera about $y$-axis counterclockwise
* `Z`: Rotate camera about $z$-axis clockwise
* `CTRL + z`: Rotate camera about $z$-axis counterclockwise
