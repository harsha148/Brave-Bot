import copy
import logging
import time

from Simulations import *
import argparse


def add_arguments_to_parser(bot_parser):
    """
    :param bot_parser:
    :return: None
    """
    bot_parser.add_argument('-sd', '--ship_size',
                            required=True, type=int,
                            help='The dimension of the ship layout')
    bot_parser.add_argument('-k1', '--k_min',
                            required=True, type=int,
                            help='The minimum value of K(number of aliens) in the range of K')
    bot_parser.add_argument('-k2', '--k_max',
                            required=True, type=int,
                            help='The maximum value of K(number of aliens) in the range of K')
    bot_parser.add_argument('-ks', '--k_step',
                            required=True, type=int,
                            help='The step size of values of K')
    bot_parser.add_argument('-t', '--time_constraint', default=100000,
                            required=False, type=int,
                            help='The time constraint for the bot step')


if __name__ == '__main__':
    start_time = time.time()
    logger = logging.getLogger('log')
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version='1.0')
    subparsers = parser.add_subparsers(dest='command', required=True)
    # mapping between the commands and the bot type enum
    bot_type_by_command = {
        'bot1': BotType.BOT1,
        'bot2': BotType.BOT2,
        'bot3': BotType.BOT3,
        'bot4': BotType.BOT4,
        'bot5': BotType.BOT5
    }
    bot1Parse = subparsers.add_parser('bot1',
                                      help='Run simulation with Bot1')
    add_arguments_to_parser(bot1Parse)
    bot2Parse = subparsers.add_parser('bot2',
                                      help='Run simulation with bot2')
    add_arguments_to_parser(bot2Parse)
    bot3Parse = subparsers.add_parser('bot3',
                                      help='Run simulation with bot3')
    add_arguments_to_parser(bot3Parse)
    bot4Parse = subparsers.add_parser('bot4',
                                      help='Run simulation with bot4')
    add_arguments_to_parser(bot4Parse)
    bot5Parse = subparsers.add_parser('bot5',
                                      help='Run simulation with bot5')
    add_arguments_to_parser(bot5Parse)
    all_botsParse = subparsers.add_parser('all_bots',
                                          help='Run simulation with all the bots')
    add_arguments_to_parser(all_botsParse)
    Bot4_tune = subparsers.add_parser('Bot4_tune',
                                      help='Run simulation with all bot 4 variants')
    add_arguments_to_parser(Bot4_tune)
    args = parser.parse_args()
    if args.k_max < args.k_min:
        logging.error('K_max value is lesser than K_min')
        sys.exit(0)
    kRange = []
    k = args.k_min
    while k <= args.k_max:
        kRange.append(k)
        k += args.k_step
    alive_metrics = {}
    success_metrics = {}
    # sampling_index determines the number of times we will run the simulation for a single value of k
    sampling_index = 500
    if args.command == 'all_bots':
        alive_metrics, success_metrics = run_simulations_over_krange(args.ship_size, kRange,
                                                                     sampling_index,
                                                                     args.time_constraint,
                                                                     [BotType.BOT1, BotType.BOT2, BotType.BOT3,
                                                                      BotType.BOT4], False)
    elif args.command == 'Bot4_tune':
        alive_metrics, success_metrics = run_simulations_over_krange(args.ship_size, kRange,
                                                                     500,
                                                                     10000000,
                                                                     [BotType.BOT3,
                                                                      BotType.BOT4RiskFactor2nRadius2,
                                                                      BotType.BOT4,
                                                                      BotType.BOT4RiskFactor2nRadius4,
                                                                      BotType.BOT4RiskFactor1nRadius3,
                                                                      BotType.BOT4RiskFactor4nRadius3,
                                                                      BotType.BOT4RiskLogRiskFactor2nRadius3,
                                                                      BotType.BOT4RiskTanHRiskFactor2nRadius3,
                                                                      ],
                                                                     False)
    else:
        alive_metrics, success_metrics = run_simulations_over_krange(args.ship_size, kRange,
                                                                     sampling_index,
                                                                     args.time_constraint,
                                                                     [bot_type_by_command[
                                                                          args.command]],
                                                                     False)

    plot_metrics(alive_metrics, success_metrics, kRange)
    end_time = time.time()
    logging.info(f'Time taken for entire simulation: {end_time - start_time}')
