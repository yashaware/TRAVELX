from pydantic import BaseModel, Field


class FlightCreate(BaseModel):
    airline: str
    flight_number: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str

    economy_price: int = Field(gt=0)
    premium_economy_price: int = Field(gt=0)
    business_price: int = Field(gt=0)

    available_seats: int = Field(gt=0)


class FlightResponse(BaseModel):
    id: int
    airline: str
    flight_number: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str

    economy_price: int
    premium_economy_price: int
    business_price: int

    available_seats: int


class FlightSearch(BaseModel):
    source: str
    destination: str


class FlightBookingCreate(BaseModel):
    flight_id: int
    passenger_name: str
    passenger_phone: str
    travel_class: str
    seats: int = Field(gt=0)
    payment_method: str = "demo"


class FlightBookingResponse(BaseModel):
    id: int
    user_id: int
    flight_id: int
    passenger_name: str
    passenger_phone: str
    travel_class: str
    seats: int
    total_price: int
    payment_method: str
    booking_status: str