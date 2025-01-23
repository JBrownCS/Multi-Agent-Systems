#Launch the Simulation
import numpy as np

from stable_baselines.common.env_checker import check_env
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.ppo2 import  PPO2

from MazeGame import MazeEnv

'''
maze can be changed to add apples to find
'''
world = np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, 1, 0, 0, 0, 0, 2, 0, -1],
                      [-1, 0, 0, 3, 0, 0, 0, 0, -1],
                      [-1, 4, 0, 0, 0, 0, 4, 0, -1],
                      [-1, 0, 0, 3, 3, 0, 0, 0, -1],
                      [-1, 0, 3, 0, 5, 0, 3, 0, -1],
                      [-1, -1, -1,  5, -1, -1, -1, -1, -1]])


env = DummyVecEnv([lambda: MazeEnv(world)])

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10000)


'''
#Create the model
env = DummyVecEnv([lambda: MazeEnv(world)])
model = PPO2(MlpPolicy, env, learning_rate=0.001)
model.learn(500000)
'''

'''
#Create the new environment
env = MazeEnv(world)
check_env(env)
'''

numTotalEpisodes = 10

for i in range(300):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action, _state = model.predict(state)
        observation,reward,done,n_state = env.step(action)
        score+=reward
    print(f"Episode:{env.current_episode} Score:{score}")

#env.on_cleanup()
