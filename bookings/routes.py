from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db

from db.models import (
    Booking,
    Wallet,
    WalletTransaction
)

from bookings.schemas import (
    BookingCreate,
    BookingResponse
)

from auth.security import get_current_user


# ============================================================
# BOOKING ROUTER
# ============================================================

booking_router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


# ============================================================
# CREATE BOOKING
# ============================================================

@booking_router.post(
    "/",
    response_model=BookingResponse
)
def create_booking(
    booking_data: BookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    amount = float(
        booking_data.amount
    )

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
        if wallet.balance < amount:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Insufficient wallet balance. "
                    f"Available: ₹{wallet.balance:.2f}, "
                    f"Required: ₹{amount:.2f}"
                )
            )


        # Deduct money
        wallet.balance -= amount


        # Create debit transaction
        transaction = WalletTransaction(
            user_id=current_user["id"],
            transaction_type="debit",
            amount=amount,
            description=(
                f"Payment for "
                f"{booking_data.title}"
            ),
            balance_after=wallet.balance
        )

        db.add(transaction)


    # ========================================================
    # CREATE BOOKING
    # ========================================================

    booking = Booking(

        user_id=current_user["id"],

        booking_type=booking_data.booking_type,

        title=booking_data.title,

        source=booking_data.source,

        destination=booking_data.destination,

        booking_date=booking_data.booking_date,

        amount=amount,

        payment_method=payment_method,

        status="confirmed",

        details=booking_data.details
    )


    db.add(booking)

    db.commit()

    db.refresh(booking)


    return booking


# ============================================================
# GET MY BOOKINGS
# ============================================================

@booking_router.get(
    "/my",
    response_model=list[BookingResponse]
)
def get_my_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    bookings = db.query(
        Booking
    ).filter(
        Booking.user_id == current_user["id"]
    ).order_by(
        Booking.id.desc()
    ).all()

    return bookings