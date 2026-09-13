from pydantic import BaseModel, Field


# =========================================================
# MOVIE SCHEMAS
# =========================================================

class MovieCreate(BaseModel):
    title: str
    language: str
    genre: str
    duration_minutes: int = Field(gt=0)
    rating: float = Field(default=0.0, ge=0, le=5)
    description: str = ""
    release_date: str = ""
    is_active: bool = True


class MovieResponse(BaseModel):
    id: int
    title: str
    language: str
    genre: str
    duration_minutes: int
    rating: float
    description: str
    release_date: str
    is_active: bool


class MovieSearch(BaseModel):
    city: str | None = None
    language: str | None = None
    genre: str | None = None


# =========================================================
# CINEMA SCHEMAS
# =========================================================

class CinemaCreate(BaseModel):
    name: str
    city: str
    address: str
    total_seats: int = Field(gt=0)


class CinemaResponse(BaseModel):
    id: int
    name: str
    city: str
    address: str
    total_seats: int


class CinemaSearch(BaseModel):
    city: str


# =========================================================
# MOVIE SHOW SCHEMAS
# =========================================================

class MovieShowCreate(BaseModel):
    movie_id: int
    cinema_id: int
    show_date: str
    show_time: str
    screen_name: str
    ticket_price: int = Field(gt=0)
    total_seats: int = Field(gt=0)
    available_seats: int = Field(gt=0)


class MovieShowResponse(BaseModel):
    id: int
    movie_id: int
    cinema_id: int
    show_date: str
    show_time: str
    screen_name: str
    ticket_price: int
    total_seats: int
    available_seats: int


# =========================================================
# MOVIE BOOKING SCHEMAS
# =========================================================

class MovieBookingCreate(BaseModel):
    movie_id: int
    cinema_id: int
    show_id: int

    customer_name: str
    customer_phone: str

    seats: list[str]

    payment_method: str = "demo"


class MovieBookingResponse(BaseModel):
    id: int
    user_id: int

    movie_id: int
    cinema_id: int
    show_id: int

    customer_name: str
    customer_phone: str

    show_date: str
    show_time: str

    seats: str
    number_of_seats: int

    total_price: int

    payment_method: str
    booking_status: str