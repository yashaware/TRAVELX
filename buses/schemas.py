from pydantic import BaseModel, Field
# ============================================================
# BUS CREATE
# ============================================================
class BusCreate(BaseModel):
    operator: str
    bus_number: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    price: int = Field(gt=0)
    available_seats: int = Field(gt=0)
# ============================================================
# BUS RESPONSE
# ============================================================
class BusResponse(BaseModel):
    id: int
    operator: str
    bus_number: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    price: int
    available_seats: int
# ============================================================
# BUS SEARCH
# ============================================================
class BusSearch(BaseModel):
    source: str
    destination: str
# ============================================================
# BUS BOOKING CREATE
# ============================================================
class BusBookingCreate(BaseModel):
    bus_id: int
    passenger_name: str
    passenger_phone: str
    seats: int = Field(gt=0)
    payment_method: str = "demo"
# ============================================================
# BUS BOOKING RESPONSE
# ============================================================
class BusBookingResponse(BaseModel):
    id: int
    user_id: int
    bus_id: int
    passenger_name: str
    passenger_phone: str
    seats: int
    total_price: int
    payment_method: str
    booking_status: str
