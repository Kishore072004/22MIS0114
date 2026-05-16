import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
import time

from logging_middleware.middleware import custom_logging_middleware

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Notification System")

# To run this app, use: uvicorn main:app --reload --port 8001

# Register the shared logging middleware from logging_middleware/middleware.py
app.middleware("http")(custom_logging_middleware)

def process_email_or_sms(student_id: str, message: str):
    time.sleep(2)
    print(f"\n[BACKGROUND] -> Successfully sent message to {student_id}: '{message}'\n")

@app.post("/notifications", response_model=schemas.Notification)
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    db_notif = models.Notification(
        student_id=notification.student_id,
        message=notification.message,
        priority=notification.priority
    )
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return db_notif

@app.get("/notifications", response_model=List[schemas.Notification])
def get_notifications(
    skip: int = Query(0),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    notifications = db.query(models.Notification)\
        .order_by(desc(models.Notification.priority), desc(models.Notification.created_at))\
        .offset(skip)\
        .limit(limit)\
        .all()
        
    return notifications

@app.post("/send-notification")
def send_notification(
    notification: schemas.NotificationCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    db_notif = models.Notification(
        student_id=notification.student_id,
        message=notification.message,
        priority=notification.priority
    )
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    
    background_tasks.add_task(
        process_email_or_sms, 
        student_id=db_notif.student_id, 
        message=db_notif.message
    )
    
    return {
        "status": "success",
        "message": "Notification saved and queued for background sending!",
        "notification_id": db_notif.id
    }
