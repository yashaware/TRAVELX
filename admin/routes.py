from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.database import get_db

from admin.service import (
    get_dashboard_stats,
    get_all_users,
    get_all_bookings,
)

from admin.schemas import (
    DashboardSummary,
    AdminUserResponse,
    AdminBookingResponse,
)

from auth.security import get_current_user


# ============================================================
# ADMIN ROUTER
# ============================================================

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ============================================================
# ADMIN AUTHENTICATION
# ============================================================

def verify_admin(
    current_user=Depends(get_current_user)
):
    """
    Allow access only to users whose JWT contains role='admin'.
    """

    if current_user.get("role") != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required."
        )

    return current_user


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@admin_router.get(
    "/dashboard",
    response_model=DashboardSummary
)
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(verify_admin)
):

    return get_dashboard_stats(db)


# ============================================================
# ADMIN USERS
# ============================================================

@admin_router.get(
    "/users",
    response_model=list[AdminUserResponse]
)
def admin_users(
    search: str = Query(default=""),
    limit: int = Query(
        default=100,
        ge=1,
        le=500
    ),
    db: Session = Depends(get_db),
    current_user=Depends(verify_admin)
):

    users = get_all_users(
        db,
        search=search,
        limit=limit
    )

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "created_at": (
                user.created_at.isoformat()
                if user.created_at
                else None
            ),
        }
        for user in users
    ]


# ============================================================
# ADMIN BOOKINGS
# ============================================================

@admin_router.get(
    "/bookings",
    response_model=list[AdminBookingResponse]
)
def admin_bookings(
    service: str = Query(default="All"),
    status: str = Query(default="All"),
    search: str = Query(default=""),
    db: Session = Depends(get_db),
    current_user=Depends(verify_admin)
):

    return get_all_bookings(
        db,
        service=service,
        status=status,
        search=search,
    )