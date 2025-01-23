'''
Define the Agent Class for the Cooperative and Competitive Environments
'''


class Agent:
    def __init__(self):
        self.team = 0
        self.x = 0
        self.y = 0

    # Set up agent team
    def setTeam(self, team):
        self.team = team

    # def move
    def move(self, action):
        # Current position[0] = x, current_pos[1] = y
        current_pos = (agent.x, agent.y)

        # If the agent goes backward
        if action == BACKWARD:
            new_pos = (current_pos[0] - 1, current_pos[1])
            # Making sure the agent does not go out of bounds so newpos[0] must be > 0

            # If the other agent is in the next position, don't move
            if new_pos[0] > SPACE and int(self.world[new_pos]) in range(1, numOfAgents + 1):
                new_pos = (current_pos[0], current_pos[1])

            # If the agent hits a wall, don't move
            if new_pos[0] > SPACE and int(self.world[new_pos]) == WALL:
                new_pos = (current_pos[0], current_pos[1])

            # If the agent hits a wall, don't move
            if new_pos[0] < 1:
                new_pos = (current_pos[0], current_pos[1])

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[0] >= SPACE and int(self.world[new_pos]) == SPACE:
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                # Reward Exploration
                self._exploration_prize(new_pos)
            # If the space is a trap (3), end the game
            if new_pos[0] >= SPACE and int(self.world[new_pos]) == TRAP:
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                self.state = 'Failed'
                # Reward Exploration
                self._exploration_prize(new_pos)

            if new_pos[0] >= SPACE and agent.team == 1:
                self.world[new_pos] = agent.id
            if new_pos[0] >= SPACE and agent.team == 2:
                self.world[new_pos] = agent.id

            # If the agent reaches the goal
            elif new_pos[0] >= SPACE and (int(self.world[new_pos]) == GOAL):
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                self.state = 'Succeeded'
                if agent.team == 1:
                    self.team1Win = True
                else:
                    self.team1Win = False
                self._exploration_prize(new_pos)

        # If the agent goes right
        if action == RIGHT:
            new_pos = (agent.x, agent.y + 1)
            limit = np.size(self.world, 1)

            # Making sure the agent does not go out of bounds so newpos[0] must be < max width of maze

            # If the other agent is in the next position, don't move
            if new_pos[1] < limit and agent.team != 0:
                pass

            # If there is a wall, the agent does not move
            if new_pos[1] < limit and int(self.world[new_pos]) == WALL:
                pass

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[1] < limit and int(self.world[new_pos]) == SPACE:
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                # Reward Exploration
                self._exploration_prize(new_pos)

            # If the space is a trap (3), end the game
            if new_pos[1] < limit and int(self.world[new_pos]) == TRAP:
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                self.state = 'Failed'
                # Reward Exploration
                self._exploration_prize(new_pos)


            # If the agent reaches the goal(5) End the game
            elif new_pos[1] < limit and (int(self.world[new_pos]) == GOAL):
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                self.state = 'Succeeded'
                if agent.team == 1:
                    self.team1Win = True
                else:
                    self.team1Win = False
                # Reward Exploration
                self._exploration_prize(new_pos)

        # If the agent goes forward
        if action == FORWARD:
            new_pos = (agent.x + 1, agent.y)
            limit = np.size(self.world, 0) - 1

            # Making sure the agent does not go out of bounds so newpos[0] must be > 0

            # If the other agent is in the next position, don't move
            if new_pos[0] < limit and agent.team != 0:
                pass

            # If there is a wall then the agent does not move
            if (new_pos[0] < limit and int(self.world[new_pos]) == WALL) or new_pos[0] == limit:
                pass

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[0] < limit and int(self.world[new_pos]) == SPACE:
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                # Reward Exploration
                self._exploration_prize(new_pos)

            # If the space is a trap (3), end the game
            if new_pos[0] < limit and int(self.world[new_pos]) == TRAP:
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                self.state = 'Failed'
                # Reward Exploration
                self._exploration_prize(new_pos)


            # If the agent reaches the goal End the game
            elif new_pos[0] < limit and (int(self.world[new_pos]) == GOAL):
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                self.state = 'Succeeded'
                if agent.team == 1:
                    self.team1Win = True
                else:
                    self.team1Win = False
                # Reward Exploration
                self._exploration_prize(new_pos)

        # If the agent goes left
        if action == LEFT:
            new_pos = (agent.x, agent.y - 1)

            # Making sure the agent does not go out of bounds so newpos[0] must be > 0

            # If the other agent is in the next position, don't move
            if new_pos[1] >= SPACE and agent.team != 0:
                pass

            # If there is a wall, then the agent does not move
            if new_pos[1] >= SPACE and int(self.world[new_pos]) == WALL:
                pass

            # If the space is not a trap (0), move to it and set the previous spot to 0
            if new_pos[1] >= SPACE and int(self.world[new_pos]) == SPACE:
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                # Reward Exploration
                self._exploration_prize(new_pos)
            # If the space is a trap (3), end the game
            if new_pos[1] >= SPACE and int(self.world[new_pos]) == TRAP:
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                self.state = 'Failed'
                # Reward Exploration
                self._exploration_prize(new_pos)


            # If the agent reaches the goal
            elif new_pos[1] >= SPACE and (int(self.world[new_pos]) == GOAL):
                self.world[new_pos] = agent.id
                self.world[current_pos] = SPACE
                agent.setCoords(new_pos[0], new_pos[1])
                self.state = 'Succeeded'
                if agent.team == 1:
                    self.team1Win = True
                else:
                    self.team1Win = False
                # Reward Exploration
                self._exploration_prize(new_pos)

        # Teleport the other agent
        if action == TELEPORT:
            # keep current position of current agent, move the other agent
            if agent.team == 1:
                if agent.id == len(self.agents) - 1:
                    other_agent = self.agents[0]
                else:
                    other_agent = self.agents[agent.id + 1]
            else:
                if agent.id == numOfAgents:
                    other_agent = self.agents[1]
                else:
                    other_agent = self.agents[agent.id + 1]

            other_player_pos = (other_agent.x, other_agent.y)
            other_next_pos = (other_agent.x + 3, other_agent.y)
            # Set the next position of the other agent

            # If the other agent is still within top
            if other_next_pos[0] < np.size(self.world, 0) - 2:
                pass

            else:
                # The other agent moves out of bounds, so needs to be in bounds
                increment = 1
                while other_next_pos[0] >= np.size(self.world, 0) - 2 and increment <= 3:
                    other_next_pos = (other_player_pos[0] - increment, other_player_pos[1])
                    increment += 1

            # Check if the other agent teleports into a trap or the goal
            # Otherwise the maze is still playable
            if self.world[other_next_pos] == TRAP:
                self.state = 'Failed'
            elif self.world[other_next_pos] == GOAL:
                self.state = 'Succeeded'
                if agent.team == 1:
                    self.team1Win = True
                else:
                    self.team1Win = False
            else:
                self.state = 'P'

            self.world[other_next_pos] = other_agent.id
            self.world[other_player_pos] = SPACE
            other_agent.setCoords(other_next_pos[0], other_next_pos[1])
            # Reward Exploration
            self._exploration_prize(other_next_pos)
    # Set up if agent is eliminated

