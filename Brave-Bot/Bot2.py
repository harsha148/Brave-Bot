import logging
import time
from collections import deque
import multiprocessing
from Status import Status
from utilities.Utility import random_next_step
from utilities.path_builder import get_dynamic_path, get_alien_positions


class Bot2:
    def __init__(self, ship_layout, start_position, goal_position, step_time_constraint=100000):
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
        get_dynamic_path(self.ship_layout, self.position, self.goal, result,
                         avoid_cells=get_alien_positions(self.ship_layout))
        self.path = result['path'] if result['path'] else deque()

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int], float]:
        computation_time = 0.0
        start_time = time.time()
        self.calculate_path()
        computation_time = time.time() - start_time
        # logging.info(f'Time taken for step computation by BOT2 is {computation_time}')
        if computation_time > self.step_time_constraint:
            self.path.clear()
            random_step = random_next_step(self.position, self.ship_layout)
            if random_step:
                self.path.append(random_step)
            logging.warning(
                'Bot failed to compute next step in the time constraint, so choosing the next step randomly')
        if self.path:
            next_position = self.path.popleft()
            if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
                self.position = next_position
                return Status.SUCCESS, self.ship_layout, self.position, computation_time
            elif self.ship_layout[next_position[0]][next_position[1]] == 'CP&A':
                return Status.INPROCESS, self.ship_layout, self.position, computation_time
            # Update the bot's position in the ship layout
            self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
            self.position = next_position
            self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position, computation_time
