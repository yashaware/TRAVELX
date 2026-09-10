from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import (
    Movie,
    Cinema,
    MovieShow,
    MovieBooking,
    Wallet,
    WalletTransaction
)

from movies.schemas import (
    MovieCreate,
    MovieResponse,
    MovieSearch,
    CinemaCreate,
    CinemaResponse,
    CinemaSearch,
    MovieShowCreate,
    MovieShowResponse,
    MovieBookingCreate,
    MovieBookingResponse
)

from auth.security import get_current_user


movie_router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


# =========================================================
# MOVIES
# =========================================================

@movie_router.get(
    "/",
    response_model=list[MovieResponse]
)
def get_all_movies(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Movie).filter(
        Movie.is_active == True
    ).order_by(
        Movie.rating.desc()
    ).all()


@movie_router.post(
    "/",
    response_model=MovieResponse
)
def create_movie(
    movie_data: MovieCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    movie = Movie(
        title=movie_data.title,
        language=movie_data.language,
        genre=movie_data.genre,
        duration_minutes=movie_data.duration_minutes,
        rating=movie_data.rating,
        description=movie_data.description,
        release_date=movie_data.release_date,
        is_active=movie_data.is_active
    )

    db.add(movie)
    db.commit()
    db.refresh(movie)

    return movie


@movie_router.post(
    "/search",
    response_model=list[MovieResponse]
)
def search_movies(
    search_data: MovieSearch,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Movie).filter(
        Movie.is_active == True
    )

    if search_data.language:
        query = query.filter(
            Movie.language.ilike(
                search_data.language.strip()
            )
        )

    if search_data.genre:
        query = query.filter(
            Movie.genre.ilike(
                search_data.genre.strip()
            )
        )

    return query.order_by(
        Movie.rating.desc()
    ).all()


# =========================================================
# CINEMAS
# =========================================================

@movie_router.get(
    "/cinemas/all",
    response_model=list[CinemaResponse]
)
def get_all_cinemas(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Cinema).order_by(
        Cinema.city,
        Cinema.name
    ).all()


@movie_router.post(
    "/cinemas",
    response_model=CinemaResponse
)
def create_cinema(
    cinema_data: CinemaCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cinema = Cinema(
        name=cinema_data.name,
        city=cinema_data.city,
        address=cinema_data.address,
        total_seats=cinema_data.total_seats
    )

    db.add(cinema)
    db.commit()
    db.refresh(cinema)

    return cinema


@movie_router.post(
    "/cinemas/search",
    response_model=list[CinemaResponse]
)
def search_cinemas(
    search_data: CinemaSearch,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    city = search_data.city.strip()

    return db.query(Cinema).filter(
        Cinema.city.ilike(city)
    ).order_by(
        Cinema.name
    ).all()


@movie_router.get(
    "/cinemas/{cinema_id}",
    response_model=CinemaResponse
)
def get_cinema(
    cinema_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cinema = db.query(Cinema).filter(
        Cinema.id == cinema_id
    ).first()

    if not cinema:
        raise HTTPException(
            status_code=404,
            detail="Cinema not found."
        )

    return cinema


# =========================================================
# MOVIE SHOWS
# =========================================================

@movie_router.post(
    "/shows",
    response_model=MovieShowResponse
)
def create_movie_show(
    show_data: MovieShowCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(
        Movie.id == show_data.movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found."
        )

    cinema = db.query(Cinema).filter(
        Cinema.id == show_data.cinema_id
    ).first()

    if not cinema:
        raise HTTPException(
            status_code=404,
            detail="Cinema not found."
        )

    if show_data.available_seats > show_data.total_seats:
        raise HTTPException(
            status_code=400,
            detail="Available seats cannot exceed total seats."
        )

    show = MovieShow(
        movie_id=show_data.movie_id,
        cinema_id=show_data.cinema_id,
        show_date=show_data.show_date,
        show_time=show_data.show_time,
        screen_name=show_data.screen_name,
        ticket_price=show_data.ticket_price,
        total_seats=show_data.total_seats,
        available_seats=show_data.available_seats
    )

    db.add(show)
    db.commit()
    db.refresh(show)

    return show


@movie_router.get(
    "/shows/movie/{movie_id}",
    response_model=list[MovieShowResponse]
)
def get_movie_shows(
    movie_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found."
        )

    return db.query(MovieShow).filter(
        MovieShow.movie_id == movie_id,
        MovieShow.available_seats > 0
    ).order_by(
        MovieShow.show_date,
        MovieShow.show_time
    ).all()


@movie_router.get(
    "/shows/cinema/{cinema_id}",
    response_model=list[MovieShowResponse]
)
def get_cinema_shows(
    cinema_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cinema = db.query(Cinema).filter(
        Cinema.id == cinema_id
    ).first()

    if not cinema:
        raise HTTPException(
            status_code=404,
            detail="Cinema not found."
        )

    return db.query(MovieShow).filter(
        MovieShow.cinema_id == cinema_id,
        MovieShow.available_seats > 0
    ).order_by(
        MovieShow.show_date,
        MovieShow.show_time
    ).all()


@movie_router.get(
    "/shows/{show_id}",
    response_model=MovieShowResponse
)
def get_show(
    show_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    show = db.query(MovieShow).filter(
        MovieShow.id == show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Movie show not found."
        )

    return show


# =========================================================
# MOVIE BOOKING
# =========================================================

@movie_router.post(
    "/book",
    response_model=MovieBookingResponse
)
def create_movie_booking(
    booking_data: MovieBookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Validate movie
    # -----------------------------------------------------

    movie = db.query(Movie).filter(
        Movie.id == booking_data.movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found."
        )

    # -----------------------------------------------------
    # Validate cinema
    # -----------------------------------------------------

    cinema = db.query(Cinema).filter(
        Cinema.id == booking_data.cinema_id
    ).first()

    if not cinema:
        raise HTTPException(
            status_code=404,
            detail="Cinema not found."
        )

    # -----------------------------------------------------
    # Validate show
    # -----------------------------------------------------

    show = db.query(MovieShow).filter(
        MovieShow.id == booking_data.show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Movie show not found."
        )

    # -----------------------------------------------------
    # Verify movie + cinema + show relationship
    # -----------------------------------------------------

    if show.movie_id != booking_data.movie_id:
        raise HTTPException(
            status_code=400,
            detail="Show does not belong to the selected movie."
        )

    if show.cinema_id != booking_data.cinema_id:
        raise HTTPException(
            status_code=400,
            detail="Show does not belong to the selected cinema."
        )

    # -----------------------------------------------------
    # Validate seats
    # -----------------------------------------------------

    if not booking_data.seats:
        raise HTTPException(
            status_code=400,
            detail="Please select at least one seat."
        )

    selected_seats = [
        seat.strip().upper()
        for seat in booking_data.seats
        if seat.strip()
    ]

    if not selected_seats:
        raise HTTPException(
            status_code=400,
            detail="Please select valid seats."
        )

    # -----------------------------------------------------
    # Remove duplicate seats
    # -----------------------------------------------------

    selected_seats = list(
        dict.fromkeys(selected_seats)
    )

    number_of_seats = len(selected_seats)

    # -----------------------------------------------------
    # Check available seats
    # -----------------------------------------------------

    if number_of_seats > show.available_seats:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Not enough seats available. "
                f"Available: {show.available_seats}"
            )
        )

    # -----------------------------------------------------
    # Calculate total price
    # -----------------------------------------------------

    total_price = (
        show.ticket_price * number_of_seats
    )

    # -----------------------------------------------------
    # Payment method
    # -----------------------------------------------------

    payment_method = (
        booking_data.payment_method
        .strip()
        .lower()
    )

    # -----------------------------------------------------
    # Wallet payment
    # -----------------------------------------------------

    if payment_method == "wallet":

        wallet = db.query(Wallet).filter(
            Wallet.user_id == current_user["id"]
        ).first()

        # Create wallet if user doesn't have one
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
                    f"Insufficient wallet balance. "
                    f"Available: ₹{wallet.balance:.2f}, "
                    f"Required: ₹{total_price:.2f}"
                )
            )

        # Deduct amount
        wallet.balance -= total_price

        # Create wallet transaction
        transaction = WalletTransaction(
            user_id=current_user["id"],
            transaction_type="debit",
            amount=total_price,
            description=(
                f"Movie booking - "
                f"{movie.title} "
                f"at {cinema.name}"
            ),
            balance_after=wallet.balance
        )

        db.add(transaction)

    # -----------------------------------------------------
    # Demo payment
    # -----------------------------------------------------

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
    # Reduce available seats
    # -----------------------------------------------------

    show.available_seats -= number_of_seats

    # -----------------------------------------------------
    # Create movie booking
    # -----------------------------------------------------

    booking = MovieBooking(

        user_id=current_user["id"],

        movie_id=movie.id,

        cinema_id=cinema.id,

        show_id=show.id,

        customer_name=booking_data.customer_name,

        customer_phone=booking_data.customer_phone,

        show_date=show.show_date,

        show_time=show.show_time,

        seats=",".join(selected_seats),

        number_of_seats=number_of_seats,

        total_price=total_price,

        payment_method=payment_method,

        booking_status="confirmed"
    )

    db.add(booking)

    db.commit()

    db.refresh(booking)

    return booking


# =========================================================
# MY MOVIE BOOKINGS
# =========================================================

@movie_router.get(
    "/my-bookings",
    response_model=list[MovieBookingResponse]
)
def get_my_movie_bookings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    bookings = db.query(MovieBooking).filter(
        MovieBooking.user_id == current_user["id"]
    ).order_by(
        MovieBooking.id.desc()
    ).all()

    return bookings


# =========================================================
# SINGLE MOVIE BOOKING
# =========================================================

@movie_router.get(
    "/bookings/{booking_id}",
    response_model=MovieBookingResponse
)
def get_movie_booking(
    booking_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    booking = db.query(MovieBooking).filter(
        MovieBooking.id == booking_id,
        MovieBooking.user_id == current_user["id"]
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Movie booking not found."
        )

    return booking


# =========================================================
# GET SINGLE MOVIE
# IMPORTANT:
# KEEP THIS ROUTE AT THE VERY BOTTOM
# =========================================================

@movie_router.get(
    "/{movie_id}",
    response_model=MovieResponse
)
def get_movie(
    movie_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    movie = db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found."
        )

    return movie