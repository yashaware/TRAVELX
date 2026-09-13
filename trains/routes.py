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

from auth.security import (
    get_current_user,
    require_admin
)


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

    return db.query(
        Train
    ).order_by(
        Train.id
    ).all()


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
        Train.source.ilike(search_data.source.strip()),
        Train.destination.ilike(search_data.destination.strip())
    ).order_by(
        Train.id
    ).all()

    return trains


# ============================================================
# CREATE TRAIN BOOKING
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

    # ========================================================
    # FIND TRAIN
    # ========================================================

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


    # ========================================================
    # CHECK SEATS
    # ========================================================

    if booking_data.seats <= 0:

        raise HTTPException(
            status_code=400,
            detail="Seats must be greater than 0."
        )

    if booking_data.seats > train.available_seats:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Not enough seats available. "
                f"Available: {train.available_seats}"
            )
        )


    # ========================================================
    # TRAVEL CLASS
    # ========================================================

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


    # ========================================================
    # CALCULATE TOTAL
    # ========================================================

    total_price = (
        prices[travel_class] *
        booking_data.seats
    )


    # ========================================================
    # PAYMENT METHOD
    # ========================================================

    payment_method = (
        booking_data.payment_method
        .strip()
        .lower()
    )


    if payment_method not in [
        "wallet",
        "demo"
    ]:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid payment method. "
                "Use 'wallet' or 'demo'."
            )
        )


    # ========================================================
    # WALLET PAYMENT
    # ========================================================

    if payment_method == "wallet":

        wallet = db.query(
            Wallet
        ).filter(
            Wallet.user_id == current_user["id"]
        ).first()


        # ----------------------------------------------------
        # CREATE WALLET IF NEEDED
        # ----------------------------------------------------

        if not wallet:

            wallet = Wallet(
                user_id=current_user["id"],
                balance=0.0
            )

            db.add(wallet)
            db.flush()


        # ----------------------------------------------------
        # CHECK BALANCE
        # ----------------------------------------------------

        if wallet.balance < total_price:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Insufficient wallet balance. "
                    f"Available: ₹{wallet.balance:.2f}, "
                    f"Required: ₹{total_price:.2f}"
                )
            )


        # ----------------------------------------------------
        # DEDUCT WALLET
        # ----------------------------------------------------

        wallet.balance -= total_price


        # ----------------------------------------------------
        # WALLET DEBIT TRANSACTION
        # ----------------------------------------------------

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


    # ========================================================
    # REDUCE TRAIN SEATS
    # ========================================================

    train.available_seats -= booking_data.seats


    # ========================================================
    # CREATE TRAIN BOOKING
    # ========================================================

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
# GET MY TRAIN BOOKINGS
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
# CANCEL TRAIN BOOKING + WALLET REFUND
# ============================================================

@train_router.post(
    "/bookings/{booking_id}/cancel",
    response_model=TrainBookingResponse
)
def cancel_train_booking(
    booking_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # ========================================================
    # FIND BOOKING
    # ========================================================

    booking = db.query(
        TrainBooking
    ).filter(
        TrainBooking.id == booking_id
    ).first()


    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Train booking not found."
        )


    # ========================================================
    # CHECK OWNERSHIP
    # ========================================================

    if booking.user_id != current_user["id"]:

        raise HTTPException(
            status_code=403,
            detail=(
                "You are not allowed to "
                "cancel this booking."
            )
        )


    # ========================================================
    # CHECK STATUS
    # ========================================================

    if booking.booking_status != "confirmed":

        raise HTTPException(
            status_code=400,
            detail=(
                "Booking cannot be cancelled because "
                f"its status is '{booking.booking_status}'."
            )
        )


    # ========================================================
    # FIND TRAIN
    # ========================================================

    train = db.query(
        Train
    ).filter(
        Train.id == booking.train_id
    ).first()


    if not train:

        raise HTTPException(
            status_code=404,
            detail="Associated train not found."
        )


    # ========================================================
    # RESTORE TRAIN SEATS
    # ========================================================

    train.available_seats += booking.seats


    # ========================================================
    # CHECK PAYMENT METHOD
    # ========================================================

    payment_method = (
        booking.payment_method or "demo"
    ).strip().lower()


    # ========================================================
    # WALLET REFUND
    # ========================================================

    if payment_method == "wallet":

        wallet = db.query(
            Wallet
        ).filter(
            Wallet.user_id == current_user["id"]
        ).first()


        # ----------------------------------------------------
        # CREATE WALLET IF NEEDED
        # ----------------------------------------------------

        if not wallet:

            wallet = Wallet(
                user_id=current_user["id"],
                balance=0.0
            )

            db.add(wallet)
            db.flush()


        # ----------------------------------------------------
        # CREDIT REFUND
        # ----------------------------------------------------

        wallet.balance += booking.total_price


        # ----------------------------------------------------
        # REFUND TRANSACTION
        # ----------------------------------------------------

        refund_transaction = WalletTransaction(

            user_id=current_user["id"],

            transaction_type="credit",

            amount=booking.total_price,

            description=(
                f"Train booking refund - "
                f"Booking #{booking.id} - "
                f"{train.train_name}"
            ),

            balance_after=wallet.balance
        )

        db.add(refund_transaction)


    # ========================================================
    # MARK BOOKING CANCELLED
    # ========================================================

    booking.booking_status = "cancelled"


    # ========================================================
    # SAVE
    # ========================================================

    db.commit()
    db.refresh(booking)

    return booking


