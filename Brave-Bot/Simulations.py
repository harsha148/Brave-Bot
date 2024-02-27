import copy
import logging
import sys
from tkinter import Tk, ttk

from Alien import alien_step
from Bot1 import Bot1
from Bot2 import Bot2
from Bot3 import Bot3
from Bot4 import Bot4
from Bot5 import Bot5
from Ship import Ship
from Spawner import Spawner
from Status import Status
import matplotlib.pyplot as plt

from utilities.Utility import get_num_of_open_cells
from utilities.constants import BotType


def show_tkinter(ship_layout: list[list[int]]):
    """
    :param ship_layout: layout of the ship as a 2D matrix with each element representing whether the cell at that
                        coordinates is open/closed/occupied by someone(Eg: Alien/Bot/Captain)
    :return: None
    """
    root = Tk()
    table = ttk.Frame(root)
    table.grid()
    ship_dimension = len(ship_layout)
    for row in range(ship_dimension):
        for col in range(ship_dimension):
            label = ttk.Label(table, text=ship_layout[row][col], borderwidth=1, relief="solid")
            label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
    root.mainloop()


def run_simulation(ship: list[list[int]], bot,
                   alien_positions: list[tuple[int, int]], is_show_tkinter: bool) -> \
        tuple[int, Status]:
    """
    :param ship: layout of the ship as a 2D matrix with each element representing whether the cell at that
                        coordinates is open/closed/occupied by someone(Eg: Alien/Bot/Captain)
    :param bot: an object of the bot
    :param alien_positions: set containing the positions of aliens.
    :param is_show_tkinter: flag based on which a tkinter GUI depicting the ship is displaying at each step of the
                            simulation
                            (tkinter slows down the simulation a lot after ship dimension 20)
    :return: the final status of the bot (whether the bot succeeded/failed within 1000 steps) and the number of steps
             taken
    """
    status = Status.INPROCESS
    number_of_steps = 0
    D = len(ship)
    while status == Status.INPROCESS and number_of_steps < 1000:
        if is_show_tkinter:
            show_tkinter(ship)
        status, ship, current_bot_square = bot.step()
        if status != Status.INPROCESS:
            break
        status, ship, alien_positions = alien_step(ship, alien_positions)
        number_of_steps += 1
    if status == Status.SUCCESS:
        logging.info(f'Bot succeeded after {number_of_steps + 1} steps')
    elif status == Status.FAILURE:
        logging.info(f'Bot failed after {number_of_steps + 1} steps')
    else:
        logging.info(f'Bot failed to reach the captain within 1000 steps, steps:{number_of_steps}')
    return number_of_steps, status


