import argparse
import json
import logging
from typing import Dict, Any

from main import generate_interactive_graph, LearnEverythingError

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data_from_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()

def save_result_to_file(result: Dict[str, Any], file_path: str):
    with open(file_path, 'w') as file:
        json.dump(result, file, indent=2)

def run_cli():
    parser = argparse.ArgumentParser(description="Learn Everything: Interactive Graph Generator")
    parser.add_argument('input_file', help='Path to the input JSON file containing raw data')
    parser.add_argument('--output', help='Path to save the output JSON file', default='output.json')
    parser.add_argument('--max-iterations', type=int, default=3, help='Maximum number of iterations for each step')
    args = parser.parse_args()

    setup_logging()
    logging.info(f"Starting Learn Everything with input file: {args.input_file}")

    try:
        raw_data = load_data_from_file(args.input_file)
        result = generate_interactive_graph(raw_data, max_iterations=args.max_iterations)
        save_result_to_file(result, args.output)
        logging.info(f"Process completed successfully. Output saved to {args.output}")
    except LearnEverythingError as e:
        logging.error(f"Learn Everything Error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    run_cli()
