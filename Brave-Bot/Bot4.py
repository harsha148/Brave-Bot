from Status import Status
from utilities.path_builder import dijkstra_shortest_path, get_aliens_positions
from utilities.Utility import get_risk_matrix


class Bot4:
    def __init__(self, ship_layout, start_position, goal_position):
        self.ship_layout = ship_layout
        self.position = start_position
        self.goal = goal_position
        self.risk_scores = get_risk_matrix(ship_layout, get_aliens_positions(ship_layout))
        self.path = self.calculate_path()

    def calculate_path(self):
        return dijkstra_shortest_path(self.ship_layout, self.position, self.goal, self.risk_scores)

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int]]:
        self.risk_scores = get_risk_matrix(self.ship_layout, get_aliens_positions(self.ship_layout))
        self.path = self.calculate_path()
        if self.path:
            next_position = self.path.popleft()
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
