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
                            required=False, type=float,
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
    time_constraint_parser = subparsers.add_parser('time_constraint',
                                      help='Run simulation with all bot 4 variants')
    add_arguments_to_parser(time_constraint_parser)
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
    sampling_index = 50
    if args.command == 'all_bots':
        alive_metrics, success_metrics, _, _ = run_simulations_over_krange(args.ship_size, kRange,
                                                                           sampling_index,
                                                                           args.time_constraint,
                                                                           [BotType.BOT1, BotType.BOT2, BotType.BOT3,
                                                                            BotType.BOT4], False)
    elif args.command == 'Bot4_tune':
        alive_metrics, success_metrics, _, _ = run_simulations_over_krange(args.ship_size, kRange,
                                                                           500,
                                                                           10000000,
                                                                           [BotType.BOT3,
                                                                            BotType.BOT4,
                                                                            BotType.BOT4RiskSigmoidRiskFactor2nRadius2,
                                                                            BotType.BOT4RiskSigmoidRiskFactor2nRadius4,
                                                                            BotType.BOT4RiskSigmoidRiskFactor1nRadius3,
                                                                            BotType.BOT4RiskSigmoidRiskFactor4nRadius3,
                                                                            BotType.BOT4RiskSigmoidRiskFactor2nRadius3,
                                                                            BotType.BOT4RiskTanHRiskFactor2nRadius3,
                                                                            ],
                                                                           False)
    elif args.command == 'time_constraint':
        alive_metrics, success_metrics,avg_number_of_times_time_constraint_breached, avg_step_computation_time_for_bots = run_simulations_over_krange(
            args.ship_size, kRange,
            sampling_index,
            args.time_constraint,
            [BotType.BOT1, BotType.BOT2, BotType.BOT3,
             BotType.BOT5], False)
        logging.info(f'Average number of times the time constraint is breached:'
                     f' {avg_number_of_times_time_constraint_breached}')
        logging.info(f'Average time taken for step computation: {avg_step_computation_time_for_bots}')
        plot_metric(avg_number_of_times_time_constraint_breached,kRange,
                    'Avg. number of times time constraint breached','k:Number of aliens',
                    'Avg. number of times time constraint breached by bots vs Number of aliens')
        plot_metric(avg_step_computation_time_for_bots, kRange,
                    'Avg. time taken for step computation', 'k:Number of aliens',
                    'Avg. time taken for step computation by bots vs Number of aliens')
    else:
        alive_metrics, success_metrics, _, _ = run_simulations_over_krange(args.ship_size, kRange,
                                                                     sampling_index,
                                                                     args.time_constraint,
                                                                     [bot_type_by_command[
                                                                          args.command]],
                                                                     False)
    plot_metric(success_metrics,kRange,'Number of times bot succeeds within 1000 steps','k:Number of aliens',
                'Success Rate')
    plot_metric(alive_metrics, kRange, 'Average number of steps bot stays alive when it fails', 'k:Number of aliens',
                'Avg no. of steps bot stays alive')
    plot_metrics(alive_metrics, success_metrics, kRange)
    end_time = time.time()
    logging.info(f'Time taken for entire simulation: {end_time - start_time}')
