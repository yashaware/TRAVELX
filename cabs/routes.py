from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Cab, CabBooking, Wallet, WalletTransaction

from cabs.schemas import (
    CabCreate,
    CabResponse,
    CabSearch,
    CabBookingCreate,
    CabBookingResponse
)

from auth.security import get_current_user


cab_router = APIRouter(
    prefix="/cabs",
    tags=["Cabs"]
)


# =========================
# GET ALL CABS
# =========================

@cab_router.get(
    "/",
    response_model=list[CabResponse]
)
def get_all_cabs(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(Cab).order_by(Cab.id).all()


# =========================
# CREATE CAB
# =========================

@cab_router.post(
    "/",
    response_model=CabResponse
)
def create_cab(
    cab_data: CabCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_cab = db.query(Cab).filter(
        Cab.vehicle_number == cab_data.vehicle_number
    ).first()

    if existing_cab:
        raise HTTPException(
            status_code=400,
            detail="Vehicle number already exists."
        )

    cab = Cab(
        driver_name=cab_data.driver_name,
        vehicle_number=cab_data.vehicle_number,
        cab_type=cab_data.cab_type,
        source=cab_data.source,
        destination=cab_data.destination,
        fare_per_km=cab_data.fare_per_km,
        available_seats=cab_data.available_seats,
        rating=cab_data.rating
    )

    db.add(cab)
    db.commit()
    db.refresh(cab)

    return cab


# =========================
# SEARCH CABS
# =========================

@cab_router.post(
    "/search",
    response_model=list[CabResponse]
)
def search_cabs(
    search_data: CabSearch,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    source = search_data.source.strip()
    destination = search_data.destination.strip()

    cabs = db.query(Cab).filter(
        Cab.source.ilike(source),
        Cab.destination.ilike(destination)
    ).order_by(Cab.rating.desc()).all()

    return cabs


# =========================
# BOOK CAB
# =========================

@cab_router.post(
    "/book",
    response_model=CabBookingResponse
)
def create_cab_booking(
    booking_data: CabBookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find cab
    cab = db.query(Cab).filter(
        Cab.id == booking_data.cab_id
    ).first()

    if not cab:
        raise HTTPException(
            status_code=404,
            detail="Cab not found."
        )

    # Check seats
    if cab.available_seats <= 0:
        raise HTTPException(
            status_code=400,
            detail="No seats available."
        )

    # Calculate fare
    total_price = (
        cab.fare_per_km *
        booking_data.distance_km
    )

    payment_method = (
        booking_data.payment_method
        .strip()
        .lower()
    )

    # =========================
    # WALLET PAYMENT
    # =========================

    if payment_method == "wallet":

        wallet = db.query(Wallet).filter(
            Wallet.user_id == current_user["id"]
        ).first()

        if not wallet:

            wallet = Wallet(
                user_id=current_user["id"],
                balance=0.0
            )

            db.add(wallet)
            db.flush()

        if wallet.balance < total_price:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Insufficient wallet balance. "
                    f"Available: ₹{wallet.balance:.2f}, "
                    f"Required: ₹{total_price:.2f}"
                )
            )

        # Deduct money
        wallet.balance -= total_price

        # Transaction record
        transaction = WalletTransaction(
            user_id=current_user["id"],
            transaction_type="debit",
            amount=total_price,
            description=(
                f"Cab booking - "
                f"{cab.cab_type} "
                f"({cab.source} to {cab.destination})"
            ),
            balance_after=wallet.balance
        )

        db.add(transaction)

    # Reduce available seats
    cab.available_seats -= 1

    # Create booking
    booking = CabBooking(

        user_id=current_user["id"],

        cab_id=cab.id,

        passenger_name=booking_data.passenger_name,

        passenger_phone=booking_data.passenger_phone,

        pickup_location=booking_data.pickup_location,

        drop_location=booking_data.drop_location,

        distance_km=booking_data.distance_km,

        cab_type=cab.cab_type,

        total_price=total_price,

        payment_method=payment_method,

        booking_status="confirmed"
    )

    db.add(booking)

    db.commit()

    db.refresh(booking)

    return booking


# =========================
# MY CAB BOOKINGS
# =========================

@cab_router.get(
    "/my-bookings",
    response_model=list[CabBookingResponse]
)
def get_my_cab_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    bookings = db.query(CabBooking).filter(
        CabBooking.user_id == current_user["id"]
    ).order_by(
        CabBooking.id.desc()
    ).all()

    return bookings


# =========================
# GET SINGLE CAB
# =========================

@cab_router.get(
    "/{cab_id}",
    response_model=CabResponse
)
def get_cab(
    cab_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    cab = db.query(Cab).filter(
        Cab.id == cab_id
    ).first()

    if not cab:

        raise HTTPException(
            status_code=404,
            detail="Cab not found."
        )

    return cab