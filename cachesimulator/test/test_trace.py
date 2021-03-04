from main import main
import unittest
import numpy as np
import logging
from cachesimulator.statistics import Statistic
logger = logging.getLogger("cachesimulator.Logger")
logger.setLevel(logging.INFO)

class TestTrace(unittest.TestCase):

    def setUp(self):
        print('\n')
        Statistic.reset()

    def test_val2_trace(self):
        logger.info('test_trace_test_2')
        file = r'C:\Users\James H\git\CacheSimulator\data\trace_addr_1.txt'
        main(file)

        # -- Expected -- #
        # accesses
        expected_private_accesses = 4
        expected_remote_accesses = 4
        expected_off_chip_accesses = 1
        expected_total_accesses = 9
        expected_r_writebacks = 0
        expected_c_writebacks = 1
        expected_invalidations_sent = 2
        # latencies
        # expected_priv_average_latency = 2
        # expected_rem_average_latency = 21
        # expected_off_chip_average_latency = 29
        expected_total_latency = 124
        # expected_total_average_latency = 19.21  #.2sf

        # -- Actual -- #
        actual_private_accesses = Statistic.PRIVATE_ACCESSES
        actual_remote_accesses = Statistic.REMOTE_ACCESSES
        actual_off_chip_accesses = Statistic.OFF_CHIP_ACCESS
        actual_total_accesses = actual_private_accesses + actual_remote_accesses + actual_off_chip_accesses 
        actual_r_writebacks = Statistic.REPLACEMENT_WRITEBACKS
        actual_c_writebacks = Statistic.COHERENCE_WRITEBACKS
        actual_invalidations_sent = Statistic.INVALIDATIONS_SENT
        # latencies
        # actual_priv_average_latency = Statistic.priv_average_latency()
        # actual_rem_average_latency = Statistic.rem_average_latency()
        # actual_off_chip_average_latency = Statistic.off_chip_latency()
        actual_total_latency = Statistic.total_latency()
        # actual_total_average_latency = np.round(Statistic.average_latency(),2)

        self.assertEqual(expected_private_accesses,     actual_private_accesses)
        self.assertEqual(expected_remote_accesses,      actual_remote_accesses)
        self.assertEqual(expected_off_chip_accesses,    actual_off_chip_accesses)
        self.assertEqual(expected_total_accesses,       actual_total_accesses)
        self.assertEqual(expected_r_writebacks,         actual_r_writebacks)
        self.assertEqual(expected_c_writebacks,         actual_c_writebacks)
        self.assertEqual(expected_invalidations_sent,   actual_invalidations_sent)
        # self.assertEqual(expected_priv_average_latency, actual_priv_average_latency)
        # self.assertEqual(expected_rem_average_latency,  actual_rem_average_latency)
        # self.assertEqual(expected_off_chip_average_latency, actual_off_chip_average_latency)
        self.assertEqual(expected_total_latency,        actual_total_latency)
        # self.assertEqual(expected_total_average_latency, actual_total_average_latency)

    def test_validation_trace(self):
        """This tests the validation trace file
        """
        logger.info('test_trace_test_1')
        file = r'C:\Users\James H\git\CacheSimulator\data\test_trace.txt'
        main(file)
        # need to check the statistics object contains the correct info
        # expected_cache_probes = 2
        # expected_cache_access = 2

        # -- Expected -- #
        # accesses
        expected_private_accesses = 3
        expected_remote_accesses = 7
        expected_off_chip_accesses = 5
        expected_total_accesses = 15
        expected_r_writebacks = 2
        expected_c_writebacks = 1
        expected_invalidations_sent = 5
        # latencies
        expected_priv_average_latency = 2
        expected_rem_average_latency = 21
        expected_off_chip_average_latency = 29
        expected_total_latency = 298
        expected_total_average_latency = 19.87 #.2sf

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
        actual_rem_average_latency = Statistic.rem_average_latency()
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

        return