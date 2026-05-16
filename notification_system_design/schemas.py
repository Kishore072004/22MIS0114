from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    student_id: str
    message: str
    priority: int

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
