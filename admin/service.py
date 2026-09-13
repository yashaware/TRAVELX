from sqlalchemy.orm import Session

from db.models import (
    User,
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


def calculate_stats(db: Session, model, amount_field, status_field):
    records = db.query(model).all()
    bookings = len(records)
    revenue = 0.0
    cancelled = 0

    for record in records:
        amount = getattr(record, amount_field, 0)
        if amount:
            revenue += float(amount)

        status = getattr(record, status_field, "")
        if str(status).lower() == "cancelled":
            cancelled += 1

    return {
        "bookings": bookings,
        "revenue": revenue,
        "cancelled": cancelled,
    }


def get_dashboard_stats(db: Session):
    total_users = db.query(User).count()

    booking_stats = calculate_stats(db, Booking, "amount", "status")
    bus_stats = calculate_stats(db, BusBooking, "total_price", "booking_status")
    train_stats = calculate_stats(db, TrainBooking, "total_price", "booking_status")
    hotel_stats = calculate_stats(db, HotelBooking, "total_price", "booking_status")
    flight_stats = calculate_stats(db, FlightBooking, "total_price", "booking_status")
    cab_stats = calculate_stats(db, CabBooking, "total_price", "booking_status")
    food_stats = calculate_stats(db, FoodOrder, "total_price", "order_status")
    movie_stats = calculate_stats(db, MovieBooking, "total_price", "booking_status")
    event_stats = calculate_stats(db, EventBooking, "total_price", "booking_status")

    services = [
        {"service": "General", **booking_stats},
        {"service": "Bus", **bus_stats},
        {"service": "Train", **train_stats},
        {"service": "Hotel", **hotel_stats},
        {"service": "Flight", **flight_stats},
        {"service": "Cab", **cab_stats},
        {"service": "Food", **food_stats},
        {"service": "Movies", **movie_stats},
        {"service": "Events", **event_stats},
    ]

    total_bookings = sum(item["bookings"] for item in services)
    total_revenue = sum(item["revenue"] for item in services)
    total_cancelled = sum(item["cancelled"] for item in services)
    wallet_transactions = db.query(WalletTransaction).count()

    return {
        "total_users": total_users,
        "total_bookings": total_bookings,
        "total_revenue": round(total_revenue, 2),
        "total_cancelled": total_cancelled,
        "wallet_transactions": wallet_transactions,
        "services": services,
    }


def get_all_users(db: Session, search: str = "", limit: int = 100):
    query = db.query(User)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            (User.name.ilike(term))
            | (User.email.ilike(term))
            | (User.phone.ilike(term))
        )

    return query.order_by(User.id.desc()).limit(limit).all()


def _booking_row(service, record, amount_field, status_field):
    amount = getattr(record, amount_field, 0) or 0
    status = getattr(record, status_field, "") or ""
    payment_method = getattr(record, "payment_method", None)
    created_at = getattr(record, "created_at", None)

    return {
        "id": record.id,
        "service": service,
        "user_id": getattr(record, "user_id", None),
        "amount": float(amount),
        "status": str(status),
        "payment_method": payment_method,
        "created_at": created_at.isoformat() if created_at else None,
    }


def get_all_bookings(db: Session, service: str = "All", status: str = "All", search: str = ""):
    sources = [
        ("General", Booking, "amount", "status"),
        ("Bus", BusBooking, "total_price", "booking_status"),
        ("Train", TrainBooking, "total_price", "booking_status"),
        ("Hotel", HotelBooking, "total_price", "booking_status"),
        ("Flight", FlightBooking, "total_price", "booking_status"),
        ("Cab", CabBooking, "total_price", "booking_status"),
        ("Food", FoodOrder, "total_price", "order_status"),
        ("Movies", MovieBooking, "total_price", "booking_status"),
        ("Events", EventBooking, "total_price", "booking_status"),
    ]

    rows = []

    for service_name, model, amount_field, status_field in sources:
        if service != "All" and service.lower() != service_name.lower():
            continue

        for record in db.query(model).all():
            row = _booking_row(service_name, record, amount_field, status_field)

            if status != "All" and row["status"].lower() != status.lower():
                continue

            rows.append(row)

    users = {user.id: user for user in db.query(User).all()}

    for row in rows:
        user = users.get(row["user_id"])
        row["user_name"] = user.name if user else None
        row["user_email"] = user.email if user else None

    if search:
        term = search.strip().lower()
        rows = [
            row for row in rows
            if term in str(row["id"]).lower()
            or term in str(row.get("user_name") or "").lower()
            or term in str(row.get("user_email") or "").lower()
        ]

    rows.sort(key=lambda row: row.get("created_at") or "", reverse=True)
    return rows
