from pydantic import BaseModel
from typing import Optional


# =========================================================
# CREATE GENERIC BOOKING
# =========================================================

class BookingCreate(BaseModel):

    booking_type: str

    title: str

    source: Optional[str] = None

    destination: Optional[str] = None

    booking_date: Optional[str] = None

    amount: float = 0

    payment_method: str = "demo"

    details: Optional[str] = None


# =========================================================
# BOOKING RESPONSE
# =========================================================

class BookingResponse(BaseModel):

    id: int
    user_id: int
    booking_type: str
    title: str
    source: Optional[str]
    destination: Optional[str]
    booking_date: Optional[str]
    amount: float
    payment_method: str
    status: str
    details: Optional[str]