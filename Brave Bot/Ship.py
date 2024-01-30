import random
class Ship(object):
    def __init__(self, shipsize: int):
        self.shipsize = shipsize

    def generateship(self) -> list:
        # ship is a 2D array which holds information about each square 1 indicates the square is closed and 0
        # indicates it is open
        ship = [[1 for i in range(self.shipsize)] for i in range(self.shipsize)]
        # rootx and rooty represent the coordinates of the first randomly generated open square
        rootx: int = random.randrange(self.shipsize)
        rooty: int = random.randrange(self.shipsize)
        # root stores the coordinates of the first open square which is randomly generated
        root: list[int] = [rootx, rooty]
        # updating the root square to open
        ship[rootx][rooty] = 0
        print('first open square')
        print(root)
        print('Initial ship')
        print(ship)
        while True:
            # closeds1on represents the list of closed squares with only 1 neighbouring square as open
            closeds1on = self.shipbfs(root, ship)
            print('List of closed squares')
            print(closeds1on)
            if (len(closeds1on) == 0):
                break
            # randomly selecting a square from the list of closed squares which have only one open neighbour
            squaretobeopened = random.choice(closeds1on)
            print('Opening Square')
            print(squaretobeopened)
            ship[squaretobeopened[0]][squaretobeopened[1]] = 0
            print('Updated Ship')
            print(ship)
        return ship

    def shipbfs(self, root: list[int], ship: list[list[int]]) -> list[tuple]:
        fringe: list[list[int]] = [root]
        visitedopensquares: list[list[int]] = []
        # closedsquareopenneighbours is a dict, which stores the number of open neighbours a closed square has
        # key is tuple which has the x and y coordinates of a square and the value gives the number of open neighbours
        # the square represented by the key has
        closedsquareopenneighbours: dict[tuple[int], int] = {}
        while len(fringe) > 0:
            # print('fringe')
            # print(fringe)
            currentnode = fringe.pop(0)
            if currentnode in visitedopensquares:
                continue
            x = currentnode[0]
            y = currentnode[1]
            visitedopensquares.append(currentnode)
            # left
            if x != 0:
                child = [x - 1, y]
                if ship[x - 1][y] == 1:
                    if tuple(child) in closedsquareopenneighbours:
                        closedsquareopenneighbours[tuple(child)] += 1
                    else:
                        closedsquareopenneighbours[tuple(child)] = 1
                else:
                    if child not in visitedopensquares:
                        fringe.append(child)
            # right
            if x != (len(ship) - 1):
                child = [x + 1, y]
                if ship[x + 1][y] == 1:
                    if tuple(child) in closedsquareopenneighbours:
                        closedsquareopenneighbours[tuple(child)] += 1
                    else:
                        closedsquareopenneighbours[tuple(child)] = 1
                else:
                    if child not in visitedopensquares:
                        fringe.append(child)
            # up
            if y != 0:
                child = [x, y - 1]
                if ship[x][y - 1] == 1:
                    if tuple(child) in closedsquareopenneighbours:
                        closedsquareopenneighbours[tuple(child)] += 1
                    else:
                        closedsquareopenneighbours[tuple(child)] = 1
                else:
                    if child not in visitedopensquares:
                        fringe.append(child)
            # down
            if y != (len(ship) - 1):
                child = [x, y + 1]
                if ship[x][y + 1] == 1:
                    if tuple(child) in closedsquareopenneighbours:
                        closedsquareopenneighbours[tuple(child)] += 1
                    else:
                        closedsquareopenneighbours[tuple(child)] = 1
                else:
                    if child not in visitedopensquares:
                        fringe.append(child)
        closeds1on: list[tuple[int]] = []
        for key in closedsquareopenneighbours:
            if closedsquareopenneighbours[key] == 1:
                closeds1on.append(key)
        return closeds1on


if __name__ == '__main__':
    ship = Ship(3)
    x = ship.generateship()
    print(x)
