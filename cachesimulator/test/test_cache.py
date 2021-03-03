import unittest
from cachesimulator.cache import get_address_parameters, Cache
from cachesimulator.config import *
from cachesimulator import MSI
import logging
from cachesimulator.test.setup import create_caches, create_directory

logger = logging.getLogger('cachesimulator.Logger')
logger.setLevel(logging.DEBUG)

class TestCache(unittest.TestCase):

    def setUp(self):
        print('\n')

    def test_address_parameters(self):
        address = 12611
        offset_bits = 2
        index_bits = 9
        # correct values
        expected_tag = 6
        expected_index = 80
        expected_offset = 3

        # actual values
        actual_tag, actual_index, actual_offset = get_address_parameters(address, index_bits, offset_bits)

        self.assertEqual(expected_tag, actual_tag)
        self.assertEqual(expected_index, actual_index)
        self.assertEqual(expected_offset, actual_offset)

    # -- Test writes -- #

    def test_write_hit(self):
        directory = create_directory()
        cache = create_caches(directory, 1)[0]

        address = 12611
        tag = 6
        index = 80
        offset = 3
        
        # modify line to have valid address here in modified state
        line = cache.cachelines[index]
        line.valid = True
        line.tag = tag
        line.state = MSI.MODIFIED
        
        # expected result
        expected_result = True
        # actual results
        actual_result = cache.write(address)
        # equate
        self.assertEqual(expected_result, actual_result)

    def test_write_miss_invalid_state(self):
        directory = create_directory()
        cache = create_caches(directory, 1)[0]

        address = 12611
        tag = 6
        index = 80
        offset = 3
        
        # modify line to have valid address here in modified state
        line = cache.cachelines[index]
        line.valid = True
        line.tag = tag
        line.state = MSI.INVALID
        
        # expected result
        expected_result = False
        # actual results
        actual_result = cache.write(address)
        # equate
        self.assertEqual(expected_result, actual_result)

    def test_write_miss_shared_state(self):
        directory = create_directory()
        cache = create_caches(directory, 1)[0]

        address = 12611
        tag = 6
        index = 80
        offset = 3
        
        # modify line to have valid address here in modified state
        line = cache.cachelines[index]
        line.valid = True
        line.tag = tag
        line.state = MSI.SHARED
        
        # expected result
        expected_result = False
        # actual results
        actual_result = cache.write(address)
        # equate
        self.assertEqual(expected_result, actual_result)

    def test_write_miss_bad_tag(self):
        directory = create_directory()
        cache = create_caches(directory, 1)[0]

        address = 12611
        tag = 6
        index = 80
        offset = 3
        
        # modify line to have valid address here in modified state
        line = cache.cachelines[index]
        line.valid = True
        line.tag = 3567
        line.state = MSI.SHARED
        
        # expected result
        expected_result = False
        # actual results
        actual_result = cache.write(address)
        # equate
        self.assertEqual(expected_result, actual_result)

    def test_write_miss_multi_sharers(self):
        directory = create_directory()
        caches = create_caches(directory, 4)
        directory._sharers = caches
        
        cache = caches[2]

        address = 12611
        tag = 6
        index = 80
        offset = 3
        
        # modify all cache's line to have valid address here in modified state
        for c in caches:
            line = c.cachelines[index]
            line.valid = True
            line.tag = tag
            line.state = MSI.SHARED

        # expect other caches to have states invalid
        expected_state = MSI.INVALID
        # actual 
        cache.write(address)
        for c in caches:
            if (c!= cache):
                line = c.cachelines[index]
                self.assertEqual(line.state,MSI.INVALID)

    # -- Test Reads -- #
    def test_read_hit_modified(self):
        directory = create_directory()
        cache = create_caches(directory, 1)[0]

        address = 12611
        tag = 6
        index = 80
        offset = 3
        
        # modify line to have valid address here in modified state
        line = cache.cachelines[index]
        line.valid = True
        line.tag = tag
        line.state = MSI.MODIFIED
        
        # expected result
        expected_result = True
        # actual results
        actual_result = cache.read(address)
        # equate
        self.assertEqual(expected_result, actual_result)

    def test_read_hit_shared_state(self):
        directory = create_directory()
        cache = create_caches(directory, 1)[0]

        address = 12611
        tag = 6
        index = 80
        offset = 3
        
        # modify line to have valid address here in modified state
        line = cache.cachelines[index]
        line.valid = True
        line.tag = tag
        line.state = MSI.SHARED
        
        # expected result
        expected_result = True
        # actual results
        actual_result = cache.read(address)
        # equate
        self.assertEqual(expected_result, actual_result)

    def test_read_miss_invalid_state(self):
        directory = create_directory()
        cache = create_caches(directory, 1)[0]

        address = 12611
        tag = 6
        index = 80
        offset = 3
        
        # modify line to have valid address here in modified state
        line = cache.cachelines[index]
        line.valid = True
        line.tag = tag
        line.state = MSI.INVALID
        
        # expected result
        expected_result = False
        # actual results
        actual_result = cache.write(address)
        # equate
        self.assertEqual(expected_result, actual_result)

    def test_read_miss_bad_tag(self):
        directory = create_directory()
        caches = create_caches(directory, 3)
        cache = caches[0]
        directory._sharers = caches

        address = 12611
        tag = 6
        index = 80
        offset = 3
        
        # modify line to have valid address here in modified state
        line = cache.cachelines[index]
        line.valid = True
        line.tag = 3567
        line.state = MSI.SHARED
        
        # expected result
        expected_result = False
        # actual results
        actual_result = cache.read(address)
        # equate
        self.assertEqual(expected_result, actual_result)

    def test_read_miss_multi_sharers(self):
        directory = create_directory()
        caches = create_caches(directory, 4)
        directory._sharers = caches
        
        cache = caches[3]

        address = 12611
        tag = 6
        index = 80
        offset = 3
        
        # modify all cache's line to have valid address here in modified state
        for c in caches:
            line = c.cachelines[index]
            line.valid = True
            line.tag = tag
            line.state = MSI.SHARED
        line = cache.cachelines[index]
        line.valid = True
        line.tag = tag
        line.state = MSI.INVALID

        # expect other caches to have states invalid
        expected_state = MSI.SHARED
        # actual 
        cache.read(address)
        for c in caches:
            if (c!= cache):
                line = c.cachelines[index]
                actual_state = line.state
                self.assertEqual(actual_state,expected_state)

    # -- Test multi sharers -- #
    def test_remote_miss(self):
        directory = create_directory()
        caches = create_caches(directory, 4)
        directory._sharers = caches

        address = 12611
        tag = 6
        index = 80
        offset = 3

        # set cache 3 to modified
        line = caches[3].cachelines[index]
        line.valid = True
        line.tag = tag
        line.state = MSI.MODIFIED

        # now have cache 0 ask for read
        caches[0].read(address)

        # expected result
        expected = MSI.SHARED

        # actual results
        actual = caches[3].cachelines[index].state

        self.assertEqual(expected, actual)