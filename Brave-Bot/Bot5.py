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
        self.path = result['path']

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int]]:
        start_time = time.time()
        self.calculate_path()
        end_time = time.time()
        if end_time - start_time > self.step_time_constraint:
            self.path.clear()
            if self.last_path_position:
                self.path.append(self.last_path_position)
            logging.warning(
                'Bot failed to compute next step in the time constraint, so choosing the next step randomly')
        else:
            end_time = time.time()
            logging.debug(
                f'Step computation completed before time constraint. Time taken for step computation: {end_time - start_time}')
        if self.path:
            next_position = self.path.popleft()
            if self.path:
                self.last_path_position = self.path.popleft()
                print(self.last_path_position)
            if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
                self.position = next_position
                return Status.SUCCESS, self.ship_layout, self.position
            elif self.ship_layout[next_position[0]][next_position[1]] == 'CP&A':
                return Status.INPROCESS, self.ship_layout, self.position
            # Update the bot's position in the ship layout
            self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
            self.position = next_position
            self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position
