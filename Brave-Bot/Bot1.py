import logging
import multiprocessing
import time
from collections import deque
from Status import Status
from utilities.Utility import random_next_step
from utilities.path_builder import get_alien_positions, get_dynamic_path
from utilities.constants import restricted_cells


class Bot1:
    def __init__(self, ship_layout, bot_initial_coordinates, goal_position, step_time_constraint=100000):
        self.ship_layout = ship_layout
        self.position = bot_initial_coordinates
        self.goal = goal_position
        self.shortest_path_to_goal = deque()
        self.step_time_constraint = step_time_constraint
        if self.step_time_constraint == 0:
            self.step_time_constraint = 100000

    def calculate_path(self):
        result = {'path': self.shortest_path_to_goal}
        get_dynamic_path(self.ship_layout, self.position, self.goal, result,
                         avoid_cells=get_alien_positions(self.ship_layout))
        self.shortest_path_to_goal = result['path'] if result['path'] else deque()

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int],float]:
        computation_time = 0.0
        if (not self.shortest_path_to_goal) or len(self.shortest_path_to_goal) == 0:
            start_time = time.time()
            self.calculate_path()
            computation_time = time.time() - start_time
            # logging.info(f'Time taken for step computation by BOT1:{computation_time}')
            if computation_time > self.step_time_constraint:
                self.shortest_path_to_goal.clear()
                random_step = random_next_step(self.position, self.ship_layout)
                if random_step:
                    self.shortest_path_to_goal.append(random_step)
                logging.warning(
                    'Bot failed to compute next step within the time constraint, so choosing the next step randomly')
        if self.shortest_path_to_goal and len(self.shortest_path_to_goal) > 0:
            next_position = self.shortest_path_to_goal.popleft()
            if self.ship_layout[next_position[0]][next_position[1]] in restricted_cells:
                return Status.FAILURE, self.ship_layout, next_position, computation_time

            if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
                return Status.SUCCESS, self.ship_layout, next_position, computation_time
            # Update the bot's position in the ship layout
            self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
            self.position = next_position
            self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position, computation_time
