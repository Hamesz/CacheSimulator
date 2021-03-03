from main import main
import unittest
import logging
from cachesimulator.statistics import Statistic
logger = logging.getLogger("cachesimulator.Logger")
logger.setLevel(logging.DEBUG)

class TestMain(unittest.TestCase):

    def setUp(self):
        print('\n')
        Statistic.reset()

    def test_trace_test_1(self):
        """This tests if read miss occurs properly after it has the line in shared
        """
        logger.info('test_trace_test_1')
        file = r'C:\Users\James H\git\CacheSimulator\data\trace_test_RW_no_sharers.txt'
        main(file)
        # need to check the statistics object contains the correct info
        expected_cache_probes = 2
        expected_cache_access = 2
        
        self.check_statistics(expected_cache_probes, expected_cache_access)

    def test_B0(self):
        """Tests:
            P0 perfroms a write
            local state: M
            No sharers
        """
        logger.info('test_B0')
        file = r'C:\Users\James H\git\CacheSimulator\data\tests\b0.txt'
        main(file)

        # expected requests
        expected_cache_access = 2
        expected_cache_probes = 2
        expected_directory_request = 4
        expected_directory_access = 2
        expected_memory_accesses = 1
        expected_processor_hops = 0

        # expected latency

        # read -> tag, read, dir req, dir acc, mem, dir req, probe, write
        expected_average_latency = 1 + 1 + 5 + 1 + 15 + 5 + 1 + 1
        # write -> tag, read, dir req, dir acc, mem, dir req, probe, write
        expected_average_latency = expected_average_latency + 1 + 1 + 5 + 1 + 15 + 5 + 1 + 1

        # actual
        actual_cache_access       = Statistic.CACHE_ACCESSES
        actual_cache_probes       = Statistic.CACHE_PROBES
        actual_directory_request  = Statistic.DIRECTORY_HOPS
        actual_directory_access   = Statistic.DIRECTORY_ACCESSES
        actual_memory_accesses    = Statistic.MEMORY_ACCESSES
        actual_processor_hops     = Statistic.PROCESSOR_HOPS

        # equate
        self.assertEqual(expected_cache_access, actual_cache_access)
        self.assertEqual(expected_cache_probes, actual_cache_probes)
        self.assertEqual(expected_directory_access, actual_directory_access)
        self.assertEqual(expected_directory_request, actual_directory_request)
        self.assertEqual(expected_memory_accesses, actual_memory_accesses)
        self.assertEqual(expected_processor_hops, actual_processor_hops)

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

        self.check_statistics(expected_cache_probes, expected_cache_access)
        return


    def check_statistics(self, expected_cache_probes, expected_cache_access):
        # actual
        actual_cache_probes = Statistic.CACHE_PROBES
        actual_cache_access = Statistic.CACHE_ACCESSES

        self.assertEqual(expected_cache_access, actual_cache_access)
        self.assertEqual(expected_cache_probes, actual_cache_probes)