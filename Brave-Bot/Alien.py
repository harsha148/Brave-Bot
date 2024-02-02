import random

from Status import Status


def alien_step(ship_layout: list[list[str]], aliens: list[tuple[int, int]]) -> tuple[
    Status, list[list[str]], list[tuple[int, int]]]:
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # left, right, up, down
    random.shuffle(aliens)  # randomizing the order in which the aliens move
    rules_for_updating_new_alien_square = {'CP': 'CP&A', 'O': 'A'}
    for i in range(len(aliens)):
        alien_x, alien_y = aliens[i]
        possible_steps = []
        for dx, dy in directions:
            nx, ny = alien_x + dx, alien_y + dy
            if 0<=nx<len(ship_layout) and 0<=ny<len(ship_layout[0]):
                if ship_layout[nx][ny] != 'C' and ship_layout[nx][ny] != 'A' and ship_layout[nx][ny] != 'CP&A':
                    possible_steps.append((nx, ny))
        if not possible_steps:
            continue
        nx, ny = random.choice(possible_steps)
        aliens[i] = (nx, ny)
        # updating the current square of alien to remove alien
        if ship_layout[alien_x][alien_y] == 'CP&A':
            ship_layout[alien_x][alien_y] = 'CP'
        elif ship_layout[alien_x][alien_y] == 'A':
            ship_layout[alien_x][alien_y] = 'O'
        # updating the randomly selected next square of alien to place the alien
        if ship_layout[nx][ny] == 'B':
            ship_layout[nx][ny] = 'B&A'
            return Status.FAILURE, ship_layout, aliens
        else:
            ship_layout[nx][ny] = rules_for_updating_new_alien_square[ship_layout[nx][ny]]

    return Status.INPROCESS, ship_layout, aliens
