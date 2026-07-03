"""
Evaluation endpoints for benchmarking.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.workers.tasks import run_evaluation_task

router = APIRouter()


@router.post("/run", status_code=202)
async def run_evaluation(
    dataset: str = "sample_10",
    metrics: list = ["retrieval_recall", "patch_success"],
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
):
    """
    Run evaluation benchmark on a dataset.
    
    Metrics available:
    - retrieval_recall: % of relevant files in top-k results
    - exact_file_hit: % of tasks with correct file as #1 result
    - patch_success: % of generated patches passing tests
    - test_pass: % of generated tests passing
    - latency: average end-to-end time
    - token_usage: average tokens per task
    
    Datasets:
    - sample_10: 10 sample issues for quick testing
    - sample_50: 50 issues for full evaluation
    """
    from app.models.evaluation import EvaluationRun
    
    # Create evaluation record
    eval_run = EvaluationRun(
        dataset_name=dataset,
        metrics=metrics,
        status="pending"
    )
    db.add(eval_run)
    db.commit()
    db.refresh(eval_run)
    
    # Queue evaluation task
    run_evaluation_task.delay(eval_run.id, dataset, metrics)
    
    return {
        "evaluation_id": eval_run.id,
        "dataset": dataset,
        "metrics": metrics,
        "status": "pending"
    }


@router.get("/{eval_id}")
async def get_evaluation_status(
    eval_id: int,
    db: Session = Depends(get_db),
):
    """Get evaluation run status and results."""
    from app.models.evaluation import EvaluationRun
    
    eval_run = db.query(EvaluationRun).filter(EvaluationRun.id == eval_id).first()
    
    if not eval_run:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    return {
        "id": eval_run.id,
        "dataset": eval_run.dataset_name,
        "metrics": eval_run.metrics,
        "status": eval_run.status.value,
        "results": eval_run.results,
        "summary": eval_run.summary,
        "error_message": eval_run.error_message,
        "created_at": eval_run.created_at,
        "completed_at": eval_run.completed_at
    }


@router.get("/reports/{eval_id}")
async def get_evaluation_report(
    eval_id: int,
    db: Session = Depends(get_db),
):
    """Get detailed evaluation report in markdown format."""
    from app.models.evaluation import EvaluationRun
    
    eval_run = db.query(EvaluationRun).filter(EvaluationRun.id == eval_id).first()
    
    if not eval_run:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    if eval_run.status.value != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Evaluation not completed. Status: {eval_run.status.value}"
        )
    
    # Generate markdown report
    summary = eval_run.summary or {}
    
    report = f"""# Evaluation Report

## Overview
- **Dataset**: {eval_run.dataset_name}
- **Completed**: {eval_run.completed_at}
- **Status**: {eval_run.status.value}

## Summary Metrics
"""
    
    for metric, value in summary.items():
        report += f"- **{metric}**: {value}\n"
    
    report += "\n## Detailed Results\n\n"
    report += str(eval_run.results or "No detailed results available")
    
    return {
        "format": "markdown",
        "content": report
    }
