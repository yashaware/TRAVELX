from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Bus, BusBooking

from buses.schemas import (
    BusCreate,
    BusResponse,
    BusSearch,
    BusBookingCreate,
    BusBookingResponse
)

from auth.security import get_current_user


# =========================================================
# BUS ROUTER
# =========================================================

bus_router = APIRouter(
    prefix="/buses",
    tags=["Buses"]
)


# =========================================================
# ADD BUS
# =========================================================

@bus_router.post(
    "/",
    response_model=BusResponse
)
def create_bus(
    bus_data: BusCreate,
    db: Session = Depends(get_db)
):

    new_bus = Bus(
        bus_number=bus_data.bus_number,
        operator=bus_data.operator,
        source=bus_data.source,
        destination=bus_data.destination,
        departure_time=bus_data.departure_time,
        arrival_time=bus_data.arrival_time,
        price=bus_data.price,
        available_seats=bus_data.available_seats
    )

    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)

    return new_bus


# =========================================================
# GET ALL BUSES
# =========================================================

@bus_router.get(
    "/",
    response_model=list[BusResponse]
)
def get_all_buses(
    db: Session = Depends(get_db)
):

    buses = db.query(Bus).all()

    return buses


# =========================================================
# SEARCH BUSES
# =========================================================

@bus_router.post(
    "/search",
    response_model=list[BusResponse]
)
def search_buses(
    search_data: BusSearch,
    db: Session = Depends(get_db)
):

    buses = db.query(Bus).filter(
        Bus.source == search_data.source,
        Bus.destination == search_data.destination
    ).all()

    return buses


# =========================================================
# CREATE BUS BOOKING
# =========================================================

@bus_router.post(
    "/book",
    response_model=BusBookingResponse
)
def create_bus_booking(
    booking_data: BusBookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Find the bus
    # -----------------------------------------------------

    bus = db.query(Bus).filter(
        Bus.id == booking_data.bus_id
    ).first()

    if not bus:
        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )


    # -----------------------------------------------------
    # Check number of seats
    # -----------------------------------------------------

    if booking_data.seats <= 0:
        raise HTTPException(
            status_code=400,
            detail="Seats must be at least 1"
        )


    # -----------------------------------------------------
    # Check available seats
    # -----------------------------------------------------

    if booking_data.seats > bus.available_seats:
        raise HTTPException(
            status_code=400,
            detail="Not enough seats available"
        )


    # -----------------------------------------------------
    # Calculate total price
    # -----------------------------------------------------

    total_price = bus.price * booking_data.seats


    # -----------------------------------------------------
    # Create booking
    # -----------------------------------------------------

    new_booking = BusBooking(
        user_id=current_user["id"],
        bus_id=booking_data.bus_id,
        passenger_name=booking_data.passenger_name,
        passenger_phone=booking_data.passenger_phone,
        seats=booking_data.seats,
        total_price=total_price,
        booking_status="confirmed"
    )


    # -----------------------------------------------------
    # Reduce available seats
    # -----------------------------------------------------

    bus.available_seats -= booking_data.seats


    # -----------------------------------------------------
    # Save booking
    # -----------------------------------------------------

    db.add(new_booking)

    db.commit()

    db.refresh(new_booking)

    return new_booking


# =========================================================
# GET MY BUS BOOKINGS
# =========================================================

@bus_router.get(
    "/my-bookings",
    response_model=list[BusBookingResponse]
)
def get_my_bus_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    bookings = db.query(BusBooking).filter(
        BusBooking.user_id == current_user["id"]
    ).all()

    return bookings


# =========================================================
# GET BUS BY ID
# =========================================================

@bus_router.get(
    "/{bus_id}",
    response_model=BusResponse
)
def get_bus(
    bus_id: int,
    db: Session = Depends(get_db)
):

    bus = db.query(Bus).filter(
        Bus.id == bus_id
    ).first()

    if not bus:
        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    return bus