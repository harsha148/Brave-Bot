import time
from collections import deque
import random
import multiprocessing
from Status import Status
from utilities.Utility import random_next_step
from utilities.path_builder import get_dynamic_path, get_aliens_positions


class Bot2:
    def __init__(self, ship_layout, start_position, goal_position, step_time_constraint=float('inf')):
        self.ship_layout = ship_layout
        self.position = start_position
        self.goal = goal_position
        # stores the shortest path to captain avoiding the alien positions (Bot 2 logic)
        self.path = deque()
        self.step_time_constraint = step_time_constraint

    def calculate_path(self):
        result = {}
        get_dynamic_path(self.ship_layout, self.position, self.goal, result,
                         avoid_cells=get_aliens_positions(self.ship_layout))
        self.path = result['path']

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int]]:
        # temp_path = self.path
        # start_time = time.time()
        # self.path = self.calculate_path()
        # end_time = time.time()
        # if 0 < self.step_time_constraint < (end_time - start_time):
        #     print(f'Bot failed computation time constraint')
        #     self.path = temp_path
        p = multiprocessing.Process(self.calculate_path())
        p.start()
        p.join(self.step_time_constraint)
        next_position = None
        if p.is_alive():
            p.terminate()
            p.kill()
            next_position = random_next_step(self.position)
        else:
            if not self.path:
                return Status.FAILURE, self.ship_layout, self.position
            next_position = self.path.popleft()
        if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
            self.position = next_position
            return Status.SUCCESS, self.ship_layout, self.position

        # Update the bot's position in the ship layout
        self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
        self.position = next_position
        self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position
