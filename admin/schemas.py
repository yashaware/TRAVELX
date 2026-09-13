from pydantic import BaseModel
from typing import List, Optional


# ============================================================
# SERVICE STATS
# ============================================================

class ServiceStats(BaseModel):
    service: str
    bookings: int
    revenue: float
    cancelled: int


# ============================================================
# ADMIN DASHBOARD
# ============================================================

class DashboardSummary(BaseModel):
    total_users: int
    total_bookings: int
    total_revenue: float
    total_cancelled: int
    wallet_transactions: int
    services: List[ServiceStats]


# ============================================================
# ADMIN USER
# ============================================================

class AdminUserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    created_at: Optional[str] = None


# ============================================================
# ADMIN BOOKING
# ============================================================

class AdminBookingResponse(BaseModel):
    id: int
    service: str
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    amount: float = 0.0
    status: str
    payment_method: Optional[str] = None
    created_at: Optional[str] = None