import json
import requests
import logging
import base64
from github import Github, GithubException
from io import BytesIO
from PIL import Image
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
BRANCH_NAME = os.getenv('BRANCH_NAME')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
CLAUDE_API_URL = os.getenv('CLAUDE_API_URL')

# Initialize GitHub API
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LearnEverythingError(Exception):
    """Custom exception for Learn Everything application"""
    pass

def call_deepseek_api(messages: List[Dict[str, str]]) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-coder",
        "messages": messages,
        "temperature": 0.7
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code != 200:
        raise LearnEverythingError(f"DeepSeek API call failed with status {response.status_code}: {response.text}")
    return response.json()['choices'][0]['message']['content']

def call_claude_api(messages: List[Dict[str, str]], images: List[Dict[str, bytes]] = None) -> str:
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 1024,
        "messages": messages
    }
    if images:
        data["images"] = images
    
    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    if response.status_code != 200:
        raise LearnEverythingError(f"Claude API call failed with status {response.status_code}: {response.text}")
    return response.json()['content'][0]['text']

def upload_image_to_github(image_data: str, image_id: str) -> Tuple[str, bytes]:
    try:
        # Decode base64 image
        image_content = base64.b64decode(image_data.split(',')[1])
        
        # Open image with PIL
        image = Image.open(BytesIO(image_content))
        
        # Convert to PNG
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        png_content = buffered.getvalue()
        
        # Prepare file content for GitHub
        file_content = base64.b64encode(png_content).decode()
        
        # File path in the repository
        file_path = f'assets/images/{image_id}.png'
        
        try:
            # Check if file already exists
            contents = repo.get_contents(file_path, ref=BRANCH_NAME)
            repo.update_file(file_path, f"Update image {image_id}", file_content, contents.sha, branch=BRANCH_NAME)
        except GithubException:
            # If file doesn't exist, create it
            repo.create_file(file_path, f"Add image {image_id}", file_content, branch=BRANCH_NAME)
        
        # Return the URL of the image on GitHub and the PNG content
        return f"https://raw.githubusercontent.com/{REPO_NAME}/{BRANCH_NAME}/{file_path}", png_content
    
    except Exception as e:
        logging.error(f"Error uploading image to GitHub: {str(e)}")
        raise LearnEverythingError(f"Failed to upload image: {str(e)}")

def get_image_from_github(image_url: str) -> bytes:
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        logging.error(f"Error retrieving image from GitHub: {str(e)}")
        raise LearnEverythingError(f"Failed to retrieve image: {str(e)}")

# Agent templates
agent_templates = {
    "orchestrator": """
    Rôle: Coordonner tous les agents impliqués dans la création d'un graphe interactif à partir de données brutes.
    Instructions:
    1. Analysez la structure globale des données fournies.
    2. Définissez l'ordre d'exécution des tâches pour chaque agent.
    3. Transmettez les données pertinentes à chaque agent.
    4. Intégrez les résultats de chaque agent dans le projet global.
    5. Assurez la cohérence et la qualité du graphe final.
    6. Résolvez les conflits potentiels entre les outputs des agents.
    7. Fournissez un rapport final sur le processus et le résultat.

    Données brutes: {data}

    Répondez au format JSON suivant:
    {{
      "plan": ["étape1", "étape2", ...],
      "assignations": {{"AgentX": "tâcheY", ...}},
      "intégration": {{"étapeA": "résultatB", ...}},
      "rapport_final": "description concise"
    }}
    """,
    "data_analyzer": """
    Rôle: Analyser et structurer les données brutes initiales.
    Instructions:
    1. Identifiez les éléments clés dans les données fournies.
    2. Déterminez les relations entre ces éléments.
    3. Établissez une hiérarchie ou structure logique.
    4. Identifiez les attributs pertinents pour la visualisation.
    5. Fournissez une structure de données optimisée pour la création de graphes.

    Données brutes: {data}

    Répondez au format JSON suivant:
    {{
      "éléments_clés": ["élément1", "élément2", ...],
      "relations": [{{"de": "élément1", "à": "élément2", "type": "typeRelation"}}, ...],
      "hiérarchie": {{"niveau1": ["élément1", "élément2"], ...}},
      "attributs_visualisation": ["attribut1", "attribut2", ...],
      "structure_optimisée": {{}}
    }}
    """,
    # ... (autres templates pour chaque agent)
}

class Agent:
    def __init__(self, name: str, template: str, use_claude: bool = False):
        self.name = name
        self.template = template
        self.use_claude = use_claude

    def run(self, data: Any, images: List[Dict[str, bytes]] = None) -> str:
        messages = [
            {"role": "system", "content": self.template},
            {"role": "user", "content": json.dumps(data) if isinstance(data, dict) else str(data)}
        ]
        if self.use_claude:
            return call_claude_api(messages, images)
        else:
            return call_deepseek_api(messages)

