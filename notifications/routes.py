from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from notifications.models import Notification
from notifications.schemas import (
    NotificationResponse,
    NotificationTestCreate
)

from auth.security import get_current_user


# ============================================================
# NOTIFICATION ROUTER
# ============================================================

notification_router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# ============================================================
# GET MY NOTIFICATIONS
# ============================================================

@notification_router.get(
    "/",
    response_model=list[NotificationResponse]
)
def get_my_notifications(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user["id"]
        )
        .order_by(
            Notification.created_at.desc()
        )
        .all()
    )

    return notifications


# ============================================================
# GET UNREAD COUNT
# ============================================================

@notification_router.get(
    "/unread-count"
)
def get_unread_count(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    count = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user["id"],
            Notification.is_read == False
        )
        .count()
    )

    return {
        "unread_count": count
    }


# ============================================================
# MARK ONE AS READ
# ============================================================

@notification_router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def mark_notification_read(
    notification_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id
        )
        .first()
    )

    if not notification:

        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    if notification.user_id != current_user["id"]:

        raise HTTPException(
            status_code=403,
            detail="You are not allowed to modify this notification."
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification


# ============================================================
# MARK ALL AS READ
# ============================================================

@notification_router.patch(
    "/read-all"
)
def mark_all_notifications_read(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    updated = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user["id"],
            Notification.is_read == False
        )
        .update(
            {
                Notification.is_read: True
            },
            synchronize_session=False
        )
    )

    db.commit()

    return {
        "message": "All notifications marked as read.",
        "updated_count": updated
    }


# ============================================================
# TEST NOTIFICATION
# ============================================================

@notification_router.post(
    "/test",
    response_model=NotificationResponse,
    status_code=201
)
def create_test_notification(
    data: NotificationTestCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    notification = Notification(
        user_id=current_user["id"],
        notification_type=data.notification_type,
        title=data.title,
        message=data.message,
        service=data.service,
        booking_id=data.booking_id,
        amount=data.amount,
        is_read=False
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification
