import sys
import random
from collections import deque
import time


class Ship(object):
    def __init__(self, ship_size: int):
        self.ship_size = ship_size

    def generate_ship_layout(self) -> tuple[list[list[str]], tuple[int, int]]:
        starttime = time.time()
        # ship is a 2D array which holds information about each square
        # 'C' indicates the square is closed and 'O' indicates it is open
        ship = [['C' for _ in range(self.ship_size)] for _ in range(self.ship_size)]
        ''' 
        root_open_square_x and root_open_square_y represent the coordinates of the first randomly generated open 
        square
        '''
        root_open_square_x: int = random.randrange(self.ship_size)
        root_open_square_y: int = random.randrange(self.ship_size)
        # root_open_square_open_square stores the coordinates of the first open square which is randomly generated
        root_open_square_coordinates: tuple[int, int] = (root_open_square_x, root_open_square_y)
        # updating the root_open_square square to open
        ship[root_open_square_x][root_open_square_y] = 'O'
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # left, right, up, down
        closed_squares_with_open_neighbour = set()
        closed_squares_with_one_open_neighbour = set()
        most_recent_open_square = root_open_square_coordinates
        while True:
            '''
            closed_squares_with_one_open_neighbour represents the list of closed squares with only 1 neighboring 
            square as open1
            '''
            closed_squares_with_one_open_neighbour, closed_squares_with_open_neighbour = self.get_closed_squares_with_one_open_neighbor(
                most_recent_open_square, closed_squares_with_open_neighbour, closed_squares_with_one_open_neighbour,
                ship)
            if not closed_squares_with_one_open_neighbour:
                break
            # randomly selecting a square from the list of closed squares which have only one open neighbor
            square_to_be_opened = random.choice(list(closed_squares_with_one_open_neighbour))
            most_recent_open_square = square_to_be_opened
            ship[square_to_be_opened[0]][square_to_be_opened[1]] = 'O'
            closed_squares_with_one_open_neighbour.remove(square_to_be_opened)
            # print(f'Opening square: {square_to_be_opened}')
        endtime = time.time()
        print(f'time for open cells: {endtime - starttime}')
        starttime = time.time()
        opens1on, closed_neighbors_of_dead_cells = self.get_dead_ends(ship)
        '''
        randomly selecting half the dead cells
        '''
        random_opens1on = random.sample(opens1on, int(len(opens1on) / 2))
        for cell in random_opens1on:
            closed_neighbors = closed_neighbors_of_dead_cells[cell]
            random_closed_neighbor = random.choice(closed_neighbors)
            ship[random_closed_neighbor[0]][random_closed_neighbor[1]] = 'O'
        endtime = time.time()
        print(f'time for dead cells: {endtime - starttime}')
        return ship, root_open_square_coordinates

    def get_closed_squares_with_one_open_neighbor(self, recent_open_square: tuple[int, int],
                                                  closed_square_with_open_neighbors: set[tuple[int, int]],
                                                  closed_squares_with_one_open_neighbour: set[tuple[int, int]],
                                                  ship: list[list[str]]) -> tuple[set,set]:
        '''
            closed_square_open_neighbors is a dict, which stores the number of open neighbors a closed square has
            key is a tuple which has the x and y coordinates of a square and the value gives the number of open neighbors
            the square represented by the key has
        '''
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # left, right, up, down
        for dx, dy in directions:
            nx, ny = recent_open_square[0] + dx, recent_open_square[1] + dy
            if 0 <= nx < len(ship) and 0 <= ny < len(ship) and ship[nx][ny] == 'C':
                if (nx, ny) not in closed_square_with_open_neighbors:
                    if (nx, ny) in closed_squares_with_one_open_neighbour:
                        closed_squares_with_one_open_neighbour.remove((nx, ny))
                        closed_square_with_open_neighbors.add((nx, ny))
                    else:
                        closed_squares_with_one_open_neighbour.add((nx, ny))
        return closed_squares_with_one_open_neighbour, closed_square_with_open_neighbors

        # closed_square_open_neighbors: dict[tuple[int, int], int] = {}
        # fringe: deque[tuple[int, int]] = deque([root_open_square])
        # visited_open_squares: set[tuple[int, int]] = set()
        # while fringe:
        #     current_node = fringe.popleft()
        #     if current_node in visited_open_squares:
        #         continue
        #     x, y = current_node
        #     visited_open_squares.add(current_node)
        #
        #     for dx, dy in directions:
        #         nx, ny = x + dx, y + dy
        #         if 0 <= nx < self.ship_size and 0 <= ny < self.ship_size:  # Checking boundary conditions
        #             if ship[nx][ny] == 'C':
        #                 closed_square_open_neighbors.setdefault((nx, ny), 0)
        #                 closed_square_open_neighbors[(nx, ny)] += 1
        #             elif (nx, ny) not in visited_open_squares:
        #                 fringe.append((nx, ny))
        # closed_squares_with_one_open_neighbour = [key for key, value in closed_square_open_neighbors.items() if
        #                                           value == 1]
        # return closed_squares_with_one_open_neighbour

    def get_dead_ends(self, ship: list[list[str]]) -> tuple[
        list[tuple[int, int]], dict[tuple[int, int], list[tuple[int, int]]]]:
        dead_ends: list[tuple[int, int]] = []
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # left, right, up, down
        open_cells_closed_neighbors_map: dict[tuple[int, int], list[tuple[int, int]]] = {}
        for x in range(len(ship)):
            for y in range(len(ship)):
                if ship[x][y] == 'O':  # Check for open cells
                    open_neighbors = 0
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(ship) and 0 <= ny < len(ship):  # Check for open neighbors within bounds
                            if ship[nx][ny] == 'O':
                                open_neighbors += 1
                                if open_neighbors > 1:
                                    break
                            elif ship[nx][ny] == 'C':
                                open_cells_closed_neighbors_map.setdefault((x, y), [])
                                open_cells_closed_neighbors_map[(x, y)].append((nx, ny))
                    if open_neighbors == 1:
                        dead_ends.append((x, y))

        return dead_ends, open_cells_closed_neighbors_map
