"""
Evaluation metrics for RepoPilot benchmarks.
"""

from typing import List, Dict, Any
import numpy as np


def retrieval_recall(predictions: List[List[str]], ground_truth: List[List[str]], k: int = 5) -> float:
    """
    Calculate recall@k for retrieval.
    
    Args:
        predictions: List of predicted file paths for each query
        ground_truth: List of relevant file paths for each query
        k: Number of top results to consider
    
    Returns:
        Average recall@k across all queries
    """
    recalls = []
    
    for pred, truth in zip(predictions, ground_truth):
        top_k = pred[:k]
        hits = len(set(top_k) & set(truth))
        recall = hits / len(truth) if truth else 0
        recalls.append(recall)
    
    return np.mean(recalls) if recalls else 0.0


def exact_file_hit(predictions: List[List[str]], ground_truth: List[List[str]]) -> float:
    """
    Calculate exact file hit rate (correct file as #1 result).
    
    Args:
        predictions: List of predicted file paths for each query
        ground_truth: List of relevant file paths for each query
    
    Returns:
        Percentage of queries with correct file as first result
    """
    hits = 0
    
    for pred, truth in zip(predictions, ground_truth):
        if pred and truth and pred[0] in truth:
            hits += 1
    
    return hits / len(predictions) if predictions else 0.0


def patch_success_rate(results: List[Dict[str, Any]]) -> float:
    """
    Calculate patch success rate.
    
    Args:
        results: List of task results with 'patch_success' field
    
    Returns:
        Percentage of successful patches
    """
    successes = sum(1 for r in results if r.get('patch_success', False))
    return successes / len(results) if results else 0.0


def mean_reciprocal_rank(predictions: List[List[str]], ground_truth: List[List[str]]) -> float:
    """
    Calculate Mean Reciprocal Rank (MRR).
    
    Args:
        predictions: List of predicted file paths for each query
        ground_truth: List of relevant file paths for each query
    
    Returns:
        MRR score
    """
    reciprocal_ranks = []
    
    for pred, truth in zip(predictions, ground_truth):
        rr = 0
        for i, p in enumerate(pred):
            if p in truth:
                rr = 1.0 / (i + 1)
                break
        reciprocal_ranks.append(rr)
    
    return np.mean(reciprocal_ranks) if reciprocal_ranks else 0.0


def calculate_all_metrics(
    predictions: List[List[str]],
    ground_truth: List[List[str]],
    patch_results: List[Dict[str, Any]] = None,
    latencies: List[float] = None,
    token_usages: List[int] = None
) -> Dict[str, float]:
    """
    Calculate all evaluation metrics.
    
    Returns:
        Dictionary of metric names to values
    """
    metrics = {
        "retrieval_recall@5": retrieval_recall(predictions, ground_truth, k=5),
        "retrieval_recall@10": retrieval_recall(predictions, ground_truth, k=10),
        "exact_file_hit": exact_file_hit(predictions, ground_truth),
        "mrr": mean_reciprocal_rank(predictions, ground_truth),
    }
    
    if patch_results:
        metrics["patch_success_rate"] = patch_success_rate(patch_results)
    
    if latencies:
        metrics["avg_latency_ms"] = np.mean(latencies)
        metrics["p50_latency_ms"] = np.percentile(latencies, 50)
        metrics["p95_latency_ms"] = np.percentile(latencies, 95)
    
    if token_usages:
        metrics["avg_token_usage"] = np.mean(token_usages)
    
    return metrics
