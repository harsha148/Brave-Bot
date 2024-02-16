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

    def step(self, current_ship_layout: list[list[str]], current_bot_square: tuple[int, int]) -> tuple[Status, list[list[str]], tuple[int, int]]:
        if not self.path or self.position == self.goal:
            self.path = self.calculate_path()
            if not self.path:
                return Status.FAILURE, current_ship_layout, self.position

        next_bot_square = self.path.pop(0)
        self.position = next_bot_square
        if current_ship_layout[self.position[0]][self.position[1]] == 'CP':
            return Status.SUCCESS, current_ship_layout, next_bot_square
        prev_bot_x, prev_bot_y = current_bot_square
        current_ship_layout[self.position[0]][self.position[1]] = 'B'
        current_ship_layout[prev_bot_x][prev_bot_y] = 'O'
        return Status.INPROCESS, current_ship_layout, self.position
