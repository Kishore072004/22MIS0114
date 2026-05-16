from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime
from database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    message = Column(String)
    priority = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

Index('idx_priority_created', Notification.priority, Notification.created_at)
