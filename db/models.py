from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime

from db.database import Base


# =========================================================
# USER MODEL
# =========================================================

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


# =========================================================
# BUS MODEL
# =========================================================

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


# =========================================================
# BUS BOOKING MODEL
# =========================================================

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


# =========================================================
# WALLET MODEL
# =========================================================

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


# =========================================================
# WALLET TRANSACTION MODEL
# =========================================================

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


# =========================================================
# GENERIC BOOKING MODEL
# =========================================================

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