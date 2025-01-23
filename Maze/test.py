from stable_baselines3.common.policies import MlpPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO

import numpy as np
from gym.envs import MazeEnv

#Start the Simulation
world = np.array([[1, 0, 0, 0, 0, 2, 0],
                  [0, 0, 3, 0, 0, 0, 0],
                  [4, 0, 0, 0, 0, 4, 0],
                  [0, 0, 3, 3, 0, 0, 0],
                  [0, 3, 0, 5, 0, 3, 0]])

