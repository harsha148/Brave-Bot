from Simulations import *

if __name__ == '__main__':
    # Prompt the user to provide the ship size
    ship_size_input = input("Please enter the ship size: ")

    try:
        ship_size = int(ship_size_input)
    except ValueError:
        print("Invalid input :(, please provide an integer for the ship size!")
        sys.exit(1)
    try:
        k_min = int(input('Please enter the minimum value of k'))
    except ValueError:
        print('Invalid input :(, please provide an integer!')
    try:
        k_max = int(input('Please enter the maximum value of k'))
    except ValueError:
        print('Invalid input :(, please provide an integer!')
    try:
        k_step = int(input('Please enter the step value for generating the range of values for k'))
    except ValueError:
        print('Invalid input :(, please provide an integer!')
    krange = []
    k = int(k_min)
    while k <= int(k_max):
        krange.append(k)
        k += int(k_step)
    run_simulations_over_krange(ship_size, krange, 10, True)
