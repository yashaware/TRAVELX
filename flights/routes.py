from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Flight, FlightBooking, Wallet, WalletTransaction
from flights.schemas import (
    FlightCreate,
    FlightResponse,
    FlightSearch,
    FlightBookingCreate,
    FlightBookingResponse
)
from auth.security import get_current_user


flight_router = APIRouter(
    prefix="/flights",
    tags=["Flights"]
)


# =========================================================
# GET ALL FLIGHTS
# =========================================================

@flight_router.get("/", response_model=list[FlightResponse])
def get_all_flights(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Flight).order_by(Flight.id).all()


# =========================================================
# CREATE FLIGHT
# =========================================================

@flight_router.post("/", response_model=FlightResponse)
def create_flight(
    flight_data: FlightCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_flight = db.query(Flight).filter(
        Flight.flight_number == flight_data.flight_number
    ).first()

    if existing_flight:
        raise HTTPException(
            status_code=400,
            detail="Flight number already exists."
        )

    flight = Flight(
        airline=flight_data.airline,
        flight_number=flight_data.flight_number,
        source=flight_data.source,
        destination=flight_data.destination,
        departure_time=flight_data.departure_time,
        arrival_time=flight_data.arrival_time,
        economy_price=flight_data.economy_price,
        premium_economy_price=flight_data.premium_economy_price,
        business_price=flight_data.business_price,
        available_seats=flight_data.available_seats
    )

    db.add(flight)
    db.commit()
    db.refresh(flight)

    return flight


# =========================================================
# SEARCH FLIGHTS
# =========================================================

@flight_router.post("/search", response_model=list[FlightResponse])
def search_flights(
    search_data: FlightSearch,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    source = search_data.source.strip()
    destination = search_data.destination.strip()

    flights = db.query(Flight).filter(
        Flight.source.ilike(source),
        Flight.destination.ilike(destination)
    ).order_by(Flight.id).all()

    return flights


# =========================================================
# BOOK FLIGHT
# =========================================================

@flight_router.post(
    "/book",
    response_model=FlightBookingResponse
)
def create_flight_booking(
    booking_data: FlightBookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    flight = db.query(Flight).filter(
        Flight.id == booking_data.flight_id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found."
        )

    if booking_data.seats > flight.available_seats:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough seats available. Available: {flight.available_seats}"
        )

    travel_class = booking_data.travel_class.strip().lower()

    prices = {
        "economy": flight.economy_price,
        "premium economy": flight.premium_economy_price,
        "premium_economy": flight.premium_economy_price,
        "business": flight.business_price
    }

    if travel_class not in prices:
        raise HTTPException(
            status_code=400,
            detail="Invalid class. Use Economy, Premium Economy or Business."
        )

    total_price = prices[travel_class] * booking_data.seats

    payment_method = booking_data.payment_method.strip().lower()

    # =====================================================
    # WALLET PAYMENT
    # =====================================================

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

        wallet.balance -= total_price

        transaction = WalletTransaction(
            user_id=current_user["id"],
            transaction_type="debit",
            amount=total_price,
            description=(
                f"Flight booking - "
                f"{flight.airline} {flight.flight_number} "
                f"({flight.source} to {flight.destination})"
            ),
            balance_after=wallet.balance
        )

        db.add(transaction)

    # =====================================================
    # REDUCE AVAILABLE SEATS
    # =====================================================

    flight.available_seats -= booking_data.seats

    # =====================================================
    # CREATE BOOKING
    # =====================================================

    booking = FlightBooking(
        user_id=current_user["id"],
        flight_id=flight.id,
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


# =========================================================
# MY FLIGHT BOOKINGS
# =========================================================

@flight_router.get(
    "/my-bookings",
    response_model=list[FlightBookingResponse]
)
def get_my_flight_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    bookings = db.query(FlightBooking).filter(
        FlightBooking.user_id == current_user["id"]
    ).order_by(
        FlightBooking.id.desc()
    ).all()

    return bookings


# =========================================================
# GET SINGLE FLIGHT
# =========================================================

@flight_router.get(
    "/{flight_id}",
    response_model=FlightResponse
)
def get_flight(
    flight_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    flight = db.query(Flight).filter(
        Flight.id == flight_id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found."
        )

    return flight