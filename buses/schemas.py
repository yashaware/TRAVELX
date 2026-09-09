from pydantic import BaseModel
from typing import Optional


# =========================================================
# CREATE BUS
# =========================================================

class BusCreate(BaseModel):

    bus_number: str
    operator: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    price: int
    available_seats: int


# =========================================================
# BUS RESPONSE
# =========================================================

class BusResponse(BaseModel):

    id: int
    bus_number: str
    operator: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    price: int
    available_seats: int


# =========================================================
# BUS SEARCH
# =========================================================

class BusSearch(BaseModel):

    source: str
    destination: str
    
# =========================================================
# BUS BOOKING
# =========================================================

class BusBookingCreate(BaseModel):

    bus_id: int
    passenger_name: str
    passenger_phone: str
    seats: int


class BusBookingResponse(BaseModel):

    id: int
    user_id: int
    bus_id: int
    passenger_name: str
    passenger_phone: str
    seats: int
    total_price: int
    booking_status: str

    class Config:
        from_attributes = True