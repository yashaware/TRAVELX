from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime

from db.database import Base


# ============================================================
# USER MODEL
# ============================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    phone = Column(
        String,
        nullable=True
    )

    password = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# BUS MODEL
# ============================================================

class Bus(Base):

    __tablename__ = "buses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    operator = Column(
        String,
        nullable=False
    )

    bus_number = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    source = Column(
        String,
        nullable=False,
        index=True
    )

    destination = Column(
        String,
        nullable=False,
        index=True
    )

    departure_time = Column(
        String,
        nullable=False
    )

    arrival_time = Column(
        String,
        nullable=False
    )

    price = Column(
        Integer,
        nullable=False
    )

    available_seats = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# BUS BOOKING MODEL
# ============================================================

class BusBooking(Base):

    __tablename__ = "bus_bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    bus_id = Column(
        Integer,
        nullable=False
    )

    passenger_name = Column(
        String,
        nullable=False
    )

    passenger_phone = Column(
        String,
        nullable=False
    )

    seats = Column(
        Integer,
        nullable=False
    )

    total_price = Column(
        Integer,
        nullable=False
    )

    booking_status = Column(
        String,
        default="confirmed"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# WALLET MODEL
# ============================================================

class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        unique=True,
        nullable=False,
        index=True
    )

    balance = Column(
        Float,
        default=0.0,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# WALLET TRANSACTION MODEL
# ============================================================

class WalletTransaction(Base):

    __tablename__ = "wallet_transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    transaction_type = Column(
        String,
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    balance_after = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# GENERIC BOOKING MODEL
# ============================================================

class Booking(Base):

    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    booking_type = Column(
        String,
        nullable=False,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    source = Column(
        String,
        nullable=True
    )

    destination = Column(
        String,
        nullable=True
    )

    booking_date = Column(
        String,
        nullable=True
    )

    amount = Column(
        Float,
        default=0.0,
        nullable=False
    )

    payment_method = Column(
        String,
        default="demo",
        nullable=False
    )

    status = Column(
        String,
        default="confirmed",
        nullable=False
    )

    details = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
# =========================================================
# TRAIN MODEL
# =========================================================

class Train(Base):

    __tablename__ = "trains"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    train_name = Column(
        String,
        nullable=False
    )

    train_number = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    source = Column(
        String,
        nullable=False,
        index=True
    )

    destination = Column(
        String,
        nullable=False,
        index=True
    )

    departure_time = Column(
        String,
        nullable=False
    )

    arrival_time = Column(
        String,
        nullable=False
    )

    sleeper_price = Column(
        Integer,
        nullable=False
    )

    third_ac_price = Column(
        Integer,
        nullable=False
    )

    second_ac_price = Column(
        Integer,
        nullable=False
    )

    first_ac_price = Column(
        Integer,
        nullable=False
    )

    available_seats = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================================================
# TRAIN BOOKING MODEL
# =========================================================

class TrainBooking(Base):

    __tablename__ = "train_bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    train_id = Column(
        Integer,
        nullable=False
    )

    passenger_name = Column(
        String,
        nullable=False
    )

    passenger_phone = Column(
        String,
        nullable=False
    )

    travel_class = Column(
        String,
        nullable=False
    )

    seats = Column(
        Integer,
        nullable=False
    )

    total_price = Column(
        Integer,
        nullable=False
    )

    payment_method = Column(
        String,
        default="demo"
    )

    booking_status = Column(
        String,
        default="confirmed"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
# ============================================================
# HOTEL
# ============================================================

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    city = Column(String, nullable=False, index=True)

    address = Column(String, nullable=True)

    description = Column(String, nullable=True)

    rating = Column(Float, default=0.0)

    price_per_night = Column(Integer, nullable=False)

    available_rooms = Column(Integer, nullable=False)

    amenities = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# HOTEL BOOKING
# ============================================================

class HotelBooking(Base):
    __tablename__ = "hotel_bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    hotel_id = Column(
        Integer,
        nullable=False
    )

    guest_name = Column(
        String,
        nullable=False
    )

    guest_phone = Column(
        String,
        nullable=False
    )

    rooms = Column(
        Integer,
        nullable=False
    )

    nights = Column(
        Integer,
        nullable=False
    )

    total_price = Column(
        Integer,
        nullable=False
    )

    payment_method = Column(
        String,
        default="demo"
    )

    booking_status = Column(
        String,
        default="confirmed"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
# =========================================================
# FLIGHT MODELS
# =========================================================

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    airline = Column(String, nullable=False)
    flight_number = Column(String, nullable=False, unique=True, index=True)
    source = Column(String, nullable=False, index=True)
    destination = Column(String, nullable=False, index=True)
    departure_time = Column(String, nullable=False)
    arrival_time = Column(String, nullable=False)

    economy_price = Column(Integer, nullable=False)
    premium_economy_price = Column(Integer, nullable=False)
    business_price = Column(Integer, nullable=False)

    available_seats = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class FlightBooking(Base):
    __tablename__ = "flight_bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    flight_id = Column(Integer, nullable=False)

    passenger_name = Column(String, nullable=False)
    passenger_phone = Column(String, nullable=False)

    travel_class = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)

    total_price = Column(Integer, nullable=False)
    payment_method = Column(String, default="demo")
    booking_status = Column(String, default="confirmed")

    created_at = Column(DateTime, default=datetime.utcnow)
# =========================
# CAB MODELS
# =========================

class Cab(Base):
    __tablename__ = "cabs"

    id = Column(Integer, primary_key=True, index=True)

    driver_name = Column(String, nullable=False)
    vehicle_number = Column(String, nullable=False, unique=True, index=True)

    cab_type = Column(String, nullable=False)

    source = Column(String, nullable=False, index=True)
    destination = Column(String, nullable=False, index=True)

    fare_per_km = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)

    rating = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)


