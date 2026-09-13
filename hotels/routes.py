from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import (
    Hotel,
    HotelBooking,
    Wallet,
    WalletTransaction
)

from hotels.schemas import (
    HotelCreate,
    HotelResponse,
    HotelSearch,
    HotelBookingCreate,
    HotelBookingResponse
)

from auth.security import (
    get_current_user,
    require_admin
)


# ============================================================
# HOTEL ROUTER
# ============================================================

hotel_router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


# ============================================================
# GET ALL HOTELS
# ============================================================

@hotel_router.get(
    "/",
    response_model=list[HotelResponse]
)
def get_all_hotels(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Hotel).order_by(
        Hotel.id
    ).all()


# ============================================================
# CREATE HOTEL
# ============================================================

@hotel_router.post(
    "/",
    response_model=HotelResponse
)
def create_hotel(
    hotel_data: HotelCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    hotel = Hotel(
        name=hotel_data.name,
        city=hotel_data.city,
        address=hotel_data.address,
        description=hotel_data.description,
        rating=hotel_data.rating,
        price_per_night=hotel_data.price_per_night,
        available_rooms=hotel_data.available_rooms,
        amenities=hotel_data.amenities
    )

    db.add(hotel)
    db.commit()
    db.refresh(hotel)

    return hotel


# ============================================================
# SEARCH HOTELS
# ============================================================

@hotel_router.post(
    "/search",
    response_model=list[HotelResponse]
)
def search_hotels(
    search_data: HotelSearch,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    hotels = db.query(Hotel).filter(
        Hotel.city.ilike(
            search_data.city.strip()
        )
    ).order_by(
        Hotel.rating.desc()
    ).all()

    return hotels


# ============================================================
# CREATE HOTEL BOOKING
# ============================================================

@hotel_router.post(
    "/book",
    response_model=HotelBookingResponse
)
def create_hotel_booking(
    booking_data: HotelBookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # ========================================================
    # FIND HOTEL
    # ========================================================

    hotel = db.query(Hotel).filter(
        Hotel.id == booking_data.hotel_id
    ).first()

    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Hotel not found"
        )


    # ========================================================
    # VALIDATE ROOMS
    # ========================================================

    if booking_data.rooms <= 0:
        raise HTTPException(
            status_code=400,
            detail="Number of rooms must be greater than 0"
        )

    if booking_data.rooms > hotel.available_rooms:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Only {hotel.available_rooms} "
                f"rooms are available"
            )
        )


    # ========================================================
    # VALIDATE NIGHTS
    # ========================================================

    if booking_data.nights <= 0:
        raise HTTPException(
            status_code=400,
            detail="Number of nights must be greater than 0"
        )


    # ========================================================
    # CALCULATE TOTAL
    # ========================================================

    total_price = (
        hotel.price_per_night
        * booking_data.rooms
        * booking_data.nights
    )


    # ========================================================
    # PAYMENT METHOD
    # ========================================================

    payment_method = (
        booking_data.payment_method
        .strip()
        .lower()
    )

    if payment_method not in ["wallet", "demo"]:
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

        wallet = db.query(Wallet).filter(
            Wallet.user_id == current_user["id"]
        ).first()


        # ----------------------------------------------------
        # CREATE WALLET IF NOT EXISTS
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
        # DEDUCT MONEY
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
                f"Hotel booking - "
                f"{hotel.name} "
                f"({hotel.city})"
            ),
            balance_after=wallet.balance
        )

        db.add(transaction)


    # ========================================================
    # REDUCE AVAILABLE ROOMS
    # ========================================================

    hotel.available_rooms -= booking_data.rooms


    # ========================================================
    # CREATE HOTEL BOOKING
    # ========================================================

    booking = HotelBooking(
        user_id=current_user["id"],
        hotel_id=booking_data.hotel_id,
        guest_name=booking_data.guest_name,
        guest_phone=booking_data.guest_phone,
        rooms=booking_data.rooms,
        nights=booking_data.nights,
        total_price=total_price,
        payment_method=payment_method,
        booking_status="confirmed"
    )

    db.add(booking)

    db.commit()
    db.refresh(booking)

    return booking


# ============================================================
# GET MY HOTEL BOOKINGS
# ============================================================

@hotel_router.get(
    "/my-bookings",
    response_model=list[HotelBookingResponse]
)
def get_my_hotel_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    bookings = db.query(
        HotelBooking
    ).filter(
        HotelBooking.user_id == current_user["id"]
    ).order_by(
        HotelBooking.id.desc()
    ).all()

    return bookings


# ============================================================
# CANCEL HOTEL BOOKING + WALLET REFUND
# ============================================================

