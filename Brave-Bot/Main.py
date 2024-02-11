import sys
import Ship
import Spawner
from Alien import alien_step
from Bot1 import Bot1
from Status import Status
from tkinter import *
from tkinter import ttk


def run_simulation(ship_layout: list[list[int]], bot, current_bot_square: tuple[int, int],
                   alien_positions: list[tuple[int, int]]):
    status = Status.INPROCESS
    number_of_steps = 0
    D = len(ship_layout)
    for i in range(D):
        for j in range(D):
            if ship_layout[i][j] == 'CP' or ship_layout[i][j] == 'CP&A':
                print(f'The position of captain {i},{j}')
                break
    while status == Status.INPROCESS:
        root = Tk()
        table = ttk.Frame(root)
        table.grid()
        ship_dimension = len(ship_layout)
        print(f'After {number_of_steps} steps, the state is:')
        for row in range(ship_dimension):
            for col in range(ship_dimension):
                label = ttk.Label(table, text=ship_layout[row][col], borderwidth=1, relief="solid")
                label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        root.mainloop()
        status, ship_layout, current_bot_square = bot.step(ship_layout, current_bot_square)
        print(f'The current position of the bot is {current_bot_square}')
        if status != Status.INPROCESS:
            break
        status, ship_layout, alien_positions = alien_step(ship_layout, alien_positions)
        print('Alien positions')
        print(aliens)
        number_of_steps += 1
    if status == Status.SUCCESS:
        print(f'Bot succeeded after {number_of_steps} steps')
    elif status == Status.FAILURE:
        print(f'Bot failed after {number_of_steps} steps')
    return number_of_steps


if __name__ == '__main__':
    # Prompt the user to provide the ship size
    ship_size_input = 10#input("Please enter the ship size: ")

    try:
        ship_size = int(ship_size_input)
    except ValueError:
        print("Invalid input :(, please provide an integer for the ship size!")
        sys.exit(1)

    ship = Ship.Ship(ship_size)
    ship_layout, root_open_square = ship.generate_ship_layout()
    print(ship_layout)
    spawner = Spawner.Spawner(ship_layout, root_open_square)
    ship_layout, bot_initial_coordinates = spawner.spawn_bot()
    print('Bot Spawned')
    print('ship layout')
    print(ship_layout)
    number_of_aliens = 5#input("Please enter the number of aliens: ")
    try:
        number_of_aliens = int(number_of_aliens)
    except ValueError:
        print("Invalid input :(, please provide an integer for the ship size!")
        sys.exit(1)
    ship_layout, aliens = spawner.spawn_aliens(number_of_aliens)
    print('aliens spawned')
    print(ship_layout)
    print(aliens)

    ship_layout, captain = spawner.spawn_captain()
    print('Captain Spawned')
    print(ship_layout)
    print(captain)

    bot1 = Bot1(ship_layout, bot_initial_coordinates)
    run_simulation(ship_layout, bot1, bot_initial_coordinates, aliens)