class CabBooking(Base):
    __tablename__ = "cab_bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False, index=True)
    cab_id = Column(Integer, nullable=False)

    passenger_name = Column(String, nullable=False)
    passenger_phone = Column(String, nullable=False)

    pickup_location = Column(String, nullable=False)
    drop_location = Column(String, nullable=False)

    distance_km = Column(Integer, nullable=False)

    cab_type = Column(String, nullable=False)

    total_price = Column(Integer, nullable=False)

    payment_method = Column(String, default="demo")
    booking_status = Column(String, default="confirmed")

    created_at = Column(DateTime, default=datetime.utcnow)
    
# =========================
# FOOD ORDERING MODELS
# =========================

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    address = Column(String, nullable=True)

    cuisine = Column(String, nullable=True)
    description = Column(String, nullable=True)

    rating = Column(Float, default=0.0)
    delivery_time = Column(Integer, nullable=False, default=30)

    is_open = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_id = Column(Integer, nullable=False, index=True)

    name = Column(String, nullable=False)
    category = Column(String, nullable=False)

    description = Column(String, nullable=True)

    price = Column(Integer, nullable=False)

    is_available = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class FoodOrder(Base):
    __tablename__ = "food_orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False, index=True)
    restaurant_id = Column(Integer, nullable=False)

    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)

    delivery_address = Column(String, nullable=False)

    total_price = Column(Integer, nullable=False)

    payment_method = Column(String, default="demo")
    order_status = Column(String, default="confirmed")

    created_at = Column(DateTime, default=datetime.utcnow)


class FoodOrderItem(Base):
    __tablename__ = "food_order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, nullable=False, index=True)
    food_item_id = Column(Integer, nullable=False)

    item_name = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    subtotal = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
# =========================
# MOVIE BOOKING MODELS
# =========================

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    language = Column(String, nullable=False)
    genre = Column(String, nullable=False)

    duration_minutes = Column(Integer, nullable=False)

    rating = Column(Float, default=0.0)

    description = Column(String, nullable=True)

    release_date = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class Cinema(Base):
    __tablename__ = "cinemas"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)

    total_seats = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class MovieShow(Base):
    __tablename__ = "movie_shows"

    id = Column(Integer, primary_key=True, index=True)

    movie_id = Column(Integer, nullable=False, index=True)
    cinema_id = Column(Integer, nullable=False, index=True)

    show_date = Column(String, nullable=False)
    show_time = Column(String, nullable=False)

    screen_name = Column(String, nullable=False)

    ticket_price = Column(Integer, nullable=False)

    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class MovieBooking(Base):
    __tablename__ = "movie_bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False, index=True)

    movie_id = Column(Integer, nullable=False)
    cinema_id = Column(Integer, nullable=False)
    show_id = Column(Integer, nullable=False)

    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)

    show_date = Column(String, nullable=False)
    show_time = Column(String, nullable=False)

    seats = Column(String, nullable=False)

    number_of_seats = Column(Integer, nullable=False)

    total_price = Column(Integer, nullable=False)

    payment_method = Column(String, default="demo")

    booking_status = Column(String, default="confirmed")

    created_at = Column(DateTime, default=datetime.utcnow)
# =========================================================
# EVENTS
# =========================================================

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    language = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    rating = Column(Float, default=0.0)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class EventVenue(Base):
    __tablename__ = "event_venues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class EventShow(Base):
    __tablename__ = "event_shows"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False, index=True)
    venue_id = Column(Integer, nullable=False, index=True)
    show_date = Column(String, nullable=False)
    show_time = Column(String, nullable=False)
    ticket_type = Column(String, nullable=False)
    ticket_price = Column(Integer, nullable=False)
    total_tickets = Column(Integer, nullable=False)
    available_tickets = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class EventBooking(Base):
    __tablename__ = "event_bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    event_id = Column(Integer, nullable=False)
    venue_id = Column(Integer, nullable=False)
    show_id = Column(Integer, nullable=False)

    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)

    show_date = Column(String, nullable=False)
    show_time = Column(String, nullable=False)
    ticket_type = Column(String, nullable=False)

    number_of_tickets = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)

    payment_method = Column(String, default="demo")
    booking_status = Column(String, default="confirmed")

    created_at = Column(DateTime, default=datetime.utcnow)