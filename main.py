from cachesimulator.trace_parser import parse
from cachesimulator.config import NUMBER_OF_CACHES
from cachesimulator.directory import Directory
from cachesimulator.cache import Cache
from cachesimulator.statistics import Statistic, save_statistics
import logging
logger = logging.getLogger('cachesimulator.Logger')
logger.setLevel(logging.INFO)

def main(trace_file):
    # get the parsed text
    parsed_text = parse(trace_file)
    # create the directory
    directory = Directory()
    # create the caches
    caches = [Cache(x, directory=directory) for x in range(NUMBER_OF_CACHES)]
    # append the caches to the directory
    for c in caches:
        directory.append_sharer(c)
    
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
            logger.info(Statistic.key_statistics())
            input()
        elif(command == 'W'):
            Statistic.add_instructions()
            cache.write(address)
            # logger.info(Statistic.debug_statistics())

            Statistic.end_instruction()
            logger.info(Statistic.key_statistics())
            input()
        # deal with other stuff
        elif(command == 'v'):
            print('switch line by line reading')
            if (logger.level != logging.INFO):
                logger.setLevel(logging.INFO)
            else:
                logger.setLevel(logging.WARNING)
        elif(command == 'h'):
            print(f"{Statistic.hit_rate()}")
        elif(command == 'p'):
            print('Print out cache content')
    print(Statistic.key_statistics())
    # save statistics to file
    save_statistics(trace_file)


if __name__ == '__main__':
    trace1 = r'C:\Users\James H\git\CacheSimulator\data\trace1.txt'
    main(trace1)