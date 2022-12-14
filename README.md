# JSBGym
[![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Current Progress

**Some features will not work properly yet, as gym in being converted to gymnasium**

JSBGym provides reinforcement learning environments for the control of fixed-wing aircraft using the JSBSim flight dynamics model. JSBGym requires at least Python 3.7.

The package's environments implement the Farama-Foundation's Gymnasium interface allowing environments to be created and interacted with in the usual way.

## Setup

Firstly, follow the instructions on the [JSBSim](https://github.com/JSBSim-Team/jsbsim) repository to install JSBSim and its libraries.

Confirm that JSBSim is installed from the terminal:

Linux

```console
$ JSBSim --version
JSBSim Version: 1.0.0 Jul 16 2018 09:14:35
```

Windows

```console
$ cd <JSBSim Directory>
$ ./JSBSim --version
JSBSim Version: 1.1.13 [GitHub build 986/commit a09715f01b9e568ce75ca2635ba0a78ce57f7cdd] Dec  3 2022 12:21:06
```

And confirm that its Python library is correctly installed from a Python interpreter or IDE:

```python
import jsbsim
```

Make sure that JSBSim is installed into C:\JSBSim (That is the default location for JSBSim when installed)

Also install gymnasium and jsbgym

```console
pip install gymnasium, git+https://github.com/sryu1/jsbgym
```

## Getting Started

```python
import gymnasium as gym
import jsbsim
import jsbgym

env = gym.make(ENV_ID)
env.reset()
observation, reward, terminated, truncated, info = env.step(action)
```

JSBGym optionally provides 3D visualisation of controlled aircraft using the FlightGear simulator.

## Dependencies

* [JSBSim](https://github.com/JSBSim-Team/jsbsim) flight dynamics model, including the C++ and Python libraries
* FlightGear simulator (optional for visualisation)
* gymnasium, numpy, matplotlib

## Environments

JSBGym implements two tasks for controlling the altitude and heading of aircraft:

* **HeadingControlTask**: aircraft must fly in a straight line, maintaining its initial altitude and direction of travel (heading)
* **TurnHeadingControlTask**: aircraft must turn to face a random target heading while maintaining their initial altitude

The environment can be configured to use one of three aircraft:

* **Cessna172P** light aircraft
* **F15** fighter jet
* **A320** airliner

Environment ID strings are constructed as follows:

```python
f'JSBSim-{task}-{aircraft}-SHAPING_STANDARD-NoFG-v0'
```

For example, to fly a Cessna on the TurnHeadingControl task,

```python
env = gym.make('JSBSim-TurnHeadingControlTask-Cessna172P-Shaping.STANDARD-NoFG-v0')
```

## Visualisation

### 2D

A basic plot of agent actions and current state information can be using `human` render mode by calling `env.render()`.

```python
env = gym.make('JSBSim-TurnHeadingControlTask-Cessna172P-Shaping.STANDARD-NoFG-v0', render_mode="human")
env.reset()
env.render()
```

### 3D
Make sure the FlightGear bin directory is in PATH (Usually C:\Program Files\FlighGear 2020.3\bin)and there is a system variable called `FG_ROOT` with the FG data folder as it's value (Usually C:\Program Files\FlightGear 2020.3\data).
3D visualisation requires installation of the FlightGear simulator. Confirm it is runnable from terminal with:

```console
$ fgfs --version
FlightGear version: 2020.3.17
Revision: 54e774dc0f3d280266ed17f2593872d7bab79e2a
Build-Id: 340
Build-Type: Release
FG_ROOT=C:/Program Files/FlightGear 2020.3/data
FG_HOME=C:/Users/Noah Ryu/AppData/Roaming/flightgear.org
FG_SCENERY=C:/Users/Noah Ryu/FlightGear/Downloads/TerraSync;C:/Program Files/FlightGear 2020.3/data/Scenery
SimGear version: 2020.3.17
OSG version: 3.4.2
PLIB version: 185
```

Visualising with FlightGear requires the Gym to be created with a FlightGear-enabled environment ID by changing 'NoFG' -> 'FG'. For example,

```python
env = gym.make('JSBSim-TurnHeadingControlTask-Cessna172P-Shaping.STANDARD-FG-v0', render_mode="flightgear")
env.reset()
env.render()
```

Then, the first call to `env.render()` will launch FlightGear and begin visualisation.

## State and Action Space

JSBGym's environments have a continuous state and action space. The state is a 17-tuple:

```python
(name='position/h-sl-ft', description='altitude above mean sea level [ft]', min=-1400, max=85000)
(name='attitude/pitch-rad', description='pitch [rad]', min=-1.5707963267948966, max=1.5707963267948966)
(name='attitude/roll-rad', description='roll [rad]', min=-3.141592653589793, max=3.141592653589793)
(name='velocities/u-fps', description='body frame x-axis velocity [ft/s]', min=-2200, max=2200)
(name='velocities/v-fps', description='body frame y-axis velocity [ft/s]', min=-2200, max=2200)
(name='velocities/w-fps', description='body frame z-axis velocity [ft/s]', min=-2200, max=2200)
(name='velocities/p-rad_sec', description='roll rate [rad/s]', min=-6.283185307179586, max=6.283185307179586)
(name='velocities/q-rad_sec', description='pitch rate [rad/s]', min=-6.283185307179586, max=6.283185307179586)
(name='velocities/r-rad_sec', description='yaw rate [rad/s]', min=-6.283185307179586, max=6.283185307179586)
(name='fcs/left-aileron-pos-norm', description='left aileron position, normalised', min=-1, max=1)
(name='fcs/right-aileron-pos-norm', description='right aileron position, normalised', min=-1, max=1)
(name='fcs/elevator-pos-norm', description='elevator position, normalised', min=-1, max=1)
(name='fcs/rudder-pos-norm', description='rudder position, normalised', min=-1, max=1)
(name='error/altitude-error-ft', description='error to desired altitude [ft]', min=-1400, max=85000)
(name='aero/beta-deg', description='sideslip [deg]', min=-180, max=180)
(name='error/track-error-deg', description='error to desired track [deg]', min=-180, max=180)
(name='info/steps_left', description='steps remaining in episode', min=0, max=300)
 ```

 Actions are 3-tuples of floats in the range [-1,+1] describing commands to move the aircraft's control surfaces (ailerons, elevator, rudder):

 ```python
 (name='fcs/aileron-cmd-norm', description='aileron commanded position, normalised', min=-1.0, max=1.0)
 (name='fcs/elevator-cmd-norm', description='elevator commanded position, normalised', min=-1.0, max=1.0)
 (name='fcs/rudder-cmd-norm', description='rudder commanded position, normalised', min=-1.0, max=1.0)
 ```
