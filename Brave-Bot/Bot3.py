from Status import Status
from utilities.path_builder import get_safe_path

class Bot3:
    def __init__(self, ship_layout, start_position, goal_position):
        self.ship_layout = ship_layout
        self.position = start_position
        self.goal = goal_position
        self.path = self.calculate_path()

    def calculate_path(self):
        return get_safe_path(self.ship_layout, self.position, self.goal)

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int]]:
        if not self.path or self.position == self.goal:
            self.path = self.calculate_path()
            if not self.path:
                return Status.FAILURE, self.ship_layout, self.position

        next_position = self.path.pop(0)
        if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
            self.position = next_position
            return Status.SUCCESS, self.ship_layout, self.position

        # Update the bot's position in the ship layout
        self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
        self.position = next_position
        self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position
