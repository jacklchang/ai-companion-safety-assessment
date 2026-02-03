"""
AI Companion Safety Assessment - Main Evaluation Script

This script runs test scenarios against GPT-4 and Claude APIs,
collecting responses for safety evaluation.
"""

import os
import csv
import json
import time
from datetime import datetime
from pathlib import Path
import argparse
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
        context = scenario.get('relationship_context', None)  # Get context if present
        
        # Select appropriate client and pass context
        if model_name.startswith('gpt'):
            response = self.openai_client.get_completion(prompt, model=model_name, context=context)
        elif model_name.startswith('claude'):
            response = self.anthropic_client.get_completion(prompt, model=model_name, context=context)
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Prepare result
        result = {
            'scenario_id': scenario['scenario_id'],
            'category': scenario['category'],
            'subcategory': scenario['subcategory'],
            'demographic_variation': scenario['demographic_variation'],
            'relationship_context': scenario.get('relationship_context', ''),
            'prompt': prompt,
            'model': model_name,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'expected_safe_behavior': scenario['expected_safe_behavior']
        }
        
        return result
    
    def run_batch_evaluation(self, scenarios, models, category_filter=None):
        """Run multiple scenarios across multiple models"""
        results = []
        
        # Filter by category if specified
        if category_filter:
            scenarios = [s for s in scenarios if s['category'] == category_filter]
            print(f"Filtered to {len(scenarios)} scenarios in category: {category_filter}")
        
        total_tests = len(scenarios) * len(models)
        current_test = 0
        
        for scenario in scenarios:
            for model in models:
                current_test += 1
                print(f"[{current_test}/{total_tests}] Testing {scenario['scenario_id']} with {model}...")
                
                try:
                    result = self.run_single_evaluation(scenario, model)
                    results.append(result)
                    
                    # Rate limiting - pause between requests
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error testing {scenario['scenario_id']} with {model}: {e}")
                    # Log error but continue
                    results.append({
                        'scenario_id': scenario['scenario_id'],
                        'model': model,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
        
        return results
    
    def save_results(self, results, filename=None):
        """Save results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_results_{timestamp}.json"
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to: {output_path}")
        return output_path
    
    def print_summary(self, results):
        """Print summary statistics"""
        total = len(results)
        errors = sum(1 for r in results if 'error' in r)
        successful = total - errors
        
        print("\n" + "="*60)
        print("EVALUATION SUMMARY")
        print("="*60)
        print(f"Total tests run: {total}")
        print(f"Successful: {successful}")
        print(f"Errors: {errors}")
        
        if successful > 0:
            # Group by model
            models = {}
            for result in results:
                if 'error' not in result:
                    model = result['model']
                    models[model] = models.get(model, 0) + 1
            
            print("\nTests by model:")
            for model, count in models.items():
                print(f"  {model}: {count}")
            
            # Group by category
            categories = {}
            for result in results:
                if 'error' not in result:
                    cat = result['category']
                    categories[cat] = categories.get(cat, 0) + 1
            
            print("\nTests by category:")
            for cat, count in categories.items():
                print(f"  {cat}: {count}")
        
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='Run AI companion safety evaluations')
    parser.add_argument('--model', type=str, default='all',
                       help='Model to test: gpt5, claude, or all (default: all)')
    parser.add_argument('--category', type=str, default=None,
                       help='Filter to specific category (optional)')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of scenarios to test (optional)')
    
    args = parser.parse_args()
    
    # Initialize evaluator
    evaluator = SafetyEvaluator()
    
    # Load scenarios
    print("Loading test scenarios...")
    scenarios = evaluator.load_scenarios()
    print(f"Loaded {len(scenarios)} scenarios")
    
    # Limit scenarios if specified
    if args.limit:
        scenarios = scenarios[:args.limit]
        print(f"Limited to first {args.limit} scenarios")
    
    # Determine which models to test
    if args.model == 'all':
        models = ['gpt-5.2', 'claude-sonnet-4-5-20250929']
    elif args.model == 'gpt':
        models = ['gpt-5.2']
    elif args.model == 'claude':
        models = ['claude-sonnet-4-5-20250929']
    else:
        models = [args.model]
    
    print(f"Testing with models: {', '.join(models)}")
    
    # Run evaluations
    print("\nStarting evaluations...")
    print("-" * 60)
    
    results = evaluator.run_batch_evaluation(
        scenarios=scenarios,
        models=models,
        category_filter=args.category
    )
    
    # Save and summarize
    evaluator.save_results(results)
    evaluator.print_summary(results)
    
    print("\nNext steps:")
    print("1. Review results in results/raw_responses/")
    print("2. Manually classify responses using data/evaluation_rubric.md")
    print("3. Run: python src/analyze_results.py")


if __name__ == "__main__":
    main()
