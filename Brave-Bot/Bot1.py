import logging
import multiprocessing
import time
from collections import deque
from Status import Status
from utilities.Utility import random_next_step
from utilities.path_builder import get_alien_positions, get_dynamic_path
from utilities.constants import restricted_cells


class Bot1:

    #Constructor
    def __init__(self, ship_layout, bot_initial_coordinates, goal_position, step_time_constraint=100000):
        """
        :param ship_layout: layout of the ship as a 2D matrix with each element representing whether the cell at that
                             coordinates is open/closed/occupied by someone(Eg: Alien/Bot/Captain)
        :param bot_initial_coordinates: tuple containing the coordinates of the cell in which the bot is spawned
        :param goal_position: tuple containing the coordinates of the cell in which the captain is spawned in.
        :param step_time_constraint: time constraint that limits the time taken by the bot for next step computation.
        """
        self.ship_layout = ship_layout
        self.position = bot_initial_coordinates
        self.goal = goal_position
        self.shortest_path_to_goal = deque()
        self.step_time_constraint = step_time_constraint
        if self.step_time_constraint == 0:
            self.step_time_constraint = 100000

    # Function to calculate the shortest path to the goal i.e position of the captain, avoiding all the aliens within
    # the ship
    def calculate_path(self):
        result = {'path': self.shortest_path_to_goal}
        # Calling the utility function with the parameters as the current ship layout, current position of the bot,
        # goal position, and cells to be avoided as positions of the aliens.
        get_dynamic_path(self.ship_layout, self.position, self.goal, result,
                         avoid_cells=get_alien_positions(self.ship_layout))
        # if no path to the captain is identified, we are returning an empty queue.If path is identified, we store it in
        # the class variable self.shortest_path_to_goal and use it for the rest of the simulation.
        self.shortest_path_to_goal = result['path'] if result['path'] else deque()

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int],float]:
        computation_time = 0.0
        # For Bot1, we are only computing the shortest path to the goal once. So, we are checking if the path has
        # already been calculated, and calculating the path only if we do not have a path already
        if (not self.shortest_path_to_goal) or len(self.shortest_path_to_goal) == 0:
            start_time = time.time()
            # calculating path from bot's current position to the goal for one time, storing it in the class variable
            # self.shortest_path_to_goal and using this path for the rest of the simulation.
            self.calculate_path()
            # calculating the time taken for computing the next step
            computation_time = time.time() - start_time
            # checking if the time constraint is breached. If the constraint is breached, we are forcing the bot to
            # behave randomly( so that it does not make a definite decision when the time constraint is breached)
            if computation_time > self.step_time_constraint:
                self.shortest_path_to_goal.clear()
                # calling function to identify the random step from a list of valid neighbors.
                random_step = random_next_step(self.position, self.ship_layout)
                if random_step:
                    self.shortest_path_to_goal.append(random_step)
        # if we have identified a path to goal, we are popping the next position of the bot from the start of the queue
        # if we are not able to find any path to the goal, then the bot stays in the current position.
        if self.shortest_path_to_goal and len(self.shortest_path_to_goal) > 0:
            # popping the next position from the start of the path queue
            next_position = self.shortest_path_to_goal.popleft()
            # checking if the next position of the bot is within a restricted i.e the cell contains an alien
            if self.ship_layout[next_position[0]][next_position[1]] in restricted_cells:
                # if yes, the bot fails, and we return the status of the simulation as Failure
                return Status.FAILURE, self.ship_layout, next_position, computation_time
            # checking if the next cell of the bot contains the captain
            if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
                # if yes, then the bot succeeded in reaching the captain, without encountering the aliens
                return Status.SUCCESS, self.ship_layout, next_position, computation_time
            # Update the bot's position in the ship layout
            # Updating the current position of the bot to an unoccupied open cell
            self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
            # Updating the position of the bot
            self.position = next_position
            # Updating the ship layout, so that the next position of the bot reflects the bot
            self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position, computation_time
