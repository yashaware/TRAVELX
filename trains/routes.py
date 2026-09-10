from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db

from db.models import (
    Train,
    TrainBooking,
    Wallet,
    WalletTransaction
)

from trains.schemas import (
    TrainCreate,
    TrainResponse,
    TrainSearch,
    TrainBookingCreate,
    TrainBookingResponse
)

from auth.security import get_current_user


# ============================================================
# TRAIN ROUTER
# ============================================================

train_router = APIRouter(
    prefix="/trains",
    tags=["Trains"]
)


# ============================================================
# GET ALL TRAINS
# ============================================================

@train_router.get(
    "/",
    response_model=list[TrainResponse]
)
def get_all_trains(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    trains = db.query(
        Train
    ).order_by(
        Train.id
    ).all()

    return trains


# ============================================================
# CREATE TRAIN
# ============================================================

@train_router.post(
    "/",
    response_model=TrainResponse
)
def create_train(
    train_data: TrainCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_train = db.query(
        Train
    ).filter(
        Train.train_number == train_data.train_number
    ).first()

    if existing_train:
        raise HTTPException(
            status_code=400,
            detail="Train number already exists."
        )

    train = Train(
        train_name=train_data.train_name,
        train_number=train_data.train_number,
        source=train_data.source,
        destination=train_data.destination,
        departure_time=train_data.departure_time,
        arrival_time=train_data.arrival_time,
        sleeper_price=train_data.sleeper_price,
        third_ac_price=train_data.third_ac_price,
        second_ac_price=train_data.second_ac_price,
        first_ac_price=train_data.first_ac_price,
        available_seats=train_data.available_seats
    )

    db.add(train)
    db.commit()
    db.refresh(train)

    return train


# ============================================================
# SEARCH TRAINS
# ============================================================

@train_router.post(
    "/search",
    response_model=list[TrainResponse]
)
def search_trains(
    search_data: TrainSearch,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    trains = db.query(
        Train
    ).filter(
        Train.source.ilike(
            search_data.source.strip()
        ),
        Train.destination.ilike(
            search_data.destination.strip()
        )
    ).order_by(
        Train.id
    ).all()

    return trains


# ============================================================
# BOOK TRAIN
# ============================================================

@train_router.post(
    "/book",
    response_model=TrainBookingResponse
)
def create_train_booking(
    booking_data: TrainBookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # FIND TRAIN
    # --------------------------------------------------------

    train = db.query(
        Train
    ).filter(
        Train.id == booking_data.train_id
    ).first()

    if not train:
        raise HTTPException(
            status_code=404,
            detail="Train not found."
        )


    # --------------------------------------------------------
    # CHECK SEATS
    # --------------------------------------------------------

    if booking_data.seats > train.available_seats:
        raise HTTPException(
            status_code=400,
            detail=(
                "Not enough seats available. "
                f"Available: {train.available_seats}"
            )
        )


    # --------------------------------------------------------
    # TRAVEL CLASS
    # --------------------------------------------------------

    travel_class = (
        booking_data.travel_class
        .strip()
        .lower()
    )

    prices = {
        "sleeper": train.sleeper_price,
        "3a": train.third_ac_price,
        "2a": train.second_ac_price,
        "1a": train.first_ac_price
    }

    if travel_class not in prices:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid travel class. "
                "Use Sleeper, 3A, 2A or 1A."
            )
        )


    # --------------------------------------------------------
    # CALCULATE PRICE
    # --------------------------------------------------------

    total_price = (
        prices[travel_class]
        * booking_data.seats
    )


    # --------------------------------------------------------
    # PAYMENT METHOD
    # --------------------------------------------------------

    payment_method = (
        booking_data.payment_method
        .strip()
        .lower()
    )


    # --------------------------------------------------------
    # WALLET PAYMENT
    # --------------------------------------------------------

    if payment_method == "wallet":

        wallet = db.query(
            Wallet
        ).filter(
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
                    "Insufficient wallet balance. "
                    f"Available: ₹{wallet.balance:.2f}, "
                    f"Required: ₹{total_price:.2f}"
                )
            )


        wallet.balance -= total_price


        transaction = WalletTransaction(
            user_id=current_user["id"],
            transaction_type="debit",
            amount=total_price,
            description=(
                f"Train booking - "
                f"{train.train_name} "
                f"({train.source} to "
                f"{train.destination})"
            ),
            balance_after=wallet.balance
        )

        db.add(transaction)


    # --------------------------------------------------------
    # REDUCE AVAILABLE SEATS
    # --------------------------------------------------------

    train.available_seats -= booking_data.seats


    # --------------------------------------------------------
    # CREATE BOOKING
    # --------------------------------------------------------

    booking = TrainBooking(
        user_id=current_user["id"],
        train_id=train.id,
        passenger_name=booking_data.passenger_name,
        passenger_phone=booking_data.passenger_phone,
        travel_class=travel_class,
        seats=booking_data.seats,
        total_price=total_price,
        payment_method=payment_method,
        booking_status="confirmed"
    )

    db.add(booking)

    db.commit()

    db.refresh(booking)

    return booking


# ============================================================
# MY TRAIN BOOKINGS
# ============================================================

@train_router.get(
    "/my-bookings",
    response_model=list[TrainBookingResponse]
)
def get_my_train_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    bookings = db.query(
        TrainBooking
    ).filter(
        TrainBooking.user_id == current_user["id"]
    ).order_by(
        TrainBooking.id.desc()
    ).all()

    return bookings


# ============================================================
# GET SINGLE TRAIN
# ============================================================

@train_router.get(
    "/{train_id}",
    response_model=TrainResponse
)
def get_train(
    train_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    train = db.query(
        Train
    ).filter(
        Train.id == train_id
    ).first()

    if not train:
        raise HTTPException(
            status_code=404,
            detail="Train not found."
        )

    return train