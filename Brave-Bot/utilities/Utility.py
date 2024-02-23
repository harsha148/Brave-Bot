import random


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


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_risk_matrix(ship_layout, alien_positions):
    risk_scores = [[0 for _ in row] for row in ship_layout]
    for x in range(len(ship_layout)):
        for y in range(len(ship_layout)):
            total_distance = sum(manhattan_distance((x, y), alien) for alien in alien_positions)
            risk_scores[x][y] = 1 / (1 + total_distance)
    return risk_scores


