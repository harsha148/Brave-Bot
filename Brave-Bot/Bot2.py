import logging
import time
from collections import deque
import multiprocessing
from Status import Status
from utilities.Utility import random_next_step
from utilities.path_builder import get_dynamic_path, get_alien_positions


class Bot2:
    def __init__(self, ship_layout, start_position, goal_position, step_time_constraint=100000):
        """
        :param ship_layout: layout of the ship as a 2D matrix with each element representing whether the cell at that
                             coordinates is open/closed/occupied by someone(Eg: Alien/Bot/Captain)
        :param start_position: tuple containing the coordinates of the cell in which the bot is spawned
        :param goal_position: tuple containing the coordinates of the cell in which the captain is spawned in.
        :param step_time_constraint: time constraint that limits the time taken by the bot for next step computation.
        """
        self.ship_layout = ship_layout
        self.position = start_position
        self.goal = goal_position
        # stores the shortest path to captain avoiding the alien positions (Bot 2 logic)
        self.path = deque()
        self.step_time_constraint = step_time_constraint
        if self.step_time_constraint == 0:
            self.step_time_constraint = 100000

    def calculate_path(self):
        result = {}
        # Calling the utility function with the parameters as the current ship layout, current position of the bot,
        # goal position, and cells to be avoided as positions of the aliens.
        get_dynamic_path(self.ship_layout, self.position, self.goal, result,
                         avoid_cells=get_alien_positions(self.ship_layout))
        # if no path to the captain is identified, we are returning an empty queue.If path is identified, we store it in
        # the class variable self.shortest_path_to_goal and use it for the next step of BOT2
        self.path = result['path'] if result['path'] else deque()

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int], float]:
        # In Bot2 we are calculating the shortest path to the captain at every step of the bot.
        start_time = time.time()
        # calculating path from bot's current position to the goal for the current timestep,
        # storing it in the class variable. We will be using this path for the next step of BOT2. For later steps, we
        # will calculate a new path to the captain based on the updated alien positions
        self.calculate_path()

        computation_time = time.time() - start_time
        # checking if the time constraint is breached. If the constraint is breached, we are forcing the bot to
        # behave randomly( so that it does not make a definite decision when the time constraint is breached)
        if computation_time > self.step_time_constraint:
            self.path.clear()
            # calling function to identify the random step from a list of valid neighbors.
            random_step = random_next_step(self.position, self.ship_layout)
            if random_step:
                self.path.append(random_step)
        # if we have identified a path to goal, we are popping the next position of the bot from the start of the queue
        # if we are not able to find any path to the goal with the current configuration of the ship, then the bot
        # stays in the current position.
        if self.path:
            # popping the next position from the start of the path queue
            next_position = self.path.popleft()
            # In BOT2 we are not checking if the next position contains aliens as we are explicitly avoiding alien cells
            # while calculating the path to the captain
            # checking if the next cell of the bot contains the captain
            if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
                # if yes, then the bot succeeded in reaching the captain, without encountering the aliens
                self.position = next_position
                return Status.SUCCESS, self.ship_layout, self.position, computation_time
            # if the next step for the bot contains both the captain and an alien, then Bot2 will wait at its current
            # position, waiting for the alien to move out of the way.
            elif self.ship_layout[next_position[0]][next_position[1]] == 'CP&A':
                # Bot2 will wait in its current position
                return Status.INPROCESS, self.ship_layout, self.position, computation_time
            # Update the bot's position in the ship layout
            # Updating the current position of the bot to an unoccupied open cell
            self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
            # Updating the class variable containing the position of the bot
            self.position = next_position
            # Updating the ship layout, so that the next position of the bot reflects the bot
            self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position, computation_time
