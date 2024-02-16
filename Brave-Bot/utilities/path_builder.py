from collections import deque


def get_shortest_path(ship_layout: list[list[str]], bot_coordinates: tuple[int, int]) -> deque[tuple[int, int]]:
    # performing BFS with bot_coordinates as root to fetch the shortest path
    # fringe to store all squares at a particular depth in BFS
    fringe: deque[tuple[int, int]] = deque([bot_coordinates])
    # visited_open_squares to store the visited squares during BFS
    visited_open_squares: set[tuple[int, int]] = set()
    # prev is a dictionary to store mapping between child and parent nodes
    prev: dict[tuple[int, int], tuple[int, int]] = {bot_coordinates: bot_coordinates}
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # left, right, up, down
    final_node: tuple[int, int] = (-1, -1)
    # BFS
    while fringe:
        current_node = fringe.popleft()
        x, y = current_node
        if ship_layout[x][y] == 'CP':
            final_node = current_node
            break
        if current_node in visited_open_squares:
            continue
        visited_open_squares.add(current_node)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(ship_layout) and 0 <= ny < len(ship_layout[0]):
                if (ship_layout[nx][ny] == 'O' or ship_layout[nx][ny] == 'CP') and ship_layout[nx][
                    ny] != 'A' and (
                        nx, ny) not in visited_open_squares:
                    fringe.append((nx, ny))
                    prev[(nx, ny)] = current_node
    if final_node == (-1, -1):
        return deque()
    shortest_path_to_goal: list[tuple[int, int]] = [final_node]
    current_node = final_node
    while prev[current_node] != bot_coordinates:
        shortest_path_to_goal.append(prev[current_node])
        current_node = prev[current_node]
    return deque(reversed(shortest_path_to_goal))


def get_dynamic_path(ship_layout, start, goal, avoid_cells=None):
    if start == goal:
        # If the bot is already at the goal, no movement is needed.
        return [start]

    if avoid_cells is None:
        avoid_cells = set()

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Directions: Up, Down, Left, Right
    visited = {start}  # Keep track of visited positions to avoid loops
    queue = deque([(start, [])])  # Queue for BFS: (current_position, path to this position)

    while queue:
        current_position, path = queue.popleft()

        for dx, dy in directions:
            nx, ny = current_position[0] + dx, current_position[1] + dy
            next_position = (nx, ny)

            if 0 <= nx < len(ship_layout) and 0 <= ny < len(ship_layout[0]) and next_position not in visited:
                cell = ship_layout[nx][ny]

                # Skip cells that are in the avoid_cells set
                if next_position in avoid_cells:
                    continue

                visited.add(next_position)
                new_path = path + [next_position]

                # Check if the next position is the goal
                if next_position == goal:
                    return new_path  # Goal reached, return the path

                queue.append((next_position, new_path))

    return None  # No path found if the goal is unreachable


def get_safe_path(ship_layout, start, goal):
    # Get the positions of aliens and their adjacent cells
    aliens_and_adjacent = get_aliens_and_adjacent_positions(ship_layout)

    # Attempt to find a path avoiding aliens and their adjacent cells
    safe_path = get_dynamic_path(ship_layout, start, goal, avoid_cells=aliens_and_adjacent)
    if safe_path:
        return safe_path

    # If no safe path is found, fall back to Bot 2 behavior (avoid only aliens)
    return get_dynamic_path(ship_layout, start, goal, avoid_cells=get_aliens_positions(ship_layout))


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
                        for y, cell in enumerate(row) if cell in ['A', 'CP&A']]
    return aliens_positions


