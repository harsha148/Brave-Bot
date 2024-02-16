from Status import Status
from utilities.path_builder import get_shortest_path


class Bot1:
    def __init__(self, ship_layout, bot_initial_coordinates):
        self.ship_layout = ship_layout
        self.position = bot_initial_coordinates
        self.shortest_path_to_goal = get_shortest_path(self.ship_layout, self.position)
        print('Shortest Path for Bot1')
        print(self.shortest_path_to_goal)

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int]]:
        if not self.shortest_path_to_goal:
            return Status.FAILURE, self.ship_layout, self.position

        next_position = self.shortest_path_to_goal.popleft()
        if self.ship_layout[next_position[0]][next_position[1]] in ['A', 'CP&A']:
            return Status.FAILURE, self.ship_layout, next_position

        if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
            return Status.SUCCESS, self.ship_layout, next_position

        # Update the bot's position in the ship layout
        self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
        self.position = next_position
        self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position

        return Status.INPROCESS, self.ship_layout, self.position