@hotel_router.post(
    "/bookings/{booking_id}/cancel",
    response_model=HotelBookingResponse
)
def cancel_hotel_booking(
    booking_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # ========================================================
    # FIND BOOKING
    # ========================================================

    booking = db.query(
        HotelBooking
    ).filter(
        HotelBooking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Hotel booking not found"
        )


    # ========================================================
    # CHECK OWNERSHIP
    # ========================================================

    if booking.user_id != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail=(
                "You are not allowed to "
                "cancel this booking"
            )
        )


    # ========================================================
    # CHECK BOOKING STATUS
    # ========================================================

    if booking.booking_status != "confirmed":
        raise HTTPException(
            status_code=400,
            detail=(
                "Booking cannot be cancelled because "
                f"its status is '{booking.booking_status}'"
            )
        )


    # ========================================================
    # FIND HOTEL
    # ========================================================

    hotel = db.query(
        Hotel
    ).filter(
        Hotel.id == booking.hotel_id
    ).first()

    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Associated hotel not found"
        )


    # ========================================================
    # RESTORE HOTEL ROOMS
    # ========================================================

    hotel.available_rooms += booking.rooms


    # ========================================================
    # WALLET REFUND
    # ========================================================

    payment_method = (
        booking.payment_method or "demo"
    ).strip().lower()


    if payment_method == "wallet":

        wallet = db.query(
            Wallet
        ).filter(
            Wallet.user_id == current_user["id"]
        ).first()


        # ----------------------------------------------------
        # CREATE WALLET IF NOT EXISTS
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
        # CREATE REFUND TRANSACTION
        # ----------------------------------------------------

        refund_transaction = WalletTransaction(
            user_id=current_user["id"],
            transaction_type="credit",
            amount=booking.total_price,
            description=(
                f"Hotel booking refund - "
                f"Booking #{booking.id} - "
                f"{hotel.name}"
            ),
            balance_after=wallet.balance
        )

        db.add(refund_transaction)


    # ========================================================
    # MARK BOOKING AS CANCELLED
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
# HOTEL ADMIN CRUD
# ============================================================
# ============================================================


# ============================================================
# ADMIN GET ALL HOTELS
# ============================================================

@hotel_router.get(
    "/admin/all",
    response_model=list[HotelResponse]
)
def admin_get_all_hotels(
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    return db.query(
        Hotel
    ).order_by(
        Hotel.id.desc()
    ).all()


# ============================================================
# ADMIN CREATE HOTEL
# ============================================================

@hotel_router.post(
    "/admin/create",
    response_model=HotelResponse
)
def admin_create_hotel(
    hotel_data: HotelCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    hotel = Hotel(
        name=hotel_data.name,
        city=hotel_data.city,
        address=hotel_data.address,
        description=hotel_data.description,
        rating=hotel_data.rating,
        price_per_night=hotel_data.price_per_night,
        available_rooms=hotel_data.available_rooms,
        amenities=hotel_data.amenities
    )

    db.add(hotel)
    db.commit()
    db.refresh(hotel)

    return hotel


# ============================================================
# ADMIN GET SINGLE HOTEL
# ============================================================

@hotel_router.get(
    "/admin/{hotel_id}",
    response_model=HotelResponse
)
def admin_get_hotel(
    hotel_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    hotel = db.query(
        Hotel
    ).filter(
        Hotel.id == hotel_id
    ).first()

    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Hotel not found"
        )

    return hotel


# ============================================================
# ADMIN UPDATE HOTEL
# ============================================================

@hotel_router.put(
    "/admin/{hotel_id}",
    response_model=HotelResponse
)
def admin_update_hotel(
    hotel_id: int,
    hotel_data: HotelCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    hotel = db.query(
        Hotel
    ).filter(
        Hotel.id == hotel_id
    ).first()

    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Hotel not found"
        )


    # --------------------------------------------------------
    # UPDATE HOTEL
    # --------------------------------------------------------

    hotel.name = hotel_data.name
    hotel.city = hotel_data.city
    hotel.address = hotel_data.address
    hotel.description = hotel_data.description
    hotel.rating = hotel_data.rating
    hotel.price_per_night = hotel_data.price_per_night
    hotel.available_rooms = hotel_data.available_rooms
    hotel.amenities = hotel_data.amenities


    db.commit()
    db.refresh(hotel)

    return hotel


# ============================================================
# ADMIN DELETE HOTEL
# ============================================================

@hotel_router.delete(
    "/admin/{hotel_id}"
)
def admin_delete_hotel(
    hotel_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):

    # --------------------------------------------------------
    # FIND HOTEL
    # --------------------------------------------------------

    hotel = db.query(
        Hotel
    ).filter(
        Hotel.id == hotel_id
    ).first()

    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Hotel not found"
        )


    # --------------------------------------------------------
    # CHECK EXISTING BOOKINGS
    # --------------------------------------------------------

    existing_booking = db.query(
        HotelBooking
    ).filter(
        HotelBooking.hotel_id == hotel_id
    ).first()


    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot delete this hotel because "
                "bookings are associated with it."
            )
        )


    # --------------------------------------------------------
    # DELETE HOTEL
    # --------------------------------------------------------

    db.delete(hotel)
    db.commit()


    return {
        "message": "Hotel deleted successfully.",
        "hotel_id": hotel_id
    }


# ============================================================
# GET SINGLE HOTEL
# ============================================================

@hotel_router.get(
    "/{hotel_id}",
    response_model=HotelResponse
)
def get_hotel(
    hotel_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    hotel = db.query(
        Hotel
    ).filter(
        Hotel.id == hotel_id
    ).first()

    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Hotel not found"
        )

    return hotel
