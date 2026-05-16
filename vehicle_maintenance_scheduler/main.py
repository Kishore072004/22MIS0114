import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import time
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session

from logging_middleware.middleware import custom_logging_middleware

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)


def init_dummy_data(db: Session):
    """Seed the database with sample depots, vehicles, and tasks if empty."""
    if db.query(models.Depot).first():
        return  # Already seeded

    depot1 = models.Depot(name="Central Depot", location="North City")
    depot2 = models.Depot(name="South Depot", location="South City")
    db.add(depot1)
    db.add(depot2)
    db.commit()

    v1 = models.Vehicle(name="Truck A", depot_id=depot1.id)
    v2 = models.Vehicle(name="Van B", depot_id=depot1.id)
    v3 = models.Vehicle(name="Bus C", depot_id=depot2.id)
    db.add_all([v1, v2, v3])
    db.commit()

    t1 = models.MaintenanceTask(vehicle_id=v1.id, task_name="Oil Change", impact_score=5, duration_hours=2.0)
    t2 = models.MaintenanceTask(vehicle_id=v1.id, task_name="Engine Repair", impact_score=10, duration_hours=5.0)
    t3 = models.MaintenanceTask(vehicle_id=v2.id, task_name="Tire Replacement", impact_score=3, duration_hours=1.5)
    t4 = models.MaintenanceTask(vehicle_id=v3.id, task_name="Brake Fix", impact_score=8, duration_hours=3.0)
    db.add_all([t1, t2, t3, t4])
    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler: seed data on startup."""
    db = next(get_db())
    init_dummy_data(db)
    yield
    # Shutdown cleanup (nothing needed for SQLite)


# Create the FastAPI app with the lifespan handler
app = FastAPI(title="Vehicle Maintenance Scheduler", lifespan=lifespan)

# To run this app, use: uvicorn main:app --reload --port 8000


# Register the shared logging middleware from logging_middleware/middleware.py
app.middleware("http")(custom_logging_middleware)


@app.get("/depots", response_model=List[schemas.Depot])
def get_depots(db: Session = Depends(get_db)):
    """Return all depots."""
    return db.query(models.Depot).all()


@app.get("/vehicles", response_model=List[schemas.Vehicle])
def get_vehicles(db: Session = Depends(get_db)):
    """Return all vehicles."""
    return db.query(models.Vehicle).all()


@app.get("/tasks", response_model=List[schemas.MaintenanceTask])
def get_tasks(db: Session = Depends(get_db)):
    """Return all maintenance tasks."""
    return db.query(models.MaintenanceTask).all()


@app.post("/schedule")
def create_schedule(request: schemas.ScheduleRequest, db: Session = Depends(get_db)):
    """
    Greedy scheduling: prioritize tasks by highest impact score
    and fit as many as possible within the available machine hours.
    """
    tasks = db.query(models.MaintenanceTask).all()
    sorted_tasks = sorted(tasks, key=lambda t: t.impact_score, reverse=True)

    scheduled_tasks = []
    remaining_hours = request.available_machine_hours

    for task in sorted_tasks:
        if task.duration_hours <= remaining_hours:
            scheduled_tasks.append({
                "task_id": task.id,
                "task_name": task.task_name,
                "impact": task.impact_score,
                "duration": task.duration_hours
            })
            remaining_hours -= task.duration_hours

    return {
        "message": "Schedule created successfully",
        "total_available_hours": request.available_machine_hours,
        "hours_used": round(request.available_machine_hours - remaining_hours, 2),
        "hours_remaining": round(remaining_hours, 2),
        "scheduled_tasks": scheduled_tasks
    }
