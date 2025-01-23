from MazeEnv import MazeEnv
from IPython.display import clear_output
from time import sleep
import numpy as np
import random
import tqdm
import joblib
tqdm.monitor_interval = 0


# Create a Random Policy
def create_random_policy(env):
    policy = {}
    for key in range(0, env.observation_space.n):
        p = {}
        for action in range(0, env.action_space.n):
            p[action] = 1 / env.action_space.n
        policy[key] = p
    return policy


# Dictionary for Storing the Action Value
def create_state_action_dictionary(env, policy):
    Q = {}
    for key in policy.keys():
        Q[key] = {a: 0.0 for a in range(0, env.action_space.n)}
    return Q


# Function for running the Environment
def run_game(env, policy, display=True):
    env.reset()
    episode = []
    finished = False

    while not finished:
        s = int(env.state)
        if display:
            clear_output(True)
            env.render()
            sleep(1)

        timestep = []
        timestep.append(s)
        n = random.uniform(0, sum(policy[s].values()))
        top_range = 0
        for prob in policy[s].items():
            top_range += prob[1]
            if n < top_range:
                action = prob[0]
                break
        state, reward, finished, info = env.step(action)
        print(f"Reward for this action: {reward}")
        timestep.append(action)
        timestep.append(reward)

        episode.append(timestep)

    if display:
        clear_output(True)
        env.render()
        sleep(1)
    return episode


# Function to test policy and print Win Percentage
def test_policy(policy, env):
    wins = 0
    r = 10
    for i in range(r):
        w = run_game(env, policy, display=False)[-1][-1]
        if w == 2:
            wins += 1
    return wins / r


# First Visit Monte Carlo Policy
'''
This will provide a non zero probability to all possible actions;
this will ensure that new states will be created and thus 
more environment exploration
'''


def monte_carlo_e_soft(env, episodes=100, policy=None, epsilon=0.01):
    if not policy:
        # Create an empty dictionary to store state action values
        policy = create_random_policy(env)
    # Empty dictionary for storing rewards for each state-action pair
    Q = create_state_action_dictionary(env, policy)
    returns = {}  # 3.

    # Looping through episodes
    for i in range(episodes):
        # Store cumulative reward (initialized at 0)
        cumulative_Reward = 0
        # Store state, action and value respectively
        episode = run_game(env=env, policy=policy, display=False)

        '''
        Loop through the episode array in reverse so that the eventual reward will be at the end
        by going back from the last timestep to the first one propagating the result from the future
        '''

        for i in reversed(range(0, len(episode))):
            state, action, reward = episode[i]
            state_action = (state, action)
            # Increment total reward by reward on current timestep
            cumulative_Reward += reward

            if not state_action in [(x[0], x[1]) for x in episode[0:i]]:  #
                if returns.get(state_action):
                    returns[state_action].append(cumulative_Reward)
                else:
                    returns[state_action] = [cumulative_Reward]

                Q[state][action] = sum(returns[state_action]) / len(returns[state_action])  # Average reward across episodes

                Q_list = list(map(lambda x: x[1], Q[state].items()))  # Finding the action with maximum value
                indices = [i for i, x in enumerate(Q_list) if x == max(Q_list)]
                max_Q = random.choice(indices)

                A_star = max_Q  # 14.

                # Update action probability for a given state in the policy
                for a in policy[state].items():
                    if a[0] == A_star:
                        policy[state][a[0]] = (1 - epsilon) + (epsilon / abs(sum(policy[state].values())))
                        #policy[state][a[0]] = 1 - epsilon + (epsilon / abs(sum(policy[state].values()))
                    else:
                        policy[state][a[0]] = (epsilon / abs(sum(policy[state].values())))
                    print(f"Prob for state {state} given action {a[0]}: {a}")
    return policy

'''
Create the
'''
# Practice Map
world = np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, 1, 0, 0, 0, 0, 2, 0, -1],
                  [-1, 0, 0, 12, 0, 0, 0, 0, -1],
                  [-1, 0, 0, 0, 0, 0, 0, 0, -1],
                  [-1, 0, 0, 12, 12, 0, 0, 0, -1],
                  [-1, 0, 12, 0, 0, 0, 12, 0, -1],
                  [-1, -1, -1, 13, -1, -1, -1, -1, -1]])

