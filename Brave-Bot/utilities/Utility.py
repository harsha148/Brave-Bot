import random
import math
from utilities.path_builder import get_alien_positions


def random_next_step(position, ship_layout):
    possible_next_steps = []
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    restricted_cells = {'C', 'A', 'CP&A'}
    x, y = position[0], position[1]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (0 <= nx < len(ship_layout) and 0 <= ny < len(ship_layout[0]) and ship_layout[nx][ny]
                not in restricted_cells):
            possible_next_steps.append((nx, ny))
    if possible_next_steps:
        return random.choice(possible_next_steps)
    return ()


def get_num_of_open_cells(ship_layout):
    ship_dim = len(ship_layout)
    num_of_open_cells = 0
    for i in range(ship_dim):
        for j in range(ship_dim):
            if ship_layout[i][j] == 'O':
                num_of_open_cells += 1
    return num_of_open_cells


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_risk_scores_by_manhattan_distance_of_aliens(ship_layout):
    alien_positions = get_alien_positions(ship_layout)
    risk_scores = [[0 for _ in row] for row in ship_layout]
    for x in range(len(ship_layout)):
        for y in range(len(ship_layout)):
            if ship_layout[x][y] != 'C':  # Skip blocked cells
                total_distance = sum(manhattan_distance((x, y), alien) for alien in alien_positions)
                risk_scores[x][y] = 1 / (1 + total_distance)
    return risk_scores


def get_risk_scores_by_density_of_aliens(ship_layout, radius=3, scaling_factor=1, midpoint=3):
    alien_positions = get_alien_positions(ship_layout)
    risk_scores = [[0 for _ in row] for row in ship_layout]

    for x in range(len(ship_layout)):
        for y in range(len(ship_layout)):
            if ship_layout[x][y] != 'C':  # Skip blocked cells
                alien_count = 0
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(ship_layout) and 0 <= ny < len(ship_layout):
                            if (nx, ny) in alien_positions:
                                alien_count += 1
                # Use the sigmoid function for risk scoring
                # Experiment with different values for scaling-factor, midpoint for a better objective function
                risk_scores[x][y] = 1 / (1 + math.exp(-scaling_factor * (alien_count - midpoint)))

    return risk_scores
