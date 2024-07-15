import unittest
import time
import json
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import generate_interactive_graph

def generate_complex_network(num_nodes, num_edges):
    nodes = [{"id": f"node{i}", "type": random.choice(["user", "post", "comment"]), "value": random.randint(1, 100)} for i in range(num_nodes)]
    
    edges = []
    for _ in range(num_edges):
        source = random.choice(nodes)["id"]
        target = random.choice(nodes)["id"]
        if source != target:
            edges.append({
                "source": source,
                "target": target,
                "weight": random.uniform(0.1, 1.0),
                "type": random.choice(["friend", "like", "comment", "share"])
            })
    
    return {"nodes": nodes, "edges": edges}

class TestPerformance(unittest.TestCase):
    @unittest.skip("Long-running test")
    def test_large_data_performance(self):
        # Generate a large, complex dataset
        large_data = generate_complex_network(num_nodes=10000, num_edges=50000)
        
        start_time = time.time()
        result = generate_interactive_graph(json.dumps(large_data))
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"Execution time for large dataset: {execution_time:.2f} seconds")
        
        self.assertLess(execution_time, 300)  # Assert that it takes less than 5 minutes
        
        # Additional assertions to check the quality of the result
        self.assertIn("svg_code", result)
        self.assertIn("js_code", result)
        self.assertIn("quality_report", result)
        
        # Check if the number of nodes and edges in the result matches the input
        result_data = json.loads(result["data_analysis"])
        self.assertEqual(len(result_data["éléments_clés"]), 10000)
        self.assertEqual(len(result_data["relations"]), 50000)

    def test_load_real_dataset(self):
        # Load a real or semi-real large dataset
        with open(os.path.join(os.path.dirname(__file__), 'data', 'large_real_dataset.json'), 'r') as f:
            real_data = json.load(f)
        
        start_time = time.time()
        result = generate_interactive_graph(json.dumps(real_data))
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"Execution time for real dataset: {execution_time:.2f} seconds")
        
        self.assertLess(execution_time, 300)  # Assert that it takes less than 5 minutes
        
        # Additional assertions specific to the real dataset
        # (These would depend on the nature of your real dataset)

if __name__ == '__main__':
    unittest.main()