# CSGO Dusk 2
World2 = [
    "BBB******************BBBBBB"
    "B*BBBBBBBBBBBBBBBBBBB*****B",
    "B***********************3*B",
    "B**BBBBBBBB***BBBBBBB*BBB*x",
    "B*B*******B***B*****B*B*B*x",
    "B*BBBBBBBBB***BBBBBBB*B*B*x",
    "B*********************B*B*x",
    "BB*BBBB*******BBBBBBBBBB**x",
    "B***BBB******B*******B****x",
    "X*****Bxxxxx*BBBBBBBBB*B**x",
    "X***********5**********BBBB",
    "Xxxxxxxxxxxx5xxxxxxxxxxxxxx"
]
# 10x25, can change to 20x20
world2 = np.array(
    [
        [-1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1],
        [-1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1],
        [-1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, -1],
        [-1, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, 0, -1],
        [-1, 0, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0, -1, 0, -1, 0, -1, 0, -1],
        [-1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, -1],
        [-1, -1, 0, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, -1],
        [-1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1],
        [-1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    ]
)
# COD 4 Modern Warfare KillingHouse
World3 = [
    "XXXXXXXXXXX",
    "X000000000X",
    "XXX000000XX",
    "X0000XX000X",
    "X000XXXX00X",
    "XX000000X0X",
    "X0330000X0X",
    "X0033000X0X",
    "X000000000X",
    "XXX00XXX00X",
    "X000000000X",
    "XXXXXXXXXXX"
]
# KillingHouse 10x10
world3 = np.array([
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, -1, -1, 0, 0, 0, 0, 0, 0, 0, -1, -1],
    [-1, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, -1, -1, -1, -1, 0, 0, 0, -1],
    [-1, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1],
    [-1, 0, 12, 12, 0, 0, 0, 0, 0, -1, 0, -1],
    [-1, 0, 0, 12, 12, 0, 0, 0, 0, -1, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, -1, -1, 0, 0, 0, -1, -1, -1, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
])

# Halo 3 SandTrap (15x15)
World4 = [
    "XXXXXXXXXXXXXXXX",
    "X---XXXXXXX----X",
    "X-X-X-X-X-X--X-X",
    "X-----X-X------X",
    "X--------------X",
    "X-X-XXX-X----X-X",
    "X-X-X-X-X------X",
    "X-X-X-X-X------X",
    "X-X-X-X-X------X",
    "X-X-XXX-X------X",
    "X-X-----X----X-X",
    "X-X-XXX-X------X",
    "X--------------X",
    "X--------------X",
    "X-----X--X-----X",
    "XXXXXXXXXXXXXXXX"
]

world4 = np.array([
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 0, 1, 0, -1, -1, -1, -1, -1, -1, -1, 0, 2, 0, 0, -1],
    [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, 0, -1, 0, -1],
    [-1, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, -1, 0, -1, -1, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1],
    [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, 0, 12, 0, 0, 0, -1],
    [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, -1, 0, -1, -1, -1, 0, -1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, -1, 0, 0, 0, 12, 0, -1, 0, 0, 0, 0, -1, 0, -1],
    [-1, 0, -1, 0, -1, -1, -1, 0, -1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
])
# Battlefield 4  Golmund Railway (20x20)
World5 = [
    "000XXXXXXXXXX000000000",

    "00X000000000X0000000000",
    "00X00000000000X0000000",
    "00X000000000000X000000",
    "00X0000000000000X00000",
    "00X00000000000000X0000",
    "00X000000000000000X000",
    "00X0000000000000000X00",
    "00X00000000000000000X0",
    "00X00000000000000000X0",
    "0X000000000000000000X0",
    "0X000000000000000000X0",
    "X00000000000000000000X",
    "X00000000000000000000X",
    "0X000000000000000000X0",
    "0X00000000000000000X00",
    "00X000000000000000X000",
    "000X000000000000XX0000",
    "00000X000000000X000000",
    "0000000X000000X0000000",

    "00000000XXXXXX00000000"
]
world5 = np.array(
    [
        [0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, -1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
        [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
        [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
        [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
        [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
        [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
        [0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 13, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 13, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
# Create the new environment and test the policy
env = MazeEnv(world)
policy = monte_carlo_e_soft(env)
filename = 'trial/policy1.sav'
joblib.dump(policy, filename)
percent = test_policy(policy, env)
print(f"Win Percentage: {percent}")