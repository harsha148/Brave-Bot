import sys
import random
from collections import deque


class Ship(object):
    def __init__(self, shipsize: int):
        self.shipsize = shipsize

    def generateship(self) -> list:
        # ship is a 2D array which holds information about each square
        # 1 indicates the square is closed and 0 indicates it is open
        ship = [[1 for _ in range(self.shipsize)] for _ in range(self.shipsize)]
        # rootx and rooty represent the coordinates of the first randomly generated open square
        rootx: int = random.randrange(self.shipsize)
        rooty: int = random.randrange(self.shipsize)
        # root stores the coordinates of the first open square which is randomly generated
        root: tuple[int, int] = (rootx, rooty)
        # updating the root square to open
        ship[rootx][rooty] = 0
        print(f'first open square: {root}')
        print(f'Initial ship : {ship}')
        while True:
            # closeds1on represents the list of closed squares with only 1 neighboring square as open
            closeds1on = self.get_closed_squares_with_one_open_neighbor(root, ship)
            print(f'List of closed cells with 1 neighbor open: {closeds1on}')
            if not closeds1on:
                break
            # randomly selecting a square from the list of closed squares which have only one open neighbor
            squaretobeopened = random.choice(closeds1on)
            print(f'Opening Square {squaretobeopened}')
            ship[squaretobeopened[0]][squaretobeopened[1]] = 0
            print(f'Updated Ship {ship}')

        opens1on, closed_neighbors_of_dead_cells = self.get_dead_ends(ship)
        print(f'List of open cells with 1 neighbor open: {opens1on}')
        # print(f'Map of dead cells and their closed neighbors: {closed_neighbors_of_dead_cells}')
        # randomly selecting half the dead cells
        random_opens1on = random.sample(opens1on, int(len(opens1on)/2))
        for cell in random_opens1on:
            closed_neighbors = closed_neighbors_of_dead_cells[cell]
            random_closed_neighbor = random.choice(closed_neighbors)
            ship[random_closed_neighbor[0]][random_closed_neighbor[1]] = 0
            print(f'Updated Ship {ship}')
        return ship

    def get_closed_squares_with_one_open_neighbor(self, root: tuple[int, int], ship: list[list[int]]) -> list[tuple]:
        fringe: deque[tuple[int, int]] = deque([root])
        visitedopensquares: set[tuple[int, int]] = set()
        # closedsquareopenneighbors is a dict, which stores the number of open neighbors a closed square has
        """key is a tuple which has the x and y coordinates of a square and the value gives the number of open neighbors
        the square represented by the key has"""
        closedsquareopenneighbors: dict[tuple[int, int], int] = {}
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # left, right, up, down
        while fringe:
            currentnode = fringe.popleft()
            if currentnode in visitedopensquares:
                continue
            x, y = currentnode
            visitedopensquares.add(currentnode)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.shipsize and 0 <= ny < self.shipsize:  # Checking boundary conditions
                    if ship[nx][ny] == 1:
                        closedsquareopenneighbors.setdefault((nx, ny), 0)
                        closedsquareopenneighbors[(nx, ny)] += 1
                    elif (nx, ny) not in visitedopensquares:
                        fringe.append((nx, ny))

        closeds1on = [key for key, value in closedsquareopenneighbors.items() if value == 1]
        return closeds1on

    def get_dead_ends(self, ship: list[list[int]]) -> tuple[list[tuple[int, int]], dict[tuple[int, int], list[tuple[int, int]]]]:
        dead_ends: list[tuple[int, int]] = []
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # left, right, up, down
        open_cells_closed_neighbors_map: dict[tuple[int, int], list[tuple[int, int]]] = {}
        for x in range(len(ship)):
            for y in range(len(ship)):
                if ship[x][y] == 0:  # Check for open cells
                    open_neighbors = 0
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(ship) and 0 <= ny < len(ship):  # Check for open neighbors within bounds
                            if ship[nx][ny] == 0:
                                open_neighbors += 1
                                if open_neighbors > 1:
                                    break
                            elif ship[nx][ny] == 1:
                                open_cells_closed_neighbors_map.setdefault((x,y), [])
                                open_cells_closed_neighbors_map[(x,y)].append((nx, ny))
                    if open_neighbors == 1:
                        dead_ends.append((x, y))

        return dead_ends, open_cells_closed_neighbors_map

if __name__ == '__main__':
    # Prompt the user to provide the ship size
    ship_size_input = input("Please enter the ship size: ")

    try:
        ship_size = int(ship_size_input)
    except ValueError:
        print("Invalid input :(, please provide an integer for the ship size!")
        sys.exit(1)

    ship = Ship(ship_size)
    x = ship.generateship()
    print(x)
