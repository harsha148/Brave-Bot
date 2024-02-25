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

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int]]:
        if (not self.shortest_path_to_goal) or len(self.shortest_path_to_goal) == 0:
            p = multiprocessing.Process(self.calculate_path())
            start_time =time.time()
            p.start()
            p.join(self.step_time_constraint)
            if p.is_alive():
                p.terminate()
                p.kill()
                self.shortest_path_to_goal.clear()
                random_step = random_next_step(self.position, self.ship_layout)
                if random_step:
                    self.shortest_path_to_goal.append(random_step)
                logging.warning('Bot failed to compute the next step within the time constraint. So choosing next step '
                               'randomly')
        if len(self.shortest_path_to_goal) > 0:
            next_position = self.shortest_path_to_goal.popleft()
            if self.ship_layout[next_position[0]][next_position[1]] in restricted_cells:
                return Status.FAILURE, self.ship_layout, next_position

            if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
                return Status.SUCCESS, self.ship_layout, next_position
            # Update the bot's position in the ship layout
            self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
            self.position = next_position
            self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position
