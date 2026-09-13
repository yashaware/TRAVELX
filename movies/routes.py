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

from auth.security import (
    get_current_user,
    require_admin
)


movie_router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


# =========================================================
# ADMIN - MOVIES
# JWT + ADMIN ROLE PROTECTED
# =========================================================

@movie_router.get(
    "/admin/all",
    response_model=list[MovieResponse]
)
def admin_get_all_movies(
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    return db.query(Movie).order_by(
        Movie.id.desc()
    ).all()


@movie_router.post(
    "/admin/create",
    response_model=MovieResponse
)
def admin_create_movie(
    movie_data: MovieCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
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


@movie_router.get(
    "/admin/{movie_id}",
    response_model=MovieResponse
)
def admin_get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
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


@movie_router.put(
    "/admin/{movie_id}",
    response_model=MovieResponse
)
def admin_update_movie(
    movie_id: int,
    movie_data: MovieCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    movie = db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found."
        )

    movie.title = movie_data.title
    movie.language = movie_data.language
    movie.genre = movie_data.genre
    movie.duration_minutes = movie_data.duration_minutes
    movie.rating = movie_data.rating
    movie.description = movie_data.description
    movie.release_date = movie_data.release_date
    movie.is_active = movie_data.is_active

    db.commit()
    db.refresh(movie)

    return movie


@movie_router.delete(
    "/admin/{movie_id}"
)
def admin_delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    movie = db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found."
        )

    # Prevent deleting a movie that has bookings
    booking_exists = db.query(MovieBooking).filter(
        MovieBooking.movie_id == movie_id
    ).first()

    if booking_exists:
        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot delete movie because bookings "
                "already exist for this movie."
            )
        )

    # Delete associated shows first
    db.query(MovieShow).filter(
        MovieShow.movie_id == movie_id
    ).delete(
        synchronize_session=False
    )

    db.delete(movie)
    db.commit()

    return {
        "message": "Movie deleted successfully.",
        "movie_id": movie_id
    }


# =========================================================
# MOVIES - CUSTOMER
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
# ADMIN - CINEMAS
# JWT + ADMIN ROLE PROTECTED
# =========================================================

