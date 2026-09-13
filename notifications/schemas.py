from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ============================================================
# NOTIFICATION RESPONSE
# ============================================================

class NotificationResponse(BaseModel):

    id: int
    user_id: int
    notification_type: str
    title: str
    message: str
    service: Optional[str] = None
    booking_id: Optional[int] = None
    amount: Optional[float] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# TEST NOTIFICATION CREATE
# ============================================================

class NotificationTestCreate(BaseModel):

    notification_type: str = "info"
    title: str = "TRAVELX Test Notification"
    message: str = "Your TRAVELX notification system is working."
    service: Optional[str] = None
    booking_id: Optional[int] = None
    amount: Optional[float] = None
