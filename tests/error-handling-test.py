import unittest
from unittest.mock import patch
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import generate_interactive_graph, LearnEverythingError

class TestErrorHandling(unittest.TestCase):
    @patch('main.call_deepseek_api')
    def test_api_error_handling(self, mock_api):
        mock_api.side_effect = Exception("API Error")
        
        with self.assertRaises(LearnEverythingError):
            generate_interactive_graph("{}")

    @patch('main.upload_image_to_github')
    def test_image_upload_error(self, mock_upload):
        mock_upload.side_effect = Exception("Upload failed")
        
        with self.assertRaises(LearnEverythingError):
            generate_interactive_graph('{"images": [{"id": "test", "content": "base64..."}]}')

    def test_invalid_input_data(self):
        with self.assertRaises(json.JSONDecodeError):
            generate_interactive_graph("invalid json")

if __name__ == '__main__':
    unittest.main()
