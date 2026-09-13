from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import (
    Cab,
    CabBooking,
    Wallet,
    WalletTransaction
)

from cabs.schemas import (
    CabCreate,
    CabResponse,
    CabSearch,
    CabBookingCreate,
    CabBookingResponse
)

from auth.security import (
    get_current_user,
    require_admin
)


# ============================================================
# CAB ROUTER
# ============================================================

cab_router = APIRouter(
    prefix="/cabs",
    tags=["Cabs"]
)


# ============================================================
# GET ALL CABS
# ============================================================

@cab_router.get(
    "/",
    response_model=list[CabResponse]
)
def get_all_cabs(
    db: Session = Depends(get_db)
):
    return db.query(Cab).order_by(Cab.id).all()


# ============================================================
# CREATE CAB
# ============================================================

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
            detail="Vehicle number already exists"
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


# ============================================================
# SEARCH CABS
# ============================================================

@cab_router.post(
    "/search",
    response_model=list[CabResponse]
)
def search_cabs(
    search_data: CabSearch,
    db: Session = Depends(get_db)
):

    cabs = db.query(Cab).filter(
        Cab.source.ilike(search_data.source.strip()),
        Cab.destination.ilike(search_data.destination.strip())
    ).order_by(
        Cab.id
    ).all()

    return cabs


# ============================================================
# CREATE CAB BOOKING
# ============================================================

