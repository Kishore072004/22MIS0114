from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Maintenance Scheduler")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
    return response

def init_dummy_data(db: Session):
    if db.query(models.Depot).first():
        return

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

@app.on_event("startup")
def on_startup():
    db = next(get_db())
    init_dummy_data(db)

@app.get("/depots", response_model=List[schemas.Depot])
def get_depots(db: Session = Depends(get_db)):
    return db.query(models.Depot).all()

@app.get("/vehicles", response_model=List[schemas.Vehicle])
def get_vehicles(db: Session = Depends(get_db)):
    return db.query(models.Vehicle).all()

@app.post("/schedule")
def create_schedule(request: schemas.ScheduleRequest, db: Session = Depends(get_db)):
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
        "hours_used": request.available_machine_hours - remaining_hours,
        "scheduled_tasks": scheduled_tasks
    }
