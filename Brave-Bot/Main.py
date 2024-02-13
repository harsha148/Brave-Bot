import sys
from Ship import Ship
from Spawner import Spawner
from Alien import alien_step
from Bot2 import Bot2
from Status import Status
from tkinter import *
from tkinter import ttk

def run_simulation(ship_layout, bot, alien_positions):
    status = Status.INPROCESS
    number_of_steps = 0

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
        print(f"\nSimulation step {number_of_steps}")
        status, new_bot_position = bot.step()
        print(f'The current position of the bot is {new_bot_position}')
        if status != Status.INPROCESS:
            break
        status, ship_layout, alien_positions = alien_step(ship_layout, alien_positions)
        print(f"Updated alien positions: {alien_positions}")

        number_of_steps += 1

    if status == Status.SUCCESS:
        print(f'Bot succeeded after {number_of_steps} steps')
    elif status == Status.FAILURE:
        print(f'Bot failed after {number_of_steps} steps')
    return number_of_steps


if __name__ == '__main__':
    # Prompt the user to provide the ship size
    ship_size_input = input("Please enter the ship size: ")

    try:
        ship_size = int(ship_size_input)
    except ValueError:
        print("Invalid input :(, please provide an integer for the ship size!")
        sys.exit(1)

    ship = Ship(ship_size)
    ship_layout, root_open_square = ship.generate_ship_layout()
    print(ship_layout)
    spawner = Spawner(ship_layout, root_open_square)

    # Spawn the bot, aliens, and captain, initializing their positions on the ship layout
    ship_layout, bot_initial_coordinates = spawner.spawn_bot()
    print('Bot Spawned at:', bot_initial_coordinates)
    print(f'Ship_layout {ship_layout}')

    number_of_aliens = input("Please enter the number of aliens: ")
    try:
        number_of_aliens = int(number_of_aliens)
    except ValueError:
        print("Invalid input :(, please provide an integer for the number of aliens")
        sys.exit(1)
    ship_layout, aliens_positions = spawner.spawn_aliens(number_of_aliens)
    print(f'{number_of_aliens} Aliens spawned at positions: {aliens_positions}')
    print(f'Ship_layout {ship_layout}')

    ship_layout, captain_position = spawner.spawn_captain()
    print('Captain Spawned at:', captain_position)
    print(f'Ship_layout {ship_layout}')

    bot2 = Bot2(ship_layout, bot_initial_coordinates, captain_position)
    run_simulation(ship_layout, bot2, aliens_positions)
