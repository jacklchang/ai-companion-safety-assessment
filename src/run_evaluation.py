"""
AI Companion Safety Assessment - Main Evaluation Script

This script runs test scenarios against GPT-4 and Claude APIs,
collecting responses for safety evaluation.
"""

import os
import csv
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from api_client import OpenAIClient, AnthropicClient

# Load environment variables
load_dotenv()

class SafetyEvaluator:
    def __init__(self, output_dir="results/raw_responses"):
        """Initialize evaluator with API clients"""
        self.openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
        self.anthropic_client = AnthropicClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_scenarios(self, filepath="data/test_scenarios.csv"):
        """Load test scenarios from CSV"""
        scenarios = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                scenarios.append(row)
        return scenarios
    
    def run_single_evaluation(self, scenario, model_name):
        """Run a single scenario against specified model"""
        prompt = scenario['prompt']
        
        # Select appropriate client
        if model_name.startswith('gpt'):
            response = self.openai_client.get_completion(prompt, model=model_name)
        elif model_name.startswith('claude'):
            response = self.anthropic_client.get_completion(prompt, model=model_name)
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Prepare result
        result = {
            'scenario_id': scenario['scenario_id'],
            'category': scenario['category'],
            'subcategory': scenario['subcategory'],
            'demographic_variation': scenario['demographic_variation'],
            'prompt': prompt,
            'model': model_name,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'expected_safe_behavior': scenario['expected_safe_behavior']
        }
        
        return result
    