# ============================================================
# ============================================================
# TRAIN ADMIN CRUD
# ============================================================
# ============================================================


# ============================================================
# ADMIN GET ALL TRAINS
# ============================================================

@train_router.get(
    "/admin/all",
    response_model=list[TrainResponse]
)
def admin_get_all_trains(
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    return db.query(
        Train
    ).order_by(
        Train.id.desc()
    ).all()


# ============================================================
# ADMIN CREATE TRAIN
# ============================================================

@train_router.post(
    "/admin/create",
    response_model=TrainResponse
)
def admin_create_train(
    train_data: TrainCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    # --------------------------------------------------------
    # CHECK DUPLICATE TRAIN NUMBER
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # CREATE TRAIN
    # --------------------------------------------------------

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
# ADMIN GET SINGLE TRAIN
# ============================================================

@train_router.get(
    "/admin/{train_id}",
    response_model=TrainResponse
)
def admin_get_train(
    train_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
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


# ============================================================
# ADMIN UPDATE TRAIN
# ============================================================

@train_router.put(
    "/admin/{train_id}",
    response_model=TrainResponse
)
def admin_update_train(
    train_id: int,
    train_data: TrainCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    # --------------------------------------------------------
    # FIND TRAIN
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # CHECK DUPLICATE TRAIN NUMBER
    # --------------------------------------------------------

    existing_train = db.query(
        Train
    ).filter(
        Train.train_number == train_data.train_number,
        Train.id != train_id
    ).first()


    if existing_train:

        raise HTTPException(
            status_code=400,
            detail="Another train already uses this train number."
        )


    # --------------------------------------------------------
    # UPDATE TRAIN
    # --------------------------------------------------------

    train.train_name = train_data.train_name
    train.train_number = train_data.train_number
    train.source = train_data.source
    train.destination = train_data.destination
    train.departure_time = train_data.departure_time
    train.arrival_time = train_data.arrival_time
    train.sleeper_price = train_data.sleeper_price
    train.third_ac_price = train_data.third_ac_price
    train.second_ac_price = train_data.second_ac_price
    train.first_ac_price = train_data.first_ac_price
    train.available_seats = train_data.available_seats


    db.commit()
    db.refresh(train)

    return train


# ============================================================
# ADMIN DELETE TRAIN
# ============================================================

@train_router.delete(
    "/admin/{train_id}"
)
def admin_delete_train(
    train_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    # --------------------------------------------------------
    # FIND TRAIN
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # CHECK EXISTING BOOKINGS
    # --------------------------------------------------------

    existing_bookings = db.query(
        TrainBooking
    ).filter(
        TrainBooking.train_id == train_id
    ).first()


    if existing_bookings:

        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot delete this train because "
                "bookings are associated with it."
            )
        )


    # --------------------------------------------------------
    # DELETE TRAIN
    # --------------------------------------------------------

    db.delete(train)
    db.commit()


    return {
        "message": "Train deleted successfully.",
        "train_id": train_id
    }


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
