import multiprocessing
import time
from collections import deque
import logging
from Status import Status
from utilities.Utility import random_next_step
from utilities.path_builder import get_safe_path, get_dynamic_path


class Bot3:
    def __init__(self, ship_layout, start_position, goal_position, step_time_constraint=float('inf')):
        self.ship_layout = ship_layout
        self.position = start_position
        self.goal = goal_position
        self.path = deque()
        self.step_time_constraint = step_time_constraint

    def calculate_path(self):
        result = {}
        get_safe_path(self.ship_layout, self.position, self.goal, result)
        '''
        if there is no path to the captain, we try to check the shortest path without considering the 
        aliens as the blocking aliens might move out of the way in the next moves.
        '''
        if not result['path']:
            get_dynamic_path(self.ship_layout, self.position, self.goal, result)
        self.path = result['path']

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int]]:
        p = multiprocessing.Process(self.calculate_path())
        start_time = time.time()
        p.start()
        p.join(self.step_time_constraint)
        next_position = ()
        if p.is_alive():
            logging.debug('Step computation timeout error, so choosing a random cell for the bot to move to.')
            p.terminate()
            p.kill()
            self.path.clear()
            random_step = random_next_step(self.position, self.ship_layout)
            if random_step:
                self.path.append(random_step)
        else:
            end_time = time.time()
            logging.debug(
                f'Step computation completed before time constraint. Time taken for step computation: {end_time - start_time}')
        if self.path:
            next_position = self.path.popleft()
            if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
                self.position = next_position
                return Status.SUCCESS, self.ship_layout, self.position

            # Update the bot's position in the ship layout
            self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
            self.position = next_position
            self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position
