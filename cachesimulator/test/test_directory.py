import logging
import unittest
from cachesimulator.directory import Directory
from cachesimulator.cache import Cache
import cachesimulator.Logger
from cachesimulator.test.setup import create_caches, create_directory

logger = logging.getLogger("cachesimulator.Logger")
logger.setLevel(logging.DEBUG)

class TestDirectory(unittest.TestCase):

    def test_get_closest_cache_1(self):
        directory = create_directory()
        caches = create_caches(directory, 4)
        cache = caches[3]    # 4
        # expected ouput
        expected_closest_cache = caches[2]  # cache #3
        del caches[3]
        # actual ouput
        actual_closest_cache = directory._get_closest_cache(caches, cache)
        # equality
        self.assertEqual(expected_closest_cache, actual_closest_cache)

    def test_get_closest_cache_2(self):
        directory = create_directory()
        caches = create_caches(directory, 4)
        cache = caches[1]    # 4
        # expected ouput
        expected_closest_cache = caches[0]  # cache #3
        del caches[1]
        # actual ouput
        actual_closest_cache = directory._get_closest_cache(caches, cache)
        # equality
        self.assertEqual(expected_closest_cache, actual_closest_cache)
