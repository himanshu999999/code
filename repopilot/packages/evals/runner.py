"""
Evaluation runner for benchmarks.
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from packages.evals.metrics import calculate_all_metrics


def load_dataset(dataset_name: str) -> List[Dict[str, Any]]:
    """
    Load evaluation dataset.
    
    For demo purposes, returns sample data.
    In production, would load from files or database.
    """
    # Sample benchmark tasks
    return [
        {
            "id": 1,
            "question": "Where is authentication implemented?",
            "relevant_files": ["src/auth.py", "src/middleware.py"],
            "expected_answer_keywords": ["authentication", "login", "password"]
        },
        {
            "id": 2,
            "question": "How are payments processed?",
            "relevant_files": ["src/payments/processor.py", "src/payments/stripe.py"],
            "expected_answer_keywords": ["payment", "stripe", "charge"]
        },
        {
            "id": 3,
            "question": "What handles database connections?",
            "relevant_files": ["src/db/connection.py", "src/db/pool.py"],
            "expected_answer_keywords": ["database", "connection", "pool"]
        }
    ]


def run_evaluation(
    dataset_name: str = "sample_10",
    output_dir: str = "results",
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Run full evaluation suite.
    
    Args:
        dataset_name: Name of dataset to evaluate
        output_dir: Directory to save results
        dry_run: If True, don't actually call APIs
    
    Returns:
        Evaluation results dictionary
    """
    print(f"Starting evaluation on dataset: {dataset_name}")
    print(f"Dry run: {dry_run}")
    
    # Load dataset
    dataset = load_dataset(dataset_name)
    print(f"Loaded {len(dataset)} test cases")
    
    # Simulate predictions (in real eval, would call actual API)
    predictions = []
    ground_truth = []
    latencies = []
    token_usages = []
    
    for task in dataset:
        # Mock predictions - in reality would call retrieval engine
        pred = task["relevant_files"][:2]  # Top 2 predictions
        predictions.append(pred)
        ground_truth.append(task["relevant_files"])
        latencies.append(1500 + len(pred) * 100)  # Mock latency
        token_usages.append(2000 + len(pred) * 500)  # Mock tokens
    
    # Calculate metrics
    metrics = calculate_all_metrics(
        predictions=predictions,
        ground_truth=ground_truth,
        latencies=latencies,
        token_usages=token_usages
    )
    
    # Build results
    results = {
        "dataset": dataset_name,
        "timestamp": datetime.utcnow().isoformat(),
        "num_tasks": len(dataset),
        "metrics": metrics,
        "per_task_results": [
            {
                "task_id": task["id"],
                "predictions": pred,
                "ground_truth": truth,
                "latency_ms": lat,
                "tokens": tok
            }
            for task, pred, truth, lat, tok in zip(
                dataset, predictions, ground_truth, latencies, token_usages
            )
        ]
    }
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results_file = output_path / f"eval_{dataset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    print("\n=== Summary ===")
    for metric, value in metrics.items():
        if isinstance(value, float):
            print(f"{metric}: {value:.4f}")
        else:
            print(f"{metric}: {value}")
    
    return results


def generate_report(results: Dict[str, Any]) -> str:
    """Generate markdown report from results."""
    report = f"""# RepoPilot Evaluation Report

## Overview
- **Dataset**: {results['dataset']}
- **Timestamp**: {results['timestamp']}
- **Tasks**: {results['num_tasks']}

## Metrics

| Metric | Value |
|--------|-------|
"""
    
    for metric, value in results['metrics'].items():
        if isinstance(value, float):
            report += f"| {metric} | {value:.4f} |\n"
        else:
            report += f"| {metric} | {value} |\n"
    
    report += "\n## Per-Task Results\n\n"
    report += "| Task ID | Predictions | Ground Truth | Latency (ms) | Tokens |\n"
    report += "|---------|-------------|--------------|--------------|--------|\n"
    
    for task_result in results['per_task_results']:
        preds = ", ".join(task_result['predictions'])
        truths = ", ".join(task_result['ground_truth'])
        report += f"| {task_result['task_id']} | {preds} | {truths} | {task_result['latency_ms']:.0f} | {task_result['tokens']} |\n"
    
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run RepoPilot evaluations")
    parser.add_argument("--dataset", default="sample_10", help="Dataset name")
    parser.add_argument("--output", default="results", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--generate-report", action="store_true", help="Generate markdown report")
    
    args = parser.parse_args()
    
    results = run_evaluation(
        dataset_name=args.dataset,
        output_dir=args.output,
        dry_run=args.dry_run
    )
    
    if args.generate_report:
        report = generate_report(results)
        report_file = Path(args.output) / f"report_{args.dataset}.md"
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {report_file}")
