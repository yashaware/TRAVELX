from pydantic import BaseModel, Field


# ============================================================
# TRAIN CREATE
# ============================================================

class TrainCreate(BaseModel):

    train_name: str

    train_number: str

    source: str

    destination: str

    departure_time: str

    arrival_time: str

    sleeper_price: int = Field(
        gt=0
    )

    third_ac_price: int = Field(
        gt=0
    )

    second_ac_price: int = Field(
        gt=0
    )

    first_ac_price: int = Field(
        gt=0
    )

    available_seats: int = Field(
        gt=0
    )


# ============================================================
# TRAIN RESPONSE
# ============================================================

class TrainResponse(BaseModel):

    id: int

    train_name: str

    train_number: str

    source: str

    destination: str

    departure_time: str

    arrival_time: str

    sleeper_price: int

    third_ac_price: int

    second_ac_price: int

    first_ac_price: int

    available_seats: int


# ============================================================
# TRAIN SEARCH
# ============================================================

class TrainSearch(BaseModel):

    source: str

    destination: str


# ============================================================
# TRAIN BOOKING
# ============================================================

class TrainBookingCreate(BaseModel):

    train_id: int

    passenger_name: str

    passenger_phone: str

    travel_class: str

    seats: int = Field(
        gt=0
    )

    payment_method: str = "demo"


# ============================================================
# TRAIN BOOKING RESPONSE
# ============================================================

class TrainBookingResponse(BaseModel):

    id: int

    user_id: int

    train_id: int

    passenger_name: str

    passenger_phone: str

    travel_class: str

    seats: int

    total_price: int

    payment_method: str

    booking_status: str