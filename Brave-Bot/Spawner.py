import random
from collections import deque


class Spawner(object):
    def __init__(self, ship_layout, root_open_square):
        self.ship_layout = ship_layout
        self.root_open_square = root_open_square
        self.open_squares = self.get_open_squares()
        print('Calculated open squares')
        print(self.open_squares)

    ''' method get_open_squares is used to fetch the list of open squares,
     which can be later used to spawn different items/characters '''

    def get_open_squares(self) -> list[tuple[int, int]]:
        # performing BFS with root_open_square as root to fetch the list of open squares
        # fringe to store all squares at a particular depth in BFS
        fringe: deque[tuple[int, int]] = deque([self.root_open_square])
        # visited_open_squares to store the visited squares during BFS
        visited_open_squares: set[tuple[int, int]] = set()
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # left, right, up, down
        # BFS
        while fringe:
            current_node = fringe.popleft()
            if current_node in visited_open_squares:
                continue
            visited_open_squares.add(current_node)
            x, y = current_node
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.ship_layout) and 0 <= ny < len(self.ship_layout[0]):
                    if self.ship_layout[nx][ny] == 'O' and (nx, ny) not in visited_open_squares:
                        fringe.append((nx, ny))
        # visited_open_squares should contain the entire list of open squares
        return list(visited_open_squares)

    def spawn_bot(self) -> tuple[list[list[int]], tuple[int, int]]:
        random_open_square_for_bot = random.choice(self.open_squares)
        x, y = random_open_square_for_bot
        self.ship_layout[x][y] = 'B'
        self.open_squares.remove(random_open_square_for_bot)
        return self.ship_layout, random_open_square_for_bot

    def spawn_aliens(self, number_of_aliens) -> tuple[list[list[int]], list[tuple[int, int]]]:
        random_open_squares_for_aliens = random.sample(self.open_squares, number_of_aliens)
        for alien in random_open_squares_for_aliens:
            self.ship_layout[alien[0]][alien[1]] = 'A'
        return self.ship_layout, random_open_squares_for_aliens

    def spawn_captain(self) -> tuple[list[list[int]], tuple[int, int]]:
        random_open_square_for_captain = random.choice(self.open_squares)
        x, y = random_open_square_for_captain
        if self.ship_layout[x][y] == 'A':
            self.ship_layout[x][y] = 'CP&A'
        else:
            self.ship_layout[x][y] = 'CP'
        return self.ship_layout, random_open_square_for_captain

