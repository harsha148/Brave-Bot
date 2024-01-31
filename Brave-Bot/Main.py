import sys
import Ship
import Spawner
from Bot1 import Bot1

if __name__ == '__main__':
    # Prompt the user to provide the ship size
    ship_size_input = input("Please enter the ship size: ")

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
    number_of_aliens = input("Please enter the number of aliens: ")
    try:
        number_of_aliens = int(number_of_aliens)
    except ValueError:
        print("Invalid input :(, please provide an integer for the ship size!")
        sys.exit(1)
    ship_layout, aliens = spawner.spawn_aliens(number_of_aliens)
    print('aliens spawned')
    print(ship_layout)
    print(aliens)

    ship_layout, captain=spawner.spawn_captain()
    print('Captain Spawned')
    print(ship_layout)
    print(captain)

    bot1 = Bot1(ship_layout, bot_initial_coordinates)