# method for running the ship simulation over a range of number of aliens
# In this method K represents the number of aliens
def run_simulations_over_krange(ship_dim: int, krange: list[int], sampling_index: int, time_constraint: int,
                                bot_types: list[BotType],
                                is_show_tkinter: bool):
    """
    :param ship_dim: dimension of the ship
    :param krange: list of values of K (number of aliens) over which, we want to run the simulations
    :param sampling_index: the number of times, we should run a simulation with a given bot_type and number of aliens
    :param time_constraint: the time constraint for the bot step
    :param bot_types: describes the bot to run the simulation on
    :param is_show_tkinter: flag based on which a tkinter GUI depicting the ship is displaying at each step of the
                            simulation
                            (tkinter slows down the simulation a lot after ship dimension 20)
    :return: return the metrics collected from the simulation.

    """
    # sampling_index determines the number of times we will run the simulation for a single value of k
    # metric that stores the number of times a bot succeeds for a particular value of k
    # logging = coloredlogging()
    success_metrics = {}
    for bot_type in bot_types:
        success_metrics[bot_type.name] = [0] * len(krange)
    # metric that stores the number of times the bot fails to reach the captain within 1000 steps but keeps itself alive
    alive_metrics = {}
    for bot_type in bot_types:
        alive_metrics[bot_type.name] = [0] * len(krange)
    for i in range(len(krange)):
        logging.info('##################################################')
        logging.info(f'Running Simulation with K={krange[i]}')
        logging.info('##################################################')
        for j in range(sampling_index):
            ship = Ship(ship_dim)
            ship_layout, root_open_square = ship.generate_ship_layout()
            spawner = Spawner(ship_layout, root_open_square)
            ship_layout, bot_initial_coordinates = spawner.spawn_bot()
            ship_layout, aliens = spawner.spawn_aliens(krange[i])
            ship_layout, captain = spawner.spawn_captain()
            for a in range(len(bot_types)):
                logging.info('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                logging.info(
                    f'Running the simulation with {bot_types[a].name} and K={krange[i]} for the {j + 1}th time')
                logging.info('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                logging.info(f'The number of open cells in the ship_layout: {get_num_of_open_cells(ship_layout)}')
                temp_ship_layout = copy.deepcopy(ship_layout)
                temp_aliens = copy.deepcopy(aliens)
                bot = get_bot(bot_types[a], temp_ship_layout, bot_initial_coordinates, captain, time_constraint)
                if not bot:
                    logging.error(f'Invalid bot type: {bot_types[a]}')
                    sys.exit(0)
                success_metric = success_metrics[bot_types[a].name]
                alive_metric = alive_metrics[bot_types[a].name]
                number_of_steps, status = run_simulation(temp_ship_layout, bot, temp_aliens, is_show_tkinter)
                if status == Status.SUCCESS:
                    success_metric[i] += 1
                if status == Status.INPROCESS:
                    alive_metric[i] += 1
    logging.info(f'alive metrics:{alive_metrics}')
    logging.info(f'success metrics:{success_metrics}')
    return alive_metrics, success_metrics


# method for plotting bot's success metrics
def plot_metrics(alive_metrics, success_metrics, krange):
    """
    :param alive_metrics: alive_metrics is a dictionary with key as the bot name and the value as the number of times
                          the bot stayed alive without succeeding within 1000 steps
    :param success_metrics:
    :param krange:
    :return:
    """
    logging.info(f'Success Metrics for plot graph function:{success_metrics}')
    fig, (success_metrics_graph, alive_metrics_graph) = plt.subplots(1, 2, figsize=(12, 10))
    for bot in success_metrics:
        logging.info(f'The bot:{bot}')
        success_metrics_graph.plot(krange, success_metrics[bot], label=bot)
    success_metrics_graph.set_title('Success Rate')
    success_metrics_graph.set_xlabel('k')
    success_metrics_graph.set_ylabel('Number of times bot succeeds within 1000 steps')
    success_metrics_graph.legend()
    for bot in alive_metrics:
        alive_metrics_graph.plot(krange, alive_metrics[bot], label=bot)
    alive_metrics_graph.set_title('Alive')
    alive_metrics_graph.set_xlabel('k')
    alive_metrics_graph.set_ylabel('Number of times bot stays alive for 1000 steps')
    alive_metrics_graph.legend()
    plt.show()


def get_bot(bot_type: BotType, ship_layout: list[list[int]], bot_init_coordinates: tuple[int, int], captain,
            time_constraint):
    if bot_type == BotType.BOT1:
        return Bot1(ship_layout, bot_init_coordinates, captain, time_constraint)
    if bot_type == BotType.BOT2:
        return Bot2(ship_layout, bot_init_coordinates, captain, time_constraint)
    if bot_type == BotType.BOT3:
        return Bot3(ship_layout, bot_init_coordinates, captain, time_constraint)
    if bot_type == BotType.BOT4:
        return Bot4(ship_layout, bot_init_coordinates, captain, True, 2 * len(ship_layout), 3)
    if bot_type == BotType.BOT4RiskFactor1nRadius3:
        return Bot4(ship_layout, bot_init_coordinates, captain, True, 1 * len(ship_layout), 3)
    if bot_type == BotType.BOT4RiskFactor2nRadius4:
        return Bot4(ship_layout, bot_init_coordinates, captain, True, 2 * len(ship_layout), 4)
    if bot_type == BotType.BOT4RiskFactor2nRadius2:
        return Bot4(ship_layout, bot_init_coordinates, captain, True, 2 * len(ship_layout), 2)
    if bot_type == BotType.BOT4RiskFactor4nRadius3:
        return Bot4(ship_layout, bot_init_coordinates, captain, True, 4 * len(ship_layout), 3)
    if bot_type == BotType.BOT4RiskLogRiskFactor2nRadius3:
        return Bot4(ship_layout, bot_init_coordinates, captain, True, 4 * len(ship_layout), 3,
                    risk_function_type='LOG')
    if bot_type == BotType.BOT4RiskTanHRiskFactor2nRadius3:
        return Bot4(ship_layout, bot_init_coordinates, captain, True, 4 * len(ship_layout), 3,
                    risk_function_type='TANH')
    if bot_type == BotType.BOT5:
        return Bot5(ship_layout, bot_init_coordinates, captain, time_constraint)
    return None
