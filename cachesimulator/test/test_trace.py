from main import main
import unittest
import logging
from cachesimulator.statistics import Statistic
logger = logging.getLogger("cachesimulator.Logger")
logger.setLevel(logging.DEBUG)

class TestTrace(unittest.TestCase):

    def setUp(self):
        print('\n')
        Statistic.reset()

    def test_validation_trace(self):
        """This tests the validation trace file
        """
        logger.info('test_trace_test_1')
        file = r'C:\Users\James H\git\CacheSimulator\data\test_trace.txt'
        main(file)
        # need to check the statistics object contains the correct info
        expected_cache_probes = 2
        expected_cache_access = 2

        expected_private_accesses = 3
        expected_remote_accesses = 6
        expected_off_chip_accesses = 4
        expected_total_accesses = 13
        expected_r_writebacks = 2
        expected_c_writebacks = 1
        expected_invalidations_sent = 5

        return