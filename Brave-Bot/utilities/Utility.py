import random
import math


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


def get_risk_scores_by_manhattan_distance_of_aliens(ship_layout, alien_positions):
    risk_scores = [[0 for _ in row] for row in ship_layout]
    for x in range(len(ship_layout)):
        for y in range(len(ship_layout)):
            if ship_layout[x][y] != 'C':  # Skip blocked cells
                total_distance = sum(manhattan_distance((x, y), alien) for alien in alien_positions)
                risk_scores[x][y] = 1 / (1 + total_distance)
    return risk_scores


def get_risk_scores_by_density_of_aliens(ship_layout, alien_positions,risk_function_type, radius=3):
    risk_scores = [[0 for _ in row] for row in ship_layout]

    for x in range(len(ship_layout)):
        for y in range(len(ship_layout)):
            if ship_layout[x][y] != 'C':  # Skip blocked cells
                sum_inverse_manhattan_distance = 0
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(ship_layout) and 0 <= ny < len(ship_layout):
                            if (nx, ny) in alien_positions:
                                sum_inverse_manhattan_distance += (1 / (manhattan_distance((x, y), (nx, ny)))) if (nx, ny) != (x, y) else 1
                risk_scores[x][y] = get_risk_by_alien_density(sum_inverse_manhattan_distance,risk_function_type) if sum_inverse_manhattan_distance > 0 else 0

    return risk_scores


def get_risk_by_alien_density(sum_inverse_manhattan_distance,risk_function_type):
    if risk_function_type == 'SIGMOID':
        return 1 / (1 + math.exp(-1 * sum_inverse_manhattan_distance))
    if risk_function_type == 'LOG':
        return math.log(1 + sum_inverse_manhattan_distance)
    return math.tanh(1 + sum_inverse_manhattan_distance)