@cab_router.post(
    "/book",
    response_model=CabBookingResponse
)
def create_cab_booking(
    booking_data: CabBookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    cab = db.query(Cab).filter(
        Cab.id == booking_data.cab_id
    ).first()

    if not cab:
        raise HTTPException(
            status_code=404,
            detail="Cab not found"
        )

    if booking_data.distance_km <= 0:
        raise HTTPException(
            status_code=400,
            detail="Distance must be greater than 0 km"
        )

    if cab.available_seats <= 0:
        raise HTTPException(
            status_code=400,
            detail="No seats available"
        )

    total_price = (
        cab.fare_per_km * booking_data.distance_km
    )

    payment_method = (
        booking_data.payment_method
        .strip()
        .lower()
    )

    if payment_method not in ["wallet", "demo"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment method. Use 'wallet' or 'demo'."
        )

    # ========================================================
    # WALLET PAYMENT
    # ========================================================

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
                f"Cab booking - "
                f"{cab.cab_type} "
                f"({cab.source} to {cab.destination})"
            ),
            balance_after=wallet.balance
        )

        db.add(transaction)

    # ========================================================
    # CREATE CAB BOOKING
    # ========================================================

    booking = CabBooking(
        user_id=current_user["id"],
        cab_id=booking_data.cab_id,
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

    cab.available_seats -= 1

    db.add(booking)

    db.commit()
    db.refresh(booking)

    return booking


# ============================================================
# GET MY CAB BOOKINGS
# ============================================================

@cab_router.get(
    "/my-bookings",
    response_model=list[CabBookingResponse]
)
def get_my_cab_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    bookings = db.query(
        CabBooking
    ).filter(
        CabBooking.user_id == current_user["id"]
    ).order_by(
        CabBooking.id.desc()
    ).all()

    return bookings


# ============================================================
# CANCEL CAB BOOKING + WALLET REFUND
# ============================================================

@cab_router.post(
    "/bookings/{booking_id}/cancel",
    response_model=CabBookingResponse
)
def cancel_cab_booking(
    booking_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    booking = db.query(
        CabBooking
    ).filter(
        CabBooking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Cab booking not found"
        )

    if booking.user_id != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to cancel this booking"
        )

    if booking.booking_status != "confirmed":
        raise HTTPException(
            status_code=400,
            detail=(
                "Booking cannot be cancelled because "
                f"its status is '{booking.booking_status}'"
            )
        )

    cab = db.query(Cab).filter(
        Cab.id == booking.cab_id
    ).first()

    if not cab:
        raise HTTPException(
            status_code=404,
            detail="Associated cab not found"
        )

    # ========================================================
    # RESTORE CAB AVAILABILITY
    # ========================================================

    cab.available_seats += 1

    payment_method = (
        booking.payment_method or "demo"
    ).strip().lower()

    # ========================================================
    # WALLET REFUND
    # ========================================================

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

        wallet.balance += booking.total_price

        refund_transaction = WalletTransaction(
            user_id=current_user["id"],
            transaction_type="credit",
            amount=booking.total_price,
            description=(
                f"Cab booking refund - "
                f"Booking #{booking.id} - "
                f"{cab.cab_type}"
            ),
            balance_after=wallet.balance
        )

        db.add(refund_transaction)

    # ========================================================
    # MARK BOOKING AS CANCELLED
    # ========================================================

    booking.booking_status = "cancelled"

    db.commit()
    db.refresh(booking)

    return booking


# ============================================================
# ADMIN - GET ALL CABS
# ============================================================

@cab_router.get(
    "/admin/all",
    response_model=list[CabResponse]
)
def admin_get_all_cabs(
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    return db.query(Cab).order_by(
        Cab.id
    ).all()


# ============================================================
# ADMIN - CREATE CAB
# ============================================================

@cab_router.post(
    "/admin/create",
    response_model=CabResponse
)
def admin_create_cab(
    cab_data: CabCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    existing_cab = db.query(Cab).filter(
        Cab.vehicle_number == cab_data.vehicle_number
    ).first()

    if existing_cab:
        raise HTTPException(
            status_code=400,
            detail="Vehicle number already exists"
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


# ============================================================
# ADMIN - GET SINGLE CAB
# ============================================================

@cab_router.get(
    "/admin/{cab_id}",
    response_model=CabResponse
)
def admin_get_cab(
    cab_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    cab = db.query(Cab).filter(
        Cab.id == cab_id
    ).first()

    if not cab:
        raise HTTPException(
            status_code=404,
            detail="Cab not found"
        )

    return cab


# ============================================================
# ADMIN - UPDATE CAB
# ============================================================

@cab_router.put(
    "/admin/{cab_id}",
    response_model=CabResponse
)
def admin_update_cab(
    cab_id: int,
    cab_data: CabCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    cab = db.query(Cab).filter(
        Cab.id == cab_id
    ).first()

    if not cab:
        raise HTTPException(
            status_code=404,
            detail="Cab not found"
        )

    # ========================================================
    # DUPLICATE VEHICLE NUMBER CHECK
    # ========================================================

    existing_cab = db.query(Cab).filter(
        Cab.vehicle_number == cab_data.vehicle_number,
        Cab.id != cab_id
    ).first()

    if existing_cab:
        raise HTTPException(
            status_code=400,
            detail="Vehicle number already exists"
        )

    # ========================================================
    # UPDATE CAB
    # ========================================================

    cab.driver_name = cab_data.driver_name
    cab.vehicle_number = cab_data.vehicle_number
    cab.cab_type = cab_data.cab_type
    cab.source = cab_data.source
    cab.destination = cab_data.destination
    cab.fare_per_km = cab_data.fare_per_km
    cab.available_seats = cab_data.available_seats
    cab.rating = cab_data.rating

    db.commit()
    db.refresh(cab)

    return cab


# ============================================================
# ADMIN - DELETE CAB
# ============================================================

@cab_router.delete(
    "/admin/{cab_id}"
)
def admin_delete_cab(
    cab_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    cab = db.query(Cab).filter(
        Cab.id == cab_id
    ).first()

    if not cab:
        raise HTTPException(
            status_code=404,
            detail="Cab not found"
        )

    # ========================================================
    # PREVENT DELETE IF BOOKINGS EXIST
    # ========================================================

    existing_booking = db.query(CabBooking).filter(
        CabBooking.cab_id == cab_id
    ).first()

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail=(
                "Cab cannot be deleted because "
                "bookings exist for this cab."
            )
        )

    db.delete(cab)
    db.commit()

    return {
        "message": "Cab deleted successfully.",
        "cab_id": cab_id
    }


# ============================================================
# GET SINGLE CAB
# ============================================================

@cab_router.get(
    "/{cab_id}",
    response_model=CabResponse
)
def get_cab(
    cab_id: int,
    db: Session = Depends(get_db)
):

    cab = db.query(Cab).filter(
        Cab.id == cab_id
    ).first()

    if not cab:
        raise HTTPException(
            status_code=404,
            detail="Cab not found"
        )

    return cab
