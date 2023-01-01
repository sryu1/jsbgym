import gymnasium as gym
import numpy as np
from jsbgym.tasks import Shaping, HeadingControlTask
from jsbgym.simulation import Simulation
from jsbgym.visualiser import FigureVisualiser, FlightGearVisualiser
from jsbgym.aircraft import Aircraft, cessna172P
from typing import Optional, Type, Tuple, Dict


class JsbSimEnv(gym.Env):
    """
    A class wrapping the JSBSim flight dynamics module (FDM) for simulating
    aircraft as an RL environment conforming to the Gymnasium Env
    interface.

    An JsbSimEnv is instantiated with a Task that implements a specific
    aircraft control task with its own specific observation/action space and
    variables and agent_reward calculation.

    ATTRIBUTION: this class implements the Gymnasium Env API. Method
    docstrings have been adapted or copied from the Gymnasium source code.
    """

    JSBSIM_DT_HZ: int = 60  # JSBSim integration frequency
    metadata = {"render_modes": ["human", "flightgear"], "render_fps": 30}

    def __init__(
        self,
        task_type: Type[HeadingControlTask],
        aircraft: Aircraft = cessna172P,
        agent_interaction_freq: int = 5,
        shaping: Shaping = Shaping.STANDARD,
        render_mode: Optional[str] = None,
    ):
        self.render_mode = render_mode
        """
        Constructor. Inits some internal state, but JsbSimEnv.reset() must be
        called first before interacting with environment.

        :param task_type: the Task subclass for the task agent is to perform
        :param aircraft: the JSBSim aircraft to be used
        :param agent_interaction_freq: int, how many times per second the agent
            should interact with environment.
        :param shaping: a HeadingControlTask.Shaping enum, what type of agent_reward
            shaping to use (see HeadingControlTask for options)
        """
        if agent_interaction_freq > self.JSBSIM_DT_HZ:
            raise ValueError(
                "agent interaction frequency must be less than "
                "or equal to JSBSim integration frequency of "
                f"{self.JSBSIM_DT_HZ} Hz."
            )
        self.sim: Simulation = None
        self.sim_steps_per_agent_step: int = self.JSBSIM_DT_HZ // agent_interaction_freq
        self.aircraft = aircraft
        self.task = task_type(shaping, agent_interaction_freq, aircraft)
        # set Space objects
        self.observation_space: gym.spaces.Box = self.task.get_state_space()
        self.action_space: gym.spaces.Box = self.task.get_action_space()
        # set visualisation objects
        self.figure_visualiser: FigureVisualiser = None
        self.flightgear_visualiser: FlightGearVisualiser = None
        self.step_delay = None

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, Dict]:
        if self.render_mode == "human":
            self.render()
        """
        Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).

        :param action: the agent's action, with same length as action variables.
        :return:
            state: agent's observation of the current environment
            reward: amount of reward returned after previous action
            done: whether the episode has ended, in which case further step() calls are undefined
            info: auxiliary information, e.g. full reward shaping data
        """
        if action.shape != self.action_space.shape:
            raise ValueError("mismatch between action and action space size")

        state, reward, done, info = self.task.step(self.sim, action)

        for _ in range(self.sim_steps_per_agent_step):
            self.sim.run_one_step()

        return state, reward, done, info

    def reset(self, seed: Optional[int] = None) -> np.ndarray:
        """
        Reset the state of the environment and returns an initial observation.

        :param seed: int, seed for the random number generator
        """
        dt = 1 / self.JSBSIM_DT_HZ
        initial_conditions = self.task.get_initial_conditions()
        self.sim = self._init_new_sim(dt, self.aircraft, initial_conditions, seed)
        self.figure_visualiser = FigureVisualiser(
            dt=dt, aircraft=self.aircraft, sim=self.sim
        )
        self.flightgear_visualiser = FlightGearVisualiser(
            dt=dt, aircraft=self.aircraft, sim=self.sim
        )
        return self.task.get_initial_state(self.sim)

    def render(self, flightgear_blocking=True):
        mode = self.render_mode
        if mode == "flightgear":
            self.flightgear_visualiser.run_one_step(blocking=flightgear_blocking)
        elif mode == "human":
            self.figure_visualiser.run_one_step()

    def close(self):
        if self.render_mode == "flightgear":
            self.flightgear_visualiser.close()
        elif self.render_mode == "human":
            self.figure_visualiser.close()

    def _init_new_sim(
        self,
        dt: float,
        aircraft: Aircraft,
        initial_conditions: Dict,
        seed: Optional[int] = None,
    ):
        return Simulation(
            sim_frequency_hz=dt,
            aircraft=aircraft,
            init_conditions=initial_conditions,
            seed=seed,
        )


class NoFGJsbSimEnv(JsbSimEnv):
    """
    An RL environment for JSBSim with rendering to FlightGear disabled.

    This class exists to be used for training agents where visualisation is not
    required. Otherwise, restrictions in JSBSim output initialisation cause it
    to open a new socket for every single episode, eventually leading to
    failure of the network.
    """

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def _init_new_sim(
        self,
        dt: float,
        aircraft: Aircraft,
        initial_conditions: Dict,
        seed: Optional[int] = None,
    ):
        return Simulation(
            sim_frequency_hz=dt,
            aircraft=aircraft,
            init_conditions=initial_conditions,
            allow_flightgear_output=False,
            seed=seed,
        )

    def render(self, flightgear_blocking=True):
        mode = self.render_mode
        if mode == "flightgear":
            raise ValueError("flightgear rendering is disabled for this class")
        else:
            super().render(flightgear_blocking)
