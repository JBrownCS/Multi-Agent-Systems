# Discrete allows us to define how many actions can occur in the space
# Box allows us to record the state of the space
# Turtle is for drawing each step of the environment
import numpy as np
from gym import Env
from gym.spaces import Discrete, Box
import turtle

# Define the possible actions of the maze
BACKWARD = 0
RIGHT = 1
FORWARD = 2
LEFT = 3
# Teleport other agent
TELEPORT = 4

# Define the possible maze values for visualization
WALL = -1
SPACE = 0
numOfAgents = 2
TRAP = 12
AGENTS = range(1, numOfAgents + 1)
GOAL = 13


class MazeEnv(Env):
    '''

    """
    Agents move throughout a maze environment

    ### Action Space
    The agent takes a 1-element vector for actions.
    The action space is `(dir)`, where `dir` decides direction to move in which can be:
    - 0: LEFT
    - 1: DOWN
    - 2: RIGHT
    - 3: UP
    - 4: TELEPORT (move another agent 3 spaces forward)
    ### Observation Space
    The observation is a value representing the agent's current position as
    current_row * nrows + current_col (where both the row and col start at 0).
    For example, the goal position in the 4x4 map can be calculated as follows: 3 * 4 + 3 = 15.
    The number of possible observations is dependent on the size of the map.
    For example, the 5x5 map has 25 possible observations.
    ### Rewards
    Reward schedule:
    - Reach goal(14): +100
    - Reach trap(13): -100
    - Reach Empty Space: -2 per step to incentivize exiting faster

    #### Environment States
    - Playable = 0
    - Success = 1
    - Failure = 2
    '''

    # Constructor
    def __init__(self, world):
        self.world_start = world
        # Set number of actions (LEFT, RIGHT, UP, DOWN, TELEPORT OTHER AGENT)
        self.action_space = Discrete(5)

        shape_0 = np.size(self.world_start, 0)
        shape_1 = np.size(self.world_start, 1)
        # The observation space of the maze
        self.observation_space = Discrete(
            np.size(self.world_start, 0) * np.size(self.world_start, 1)
        )
        self.reward_range = (-200, 200)

        # Initialize the current agent, world, and state of the world
        self.current_agent = 1
        self.world = np.copy(self.world_start)
        self.state = '0'
        self.current_step = 0
        self.max_step = 50
        self.exploration_prize = None
        self.bonus_reward = 0
        self.current_episode = 0
        self.success_episode = []

        # Initialize the Visualization window and turtle drawing it
        # Maze Window
        self.window = turtle.Screen()
        self.bgcolor = "light blue"
        self.window.bgcolor(self.bgcolor)
        self.window.title("Multi Agent Maze")
        self.window.setup(800, 650)
        self.window.tracer(0, 0)
        self.pen = turtle.Turtle()
        self.pen.color("white")
        self.pen.penup()
        self.pen.speed(0)

    # Get current Episode number
    def getEpisodeNumber(self):
        return self.current_episode

    # Draw the maze on the turtle screen
    def drawMaze(self, maze):
        # Define x and y coordinates
        for y in range(np.size(maze, 0)):
            for x in range(np.size(maze, 1)):
                # Get the character from the x and y value
                value = maze[y, x]
                # Get screen coordinates
                screen_x = -288 + (x * 25)
                screen_y = 288 - (y * 25)

                # If there is an empty space (0)
                if value == WALL:
                    self.pen.shape("square")
                    self.pen.color("white")
                    self.pen.goto(screen_x, screen_y)
                    self.pen.stamp()

                if value == SPACE:
                    self.pen.shape("square")
                    self.pen.color(self.bgcolor)
                    self.pen.goto(screen_x, screen_y)
                    self.pen.stamp()

                if value in AGENTS:
                    self.pen.shape("turtle")
                    self.pen.color("blue")
                    self.pen.goto(screen_x, screen_y)
                    self.pen.stamp()
                if value == TRAP:
                    self.pen.shape("circle")
                    self.pen.color("red")
                    self.pen.goto(screen_x, screen_y)
                    self.pen.stamp()

                if value == GOAL:
                    self.pen.color("green")  # change to (self.bgcolor)
                    self.pen.goto(screen_x, screen_y)
                    self.pen.begin_fill()
                    self.pen.pendown()
                    for i in range(5):
                        self.pen.forward(17)
                        self.pen.right(144)
                    self.pen.end_fill()
                    self.pen.penup()
        self.window.update()

    # Function to teleport agents
    def teleportAgent(self, current_agent):
        pass

    # Function to move the current agent about the maze
    def moveAgent(self, action):
        # Current position[0] = x, current_pos[1] = y
        current_pos = np.where(self.world == self.current_agent)

        # If the agent goes backward
        if action == BACKWARD:
            print(f"Agent {self.current_agent} is going Backwards")
            new_pos = (current_pos[0] - 1, current_pos[1])
            # Making sure the agent does not go out of bounds so newpos[0] must be > 0

            # If the other agent is in the next position, don't move
            if new_pos[0] > SPACE and int(self.world[new_pos]) in AGENTS:
                new_pos = (current_pos[0], current_pos[1])

            # If the agent hits a wall, don't move
            if new_pos[0] > SPACE and int(self.world[new_pos]) == WALL:
                new_pos = (current_pos[0], current_pos[1])

            # If the agent hits a wall, don't move
            if new_pos[0] < 1:
                new_pos = (current_pos[0], current_pos[1])

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[0] >= SPACE and int(self.world[new_pos]) == SPACE:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                # Reward Exploration
                self._exploration_prize(new_pos)
            # If the space is a trap (3), end the game
            if new_pos[0] >= SPACE and int(self.world[new_pos]) == TRAP:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = '1'
                # Reward Exploration
                self._exploration_prize(new_pos)
            if new_pos[0] >= SPACE and int(self.world[new_pos]) in AGENTS:
                self.world[new_pos] = self.current_agent

            # If the agent reaches the goal
            elif new_pos[0] >= SPACE and (int(self.world[new_pos]) == GOAL):
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = '2'
                self._exploration_prize(new_pos)

        # If the agent goes right
        if action == RIGHT:
            print(f"Agent {self.current_agent} is going Right")
            new_pos = (current_pos[0], current_pos[1] + 1)
            limit = np.size(self.world, 1)

            # Making sure the agent does not go out of bounds so newpos[0] must be < max width of maze

            # If the other agent is in the next position, don't move
            if new_pos[1] < limit and int(self.world[new_pos[0], new_pos[1]]) in AGENTS:
                pass

            # If there is a wall, the agent does not move
            if new_pos[1] < limit and int(self.world[new_pos[0], new_pos[1]]) == WALL:
                pass

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[1] < limit and int(self.world[new_pos[0], new_pos[1]]) == SPACE:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                # Reward Exploration
                self._exploration_prize(new_pos)

            # If the space is a trap (3), end the game
            if new_pos[1] < limit and int(self.world[new_pos[0], new_pos[1]]) == TRAP:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = '1'
                # Reward Exploration
                self._exploration_prize(new_pos)


            # If the agent reaches the goal(5) End the game
            elif new_pos[1] < limit and int(self.world[new_pos[0], new_pos[1]]) == GOAL:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = '2'
                # Reward Exploration
                self._exploration_prize(new_pos)

        # If the agent goes forward
        if action == FORWARD:
            print(f"Agent {self.current_agent} is going Forward")
            new_pos = (current_pos[0] + 1, current_pos[1])
            limit = np.size(self.world, 0) - 1

            # Making sure the agent does not go out of bounds so newpos[0] must be > 0

            # If the other agent is in the next position, don't move
            if new_pos[0] < limit and int(self.world[new_pos[0], new_pos[1]]) in AGENTS:
                pass

            # If there is a wall then the agent does not move
            if (new_pos[0] < limit and int(self.world[new_pos[0], new_pos[1]]) == WALL) or new_pos[0] == limit:
                pass

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[0] < limit and int(self.world[new_pos[0], new_pos[1]]) == SPACE:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                # Reward Exploration
                self._exploration_prize(new_pos)

            # If the space is a trap (3), end the game
            if new_pos[0] < limit and int(self.world[new_pos[0], new_pos[1]]) == TRAP:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = '1'
                # Reward Exploration
                self._exploration_prize(new_pos)


            # If the agent reaches the goal End the game
            elif new_pos[0] < limit and int(self.world[new_pos[0], new_pos[1]]) == GOAL:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = '2'
                # Reward Exploration
                self._exploration_prize(new_pos)

        # If the agent goes left
        if action == LEFT:
            print(f"Agent {self.current_agent} is going Left")
            new_pos = (current_pos[0], current_pos[1] - 1)

            # Making sure the agent does not go out of bounds so newpos[0] must be > 0

            # If the other agent is in the next position, don't move
            if new_pos[1] >= SPACE and int(self.world[new_pos[0], new_pos[1]]) in AGENTS:
                pass

            # If there is a wall, then the agent does not move
            if new_pos[1] >= SPACE and int(self.world[new_pos[0], new_pos[1]]) == WALL:
                pass

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[1] >= SPACE and int(self.world[new_pos[0], new_pos[1]]) == SPACE:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                # Reward Exploration
                self._exploration_prize(new_pos)
            # If the space is a trap (3), end the game
            if new_pos[1] >= SPACE and int(self.world[new_pos[0], new_pos[1]]) == TRAP:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = '1'
                # Reward Exploration
                self._exploration_prize(new_pos)


            # If the agent reaches the goal
            elif new_pos[1] >= SPACE and (int(self.world[new_pos[0], new_pos[1]]) == GOAL):
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = '2'
                # Reward Exploration
                self._exploration_prize(new_pos)

        # Teleport the other agent
        if action == TELEPORT:

            # keep current position of current agent, move the other agent
            other_agent = (self.current_agent + 1) % (numOfAgents + 1)
            if other_agent == 0:
                other_agent = 1
            print(f"Agent {self.current_agent} is teleporting Agent {other_agent} forward")

            other_player_pos = np.where(self.world == other_agent)
            other_next_pos = (other_player_pos[0] + 3, other_player_pos[1])
            # Set the next position of the other agent

            # Set the next position of the other agent
            if other_next_pos[0] < np.size(self.world, 0) - 1:
                self.world[other_player_pos] = 0
            # Place the other agent in range if it teleports out of bounds
            else:
                print(int(other_next_pos.__getitem__(0)))
                while int(other_next_pos[0]) > np.size(self.world, axis=0) - 2:
                    other_next_pos = (other_next_pos[0] - 1, other_next_pos[1])
                self.world[other_player_pos] = 0
            # Check if the other agent teleports into a trap or the goal
            # Otherwise the maze is still playable
            if int(self.world[other_next_pos]) == 12:
                self.state = '1'
            elif int(self.world[other_next_pos]) == 13:
                self.state = '2'
            else:
                self.state = '0'
            self.world[other_next_pos] = other_agent
            # Reward Exploration
            self._exploration_prize(other_next_pos)

    # Function to perform each action per timestep
    def step(self, action):
        '''

        :param action: A given action the agent takes (0,1,2,3)
        -Determine what happens after the action is taken
        -Increase number of steps taken
        -Print the world with the updated agent location
        '''
        print(f"Step {self.current_step}")
        self.moveAgent(action)
        self.current_step += 1
        print(self.world)
        print(self.exploration_prize)
        self.drawMaze(self.world)
        print()

        # Reward Assignment
        if self.state == "2":
            print(f'Agent {self.current_agent} found the exit')
            reward = 100 * (1 + 1 / self.current_step)
            done = True
        elif self.state == '1':
            print(f'Agent {self.current_agent} fell into a trap')
            reward = -200
            done = True
        elif self.state == '0':
            reward = -2
            done = False

        # Have new episodes be created
        if self.current_step >= self.max_step:
            print(f'New episode number {self.current_episode + 1}')
            done = True

        # Switch the agent turns
        new_agent = (self.current_agent + 1) % (numOfAgents + 1)
        if new_agent == 0:
            new_agent = 1
        self.current_agent = new_agent

        # Apply the bonus reward for this step then reset him to 0
        reward += self.bonus_reward
        print(f"Reward for this step is {reward}")
        self.bonus_reward = 0

        if done:
            self.render(self.state)
            self.current_episode += 1
            self.window.title(f"Multi Agent Maze --- Episode{self.current_episode + 1}")

        obs = self.createObservation()

        return int(self.state), reward, done, obs

    # Render the environment
    def render(self, state):
        # Add a successfull episode
        self.success_episode.append(
            'Success' if state == '2' else 'Failure')

        file = open('trial/render.txt', 'a')
        file.write('----------------------------\n')
        file.write(f'Episode number {self.current_episode}\n')
        file.write(
            f'{self.success_episode[-1]} in {self.current_step} steps\n')
        file.close()

    # Function that resets the environment
    def reset(self):
        self.pen.clear()
        self.current_agent = 1
        # P means the game is playable, W means somenone wins, L someone lose
        self.state = '0'
        self.current_step = 0
        if np.size(self.world, 0) * np.size(self.world, 1) < 100:
            self.max_step = 30
        else:
            self.max_step = 40
        self.world = np.copy(self.world_start)

        self.exploration_prize = np.ones(
            shape=(np.size(self.world, 0),
                   np.size(self.world, 1))
        )

        self.bonus_reward = 0

        return self.createObservation()

    # Create observations for further analysis
    def createObservation(self):
        observation = self.world

        # Numpy.size(array, axis value)
        data_to_add = [0] * np.size(self.world, 1)
        data_to_add[0] = self.current_agent

        observation = np.append(observation, [data_to_add], axis=0)

        return observation

    def _exploration_prize(self, next_pos):
        """
        Incentive mechanism for exploration.
        :param next_pos (int):
        """
        if self.exploration_prize[next_pos] == 1:
            self.exploration_prize[next_pos] = 0
            self.bonus_reward += 1


if __name__ == "__main__":
    # Practice Map
    world1 = np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                       [-1, 1, 0, 0, 0, 0, 2, 0, -1],
                       [-1, 0, 0, 12, 0, 0, 0, 0, -1],
                       [-1, 0, 0, 0, 0, 0, 0, 0, -1],
                       [-1, 0, 0, 12, 12, 0, 0, 0, -1],
                       [-1, 0, 12, 0, 13, 0, 12, 0, -1],
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
    # Create the new environment
    env = MazeEnv(world1)
    numTotalEpisodes = 3

    while env.current_episode < numTotalEpisodes:
        state = env.reset()
        done = False
        score = 0

        while not done:
            action = env.action_space.sample()
            observation, reward, done, n_state = env.step(action)
            score += reward
        print(f"Episode:{env.current_episode} Score:{score}")
