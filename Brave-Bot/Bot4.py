from collections import deque

from Status import Status
from utilities.path_builder import a_star_least_risky_path, get_alien_positions, get_safe_neighbouring_cell
from utilities.Utility import get_risk_scores_by_manhattan_distance_of_aliens, get_risk_scores_by_density_of_aliens
import time


class Bot4:
    def __init__(self, ship_layout, start_position, goal_position, is_density,risk_factor,
                 risk_density_radius, risk_function_type='SIGMOID'):
        """
        :param ship_layout: layout of the ship as a 2D matrix with each element representing whether the cell at that
                             coordinates is open/closed/occupied by someone(Eg: Alien/Bot/Captain)
        :param start_position: tuple containing the coordinates of the cell in which the bot is spawned
        :param goal_position: tuple containing the coordinates of the cell in which the captain is spawned in.
        :param is_density: Boolean flag that determines whether the risk score of an open cell is a function of
                                1.the manhattan distance from aliens within a radius or
                                2. the manhattan distance from all aliens within the ship
        :param risk_factor: Factor used to upscale the contribution of risk score to the heuristic. This heuristic is
                            used to choose the least risky path to the captain.
        :param risk_density_radius: The radius considered around an open cell to compute the risk score of that open
                                    cell
        :param risk_function_type: Determines the type of function to use for risk score computation. By default, we
                                    set it to SIGMOID. The other options for this parameter are LOG, TANH
        """
        self.risk_function_type = risk_function_type
        self.risk_factor = risk_factor
        self.risk_density_radius = risk_density_radius
        self.ship_layout = ship_layout
        self.position = start_position
        self.goal = goal_position
        self.risk_scores = get_risk_scores_by_density_of_aliens(ship_layout, get_alien_positions(ship_layout),
                                                                risk_function_type,risk_density_radius)
        self.path = self.calculate_path()
        self.is_density = is_density

    def calculate_path(self):
        # Calling the utility function with the parameters as the current ship layout, current position of the bot,
        # goal position,risk_scores and risk_factor, to get the least risky path to the captain
        path = a_star_least_risky_path(self.ship_layout, self.position, self.goal, self.risk_scores, self.risk_factor)
        if path:
            return path
        # if we find no path to the captain, we move the bot to a less risky cell within the immediate neighborhood
        # of the bot's current position. If none of the cells within the immediate neighborhood of the bot's current
        # position are less risky than the current position, then the bot will remain in the current position itself.
        return get_safe_neighbouring_cell(self.position, self.risk_scores, self.ship_layout)

    def step(self) -> tuple[Status, list[list[str]], tuple[int, int],float]:
        start_time = time.time()
        # calculating risk_scores for all open cells of the ship.
        if self.is_density:
            # if the is_density flag is True, we are calculating the risk of an open cell based on the manhattan
            # distance from aliens within a radius around that cell
            self.risk_scores = get_risk_scores_by_density_of_aliens(self.ship_layout,
                                                                    get_alien_positions(self.ship_layout),
                                                                    risk_function_type=self.risk_function_type,
                                                                    radius=self.risk_density_radius)
        else:
            # if the is_density flag is False, we are calculating the risk of an open cell based on the manhattan
            # distance from all aliens within the ship
            self.risk_scores = get_risk_scores_by_manhattan_distance_of_aliens(self.ship_layout,
                                                                               get_alien_positions(self.ship_layout))
        # calculating the least risky path from bot's current position to the goal based on the risk scores calculated,
        # storing it in the class variable. We will be using this path for the next step of BOT4. For later steps, we
        # will calculate a new path to the captain based on the updated alien positions
        self.path = self.calculate_path()
        computation_time = time.time() - start_time
        # if we have identified a path to goal, we are popping the next position of the bot from the start of the queue
        # if we are not able to find any path to the goal with the current configuration of the ship, then we try to
        # find a less risky cell within the immediate neighborhood of the bot's current position. If we are not able to
        # find any less risky cell, then the bot stays in the current position.
        if self.path and len(self.path) > 0:
            # popping the next position from the start of the path queue
            next_position = self.path.popleft()
            # In BOT4 we are not checking if the next position contains aliens as we are explicitly avoiding alien cells
            # while calculating the least risky path to the captain
            # checking if the next cell of the bot contains the captain
            if self.ship_layout[next_position[0]][next_position[1]] == 'CP':
                # if yes, then the bot succeeded in reaching the captain, without encountering the aliens
                self.position = next_position
                return Status.SUCCESS, self.ship_layout, self.position, computation_time
            # if the next step for the bot contains both the captain and an alien, then Bot4 will wait at its current
            # position, waiting for the alien to move out of the way.
            elif self.ship_layout[next_position[0]][next_position[1]] == 'CP&A':
                # Bot4 will wait in its current position
                return Status.INPROCESS, self.ship_layout, self.position, computation_time
            # Update the bot's position in the ship layout
            # Updating the current position of the bot to an unoccupied open cell
            self.ship_layout[self.position[0]][self.position[1]] = 'O'  # Clear the old position
            # Updating the class variable containing the position of the bot
            self.position = next_position
            # Updating the ship layout, so that the next position of the bot reflects the bot
            self.ship_layout[self.position[0]][self.position[1]] = 'B'  # Mark the new position
        return Status.INPROCESS, self.ship_layout, self.position, computation_time
