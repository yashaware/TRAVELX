from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime

from db.database import Base


# ============================================================
# NOTIFICATION MODEL
# ============================================================

class Notification(Base):

    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    notification_type = Column(
        String,
        nullable=False,
        default="info"
    )

    title = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    service = Column(
        String,
        nullable=True
    )

    booking_id = Column(
        Integer,
        nullable=True
    )

    amount = Column(
        Float,
        nullable=True
    )

    is_read = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
