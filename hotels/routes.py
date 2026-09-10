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

from auth.security import get_current_user


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

    hotels = db.query(
        Hotel
    ).order_by(
        Hotel.id
    ).all()

    return hotels


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

    city = search_data.city.strip()

    hotels = db.query(
        Hotel
    ).filter(
        Hotel.city.ilike(city)
    ).order_by(
        Hotel.rating.desc()
    ).all()

    return hotels


# ============================================================
# BOOK HOTEL
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

    # --------------------------------------------------------
    # FIND HOTEL
    # --------------------------------------------------------

    hotel = db.query(
        Hotel
    ).filter(
        Hotel.id == booking_data.hotel_id
    ).first()

    if not hotel:

        raise HTTPException(
            status_code=404,
            detail="Hotel not found."
        )


    # --------------------------------------------------------
    # CHECK ROOM AVAILABILITY
    # --------------------------------------------------------

    if booking_data.rooms > hotel.available_rooms:

        raise HTTPException(
            status_code=400,
            detail=(
                "Not enough rooms available. "
                f"Available: {hotel.available_rooms}"
            )
        )


    # --------------------------------------------------------
    # CALCULATE TOTAL PRICE
    # --------------------------------------------------------

    total_price = (
        hotel.price_per_night
        * booking_data.rooms
        * booking_data.nights
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


        # Create wallet if it doesn't exist
        if not wallet:

            wallet = Wallet(
                user_id=current_user["id"],
                balance=0.0
            )

            db.add(wallet)

            db.flush()


        # Check wallet balance
        if wallet.balance < total_price:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Insufficient wallet balance. "
                    f"Available: ₹{wallet.balance:.2f}, "
                    f"Required: ₹{total_price:.2f}"
                )
            )


        # Deduct amount
        wallet.balance -= total_price


        # Create transaction
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


    # --------------------------------------------------------
    # REDUCE AVAILABLE ROOMS
    # --------------------------------------------------------

    hotel.available_rooms -= booking_data.rooms


    # --------------------------------------------------------
    # CREATE HOTEL BOOKING
    # --------------------------------------------------------

    booking = HotelBooking(
        user_id=current_user["id"],
        hotel_id=hotel.id,
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
# MY HOTEL BOOKINGS
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
            detail="Hotel not found."
        )

    return hotel