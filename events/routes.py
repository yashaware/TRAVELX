from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db

from db.models import (
    Event,
    EventVenue,
    EventShow,
    EventBooking,
    Wallet,
    WalletTransaction
)

from events.schemas import (
    EventCreate,
    EventResponse,
    EventSearch,
    EventVenueCreate,
    EventVenueResponse,
    EventVenueSearch,
    EventShowCreate,
    EventShowResponse,
    EventBookingCreate,
    EventBookingResponse
)

from auth.security import get_current_user


event_router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


# =========================================================
# EVENTS
# =========================================================

@event_router.get(
    "/",
    response_model=list[EventResponse]
)
def get_all_events(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Event).order_by(
        Event.rating.desc()
    ).all()


@event_router.post(
    "/",
    response_model=EventResponse
)
def create_event(
    event_data: EventCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    event = Event(
        name=event_data.name,
        category=event_data.category,
        description=event_data.description,
        language=event_data.language,
        duration_minutes=event_data.duration_minutes,
        rating=event_data.rating,
        image_url=event_data.image_url
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@event_router.post(
    "/search",
    response_model=list[EventResponse]
)
def search_events(
    search_data: EventSearch,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    query = db.query(Event)

    if search_data.category:
        query = query.filter(
            Event.category.ilike(
                search_data.category.strip()
            )
        )

    if search_data.language:
        query = query.filter(
            Event.language.ilike(
                search_data.language.strip()
            )
        )

    return query.order_by(
        Event.rating.desc()
    ).all()


# =========================================================
# VENUES
# =========================================================

@event_router.get(
    "/venues/all",
    response_model=list[EventVenueResponse]
)
def get_all_event_venues(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(EventVenue).order_by(
        EventVenue.city,
        EventVenue.name
    ).all()


@event_router.post(
    "/venues",
    response_model=EventVenueResponse
)
def create_event_venue(
    venue_data: EventVenueCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    venue = EventVenue(
        name=venue_data.name,
        city=venue_data.city,
        address=venue_data.address,
        capacity=venue_data.capacity
    )

    db.add(venue)
    db.commit()
    db.refresh(venue)

    return venue


@event_router.post(
    "/venues/search",
    response_model=list[EventVenueResponse]
)
def search_event_venues(
    search_data: EventVenueSearch,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(EventVenue).filter(
        EventVenue.city.ilike(
            search_data.city.strip()
        )
    ).order_by(
        EventVenue.name
    ).all()


# =========================================================
# EVENT SHOWS
# =========================================================

@event_router.post(
    "/shows",
    response_model=EventShowResponse
)
def create_event_show(
    show_data: EventShowCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == show_data.event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found."
        )

    venue = db.query(EventVenue).filter(
        EventVenue.id == show_data.venue_id
    ).first()

    if not venue:
        raise HTTPException(
            status_code=404,
            detail="Event venue not found."
        )

    if show_data.available_tickets > show_data.total_tickets:
        raise HTTPException(
            status_code=400,
            detail="Available tickets cannot exceed total tickets."
        )

    show = EventShow(
        event_id=show_data.event_id,
        venue_id=show_data.venue_id,
        show_date=show_data.show_date,
        show_time=show_data.show_time,
        ticket_type=show_data.ticket_type,
        ticket_price=show_data.ticket_price,
        total_tickets=show_data.total_tickets,
        available_tickets=show_data.available_tickets
    )

    db.add(show)
    db.commit()
    db.refresh(show)

    return show


@event_router.get(
    "/shows/event/{event_id}",
    response_model=list[EventShowResponse]
)
def get_event_shows(
    event_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found."
        )

    return db.query(EventShow).filter(
        EventShow.event_id == event_id,
        EventShow.available_tickets > 0
    ).order_by(
        EventShow.show_date,
        EventShow.show_time
    ).all()


@event_router.get(
    "/shows/venue/{venue_id}",
    response_model=list[EventShowResponse]
)
def get_venue_shows(
    venue_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    venue = db.query(EventVenue).filter(
        EventVenue.id == venue_id
    ).first()

    if not venue:
        raise HTTPException(
            status_code=404,
            detail="Event venue not found."
        )

    return db.query(EventShow).filter(
        EventShow.venue_id == venue_id,
        EventShow.available_tickets > 0
    ).order_by(
        EventShow.show_date,
        EventShow.show_time
    ).all()


@event_router.get(
    "/shows/{show_id}",
    response_model=EventShowResponse
)
def get_event_show(
    show_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    show = db.query(EventShow).filter(
        EventShow.id == show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Event show not found."
        )

    return show


# =========================================================
# EVENT BOOKING
# =========================================================

@event_router.post(
    "/book",
    response_model=EventBookingResponse
)
def create_event_booking(
    booking_data: EventBookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Validate event
    # -----------------------------------------------------

    event = db.query(Event).filter(
        Event.id == booking_data.event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found."
        )

    # -----------------------------------------------------
    # Validate venue
    # -----------------------------------------------------

    venue = db.query(EventVenue).filter(
        EventVenue.id == booking_data.venue_id
    ).first()

    if not venue:
        raise HTTPException(
            status_code=404,
            detail="Event venue not found."
        )

    # -----------------------------------------------------
    # Validate show
    # -----------------------------------------------------

    show = db.query(EventShow).filter(
        EventShow.id == booking_data.show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Event show not found."
        )

    # -----------------------------------------------------
    # Verify event + venue + show
    # -----------------------------------------------------

    if show.event_id != booking_data.event_id:
        raise HTTPException(
            status_code=400,
            detail="Show does not belong to the selected event."
        )

    if show.venue_id != booking_data.venue_id:
        raise HTTPException(
            status_code=400,
            detail="Show does not belong to the selected venue."
        )

    # -----------------------------------------------------
    # Validate tickets
    # -----------------------------------------------------

    if booking_data.number_of_tickets <= 0:
        raise HTTPException(
            status_code=400,
            detail="Number of tickets must be greater than zero."
        )

    if booking_data.number_of_tickets > show.available_tickets:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Not enough tickets available. "
                f"Available: {show.available_tickets}"
            )
        )

    # -----------------------------------------------------
    # Calculate price
    # -----------------------------------------------------

    total_price = (
        show.ticket_price *
        booking_data.number_of_tickets
    )

    # -----------------------------------------------------
    # Payment method
    # -----------------------------------------------------

    payment_method = (
        booking_data.payment_method
        .strip()
        .lower()
    )

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
                f"Event booking - "
                f"{event.name} "
                f"at {venue.name}"
            ),
            balance_after=wallet.balance
        )

        db.add(transaction)

    elif payment_method == "demo":

        pass

    else:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid payment method. "
                "Use wallet or demo."
            )
        )

    # -----------------------------------------------------
    # Reduce available tickets
    # -----------------------------------------------------

    show.available_tickets -= (
        booking_data.number_of_tickets
    )

    # -----------------------------------------------------
    # Create booking
    # -----------------------------------------------------

    booking = EventBooking(

        user_id=current_user["id"],

        event_id=event.id,

        venue_id=venue.id,

        show_id=show.id,

        customer_name=booking_data.customer_name,

        customer_phone=booking_data.customer_phone,

        show_date=show.show_date,

        show_time=show.show_time,

        ticket_type=show.ticket_type,

        number_of_tickets=(
            booking_data.number_of_tickets
        ),

        total_price=total_price,

        payment_method=payment_method,

        booking_status="confirmed"
    )

    db.add(booking)

    db.commit()

    db.refresh(booking)

    return booking


# =========================================================
# MY EVENT BOOKINGS
# =========================================================

@event_router.get(
    "/my-bookings",
    response_model=list[EventBookingResponse]
)
def get_my_event_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(EventBooking).filter(
        EventBooking.user_id == current_user["id"]
    ).order_by(
        EventBooking.id.desc()
    ).all()


# =========================================================
# SINGLE EVENT BOOKING
# =========================================================

@event_router.get(
    "/bookings/{booking_id}",
    response_model=EventBookingResponse
)
def get_event_booking(
    booking_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    booking = db.query(EventBooking).filter(
        EventBooking.id == booking_id,
        EventBooking.user_id == current_user["id"]
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Event booking not found."
        )

    return booking


# =========================================================
# SINGLE EVENT
# IMPORTANT:
# KEEP THIS AT THE VERY BOTTOM
# =========================================================

@event_router.get(
    "/{event_id}",
    response_model=EventResponse
)
def get_event(
    event_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found."
        )

    return event
