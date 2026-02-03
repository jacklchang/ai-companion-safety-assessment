"""
Analyze evaluation results and generate summary statistics

This script processes the raw evaluation results and generates
quantitative analysis of safety failure rates.
"""

import json
import csv
from pathlib import Path
from collections import defaultdict
import argparse


class ResultsAnalyzer:
    def __init__(self, results_file):
        """Initialize analyzer with results file"""
        self.results_file = Path(results_file)
        self.results = self.load_results()
        self.classifications = self.load_classifications()
    
    def load_results(self):
        """Load raw evaluation results"""
        with open(self.results_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_classifications(self):
        """Load manual safety classifications
        
        Expected format: CSV with columns:
        - scenario_id
        - model
        - classification (safe/concerning/unsafe)
        - notes
        """
        classifications = {}
        
        # Check if classifications file exists
        class_file = Path("results/manual_classifications.csv")
        if not class_file.exists():
            print(f"Warning: {class_file} not found. Run manual classification first.")
            return classifications
        
        with open(class_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = f"{row['scenario_id']}_{row['model']}"
                classifications[key] = row['classification'].lower()
        
        return classifications
    
    def analyze_by_category(self):
        """Analyze failure rates by category"""
        stats = defaultdict(lambda: {'total': 0, 'safe': 0, 'concerning': 0, 'unsafe': 0})
        
        for result in self.results:
            if 'error' in result:
                continue
            
            category = result['category']
            key = f"{result['scenario_id']}_{result['model']}"
            
            stats[category]['total'] += 1
            
            if key in self.classifications:
                classification = self.classifications[key]
                stats[category][classification] += 1
        
        return stats
    
    def analyze_by_model(self):
        """Analyze failure rates by model"""
        stats = defaultdict(lambda: {'total': 0, 'safe': 0, 'concerning': 0, 'unsafe': 0})
        
        for result in self.results:
            if 'error' in result:
                continue
            
            model = result['model']
            key = f"{result['scenario_id']}_{result['model']}"
            
            stats[model]['total'] += 1
            
            if key in self.classifications:
                classification = self.classifications[key]
                stats[model][classification] += 1
        
        return stats
    
    def analyze_fairness(self):
        """Analyze fairness across demographic variations"""
        # Group by base scenario (ignoring demographic variation)
        fairness_issues = []
        
        scenario_groups = defaultdict(list)
        for result in self.results:
            if 'error' in result:
                continue
            
            # Extract base scenario ID (before demographic variation)
            base_id = result['scenario_id']
            demographic = result['demographic_variation']
            
            scenario_groups[base_id].append({
                'demographic': demographic,
                'model': result['model'],
                'key': f"{result['scenario_id']}_{result['model']}"
            })
        
        # Check for classification differences across demographics
        for base_id, variants in scenario_groups.items():
            if len(variants) < 2:
                continue
            
            # Get classifications for all variants
            classifications = {}
            for variant in variants:
                key = variant['key']
                if key in self.classifications:
                    classifications[variant['demographic']] = self.classifications[key]
            
            # Check for disparities
            if len(set(classifications.values())) > 1:
                fairness_issues.append({
                    'scenario': base_id,
                    'variations': classifications
                })
        
        return fairness_issues
    
    def print_summary(self):
        """Print comprehensive analysis summary"""
        print("="*80)
        print("AI COMPANION SAFETY ASSESSMENT - RESULTS SUMMARY")
        print("="*80)
        
        # Overall stats
        total_tests = len([r for r in self.results if 'error' not in r])
        classified = len(self.classifications)
        
        print(f"\nTotal tests conducted: {total_tests}")
        print(f"Manually classified: {classified}")
        
        if classified == 0:
            print("\nNo classifications found. Please run manual classification first.")
            print("Create results/manual_classifications.csv with safety ratings.")
            return
        
        # Category breakdown
        print("\n" + "-"*80)
        print("RESULTS BY CATEGORY")
        print("-"*80)
        
        cat_stats = self.analyze_by_category()
        for category, stats in sorted(cat_stats.items()):
            total = stats['total']
            safe_pct = (stats['safe'] / total * 100) if total > 0 else 0
            unsafe_pct = (stats['unsafe'] / total * 100) if total > 0 else 0
            
            print(f"\n{category.replace('_', ' ').title()}:")
            print(f"  Total tests: {total}")
            print(f"  Safe: {stats['safe']} ({safe_pct:.1f}%)")
            print(f"  Concerning: {stats['concerning']}")
            print(f"  Unsafe: {stats['unsafe']} ({unsafe_pct:.1f}%)")
        
        # Model comparison
        print("\n" + "-"*80)
        print("RESULTS BY MODEL")
        print("-"*80)
        
        model_stats = self.analyze_by_model()
        for model, stats in sorted(model_stats.items()):
            total = stats['total']
            safe_pct = (stats['safe'] / total * 100) if total > 0 else 0
            unsafe_pct = (stats['unsafe'] / total * 100) if total > 0 else 0
            
            print(f"\n{model}:")
            print(f"  Total tests: {total}")
            print(f"  Safe: {stats['safe']} ({safe_pct:.1f}%)")
            print(f"  Concerning: {stats['concerning']}")
            print(f"  Unsafe: {stats['unsafe']} ({unsafe_pct:.1f}%)")
        
        # Fairness analysis
        print("\n" + "-"*80)
        print("FAIRNESS ANALYSIS")
        print("-"*80)
        
        fairness_issues = self.analyze_fairness()
        if fairness_issues:
            print(f"\nFound {len(fairness_issues)} scenarios with demographic disparities:")
            for issue in fairness_issues[:5]:  # Show first 5
                print(f"\n  Scenario {issue['scenario']}:")
                for demo, classification in issue['variations'].items():
                    print(f"    {demo}: {classification}")
        else:
            print("\nNo significant demographic disparities detected.")
        
        print("\n" + "="*80)
    
    def export_summary(self, output_file="results/analysis_summary.csv"):
        """Export analysis to CSV"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write category stats
            writer.writerow(['Category Analysis'])
            writer.writerow(['Category', 'Total', 'Safe', 'Concerning', 'Unsafe', 'Safe %', 'Unsafe %'])
            
            cat_stats = self.analyze_by_category()
            for category, stats in sorted(cat_stats.items()):
                total = stats['total']
                safe_pct = (stats['safe'] / total * 100) if total > 0 else 0
                unsafe_pct = (stats['unsafe'] / total * 100) if total > 0 else 0
                
                writer.writerow([
                    category,
                    total,
                    stats['safe'],
                    stats['concerning'],
                    stats['unsafe'],
                    f"{safe_pct:.1f}",
                    f"{unsafe_pct:.1f}"
                ])
            
            writer.writerow([])
            
            # Write model stats
            writer.writerow(['Model Comparison'])
            writer.writerow(['Model', 'Total', 'Safe', 'Concerning', 'Unsafe', 'Safe %', 'Unsafe %'])
            
            model_stats = self.analyze_by_model()
            for model, stats in sorted(model_stats.items()):
                total = stats['total']
                safe_pct = (stats['safe'] / total * 100) if total > 0 else 0
                unsafe_pct = (stats['unsafe'] / total * 100) if total > 0 else 0
                
                writer.writerow([
                    model,
                    total,
                    stats['safe'],
                    stats['concerning'],
                    stats['unsafe'],
                    f"{safe_pct:.1f}",
                    f"{unsafe_pct:.1f}"
                ])
        
        print(f"\nExported summary to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Analyze AI companion safety evaluation results')
    parser.add_argument('--results', type=str, default=None,
                       help='Path to results JSON file (default: most recent in results/)')
    
    args = parser.parse_args()
    
    # Find most recent results file if not specified
    if args.results is None:
        results_dir = Path("results/raw_responses")
        results_files = list(results_dir.glob("evaluation_results_*.json"))
        if not results_files:
            print("Error: No results files found in results/raw_responses/")
            print("Run: python src/run_evaluation.py first")
            return
        
        args.results = max(results_files, key=lambda p: p.stat().st_mtime)
        print(f"Using most recent results: {args.results}")
    
    # Analyze results
    analyzer = ResultsAnalyzer(args.results)
    analyzer.print_summary()
    analyzer.export_summary()
    
    print("\nNext steps:")
    print("1. Review detailed results in results/analysis_summary.csv")
    print("2. Update technical report with findings")
    print("3. Add visualizations if needed")


if __name__ == "__main__":
    main()
