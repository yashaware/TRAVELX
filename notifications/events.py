"""Automatic TRAVELX notifications.

This module listens to SQLAlchemy session flushes so booking/payment/cancellation
notifications are generated centrally without changing every booking router.
"""

from sqlalchemy import event, inspect
from sqlalchemy.orm import Session

from db.models import (
    Booking,
    BusBooking,
    TrainBooking,
    HotelBooking,
    FlightBooking,
    CabBooking,
    FoodOrder,
    MovieBooking,
    EventBooking,
    WalletTransaction,
)
from notifications.models import Notification


# Session-local guard prevents the same notification from being created
# more than once during nested SQLAlchemy flush cycles.
PROCESSED_KEY = "_travelx_notification_processed"


BOOKING_TYPES = (
    Booking,
    BusBooking,
    TrainBooking,
    HotelBooking,
    FlightBooking,
    CabBooking,
    FoodOrder,
    MovieBooking,
    EventBooking,
)


SERVICE_NAMES = {
    Booking: "Booking",
    BusBooking: "Bus",
    TrainBooking: "Train",
    HotelBooking: "Hotel",
    FlightBooking: "Flight",
    CabBooking: "Cab",
    FoodOrder: "Food",
    MovieBooking: "Movies",
    EventBooking: "Events",
}


def _service_for(obj):
    for model, name in SERVICE_NAMES.items():
        if isinstance(obj, model):
            return name
    return "TRAVELX"


def _status_attr(obj):
    if isinstance(obj, FoodOrder):
        return "order_status"
    if isinstance(obj, Booking):
        return "status"
    return "booking_status"


def _booking_amount(obj):
    return getattr(obj, "total_price", getattr(obj, "amount", 0)) or 0


def _payment_method(obj):
    return (getattr(obj, "payment_method", "demo") or "demo").upper()


def _booking_message(obj, service):
    booking_id = getattr(obj, "id", "")
    amount = _booking_amount(obj)
    payment = _payment_method(obj)

    if isinstance(obj, FoodOrder):
        noun = f"Food order #{booking_id}"
    elif isinstance(obj, MovieBooking):
        noun = f"Movie ticket booking #{booking_id}"
    elif isinstance(obj, EventBooking):
        noun = f"Event booking #{booking_id}"
    else:
        noun = f"{service} booking #{booking_id}"

    return (
        f"{noun} has been confirmed successfully. "
        f"Amount: ₹{amount:,.2f}. Payment: {payment}."
    )


def _add_notification(
    session,
    *,
    user_id,
    notification_type,
    title,
    message,
    service=None,
    booking_id=None,
    amount=None,
):
    session.add(
        Notification(
            user_id=int(user_id),
            notification_type=notification_type,
            title=title,
            message=message,
            service=service,
            booking_id=booking_id,
            amount=float(amount) if amount is not None else None,
            is_read=False,
        )
    )


@event.listens_for(Session, "after_flush")
def create_automatic_notifications(session, flush_context):
    """Create notifications for new bookings, status changes and wallet txns."""

    processed = getattr(session, PROCESSED_KEY, None)
    if processed is None:
        processed = set()
        setattr(session, PROCESSED_KEY, processed)

    pending = []

    # ------------------------------------------------------------
    # NEW BOOKINGS / FOOD ORDERS
    # ------------------------------------------------------------
    for obj in list(session.new):
        if isinstance(obj, BOOKING_TYPES):
            user_id = getattr(obj, "user_id", None)
            if not user_id:
                continue

            service = _service_for(obj)
            booking_id = getattr(obj, "id", None)
            amount = _booking_amount(obj)
            event_key = ("booking", type(obj).__name__, booking_id)
            if event_key in processed:
                continue
            processed.add(event_key)

            if isinstance(obj, FoodOrder):
                title = "🍔 Food Order Confirmed"
            elif isinstance(obj, MovieBooking):
                title = "🎬 Movie Booking Confirmed"
            elif isinstance(obj, EventBooking):
                title = "🎟️ Event Booking Confirmed"
            else:
                title = f"{service} Booking Confirmed"

            pending.append(
                dict(
                    user_id=user_id,
                    notification_type="booking",
                    title=title,
                    message=_booking_message(obj, service),
                    service=service,
                    booking_id=booking_id,
                    amount=amount,
                )
            )

    # ------------------------------------------------------------
    # CANCELLATIONS / STATUS CHANGES
    # ------------------------------------------------------------
    for obj in list(session.dirty):
        if not isinstance(obj, BOOKING_TYPES):
            continue

        state = inspect(obj)
        attr = _status_attr(obj)
        if attr not in state.attrs:
            continue

        history = state.attrs[attr].history
        if not history.has_changes():
            continue

        new_status = getattr(obj, attr, None)
        old_status = history.deleted[0] if history.deleted else None

        if str(new_status).lower() != "cancelled":
            continue
        if str(old_status).lower() == "cancelled":
            continue

        user_id = getattr(obj, "user_id", None)
        if not user_id:
            continue

        service = _service_for(obj)
        booking_id = getattr(obj, "id", None)
        amount = _booking_amount(obj)
        event_key = ("cancel", type(obj).__name__, booking_id)
        if event_key in processed:
            continue
        processed.add(event_key)

        pending.append(
            dict(
                user_id=user_id,
                notification_type="cancel",
                title=f"❌ {service} Booking Cancelled",
                message=(
                    f"Your {service.lower()} booking #{booking_id} has been "
                    f"cancelled successfully."
                ),
                service=service,
                booking_id=booking_id,
                amount=amount,
            )
        )

    # ------------------------------------------------------------
    # WALLET PAYMENTS / TOP-UPS / REFUNDS
    # ------------------------------------------------------------
    for obj in list(session.new):
        if not isinstance(obj, WalletTransaction):
            continue

        transaction_type = (obj.transaction_type or "").lower()
        description = obj.description or ""
        amount = obj.amount or 0
        transaction_id = getattr(obj, "id", None)
        event_key = ("wallet", transaction_id)
        if event_key in processed:
            continue
        processed.add(event_key)
        is_refund = "refund" in description.lower()

        if is_refund or transaction_type == "credit":
            title = "💰 Refund / Wallet Credit"
            message = (
                f"₹{amount:,.2f} has been credited to your TRAVELX Wallet. "
                f"New balance: ₹{obj.balance_after:,.2f}."
            )
            notification_type = "refund" if is_refund else "wallet"
        else:
            title = "💳 Payment Successful"
            message = (
                f"₹{amount:,.2f} was paid from your TRAVELX Wallet. "
                f"New balance: ₹{obj.balance_after:,.2f}."
            )
            notification_type = "payment"

        pending.append(
            dict(
                user_id=obj.user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                service="Wallet",
                booking_id=None,
                amount=amount,
            )
        )

    for data in pending:
        _add_notification(session, **data)
