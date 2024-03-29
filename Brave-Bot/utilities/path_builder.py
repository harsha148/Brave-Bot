import logging
from collections import deque
import heapq


def get_dynamic_path(ship_layout, start, goal, result, avoid_cells=None):
    """
    :param ship_layout: layout of the ship as a 2D matrix with each element representing whether the cell at that
                                 coordinates is open/closed/occupied by someone(Eg: Alien/Bot/Captain)
    :param start: tuple containing the coordinates of the cell in which the bot is spawned
    :param goal: tuple containing the coordinates of the cell in which the captain is spawned in.
    :param result: dictionary to store the output
    :param avoid_cells: set of cells to avoid in the path to the captain
    :return: dictionary containing the path
    """
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

    # performing BFS
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


def get_safe_path(ship_layout, start, goal, result):
    # Get the positions of aliens and their adjacent cells
    aliens_and_adjacent = get_aliens_and_adjacent_positions(ship_layout)

    # Attempt to find a path avoiding aliens and their adjacent cells
    safe_path = get_dynamic_path(ship_layout, start, goal, result, avoid_cells=aliens_and_adjacent)
    if safe_path:
        return safe_path

    # If no safe path is found, fall back to Bot 2 behavior (avoid only aliens)
    return get_dynamic_path(ship_layout, start, goal, result, avoid_cells=get_alien_positions(ship_layout))


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_least_risky_path(ship_layout, start, goal, risk_scores, risk_factor):
    # directions for finding the neighboring cells of the bot
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    # dimension of the ship
    n = len(ship_layout)
    # matrix to store the heuristic distance
    distances = [[float('inf') for _ in range(n)] for _ in range(n)]
    steps = [[None for _ in range(n)] for _ in range(n)]
    distances[start[0]][start[1]] = 0
    pq = [(0, start)]
    # A star algorithm for finding the least risky path based on the heuristic to the captain
    while pq:
        current_distance, current_position = heapq.heappop(pq)
        x, y = current_position
        if current_distance > distances[x][y]:
            continue
        if current_position == goal:
            return reconstruct_path(start, goal, steps)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and ship_layout[nx][ny] not in ['C', 'A'] and (nx, ny) != steps[x][y]:
                # heuristic for the neighboring cell (nx,ny)
                new_distance = (manhattan_distance((nx, ny), start)) + risk_factor * \
                               risk_scores[nx][ny] + manhattan_distance((nx, ny), goal)
                if new_distance < distances[nx][ny]:
                    distances[nx][ny] = new_distance
                    steps[nx][ny] = (x, y)  # Store the previous cell to get the steps
                    heapq.heappush(pq, (new_distance, (nx, ny)))

    return None  # No path found


def get_safe_neighbouring_cell(current_cell, risk_scores, ship_layout):
    x, y = current_cell
    result = deque()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    n = len(ship_layout)
    safe_neighbor = None
    min_risk = risk_scores[x][y]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and ship_layout[nx][ny] not in ['C', 'A']:
            if risk_scores[nx][ny] < min_risk:
                safe_neighbor = (nx, ny)
                min_risk = risk_scores[nx][ny]
    if safe_neighbor:
        result.append(safe_neighbor)
    return result


def reconstruct_path(start, goal, steps):
    path = deque()
    current = goal
    while current != start:
        path.appendleft(current)
        current = steps[current[0]][current[1]]
    return path


def get_aliens_and_adjacent_positions(ship_layout):
    aliens_positions = get_alien_positions(ship_layout)
    adjacent_positions = set()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for ax, ay in aliens_positions:
        for dx, dy in directions:
            nx, ny = ax + dx, ay + dy
            if 0 <= nx < len(ship_layout) and 0 <= ny < len(ship_layout[0]):
                adjacent_positions.add((nx, ny))

    return aliens_positions.union(adjacent_positions)


def get_alien_positions(ship_layout):
    aliens_positions = [(x, y) for x, row in enumerate(ship_layout)
                        for y, cell in enumerate(row) if cell == 'A']
    return set(aliens_positions)
