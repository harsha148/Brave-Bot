from Status import Status
from utilities.path_builder import get_aliens_positions, get_dynamic_path
from utilities.constants import restricted_cells


class Bot1:
    def __init__(self, ship_layout, bot_initial_coordinates, goal_position):
        self.ship_layout = ship_layout
        self.position = bot_initial_coordinates
        self.goal = goal_position
        self.shortest_path_to_goal = get_dynamic_path(ship_layout, self.position, self.goal,
                                                      avoid_cells=get_aliens_positions(self.ship_layout))
        print('Shortest Path for Bot1')
        print(self.shortest_path_to_goal)

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int]]:
        if not self.shortest_path_to_goal:
            return Status.FAILURE, self.ship_layout, self.position
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
