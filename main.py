from cachesimulator.trace_parser import parse
from cachesimulator.config import NUMBER_OF_CACHES
from cachesimulator.directory import Directory
from cachesimulator.cache import Cache
from cachesimulator.statistics import Statistic, save_statistics
from cachesimulator.optimizer import Optimizer
from data.trace_files import trace1, trace2, test_trace
import sys
import logging

logger = logging.getLogger('cachesimulator.Logger')
logger.setLevel(logging.WARNING)


def main(trace_file, optimize=False):
    # get the parsed text
    parsed_text = parse(trace_file)
    # create the directory
    directory = Directory()
    # create the caches
    caches = [Cache(x, directory=directory) for x in range(NUMBER_OF_CACHES)]
    # append the caches to the directory
    for c in caches:
        directory.append_sharer(c)

    # set the optimizer
    Optimizer.OPTIMIZE = optimize
    # run the main code
    for entry in parsed_text:
        cache_id, command, address = entry
        cache = caches[cache_id]

        # check the command
        if (command == 'R'):
            Statistic.add_instructions()
            cache.read(address)
            # logger.info(Statistic.debug_statistics())

            Statistic.end_instruction()
            # logger.info(Statistic.key_statistics())
            # input()
        elif(command == 'W'):
            Statistic.add_instructions()
            cache.write(address)
            # logger.info(Statistic.debug_statistics())

            Statistic.end_instruction()
            # logger.info(Statistic.key_statistics())
            # input()
        # deal with other stuff
        elif(command == 'v'):
            # print('switch line by line reading')
            if (logger.level != logging.INFO):
                logger.setLevel(logging.INFO)
            else:
                logger.setLevel(logging.WARNING)
        elif(command == 'h'):
            print(f"Hit Rate: {Statistic.hit_rate()}")
        elif(command == 'p'):
            for c in caches:
                contents = c.cache_contents()
                print(f"Cache {c} contents:\n{contents}")
    print()
    print(Statistic.key_statistics())
    # print(Statistic.debug_statistics())
    # save statistics to file
    save_statistics(trace_file)


if __name__ == '__main__':

    args = sys.argv[1:]
    # first arg should be trace file
    trace_file = args[0]
    # global OPTIMIZE
    optimize = (( args[1]) == "True")

    main(trace_file, optimize=optimize)
