from pydantic import BaseModel, Field


# =========================
# CAB CREATE
# =========================

class CabCreate(BaseModel):
    driver_name: str
    vehicle_number: str
    cab_type: str

    source: str
    destination: str

    fare_per_km: int = Field(gt=0)
    available_seats: int = Field(gt=0)

    rating: float = Field(default=0.0, ge=0, le=5)


# =========================
# CAB RESPONSE
# =========================

class CabResponse(BaseModel):
    id: int

    driver_name: str
    vehicle_number: str
    cab_type: str

    source: str
    destination: str

    fare_per_km: int
    available_seats: int

    rating: float


# =========================
# CAB SEARCH
# =========================

class CabSearch(BaseModel):
    source: str
    destination: str


# =========================
# CAB BOOKING
# =========================

class CabBookingCreate(BaseModel):
    cab_id: int

    passenger_name: str
    passenger_phone: str

    pickup_location: str
    drop_location: str

    distance_km: int = Field(gt=0)

    payment_method: str = "demo"


# =========================
# CAB BOOKING RESPONSE
# =========================

class CabBookingResponse(BaseModel):
    id: int

    user_id: int
    cab_id: int

    passenger_name: str
    passenger_phone: str

    pickup_location: str
    drop_location: str

    distance_km: int

    cab_type: str

    total_price: int

    payment_method: str
    booking_status: str