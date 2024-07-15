import unittest
from unittest.mock import patch
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import generate_interactive_graph

class TestEndToEnd(unittest.TestCase):
    @patch('main.call_deepseek_api')
    @patch('main.call_claude_api')
    @patch('main.upload_image_to_github')
    @patch('main.get_image_from_github')
    def test_full_graph_generation_process(self, mock_get_image, mock_upload, mock_claude, mock_deepseek):
        # Mock API responses
        mock_deepseek.side_effect = [
            json.dumps({"plan": ["step1", "step2"]}),  # Orchestrator
            json.dumps({"elements": ["node1", "node2"]}),  # Data Analyzer
            json.dumps({"layout": "force-directed"}),  # Graph Designer
            "<svg>...</svg>",  # SVG Generator
            "function interactive() {...}",  # JS Generator
            json.dumps({"images": [{"id": "img1", "content": "base64..."}]}),  # Image Generator
            json.dumps({"optimized_svg": "<svg>...</svg>", "optimized_js": "function..."})  # Performance Optimizer
        ]
        mock_claude.return_value = json.dumps({"evaluation": "8/10", "suggestions": ["Improve contrast"]})
        
        mock_upload.return_value = ("https://example.com/image.png", b"image_content")
        mock_get_image.return_value = b"image_content"

        # Test data
        raw_data = json.dumps({"nodes": [{"id": "A"}, {"id": "B"}], "edges": [{"source": "A", "target": "B"}]})

        # Run the full process
        result = generate_interactive_graph(raw_data)

        # Assertions
        self.assertIn("orchestrator_output", result)
        self.assertIn("data_analysis", result)
        self.assertIn("graph_design", result)
        self.assertIn("svg_code", result)
        self.assertIn("js_code", result)
        self.assertIn("images", result)
        self.assertIn("optimized_code", result)
        self.assertIn("quality_report", result)

        # Check if all mock functions were called
        mock_deepseek.assert_called()
        mock_claude.assert_called_once()
        mock_upload.assert_called()
        mock_get_image.assert_called()

if __name__ == '__main__':
    unittest.main()