# Create agents
agents = {name: Agent(name, template, use_claude=(name == "quality_checker")) 
          for name, template in agent_templates.items()}

def handle_image_generation(graph_design: Dict) -> Tuple[str, List[Dict[str, bytes]]]:
    images_response = agents["image_generator"].run(json.dumps(graph_design))
    images_data = json.loads(images_response)
    
    image_contents = []
    for image in images_data["images"]:
        try:
            image_url, png_content = upload_image_to_github(image["content"], image["id"])
            image["url"] = image_url
            del image["content"]  # Remove base64 content to save space
            
            # Verify that we can retrieve the image
            retrieved_content = get_image_from_github(image_url)
            if retrieved_content != png_content:
                raise LearnEverythingError(f"Retrieved image content does not match uploaded content for image {image['id']}")
            
            image_contents.append({"type": "image/png", "data": base64.b64encode(png_content).decode()})
            logging.info(f"Image {image['id']} uploaded and verified successfully")
        except LearnEverythingError as e:
            logging.error(f"Error handling image {image['id']}: {str(e)}")
    
    return json.dumps(images_data), image_contents

def generate_interactive_graph(raw_data: str, max_iterations: int = 3) -> Dict[str, Any]:
    try:
        logging.info("Starting interactive graph generation process")

        # Step 1: Orchestration
        logging.info("Step 1: Orchestration")
        orchestrator_response = agents["orchestrator"].run(raw_data)
        orchestrator_output = json.loads(orchestrator_response)
        logging.info(f"Orchestrator output: {orchestrator_output}")

        # Step 2: Data Analysis
        logging.info("Step 2: Data Analysis")
        data_analysis = agents["data_analyzer"].run(raw_data)
        data_analysis_output = json.loads(data_analysis)
        logging.info(f"Data analysis output: {data_analysis_output}")

        # Step 3: Graph Design
        logging.info("Step 3: Graph Design")
        graph_design = agents["graph_designer"].run(data_analysis)
        graph_design_output = json.loads(graph_design)
        logging.info(f"Graph design output: {graph_design_output}")

        # Step 4: SVG Generation
        logging.info("Step 4: SVG Generation")
        svg_code = agents["svg_generator"].run(graph_design)
        logging.info("SVG code generated successfully")

        # Step 5: JavaScript Generation
        logging.info("Step 5: JavaScript Generation")
        js_code = agents["js_generator"].run(graph_design)
        logging.info("JavaScript code generated successfully")

        # Step 6: Image Generation and Verification
        logging.info("Step 6: Image Generation and Verification")
        images_response, image_contents = handle_image_generation(graph_design_output)
        images_data = json.loads(images_response)

        # Step 7: Performance Optimization
        logging.info("Step 7: Performance Optimization")
        optimized_code = agents["performance_optimizer"].run({
            "svg_code": svg_code, 
            "js_code": js_code
        })
        optimized_code_json = json.loads(optimized_code)
        logging.info("Code optimization completed")

        # Step 8: Quality Check
        logging.info("Step 8: Quality Check")
        quality_check_data = {
            "svg_code": optimized_code_json["code_optimisé"]["svg"],
            "js_code": optimized_code_json["code_optimisé"]["js"],
            "images": images_data["images"]
        }
        quality_report = agents["quality_checker"].run(quality_check_data, image_contents)
        quality_report_json = json.loads(quality_report)
        logging.info(f"Quality report: {quality_report_json}")

        logging.info("Interactive graph generation process completed successfully")

        return {
            "orchestrator_output": orchestrator_output,
            "data_analysis": data_analysis_output,
            "graph_design": graph_design_output,
            "svg_code": svg_code,
            "js_code": js_code,
            "images": images_data["images"],
            "optimized_code": optimized_code_json,
            "quality_report": quality_report_json
        }

    except LearnEverythingError as e:
        logging.error(f"Learn Everything Error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in generate_interactive_graph: {str(e)}")
        raise LearnEverythingError(f"Unexpected error: {str(e)}")

def debug_agent_output(agent_name: str, input_data: str, output_data: str):
    logging.debug(f"Agent: {agent_name}")
    logging.debug(f"Input: {input_data[:100]}...")  # Log first 100 characters
    logging.debug(f"Output: {output_data[:100]}...")  # Log first 100 characters

if __name__ == "__main__":
    print("This script is not meant to be run directly. Please use cli.py instead.")
