from Status import Status
from utilities.path_builder import get_dynamic_path


class Bot2:
    def __init__(self, ship_layout, start_position, goal_position):
        self.ship_layout = ship_layout
        self.position = start_position
        self.goal = goal_position
        self.path = self.calculate_path()

    def calculate_path(self):
        return get_dynamic_path(self.ship_layout, self.position, self.goal)

    def step(self):
        if not self.path or self.position == self.goal:
            self.path = self.calculate_path()
            if not self.path:
                return Status.FAILURE, self.position

        self.position = self.path.pop(0)

        if self.position == self.goal:
            return Status.SUCCESS, self.position

        return Status.INPROCESS, self.position
