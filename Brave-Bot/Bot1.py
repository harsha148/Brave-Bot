from Status import Status
from utilities.path_builder import get_shortest_path


class Bot1(object):
    def __init__(self, ship_layout, bot_initial_coordinates):
        self.ship_layout = ship_layout
        self.bot_initial_coordinates = bot_initial_coordinates
        self.shortest_path_to_goal = get_shortest_path(self.ship_layout, self.bot_initial_coordinates)
        print('Shortest Path for Bot1')
        print(self.shortest_path_to_goal)

    def step(self, current_ship_layout: list[list[str]], current_bot_square: tuple[int, int]) -> tuple[Status, list[list[str]], tuple[int, int]]:
        if not self.shortest_path_to_goal:
            return Status.FAILURE, current_ship_layout, current_bot_square
        next_bot_square = self.shortest_path_to_goal.popleft()
        x, y = next_bot_square
        if current_ship_layout[x][y] == 'A':
            return Status.FAILURE, current_ship_layout, next_bot_square
        if current_ship_layout[x][y] == 'CP':
            return Status.SUCCESS, current_ship_layout, next_bot_square
        prev_bot_x, prev_bot_y = current_bot_square
        current_ship_layout[x][y] = 'B'
        current_ship_layout[prev_bot_x][prev_bot_y] = 'O'
        return Status.INPROCESS, current_ship_layout, next_bot_square
