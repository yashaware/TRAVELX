from pydantic import BaseModel, Field


# ============================================================
# CREATE HOTEL
# ============================================================

class HotelCreate(BaseModel):

    name: str

    city: str

    address: str | None = None

    description: str | None = None

    rating: float = Field(
        default=0.0,
        ge=0,
        le=5
    )

    price_per_night: int = Field(
        gt=0
    )

    available_rooms: int = Field(
        gt=0
    )

    amenities: str | None = None


# ============================================================
# HOTEL RESPONSE
# ============================================================

class HotelResponse(BaseModel):

    id: int

    name: str

    city: str

    address: str | None

    description: str | None

    rating: float

    price_per_night: int

    available_rooms: int

    amenities: str | None


# ============================================================
# HOTEL SEARCH
# ============================================================

class HotelSearch(BaseModel):

    city: str


# ============================================================
# HOTEL BOOKING
# ============================================================

class HotelBookingCreate(BaseModel):

    hotel_id: int

    guest_name: str

    guest_phone: str

    rooms: int = Field(
        gt=0
    )

    nights: int = Field(
        gt=0
    )

    payment_method: str = "demo"


# ============================================================
# HOTEL BOOKING RESPONSE
# ============================================================

class HotelBookingResponse(BaseModel):

    id: int

    user_id: int

    hotel_id: int

    guest_name: str

    guest_phone: str

    rooms: int

    nights: int

    total_price: int

    payment_method: str

    booking_status: str