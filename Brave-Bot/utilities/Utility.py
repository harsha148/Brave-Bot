import random


def random_next_step(position):
    possible_next_steps = []
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    restricted_cells = {'C', 'A', 'CP&A'}
    x, y = position[0], position[1]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (0 <= nx < len(self.ship_layout) and 0 <= ny <= len(self.ship_layout[0]) and self.ship_layout[nx][ny]
                not in restricted_cells):
            possible_next_steps.append((nx, ny))
    return random.choice(possible_next_steps)
