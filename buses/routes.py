from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

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

from auth.security import (
    get_current_user,
    require_admin
)

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

    return db.query(
        Bus
    ).order_by(
        Bus.id
    ).all()


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

    existing_bus = db.query(
        Bus
    ).filter(
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

    buses = db.query(
        Bus
    ).filter(
        Bus.source.ilike(
            search_data.source.strip()
        ),
        Bus.destination.ilike(
            search_data.destination.strip()
        )
    ).order_by(
        Bus.id
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

    bus = db.query(
        Bus
    ).filter(
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
        bus.price *
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
        # CHECK WALLET BALANCE
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
        # CREATE DEBIT TRANSACTION
        # ----------------------------------------------------

        transaction = WalletTransaction(
            user_id=current_user["id"],
            transaction_type="debit",
            amount=total_price,
            description=(
                f"Bus booking - "
                f"{bus.operator} "
                f"({bus.source} to "
                f"{bus.destination})"
            ),
            balance_after=wallet.balance
        )

        db.add(transaction)

    # ========================================================
    # REDUCE BUS SEATS
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
        payment_method=payment_method,
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
# CANCEL BUS BOOKING + WALLET REFUND
# ============================================================

@bus_router.post(
    "/bookings/{booking_id}/cancel",
    response_model=BusBookingResponse
)
def cancel_bus_booking(
    booking_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # ========================================================
    # FIND BOOKING
    # ========================================================

    booking = db.query(
        BusBooking
    ).filter(
        BusBooking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Bus booking not found"
        )

    # ========================================================
    # CHECK OWNERSHIP
    # ========================================================

    if booking.user_id != current_user["id"]:

        raise HTTPException(
            status_code=403,
            detail=(
                "You are not allowed "
                "to cancel this booking"
            )
        )

    # ========================================================
    # CHECK BOOKING STATUS
    # ========================================================

    if booking.booking_status != "confirmed":

        raise HTTPException(
            status_code=400,
            detail=(
                "Booking cannot be cancelled "
                f"because its status is "
                f"'{booking.booking_status}'"
            )
        )

    # ========================================================
    # FIND BUS
    # ========================================================

    bus = db.query(
        Bus
    ).filter(
        Bus.id == booking.bus_id
    ).first()

    if not bus:

        raise HTTPException(
            status_code=404,
            detail="Associated bus not found"
        )

    # ========================================================
    # RESTORE BUS SEATS
    # ========================================================

    bus.available_seats += booking.seats

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
                f"Bus booking refund - "
                f"Booking #{booking.id} - "
                f"{bus.operator}"
            ),
            balance_after=wallet.balance
        )

        db.add(refund_transaction)

    # ========================================================
    # MARK BOOKING AS CANCELLED
    # ========================================================

    booking.booking_status = "cancelled"

    # ========================================================
    # SAVE CHANGES
    # ========================================================

    db.commit()
    db.refresh(booking)

    return booking


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

    bus = db.query(
        Bus
    ).filter(
        Bus.id == bus_id
    ).first()

    if not bus:

        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    return bus


# ============================================================
# 👑 ADMIN BUS MANAGEMENT
# ============================================================
#
# These endpoints are intentionally separate from the normal
# customer bus APIs.
#
# Customer:
#   /buses/
#   /buses/search
#   /buses/book
#
# Admin:
#   /buses/admin/all
#   /buses/admin/create
#   /buses/admin/{bus_id}
#
# ============================================================


# ============================================================
# ADMIN - GET ALL BUSES
# ============================================================

@bus_router.get(
    "/admin/all",
    response_model=list[BusResponse]
)
def admin_get_all_buses(
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):

    return db.query(
        Bus
    ).order_by(
        Bus.id.desc()
    ).all()


# ============================================================
# ADMIN - CREATE BUS
# ============================================================

@bus_router.post(
    "/admin/create",
    response_model=BusResponse
)
def admin_create_bus(
    bus_data: BusCreate,
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # CHECK DUPLICATE BUS NUMBER
    # --------------------------------------------------------

    existing_bus = db.query(
        Bus
    ).filter(
        Bus.bus_number == bus_data.bus_number
    ).first()

    if existing_bus:

        raise HTTPException(
            status_code=400,
            detail="Bus number already exists"
        )

    # --------------------------------------------------------
    # CREATE BUS
    # --------------------------------------------------------

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
# ADMIN - GET SINGLE BUS
# ============================================================

@bus_router.get(
    "/admin/{bus_id}",
    response_model=BusResponse
)
def admin_get_bus(
    bus_id: int,
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):

    bus = db.query(
        Bus
    ).filter(
        Bus.id == bus_id
    ).first()

    if not bus:

        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    return bus


# ============================================================
# ADMIN - UPDATE BUS
# ============================================================

@bus_router.put(
    "/admin/{bus_id}",
    response_model=BusResponse
)
def admin_update_bus(
    bus_id: int,
    bus_data: BusCreate,
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # FIND BUS
    # --------------------------------------------------------

    bus = db.query(
        Bus
    ).filter(
        Bus.id == bus_id
    ).first()

    if not bus:

        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    # --------------------------------------------------------
    # CHECK DUPLICATE BUS NUMBER
    # --------------------------------------------------------

    duplicate_bus = db.query(
        Bus
    ).filter(
        Bus.bus_number == bus_data.bus_number,
        Bus.id != bus_id
    ).first()

    if duplicate_bus:

        raise HTTPException(
            status_code=400,
            detail="Another bus already uses this bus number"
        )

    # --------------------------------------------------------
    # UPDATE BUS
    # --------------------------------------------------------

    bus.operator = bus_data.operator
    bus.bus_number = bus_data.bus_number
    bus.source = bus_data.source
    bus.destination = bus_data.destination
    bus.departure_time = bus_data.departure_time
    bus.arrival_time = bus_data.arrival_time
    bus.price = bus_data.price
    bus.available_seats = bus_data.available_seats

    db.commit()
    db.refresh(bus)

    return bus


# ============================================================
# ADMIN - DELETE BUS
# ============================================================

@bus_router.delete(
    "/admin/{bus_id}"
)
def admin_delete_bus(
    bus_id: int,
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # FIND BUS
    # --------------------------------------------------------

    bus = db.query(
        Bus
    ).filter(
        Bus.id == bus_id
    ).first()

    if not bus:

        raise HTTPException(
            status_code=404,
            detail="Bus not found"
        )

    # --------------------------------------------------------
    # CHECK EXISTING BOOKINGS
    # --------------------------------------------------------

    booking_count = db.query(
        BusBooking
    ).filter(
        BusBooking.bus_id == bus_id
    ).count()

    if booking_count > 0:

        raise HTTPException(
            status_code=400,
            detail=(
                "This bus cannot be deleted because "
                f"{booking_count} booking(s) are associated "
                "with it. Cancel or resolve the bookings first."
            )
        )

    # --------------------------------------------------------
    # DELETE BUS
    # --------------------------------------------------------

    db.delete(bus)
    db.commit()

    return {
        "message": "Bus deleted successfully",
        "bus_id": bus_id
    }