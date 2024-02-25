from Status import Status
from utilities.path_builder import dijkstra_shortest_path, get_alien_positions
from utilities.Utility import get_risk_scores_by_manhattan_distance_of_aliens, get_risk_scores_by_density_of_aliens
import time


class Bot4:
    def __init__(self, ship_layout, start_position, goal_position,is_density):
        self.ship_layout = ship_layout
        self.position = start_position
        self.goal = goal_position
        self.risk_scores = get_risk_scores_by_density_of_aliens(ship_layout, get_alien_positions(ship_layout))
        self.path = self.calculate_path()
        self.is_density = is_density

    def calculate_path(self):
        return dijkstra_shortest_path(self.ship_layout, self.position, self.goal, self.risk_scores)

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int]]:
        start_time = time.time()
        if self.is_density:
            self.risk_scores = get_risk_scores_by_density_of_aliens(self.ship_layout, get_alien_positions(self.ship_layout))
        else:
            self.risk_scores = get_risk_scores_by_manhattan_distance_of_aliens(self.ship_layout)
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
