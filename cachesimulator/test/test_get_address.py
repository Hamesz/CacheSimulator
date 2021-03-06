import unittest
from cachesimulator.cache import get_stored_address, get_address_parameters
from cachesimulator.cache import Cache
import logging

logger = logging.getLogger('cachesimulator.Logger')
logger.setLevel(logging.WARNING)

class TestGetAddress(unittest.TestCase):

    def test_1(self):
        OFFSET_BITS = 2
        INDEX_BITS = 9

        address = 1
        tag, index, offset = get_address_parameters(address, INDEX_BITS, OFFSET_BITS)
        
        # expected
        expected_address = 0
        # actual 
        actual_address = get_stored_address(tag, index, INDEX_BITS, OFFSET_BITS)
        # equate
        self.assertEquals(expected_address, actual_address)

    def test_2(self):
        OFFSET_BITS = 2
        INDEX_BITS = 9

        address = 2048
        tag, index, offset = get_address_parameters(address, INDEX_BITS, OFFSET_BITS)
        print(tag, index, offset)
        # expected
        expected_address = 2048
        # actual 
        actual_address = get_stored_address(tag, index, INDEX_BITS, OFFSET_BITS)
        
        # equate
        self.assertEquals(expected_address, actual_address)

    def test_3(self):
        OFFSET_BITS = 2
        INDEX_BITS = 9

        address = 2049
        tag, index, offset = get_address_parameters(address, INDEX_BITS, OFFSET_BITS)
        print(tag, index, offset)
        # expected
        expected_address = 2048
        # actual 
        actual_address = get_stored_address(tag, index, INDEX_BITS, OFFSET_BITS)
        
        # equate
        self.assertEquals(expected_address, actual_address)

    def test_4(self):
        OFFSET_BITS = 2
        INDEX_BITS = 9

        address = 2053
        tag, index, offset = get_address_parameters(address, INDEX_BITS, OFFSET_BITS)
        print(tag, index, offset)
        # expected
        expected_address = 2052
        # actual 
        actual_address = get_stored_address(tag, index, INDEX_BITS, OFFSET_BITS)
        
        # equate
        self.assertEquals(expected_address, actual_address)

    def test_5(self):
        OFFSET_BITS = 2
        INDEX_BITS = 9

        address = 15208
        tag, index, offset = get_address_parameters(address, INDEX_BITS, OFFSET_BITS)
        print(tag, index, offset)
        # expected
        expected_address = 15208
        # actual 
        actual_address = get_stored_address(tag, index, INDEX_BITS, OFFSET_BITS)
        
        # equate
        self.assertEquals(expected_address, actual_address)
        