@movie_router.get(
    "/admin/cinemas/all",
    response_model=list[CinemaResponse]
)
def admin_get_all_cinemas(
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    return db.query(Cinema).order_by(
        Cinema.city,
        Cinema.name
    ).all()


@movie_router.post(
    "/admin/cinemas/create",
    response_model=CinemaResponse
)
def admin_create_cinema(
    cinema_data: CinemaCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
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


@movie_router.get(
    "/admin/cinemas/{cinema_id}",
    response_model=CinemaResponse
)
def admin_get_cinema(
    cinema_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
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


@movie_router.put(
    "/admin/cinemas/{cinema_id}",
    response_model=CinemaResponse
)
def admin_update_cinema(
    cinema_id: int,
    cinema_data: CinemaCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    cinema = db.query(Cinema).filter(
        Cinema.id == cinema_id
    ).first()

    if not cinema:
        raise HTTPException(
            status_code=404,
            detail="Cinema not found."
        )

    cinema.name = cinema_data.name
    cinema.city = cinema_data.city
    cinema.address = cinema_data.address
    cinema.total_seats = cinema_data.total_seats

    db.commit()
    db.refresh(cinema)

    return cinema


@movie_router.delete(
    "/admin/cinemas/{cinema_id}"
)
def admin_delete_cinema(
    cinema_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    cinema = db.query(Cinema).filter(
        Cinema.id == cinema_id
    ).first()

    if not cinema:
        raise HTTPException(
            status_code=404,
            detail="Cinema not found."
        )

    booking_exists = db.query(MovieBooking).filter(
        MovieBooking.cinema_id == cinema_id
    ).first()

    if booking_exists:
        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot delete cinema because movie "
                "bookings already exist."
            )
        )

    db.query(MovieShow).filter(
        MovieShow.cinema_id == cinema_id
    ).delete(
        synchronize_session=False
    )

    db.delete(cinema)
    db.commit()

    return {
        "message": "Cinema deleted successfully.",
        "cinema_id": cinema_id
    }


# =========================================================
# CINEMAS - CUSTOMER
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


# =========================================================
# ADMIN - MOVIE SHOWS
# JWT + ADMIN ROLE PROTECTED
# =========================================================

@movie_router.get(
    "/admin/shows/all",
    response_model=list[MovieShowResponse]
)
def admin_get_all_shows(
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    return db.query(MovieShow).order_by(
        MovieShow.show_date,
        MovieShow.show_time
    ).all()


@movie_router.post(
    "/admin/shows/create",
    response_model=MovieShowResponse
)
def admin_create_show(
    show_data: MovieShowCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
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
    "/admin/shows/{show_id}",
    response_model=MovieShowResponse
)
def admin_get_show(
    show_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
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


@movie_router.put(
    "/admin/shows/{show_id}",
    response_model=MovieShowResponse
)
def admin_update_show(
    show_id: int,
    show_data: MovieShowCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    show = db.query(MovieShow).filter(
        MovieShow.id == show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Movie show not found."
        )

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

    # Don't allow reducing total seats below already-booked seats
    booked_seats = (
        show.total_seats - show.available_seats
    )

    if show_data.total_seats < booked_seats:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Total seats cannot be less than "
                f"already booked seats ({booked_seats})."
            )
        )

    show.movie_id = show_data.movie_id
    show.cinema_id = show_data.cinema_id
    show.show_date = show_data.show_date
    show.show_time = show_data.show_time
    show.screen_name = show_data.screen_name
    show.ticket_price = show_data.ticket_price
    show.total_seats = show_data.total_seats
    show.available_seats = show_data.available_seats

    db.commit()
    db.refresh(show)

    return show


@movie_router.delete(
    "/admin/shows/{show_id}"
)
def admin_delete_show(
    show_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    show = db.query(MovieShow).filter(
        MovieShow.id == show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Movie show not found."
        )

    booking_exists = db.query(MovieBooking).filter(
        MovieBooking.show_id == show_id
    ).first()

    if booking_exists:
        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot delete show because movie "
                "bookings already exist for this show."
            )
        )

    db.delete(show)
    db.commit()

    return {
        "message": "Movie show deleted successfully.",
        "show_id": show_id
    }


# =========================================================
# CINEMA SINGLE
# =========================================================

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
# MOVIE SHOWS - CUSTOMER
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

    movie = db.query(Movie).filter(
        Movie.id == booking_data.movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found."
        )

    cinema = db.query(Cinema).filter(
        Cinema.id == booking_data.cinema_id
    ).first()

    if not cinema:
        raise HTTPException(
            status_code=404,
            detail="Cinema not found."
        )

    show = db.query(MovieShow).filter(
        MovieShow.id == booking_data.show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Movie show not found."
        )

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

    selected_seats = list(
        dict.fromkeys(selected_seats)
    )

    number_of_seats = len(selected_seats)

    if number_of_seats > show.available_seats:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Not enough seats available. "
                f"Available: {show.available_seats}"
            )
        )

    total_price = (
        show.ticket_price * number_of_seats
    )

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
                f"Movie booking - "
                f"{movie.title} "
                f"at {cinema.name}"
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

    show.available_seats -= number_of_seats

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
# CANCEL MOVIE BOOKING + WALLET REFUND
# =========================================================

@movie_router.post(
    "/bookings/{booking_id}/cancel",
    response_model=MovieBookingResponse
)
def cancel_movie_booking(
    booking_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    booking = db.query(MovieBooking).filter(
        MovieBooking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Movie booking not found."
        )

    if booking.user_id != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to cancel this booking."
        )

    if booking.booking_status != "confirmed":
        raise HTTPException(
            status_code=400,
            detail=(
                "Booking cannot be cancelled because "
                f"its status is '{booking.booking_status}'."
            )
        )

    show = db.query(MovieShow).filter(
        MovieShow.id == booking.show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Associated movie show not found."
        )

    movie = db.query(Movie).filter(
        Movie.id == booking.movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Associated movie not found."
        )

    show.available_seats += booking.number_of_seats

    payment_method = (
        booking.payment_method or "demo"
    ).strip().lower()

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
                f"Movie booking refund - "
                f"Booking #{booking.id} - "
                f"{movie.title}"
            ),
            balance_after=wallet.balance
        )

        db.add(refund_transaction)

    booking.booking_status = "cancelled"

    db.commit()
    db.refresh(booking)

    return booking


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