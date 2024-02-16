import sys
from tkinter import Tk, ttk

from Alien import alien_step
from Bot1 import Bot1
from Bot2 import Bot2
from Ship import Ship
from Spawner import Spawner
from Status import Status
import matplotlib.pyplot as plt


def show_tkinter(ship_layout: list[list[int]]):
    root = Tk()
    table = ttk.Frame(root)
    table.grid()
    ship_dimension = len(ship_layout)
    for row in range(ship_dimension):
        for col in range(ship_dimension):
            label = ttk.Label(table, text=ship_layout[row][col], borderwidth=1, relief="solid")
            label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
    root.mainloop()


def run_simulation(ship_layout: list[list[int]], bot, current_bot_square: tuple[int, int],
                   alien_positions: list[tuple[int, int]], is_show_tkinter: bool) -> tuple[int, Status]:
    status = Status.INPROCESS
    number_of_steps = 0
    D = len(ship_layout)
    while status == Status.INPROCESS and number_of_steps < 1000:
        if is_show_tkinter:
            show_tkinter(ship_layout)
        status, ship_layout, current_bot_square = bot.step(ship_layout, current_bot_square)
        if status != Status.INPROCESS:
            break
        status, ship_layout, alien_positions = alien_step(ship_layout, alien_positions)
        number_of_steps += 1
    if status == Status.SUCCESS:
        print(f'Bot succeeded after {number_of_steps} steps')
    elif status == Status.FAILURE:
        print(f'Bot failed after {number_of_steps} steps')
    return number_of_steps, status


# method for running the ship simulation over a range of number of aliens
# In this method K represents the number of aliens
def run_simulations_over_krange(ship_dim: int, krange: list[int], sampling_index: int, is_show_tkinter: bool):
    # sampling_index determines the number of times we will run the simulation for a single value of k
    # metric that stores the number of times a bot succeeds for a particular value of k
    success_metrics = [0] * len(krange)
    # metric that stores the number of times the bot fails to reach the captain within 1000 steps but keeps itself alive
    alive_metrics = [0] * len(krange)
    for i in range(len(krange)):
        print(f'Running Simulation with K={krange[i]}')
        for j in range(sampling_index):
            ship = Ship(ship_dim)
            ship_layout, root_open_square = ship.generate_ship_layout()
            spawner = Spawner(ship_layout, root_open_square)
            ship_layout, bot_initial_coordinates = spawner.spawn_bot()
            print(f'Running the simulation with K={krange[i]} for the {j + 1}th time')
            ship_layout, aliens = spawner.spawn_aliens(krange[i])
            ship_layout, captain = spawner.spawn_captain()
            bot = Bot2(ship_layout, bot_initial_coordinates, captain)
            number_of_steps, status = run_simulation(ship_layout, bot, bot_initial_coordinates, aliens, is_show_tkinter)
            if status == Status.SUCCESS:
                success_metrics[i] += 1
            if status == Status.INPROCESS:
                alive_metrics[i] += 1
    print(f'alive metrics:{alive_metrics}')
    print(f'success metrics:{success_metrics}')
    fig, (success_metrics_graph, alive_metrics_graph) = plt.subplots(1, 2, figsize=(12, 10))
    success_metrics_graph.plot(krange, success_metrics)
    success_metrics_graph.set_title('Success Rate')
    success_metrics_graph.set_xlabel('k')
    success_metrics_graph.set_ylabel('Number of times bot succeeds within 1000 steps')
    alive_metrics_graph.plot(krange, alive_metrics)
    alive_metrics_graph.set_title('Alive')
    alive_metrics_graph.set_xlabel('k')
    alive_metrics_graph.set_ylabel('Number of times bot stays alive for 1000 steps')
    plt.show()
