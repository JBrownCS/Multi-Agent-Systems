# Discrete allows us to define how many actions can occur in the space
# Box allows us to record the state of the space
#Turtle is for drawing each step of the environment
import numpy as np
from gym import Env
from gym.spaces import Discrete, Box
import turtle

# Define the possible actions of the maze
BACKWARD = 0
RIGHT = 1
FORWARD = 2
LEFT = 3

# Define the possible maze values for visualization
WALL = -1
SPACE = 0
numOfAgents = 2
TRAP = 3
AGENTS = range(1, numOfAgents + 1)
TELEPORTER = 4
GOAL = 5


class MazeEnv(Env):
    # Constructor
    def __init__(self, world):
        self.world_start = world
        # Set number of actions (LEFT, RIGHT, UP, DOWN)
        self.action_space = Discrete(4)

        shape_0 = np.size(self.world_start, 0)
        shape_1 = np.size(self.world_start, 1)
        # The observation space of the maze
        self.observation_space = Box(low=0,
                                     high=5,
                                     shape=(shape_0 + 1, shape_1),
                                     dtype=np.int16)
        self.reward_range = (-200, 200)

        # Initialize the current agent, world, and state of the world
        self.current_agent = 1
        self.world = np.copy(self.world_start)
        self.state = 'P'
        self.current_step = 0
        self.max_step = 50

        self.current_episode = 0
        self.success_episode = []

        # Initialize the Visualization window and turtle drawing it
        # Maze Window
        self.window = turtle.Screen()
        self.bgcolor = "black"
        self.window.bgcolor(self.bgcolor)
        self.window.title("Multi Agent Maze")
        self.window.setup(700, 650)
        self.pen = turtle.Turtle()
        self.pen.color("white")
        self.pen.penup()
        self.pen.speed(0)

    # Draw the maze on the turtle screen
    def drawMaze(self, maze):
        # Define x and y coordinates
        for y in range(np.size(maze, 0)):
            for x in range(np.size(maze, 1)):
                # Get the character from the x and y value
                value = maze[y, x]
                # Get screen coordinates
                screen_x = -288 + (x * 30)
                screen_y = 288 - (y * 30)

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
                if value == TELEPORTER:
                    self.pen.shape("arrow")
                    self.pen.color("orange")
                    self.pen.goto(screen_x, screen_y)
                    self.pen.stamp()
                if value == GOAL:
                    self.pen.shape("square")
                    self.pen.color(self.bgcolor)
                    self.pen.goto(screen_x, screen_y)
                    self.pen.stamp()

    # Function to move the current agent about the maze
    def moveAgent(self, action):
        # Current position[0] = x, current_pos[1] = y
        current_pos = np.where(self.world == self.current_agent)

        # If the agent goes backward
        if action == BACKWARD:
            new_pos = (current_pos[0] - 1, current_pos[1])

            # Making sure the agent does not go out of bounds so newpos[0] must be > 0

            # If the other agent is in the next position, don't move
            if new_pos[0] >= SPACE and int(self.world[new_pos]) in AGENTS:
                pass

            # If the other agent is in the next position, don't move
            if new_pos[0] >= SPACE and int(self.world[new_pos]) == WALL:
                pass

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[0] > SPACE and int(self.world[new_pos]) == SPACE:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                '''Implement This Later: self._exploration_prize(next_pos)'''
            # If the space is a trap (3), end the game
            if new_pos[0] >= SPACE and int(self.world[new_pos]) == TRAP:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = 'Failed'
                '''Implement This Later: self._exploration_prize(next_pos)'''

            # If the space is a teleporter
            elif new_pos[0] >= SPACE and int(self.world[new_pos] == TELEPORTER):
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE

                # Teleport the other agent
                other_agent = 2 if self.current_agent == 1 else 1
                other_player_pos = np.where(self.world == other_agent)
                other_next_pos = (other_player_pos[0] + 3, other_player_pos[1])
                # If the next position of the other agent
                if other_next_pos[0] < np.size(self.world, 0):
                    self.world[other_next_pos] = other_agent
                    self.world[other_player_pos] = SPACE

                self.state = 'P'
                '''Implement This Later: self._exploration_prize(next_pos)'''

            # If the agent reaches the goal
            elif new_pos[0] >= SPACE and (int(self.world[new_pos]) == GOAL):
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = 'Succeeded'
                self._exploration_prize(new_pos)

        # If the agent goes right
        if action == RIGHT:
            new_pos = (current_pos[0], current_pos[1] + 1)
            print(f"New X: {new_pos[0]}, New Y:{new_pos[1]}")
            limit = np.size(self.world, 1)

            # Making sure the agent does not go out of bounds so newpos[0] must be < max width of maze

            # If the other agent is in the next position, don't move
            if new_pos[1] < limit and int(self.world[new_pos]) in AGENTS:
                pass

            #If there is a wall, the agent does not move
            if new_pos[1] < limit and int(self.world[new_pos]) == WALL:
                pass

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[1] < limit and int(self.world[new_pos]) == SPACE:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                '''Implement This Later: self._exploration_prize(next_pos)'''

            # If the space is a trap (3), end the game
            if new_pos[1] < limit and int(self.world[new_pos]) == 3:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = 'Failed'
                '''Implement This Later: self._exploration_prize(next_pos)'''

            # If the space is a teleporter(4) move the other agent
            elif new_pos[1] < limit and int(self.world[new_pos] == TELEPORTER):
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE

                # Teleport the other agent
                other_agent = 2 if self.current_agent == 1 else 1
                other_player_pos = np.where(self.world == other_agent)
                other_next_pos = (other_player_pos[0] + 3, other_player_pos[1])
                # If the next position of the other agent
                if other_next_pos[0] < np.size(self.world, 0):
                    self.world[other_next_pos] = other_agent
                    self.world[other_player_pos] = SPACE

                    self.state = 'P'
                    '''Implement This Later: self._exploration_prize(next_pos)'''

            # If the agent reaches the goal(5) End the game
            elif new_pos[1] < limit and (int(self.world[new_pos]) == GOAL):
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = 'Succeeded'
                ''' Implement self._exploration_prize(new_pos) '''

        # If the agent goes forward
        if action == FORWARD:
            new_pos = (current_pos[0] + 1, current_pos[1])
            limit = np.size(self.world, 0)

            # Making sure the agent does not go out of bounds so newpos[0] must be > 0

            # If the other agent is in the next position, don't move
            if new_pos[0] < limit and int(self.world[new_pos]) in AGENTS:
                pass

            #If there is a wall then the agent does not move
            if new_pos[0] < limit and int(self.world[new_pos]) == WALL:
                pass

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[0] < limit and int(self.world[new_pos]) == SPACE:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                '''Implement This Later: self._exploration_prize(next_pos)'''

            # If the space is a trap (3), end the game
            if new_pos[0] < limit and int(self.world[new_pos]) == TRAP:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = 'Failed'
                '''Implement This Later: self._exploration_prize(next_pos)'''

            # If the space is a teleporter(4) move the other agent
            elif new_pos[0] < limit and int(self.world[new_pos] == TELEPORTER):
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE

                # Teleport the other agent
                other_agent = 2 if self.current_agent == 1 else 1
                other_player_pos = np.where(self.world == other_agent)
                other_next_pos = (other_player_pos[0] + 3, other_player_pos[1])
                # If the next position of the other agent
                if other_next_pos[0] < np.size(self.world, 0):
                    self.world[other_next_pos] = other_agent
                    self.world[other_player_pos] = SPACE

                    self.state = 'P'
                    '''Implement This Later: self._exploration_prize(next_pos)'''

                # If the agent reaches the goal(5) End the game
                elif new_pos[0] < limit and (int(self.world[new_pos]) == GOAL):
                    self.world[new_pos] = self.current_agent
                    self.world[current_pos] = SPACE
                    self.state = 'Succeeded'
                    '''Implement This Later: self._exploration_prize(next_pos)'''

        # If the agent goes backward
        if action == LEFT:
            new_pos = (current_pos[0], current_pos[1] - 1)

            # Making sure the agent does not go out of bounds so newpos[0] must be > 0

            # If the other agent is in the next position, don't move
            if new_pos[1] >= SPACE and int(self.world[new_pos]) in AGENTS:
                pass

            #If there is a wall, then the agent does not move
            if new_pos[1] >= SPACE and int(self.world[new_pos]) == WALL:
                pass

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[1] >= SPACE and int(self.world[new_pos]) == SPACE:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                '''Implement This Later: self._exploration_prize(next_pos)'''
            # If the space is a trap (3), end the game
            if new_pos[1] >= SPACE and int(self.world[new_pos]) == TRAP:
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = 'Failed'
                '''Implement This Later: self._exploration_prize(next_pos)'''

            # If the space is a teleporter
            elif new_pos[1] >= SPACE and int(self.world[new_pos] == TELEPORTER):
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE

                # Teleport the other agent
                other_agent = 2 if self.current_agent == 1 else 1
                other_player_pos = np.where(self.world == other_agent)
                other_next_pos = (other_player_pos[0] + 3, other_player_pos[1])
                # If the next position of the other agent
                if other_next_pos[0] < np.size(self.world, 0):
                    self.world[other_next_pos] = other_agent
                    self.world[other_player_pos] = SPACE

                self.state = 'P'
                '''Implement This Later: self._exploration_prize(next_pos)'''

            # If the agent reaches the goal
            elif new_pos[1] >= SPACE and (int(self.world[new_pos]) == GOAL):
                self.world[new_pos] = self.current_agent
                self.world[current_pos] = SPACE
                self.state = 'Succeeded'
                '''Implement This Later: self._exploration_prize(next_pos)'''

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
        self.drawMaze(self.world)
        print()

        # Reward Assignment
        if self.state == "Succeeded":
            print(f'Agent {self.current_agent} found the exit')
            reward = 100 * (1 + 1 / self.current_step)
            done = True
        elif self.state == 'Failed':
            print(f'Agent {self.current_agent} fell into a trap')
            reward = -200
            done = True
        elif self.state == 'P':
            reward = -2
            done = False

        # Have new episodes be created
        if self.current_step >= self.max_step:
            print(f'New episode number {self.current_episode + 1}')
            done = True

        # Switch the agent turns
        if self.current_agent == 1:
            self.current_agent = 2
        else:
            self.current_agent = 1

        # Apply the bonus reward for this step then reset him to 0
        reward += self.bonus_reward
        self.bonus_reward = 0

        if done:
            self.render(self.state)
            self.current_episode += 1
            self.window.title(f"Multi Agent Maze --- Episode{self.current_episode + 1}")

        obs = self.createObservation()

        return obs, reward, done, {'state': self.state}

    # Render the environment
    def render(self, state):
        # Add a successfull episode
        self.success_episode.append(
            'Success' if state == 'Succeeded' else 'Failure')

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
        self.state = 'P'
        self.current_step = 0
        self.max_step = 50
        self.world = np.copy(self.world_start)

        '''
        Implement This Later
        self.exploration_prize = np.ones(shape=(np.size(self.world, 0),
                                                np.size(self.world, 1)))
        '''
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


if __name__ == "__main__":
    world = np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, 1, 0, 0, 0, 0, 2, 0, -1],
                      [-1, 0, 0, 3, 0, 0, 0, 0, -1],
                      [-1, 4, 0, 0, 0, 0, 4, 0, -1],
                      [-1, 0, 0, 3, 3, 0, 0, 0, -1],
                      [-1, 0, 3, 0, 5, 0, 3, 0, -1],
                      [-1, -1, -1,  5, -1, -1, -1, -1, -1]])

    # Create the new environment
    env = MazeEnv(world)
    numTotalEpisodes = 20

    while env.current_episode < numTotalEpisodes:
        state = env.reset()
        done = False
        score = 0

        while not done:
            action = env.action_space.sample()
            observation, reward, done, n_state = env.step(action)
            score += reward
        print(f"Episode:{env.current_episode} Score:{score}")
