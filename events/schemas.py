from pydantic import BaseModel, Field


# =========================================================
# EVENT
# =========================================================

class EventCreate(BaseModel):
    name: str
    category: str
    description: str = ""
    language: str = ""
    duration_minutes: int = Field(default=60, gt=0)
    rating: float = Field(default=0.0, ge=0, le=5)
    image_url: str = ""


class EventResponse(BaseModel):
    id: int
    name: str
    category: str
    description: str
    language: str
    duration_minutes: int
    rating: float
    image_url: str


class EventSearch(BaseModel):
    city: str | None = None
    category: str | None = None
    language: str | None = None


# =========================================================
# EVENT VENUE
# =========================================================

class EventVenueCreate(BaseModel):
    name: str
    city: str
    address: str
    capacity: int = Field(gt=0)


class EventVenueResponse(BaseModel):
    id: int
    name: str
    city: str
    address: str
    capacity: int


class EventVenueSearch(BaseModel):
    city: str


# =========================================================
# EVENT SHOW
# =========================================================

class EventShowCreate(BaseModel):
    event_id: int
    venue_id: int
    show_date: str
    show_time: str
    ticket_type: str
    ticket_price: int = Field(gt=0)
    total_tickets: int = Field(gt=0)
    available_tickets: int = Field(gt=0)


class EventShowResponse(BaseModel):
    id: int
    event_id: int
    venue_id: int
    show_date: str
    show_time: str
    ticket_type: str
    ticket_price: int
    total_tickets: int
    available_tickets: int


# =========================================================
# EVENT BOOKING
# =========================================================

class EventBookingCreate(BaseModel):
    event_id: int
    venue_id: int
    show_id: int

    customer_name: str
    customer_phone: str

    number_of_tickets: int = Field(gt=0)

    payment_method: str = "demo"


class EventBookingResponse(BaseModel):
    id: int
    user_id: int

    event_id: int
    venue_id: int
    show_id: int

    customer_name: str
    customer_phone: str

    show_date: str
    show_time: str
    ticket_type: str

    number_of_tickets: int
    total_price: int

    payment_method: str
    booking_status: str