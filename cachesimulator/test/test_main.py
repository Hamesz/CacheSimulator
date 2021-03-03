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
        expected_cache_probes = 4
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


    def check_statistics(self, expected_cache_probes, expected_cache_access):
        # actual
        actual_cache_probes = Statistic.CACHE_PROBES
        actual_cache_access = Statistic.CACHE_ACCESSES

        self.assertEqual(expected_cache_access, actual_cache_access)
        self.assertEqual(expected_cache_probes, actual_cache_probes)