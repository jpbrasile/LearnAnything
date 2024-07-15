import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from cli import run_cli

class TestCLI(unittest.TestCase):
    @patch('cli.generate_interactive_graph')
    @patch('cli.load_data_from_file')
    @patch('cli.save_result_to_file')
    def test_cli_execution(self, mock_save, mock_load, mock_generate):
        mock_load.return_value = '{"test": "data"}'
        mock_generate.return_value = {"result": "success"}
        
        test_args = ['cli.py', 'input.json', '--output', 'output.json']
        with patch.object(sys, 'argv', test_args):
            run_cli()
        
        mock_load.assert_called_once_with('input.json')
        mock_generate.assert_called_once()
        mock_save.assert_called_once_with({"result": "success"}, 'output.json')

if __name__ == '__main__':
    unittest.main()
