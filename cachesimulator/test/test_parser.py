import logging
import unittest
from cachesimulator.trace_parser import parse, read_text, modify_lines
import cachesimulator.Logger

logger = logging.getLogger("cachesimulator.Logger")
logger.setLevel(logging.DEBUG)

trace_test_file = r'C:\Users\James H\git\CacheSimulator\data\trace_test_RW_no_sharers.txt'

class TestParser(unittest.TestCase):

    def test_reading(self):
        # expected text
        expected_text = ['P3 R 12611',
                'P3 W 12611']
        # actual
        actual_text = read_text(trace_test_file)
        # equality
        self.assertEqual(expected_text, actual_text)

    def test_modify_lines_command(self):
        lines = ['P0 W 1299', 'P4 R 0']
        # expected output
        expected = [[0, 'W', 1299], [4, 'R', 0]]
        # actual 
        actual = modify_lines(lines)
        self.assertEqual(expected, actual)

    def test_modify_lines_no_command(self):
        lines = ['P0 W 1299', 'P4 R 0', 'v', 'h', 'P2 W 1290', 'p']
        # expected output
        expected = [[0, 'W', 1299], [4, 'R', 0], [-1, 'v', -1], [-1, 'h', -1], [2, 'W', 1290], [-1, 'p', -1]]
        # actual 
        actual = modify_lines(lines)
        self.assertEqual(expected, actual)



def get_test_trace_file():
    path = trace_test_file
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f]
    return lines