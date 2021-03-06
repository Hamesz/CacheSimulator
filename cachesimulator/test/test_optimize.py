from main import main
import unittest
import logging
from cachesimulator.MSI import *
from cachesimulator.cache import Cache, get_address_parameters
from cachesimulator.trace_parser import parse
from cachesimulator.config import NUMBER_OF_CACHES
from cachesimulator.directory import Directory
from cachesimulator.statistics import Statistic, save_statistics
from cachesimulator.optimizer import Optimizer
from data.trace_files import trace1, trace2, optimize_trace
import numpy as np
logger = logging.getLogger("cachesimulator.Logger")
logger.setLevel(logging.WARNING)

class TestOptimize(unittest.TestCase):

    def setUp(self):
        print('\n')
        Statistic.reset()

    # def test_trace1(self):
    #     file = trace1
    #     main(file, optimize=True)

    # def test_trace2(self):
    #     file = trace2
    #     main(file, optimize=True)

    def test_optimized_trace(self):
        file = optimize_trace
        # -- expected_states for address just processed -- #
        special_instructions = [4,6,9.12]
        # lines to watch out for 4,6, 9, 12
        one = [EXCLUSIVE, INVALID, INVALID, INVALID]
        two = [MODIFIED, INVALID, INVALID, INVALID]
        three = [SHARED, SHARED, INVALID, INVALID]
        four = [EXCLUSIVE, INVALID, INVALID, INVALID] # in this time, P1 should go to EXCLUSIVE
        five = [SHARED, SHARED, INVALID, INVALID]
        six = [MODIFIED, INVALID, INVALID, INVALID] # P1 should go to exclusive
        seven = [INVALID, MODIFIED, INVALID, INVALID]
        eight = [SHARED, SHARED, INVALID, INVALID]
        nine = [EXCLUSIVE, INVALID, INVALID, INVALID] # P1 should go to exclusive
        ten = [SHARED, SHARED, INVALID, INVALID]
        eleven = [INVALID, INVALID, INVALID, EXCLUSIVE]
        twelve = [SHARED, INVALID, INVALID, SHARED] # P1 should go to exclusive
        thirteen = [MODIFIED, INVALID, INVALID, INVALID]
        fourteen = [MODIFIED, INVALID, INVALID, INVALID]
        expected_states = [one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen]
        # test it line by line
        parsed_text = parse(file)
        # create the directory
        directory = Directory()
        # create the caches
        caches = [Cache(x, directory=directory) for x in range(NUMBER_OF_CACHES)]
        # append the caches to the directory
        for c in caches:
            directory.append_sharer(c)
        
        # set the optimizer
        Optimizer.OPTIMIZE = True

        # run the main code
        for i, entry in enumerate(parsed_text):
            print()
            cache_id, command, address = entry
            cache = caches[cache_id]
            
            # check the command
            if (command == 'R'):
                Statistic.add_instructions()
                cache.read(address)
                print(Statistic.debug_statistics())
                Statistic.end_instruction()

            elif(command == 'W'):
                Statistic.add_instructions()
                cache.write(address)
                print(Statistic.debug_statistics())
                Statistic.end_instruction()

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

            # check states are proper
            print ('Testing -----------')
            tag, index, offset = get_address_parameters(address, 9, 2)
            actual_states = []
            for c in caches:
                if (c.contains_address(address)):
                    line = c.cachelines[index]
                    state = line.state
                    actual_states.append(state)
                else:
                    actual_state = INVALID
                    actual_states.append(actual_state)

            # compare to actual states
            for idx,actual_state in enumerate(actual_states):
                expected_state = expected_states[i][idx]
                msg = f"Instruction {i+1} ({entry}), processor {idx}\nExpected State: {expected_state} vs actual state: {actual_state} for address {address}"
                self.assertEquals(expected_state, actual_state, msg)

            if (i+1 in special_instructions):
                # check P1 is in state E
                c1 = caches[1]
                line = c1.cachelines[index]
                actual_state = line.state
                expected_state = EXCLUSIVE
                msg = f"Special instruction {i+1}, therfore checking cache {c1} went to E state. It is in state: {actual_state} with tag: {line.tag}"
                self.assertEquals(actual_state, expected_state, msg)
            print(Statistic.key_statistics())
            print(i+1)
            # input()

        # accesses
        expected_private_accesses = 1
        expected_remote_accesses = 8
        expected_off_chip_accesses = 5
        expected_total_accesses = 14
        expected_r_writebacks = 1
        expected_c_writebacks = 2
        expected_invalidations_sent = 3
        # latencies
        expected_priv_average_latency = 2
        expected_rem_average_latency = 21.88
        expected_off_chip_average_latency = 29
        expected_total_latency = 322
        expected_total_average_latency = 23 #.2sf

        # -- Actual -- #
        actual_private_accesses = Statistic.PRIVATE_ACCESSES
        actual_remote_accesses = Statistic.REMOTE_ACCESSES
        actual_off_chip_accesses = Statistic.OFF_CHIP_ACCESS
        actual_total_accesses = actual_private_accesses + actual_remote_accesses + actual_off_chip_accesses 
        actual_r_writebacks = Statistic.REPLACEMENT_WRITEBACKS
        actual_c_writebacks = Statistic.COHERENCE_WRITEBACKS
        actual_invalidations_sent = Statistic.INVALIDATIONS_SENT
        # latencies
        actual_priv_average_latency = Statistic.priv_average_latency()
        actual_rem_average_latency = np.round(Statistic.rem_average_latency(),2)
        actual_off_chip_average_latency = Statistic.off_chip_latency()
        actual_total_latency = Statistic.total_latency()
        actual_total_average_latency = np.round(Statistic.average_latency(),2)

        self.assertEqual(expected_private_accesses,     actual_private_accesses)
        self.assertEqual(expected_remote_accesses,      actual_remote_accesses)
        self.assertEqual(expected_off_chip_accesses,    actual_off_chip_accesses)
        self.assertEqual(expected_total_accesses,       actual_total_accesses)
        self.assertEqual(expected_r_writebacks,         actual_r_writebacks)
        self.assertEqual(expected_c_writebacks,         actual_c_writebacks)
        self.assertEqual(expected_invalidations_sent,   actual_invalidations_sent)
        self.assertEqual(expected_priv_average_latency, actual_priv_average_latency)
        self.assertEqual(expected_rem_average_latency,  actual_rem_average_latency)
        self.assertEqual(expected_off_chip_average_latency, actual_off_chip_average_latency)
        self.assertEqual(expected_total_latency,        actual_total_latency)
        self.assertEqual(expected_total_average_latency, actual_total_average_latency)

