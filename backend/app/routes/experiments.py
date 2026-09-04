"""
Experiments API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import json

from app.database import get_db, Experiment, ExperimentRun

router = APIRouter()

class ExperimentSchema(BaseModel):
    name: str
    description: str
    config: Dict[str, Any]

class ExperimentRunSchema(BaseModel):
    parameters: Dict[str, Any]
    results: Optional[Dict[str, Any]] = None

@router.post("/")
async def create_experiment(exp: ExperimentSchema, db: Session = Depends(get_db)):
    """Create new experiment"""
    exp_id = str(uuid.uuid4())
    db_exp = Experiment(
        id=exp_id,
        name=exp.name,
        description=exp.description,
        config=exp.config,
        status="created",
        created_at=datetime.utcnow()
    )
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    
    return {
        "id": db_exp.id,
        "name": db_exp.name,
        "description": db_exp.description,
        "status": db_exp.status,
        "created_at": db_exp.created_at
    }

@router.get("/{experiment_id}")
async def get_experiment(experiment_id: str, db: Session = Depends(get_db)):
    """Get experiment details"""
    exp = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    runs = db.query(ExperimentRun).filter(ExperimentRun.experiment_id == experiment_id).all()
    
    return {
        "id": exp.id,
        "name": exp.name,
        "description": exp.description,
        "status": exp.status,
        "config": exp.config,
        "created_at": exp.created_at,
        "updated_at": exp.updated_at,
        "runs": [
            {
                "id": r.id,
                "parameters": r.parameters,
                "results": r.results,
                "metrics": r.metrics,
                "status": r.status,
                "timestamp": r.timestamp
            }
            for r in runs
        ]
    }

@router.post("/{experiment_id}/runs")
async def create_experiment_run(
    experiment_id: str,
    run: ExperimentRunSchema,
    db: Session = Depends(get_db)
):
    """Create new run for experiment"""
    exp = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    run_id = str(uuid.uuid4())
    db_run = ExperimentRun(
        id=run_id,
        experiment_id=experiment_id,
        parameters=run.parameters,
        results=run.results or {},
        status="created",
        timestamp=datetime.utcnow()
    )
    db.add(db_run)
    
    # Update experiment timestamp
    exp.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_run)
    
    return {
        "id": db_run.id,
        "experiment_id": db_run.experiment_id,
        "parameters": db_run.parameters,
        "status": db_run.status,
        "timestamp": db_run.timestamp
    }

@router.patch("/{experiment_id}/runs/{run_id}")
async def update_experiment_run(
    experiment_id: str,
    run_id: str,
    data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update experiment run with results"""
    run = db.query(ExperimentRun).filter(
        ExperimentRun.id == run_id,
        ExperimentRun.experiment_id == experiment_id
    ).first()
    
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    if "results" in data:
        run.results = data["results"]
    if "metrics" in data:
        run.metrics = data["metrics"]
    if "status" in data:
        run.status = data["status"]
    
    db.commit()
    db.refresh(run)
    
    return {
        "id": run.id,
        "status": run.status,
        "results": run.results,
        "metrics": run.metrics
    }

@router.get("/{experiment_id}/runs/{run_id}")
async def get_experiment_run(
    experiment_id: str,
    run_id: str,
    db: Session = Depends(get_db)
):
    """Get specific experiment run"""
    run = db.query(ExperimentRun).filter(
        ExperimentRun.id == run_id,
        ExperimentRun.experiment_id == experiment_id
    ).first()
    
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    return {
        "id": run.id,
        "experiment_id": run.experiment_id,
        "parameters": run.parameters,
        "results": run.results,
        "metrics": run.metrics,
        "status": run.status,
        "timestamp": run.timestamp
    }
