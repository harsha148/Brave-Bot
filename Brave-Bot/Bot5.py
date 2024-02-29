import multiprocessing
import time
from collections import deque
import logging
from Status import Status
from utilities.path_builder import get_safe_path, get_dynamic_path


class Bot5:
    def __init__(self, ship_layout, start_position, goal_position, step_time_constraint=1000000):
        self.ship_layout = ship_layout
        self.position = start_position
        self.goal = goal_position
        self.path = deque()
        self.last_path_position = None
        self.step_time_constraint = step_time_constraint
        if self.step_time_constraint == 0:
            self.step_time_constraint = 1000000

    def calculate_path(self):
        result = {}
        get_safe_path(self.ship_layout, self.position, self.goal, result)
        self.path = result['path'] if result['path'] else deque()

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int], float]:
        computation_time = 0.0
        start_time = time.time()
        self.calculate_path()
        computation_time = time.time() - start_time
        if computation_time > self.step_time_constraint:
            # logging.info(f'Bot completed in {computation_time} seconds')
            self.path.clear()
            if self.last_path_position:
                self.path.append(self.last_path_position)
        if self.path:
            next_position = self.path.popleft()
            if self.path:
                self.last_path_position = self.path.popleft()
            if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
                self.position = next_position
                return Status.SUCCESS, self.ship_layout, self.position, computation_time
            elif self.ship_layout[next_position[0]][next_position[1]] == 'CP&A':
                return Status.INPROCESS, self.ship_layout, self.position, computation_time
            # Update the bots position in the ship layout
            self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
            self.position = next_position
            self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position, computation_time
