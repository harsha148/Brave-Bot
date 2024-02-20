from collections import deque

from utilities.constants import restricted_cells


def get_dynamic_path(ship_layout, start, goal, result, avoid_cells=None):
    result['path'] = None
    if start == goal:
        result['path'] = [start]
        # If the bot is already at the goal, no movement is needed.
        return result

    if avoid_cells is None:
        avoid_cells = set()

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Directions: Up, Down, Left, Right
    visited = {start}  # Keep track of visited positions to avoid loops
    queue = deque([(start, deque())])  # Queue for BFS: (current_position, path to this position)

    while queue:
        current_position, path = queue.popleft()

        for dx, dy in directions:
            nx, ny = current_position[0] + dx, current_position[1] + dy
            next_position = (nx, ny)
            if (0 <= nx < len(ship_layout) and 0 <= ny < len(ship_layout[0]) and next_position not in visited and
                    next_position not in avoid_cells and ship_layout[nx][ny] != 'C'):
                visited.add(next_position)
                new_path = path.copy()
                new_path.append(next_position)

                # Check if the next position is the goal
                if next_position == goal:
                    result['path'] = new_path
                    return result  # Goal reached, return the path

                queue.append((next_position, new_path))

    return None  # No path found if the goal is unreachable


def get_safe_path(ship_layout, start, goal,result):
    # Get the positions of aliens and their adjacent cells
    aliens_and_adjacent = get_aliens_and_adjacent_positions(ship_layout)

    # Attempt to find a path avoiding aliens and their adjacent cells
    safe_path = get_dynamic_path(ship_layout, start, goal, result, avoid_cells=aliens_and_adjacent)
    if safe_path:
        return safe_path

    # If no safe path is found, fall back to Bot 2 behavior (avoid only aliens)
    return get_dynamic_path(ship_layout, start, goal, result, avoid_cells=get_aliens_positions(ship_layout))


def get_aliens_and_adjacent_positions(ship_layout):
    aliens_positions = get_aliens_positions(ship_layout)
    adjacent_positions = set()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for ax, ay in aliens_positions:
        for dx, dy in directions:
            nx, ny = ax + dx, ay + dy
            if 0 <= nx < len(ship_layout) and 0 <= ny < len(ship_layout[0]):
                adjacent_positions.add((nx, ny))

    return aliens_positions.union(adjacent_positions)


def get_aliens_positions(ship_layout):
    aliens_positions = [(x, y) for x, row in enumerate(ship_layout)
                        for y, cell in enumerate(row) if cell in restricted_cells]
    return set(aliens_positions)
