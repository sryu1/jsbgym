import gymnasium as gym
import enum
from jsbgym.tasks import Task, HeadingControlTask, TurnHeadingControlTask
from jsbgym.aircraft import Aircraft, c172
from jsbgym import utils

"""
This script registers all combinations of task, aircraft, shaping settings
 etc. with Farama Foundation Gymnasium so that they can be instantiated with a gym.make(id)
 command.

The jsbgym.Envs enum stores all registered environments as members with
 their gym id string as value. This allows convenient autocompletion and value
 safety. To use do:
       env = gym.make(jsbgym.Envs.desired_environment.value)
"""

for env_id, (
    plane,
    task,
    shaping,
    enable_flightgear,
) in utils.get_env_id_kwargs_map().items():
    if enable_flightgear:
        entry_point = "jsbgym.environment:JsbSimEnv"
    else:
        entry_point = "jsbgym.environment:NoFGJsbSimEnv"
    kwargs = dict(aircraft=plane, task_type=task, shaping=shaping)
    gym.envs.registration.register(id=env_id, entry_point=entry_point, kwargs=kwargs)
