from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import (
    Bus,
    BusBooking,
    Wallet,
    WalletTransaction
)

from buses.schemas import (
    BusCreate,
    BusResponse,
    BusSearch,
    BusBookingCreate,
    BusBookingResponse
)

from auth.security import get_current_user


# ============================================================
# BUS ROUTER
# ============================================================

bus_router = APIRouter(
    prefix="/buses",
    tags=["Buses"]
)


# ============================================================
# GET ALL BUSES
# ============================================================

@bus_router.get(
    "/",
    response_model=list[BusResponse]
)
def get_all_buses(
    db: Session = Depends(get_db)
):

    return db.query(Bus).all()


# ============================================================
# CREATE BUS
# ============================================================

@bus_router.post(
    "/",
    response_model=BusResponse
)
def create_bus(
    bus_data: BusCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_bus = db.query(Bus).filter(
        Bus.bus_number == bus_data.bus_number
    ).first()

    if existing_bus:

        raise HTTPException(
            status_code=400,
            detail="Bus number already exists"
        )

    bus = Bus(
        operator=bus_data.operator,
        bus_number=bus_data.bus_number,
        source=bus_data.source,
        destination=bus_data.destination,
        departure_time=bus_data.departure_time,
        arrival_time=bus_data.arrival_time,
        price=bus_data.price,
        available_seats=bus_data.available_seats
    )

    db.add(bus)
    db.commit()
    db.refresh(bus)

    return bus


# ============================================================
# SEARCH BUSES
# ============================================================

@bus_router.post(
    "/search",
    response_model=list[BusResponse]
)
def search_buses(
    search_data: BusSearch,
    db: Session = Depends(get_db)
):

    buses = db.query(Bus).filter(
        Bus.source.ilike(search_data.source),
        Bus.destination.ilike(search_data.destination)
    ).all()

    return buses


# ============================================================
# CREATE BUS BOOKING
# ============================================================

@bus_router.post(
    "/book",
    response_model=BusBookingResponse
)
def create_bus_booking(
    booking_data: BusBookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # ========================================================
    # FIND BUS
    # ========================================================

    bus = db.query(Bus).filter(
        Bus.id == booking_data.bus_id
    ).first()

    if not bus:

        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )


    # ========================================================
    # CHECK SEATS
    # ========================================================

    if booking_data.seats <= 0:

        raise HTTPException(
            status_code=400,
            detail="Number of seats must be greater than 0"
        )


    if bus.available_seats < booking_data.seats:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Only {bus.available_seats} "
                f"seats are available"
            )
        )


    # ========================================================
    # CALCULATE TOTAL
    # ========================================================

    total_price = (
        bus.price * booking_data.seats
    )


    # ========================================================
    # PAYMENT METHOD
    # ========================================================

    payment_method = (
        booking_data.payment_method
        .strip()
        .lower()
    )


    # ========================================================
    # WALLET PAYMENT
    # ========================================================

    if payment_method == "wallet":

        wallet = db.query(Wallet).filter(
            Wallet.user_id == current_user["id"]
        ).first()


        # Create wallet if needed
        if not wallet:

            wallet = Wallet(
                user_id=current_user["id"],
                balance=0.0
            )

            db.add(wallet)
            db.flush()


        # Check balance
        if wallet.balance < total_price:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Insufficient wallet balance. "
                    f"Available: ₹{wallet.balance:.2f}, "
                    f"Required: ₹{total_price:.2f}"
                )
            )


        # ====================================================
        # DEDUCT WALLET
        # ====================================================

        wallet.balance -= total_price


        # ====================================================
        # CREATE WALLET TRANSACTION
        # ====================================================

        transaction = WalletTransaction(

            user_id=current_user["id"],

            transaction_type="debit",

            amount=total_price,

            description=(
                f"Bus booking - "
                f"{bus.operator} "
                f"({bus.source} to {bus.destination})"
            ),

            balance_after=wallet.balance
        )

        db.add(transaction)


    # ========================================================
    # UPDATE BUS SEATS
    # ========================================================

    bus.available_seats -= booking_data.seats


    # ========================================================
    # CREATE BUS BOOKING
    # ========================================================

    booking = BusBooking(

        user_id=current_user["id"],

        bus_id=booking_data.bus_id,

        passenger_name=booking_data.passenger_name,

        passenger_phone=booking_data.passenger_phone,

        seats=booking_data.seats,

        total_price=total_price,

        booking_status="confirmed"
    )


    db.add(booking)

    db.commit()

    db.refresh(booking)

    return booking


# ============================================================
# GET MY BUS BOOKINGS
# ============================================================

@bus_router.get(
    "/my-bookings",
    response_model=list[BusBookingResponse]
)
def get_my_bus_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    bookings = db.query(
        BusBooking
    ).filter(
        BusBooking.user_id == current_user["id"]
    ).order_by(
        BusBooking.id.desc()
    ).all()

    return bookings


# ============================================================
# GET SINGLE BUS
# ============================================================

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