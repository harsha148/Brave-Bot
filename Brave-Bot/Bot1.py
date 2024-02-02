from collections import deque

from Status import Status


class Bot1(object):
    def __init__(self, ship_layout, bot_initial_coordinates):
        self.ship_layout = ship_layout
        self.bot_initial_coordinates = bot_initial_coordinates
        self.shortest_path_to_goal = self.get_shortest_path_to_goal()
        print('Shortest Path for Bot1')
        print(self.shortest_path_to_goal)

    def get_shortest_path_to_goal(self) -> deque[tuple[int, int]]:
        # performing BFS with self.bot_coordinates as root to fetch the shortest path
        # fringe to store all squares at a particular depth in BFS
        fringe: deque[tuple[int, int]] = deque([self.bot_initial_coordinates])
        # visited_open_squares to store the visited squares during BFS
        visited_open_squares: set[tuple[int, int]] = set()
        # prev is a dictionary to store mapping between child and parent nodes
        prev: dict[tuple[int, int], tuple[int, int]] = {self.bot_initial_coordinates: self.bot_initial_coordinates}
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # left, right, up, down
        final_node: tuple[int, int] = (-1, -1)
        # BFS
        while fringe:
            current_node = fringe.popleft()
            x, y = current_node
            if self.ship_layout[x][y] == 'CP':
                final_node = current_node
                break
            if current_node in visited_open_squares:
                continue
            visited_open_squares.add(current_node)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.ship_layout) and 0 <= ny < len(self.ship_layout[0]):
                    if (self.ship_layout[nx][ny] == 'O' or self.ship_layout[nx][ny] == 'CP') and self.ship_layout[nx][
                        ny] != 'A' and (
                            nx, ny) not in visited_open_squares:
                        fringe.append((nx, ny))
                        prev[(nx, ny)] = current_node
        if final_node == (-1, -1):
            return deque()
        shortest_path_to_goal: list[tuple[int, int]] = [final_node]
        current_node = final_node
        while prev[current_node] != self.bot_initial_coordinates:
            shortest_path_to_goal.append(prev[current_node])
            current_node = prev[current_node]
        return deque(reversed(shortest_path_to_goal))

    def step(self, current_ship_layout: list[list[str]], current_bot_square: tuple[int, int]) -> tuple[
        Status, list[list[str]],tuple[int,int]]:
        if not self.shortest_path_to_goal:
            return Status.FAILURE, current_ship_layout, current_bot_square
        next_bot_square = self.shortest_path_to_goal.popleft()
        x, y = next_bot_square
        if current_ship_layout[x][y] == 'A':
            return Status.FAILURE, current_ship_layout, next_bot_square
        if current_ship_layout[x][y] == 'CP':
            return Status.SUCCESS, current_ship_layout, next_bot_square
        prev_bot_x, prev_bot_y = current_bot_square
        current_ship_layout[x][y] = 'B'
        current_ship_layout[prev_bot_x][prev_bot_y] = 'O'
        return Status.INPROCESS, current_ship_layout, next_bot_square
