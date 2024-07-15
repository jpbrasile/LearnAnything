import unittest
from unittest.mock import patch
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import debug_agent_output

class TestDebug(unittest.TestCase):
    @patch('main.logging.debug')
    def test_debug_output(self, mock_debug):
        debug_agent_output("test_agent", "input_data", "output_data")
        mock_debug.assert_any_call("Agent: test_agent")
        mock_debug.assert_any_call("Input: input_data...")
        mock_debug.assert_any_call("Output: output_data...")

if __name__ == '__main__':
    unittest.main()
