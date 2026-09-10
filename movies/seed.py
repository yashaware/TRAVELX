from db.database import SessionLocal, engine, Base
from db.models import Movie, Cinema, MovieShow


Base.metadata.create_all(bind=engine)


def seed_movies():

    db = SessionLocal()

    try:

        # =====================================================
        # PREVENT DUPLICATE SEEDING
        # =====================================================

        if db.query(Movie).count() > 0:
            print("Movies already exist.")
            return

        # =====================================================
        # MOVIES
        # =====================================================

        movies = [

            Movie(
                title="Sky Warriors",
                language="Hindi",
                genre="Action",
                duration_minutes=145,
                rating=4.7,
                description="A high-energy action adventure about a fearless team protecting the country.",
                release_date="2026-08-28",
                is_active=True
            ),

            Movie(
                title="Love Beyond Time",
                language="Hindi",
                genre="Romance",
                duration_minutes=132,
                rating=4.4,
                description="A romantic story about two people whose lives cross unexpectedly.",
                release_date="2026-09-04",
                is_active=True
            ),

            Movie(
                title="The Last Mission",
                language="English",
                genre="Action",
                duration_minutes=138,
                rating=4.6,
                description="An elite operative gets one final mission that changes everything.",
                release_date="2026-08-21",
                is_active=True
            ),

            Movie(
                title="Laugh Factory",
                language="Hindi",
                genre="Comedy",
                duration_minutes=118,
                rating=4.2,
                description="A fun-filled comedy packed with friendship, chaos and unforgettable moments.",
                release_date="2026-08-14",
                is_active=True
            ),

            Movie(
                title="Mystery House",
                language="Hindi",
                genre="Thriller",
                duration_minutes=126,
                rating=4.5,
                description="A mysterious house hides secrets that nobody expected to discover.",
                release_date="2026-08-29",
                is_active=True
            ),

            Movie(
                title="Galaxy Beyond",
                language="English",
                genre="Sci-Fi",
                duration_minutes=155,
                rating=4.8,
                description="A futuristic journey across galaxies to find a new home for humanity.",
                release_date="2026-09-05",
                is_active=True
            ),

            Movie(
                title="The Hidden Kingdom",
                language="Hindi",
                genre="Adventure",
                duration_minutes=142,
                rating=4.3,
                description="A group of explorers discovers a forgotten kingdom deep inside the mountains.",
                release_date="2026-08-07",
                is_active=True
            ),

            Movie(
                title="Family Forever",
                language="Hindi",
                genre="Drama",
                duration_minutes=125,
                rating=4.1,
                description="An emotional family story about love, relationships and second chances.",
                release_date="2026-08-01",
                is_active=True
            )
        ]

        db.add_all(movies)
        db.commit()

        for movie in movies:
            db.refresh(movie)

        # =====================================================
        # CINEMAS
        # =====================================================

        cinemas = [

            Cinema(
                name="PVR Phoenix Mall",
                city="Mumbai",
                address="Lower Parel, Mumbai",
                total_seats=180
            ),

            Cinema(
                name="INOX Malad",
                city="Mumbai",
                address="Malad West, Mumbai",
                total_seats=160
            ),

            Cinema(
                name="Cinepolis Andheri",
                city="Mumbai",
                address="Andheri East, Mumbai",
                total_seats=200
            ),

            Cinema(
                name="PVR Select Citywalk",
                city="Delhi",
                address="Saket, New Delhi",
                total_seats=220
            ),

            Cinema(
                name="INOX Connaught Place",
                city="Delhi",
                address="Connaught Place, New Delhi",
                total_seats=180
            ),

            Cinema(
                name="PVR Orion Mall",
                city="Bangalore",
                address="Rajajinagar, Bangalore",
                total_seats=200
            ),

            Cinema(
                name="INOX Garuda Mall",
                city="Bangalore",
                address="Magrath Road, Bangalore",
                total_seats=170
            ),

            Cinema(
                name="PVR Forum Mall",
                city="Hyderabad",
                address="Kukatpally, Hyderabad",
                total_seats=190
            ),

            Cinema(
                name="Cinepolis Seasons Mall",
                city="Pune",
                address="Magarpatta, Pune",
                total_seats=180
            )
        ]

        db.add_all(cinemas)
        db.commit()

        for cinema in cinemas:
            db.refresh(cinema)

        # =====================================================
        # MOVIE SHOWS
        # =====================================================

        shows = [

            # -------------------------------------------------
            # SKY WARRIORS - MUMBAI
            # -------------------------------------------------

            MovieShow(
                movie_id=movies[0].id,
                cinema_id=cinemas[0].id,
                show_date="2026-09-10",
                show_time="10:30 AM",
                screen_name="Screen 1",
                ticket_price=220,
                total_seats=180,
                available_seats=180
            ),

            MovieShow(
                movie_id=movies[0].id,
                cinema_id=cinemas[0].id,
                show_date="2026-09-10",
                show_time="02:00 PM",
                screen_name="Screen 1",
                ticket_price=250,
                total_seats=180,
                available_seats=180
            ),

            MovieShow(
                movie_id=movies[0].id,
                cinema_id=cinemas[0].id,
                show_date="2026-09-10",
                show_time="07:30 PM",
                screen_name="Screen 1",
                ticket_price=300,
                total_seats=180,
                available_seats=180
            ),

            # -------------------------------------------------
            # LOVE BEYOND TIME - MUMBAI
            # -------------------------------------------------

            MovieShow(
                movie_id=movies[1].id,
                cinema_id=cinemas[1].id,
                show_date="2026-09-10",
                show_time="11:00 AM",
                screen_name="Screen 2",
                ticket_price=180,
                total_seats=160,
                available_seats=160
            ),

            MovieShow(
                movie_id=movies[1].id,
                cinema_id=cinemas[1].id,
                show_date="2026-09-10",
                show_time="05:00 PM",
                screen_name="Screen 2",
                ticket_price=240,
                total_seats=160,
                available_seats=160
            ),

            MovieShow(
                movie_id=movies[1].id,
                cinema_id=cinemas[1].id,
                show_date="2026-09-10",
                show_time="09:00 PM",
                screen_name="Screen 2",
                ticket_price=280,
                total_seats=160,
                available_seats=160
            ),

            # -------------------------------------------------
            # THE LAST MISSION - DELHI
            # -------------------------------------------------

            MovieShow(
                movie_id=movies[2].id,
                cinema_id=cinemas[3].id,
                show_date="2026-09-10",
                show_time="11:30 AM",
                screen_name="Screen 3",
                ticket_price=250,
                total_seats=220,
                available_seats=220
            ),

            MovieShow(
                movie_id=movies[2].id,
                cinema_id=cinemas[3].id,
                show_date="2026-09-10",
                show_time="06:30 PM",
                screen_name="Screen 3",
                ticket_price=320,
                total_seats=220,
                available_seats=220
            ),

            MovieShow(
                movie_id=movies[2].id,
                cinema_id=cinemas[4].id,
                show_date="2026-09-11",
                show_time="09:30 PM",
                screen_name="Screen 1",
                ticket_price=300,
                total_seats=180,
                available_seats=180
            ),

            # -------------------------------------------------
            # LAUGH FACTORY - BANGALORE
            # -------------------------------------------------

            MovieShow(
                movie_id=movies[3].id,
                cinema_id=cinemas[5].id,
                show_date="2026-09-10",
                show_time="01:00 PM",
                screen_name="Screen 2",
                ticket_price=180,
                total_seats=200,
                available_seats=200
            ),

            MovieShow(
                movie_id=movies[3].id,
                cinema_id=cinemas[5].id,
                show_date="2026-09-10",
                show_time="07:00 PM",
                screen_name="Screen 2",
                ticket_price=240,
                total_seats=200,
                available_seats=200
            ),

            # -------------------------------------------------
            # MYSTERY HOUSE - MUMBAI
            # -------------------------------------------------

            MovieShow(
                movie_id=movies[4].id,
                cinema_id=cinemas[2].id,
                show_date="2026-09-10",
                show_time="03:00 PM",
                screen_name="Screen 4",
                ticket_price=220,
                total_seats=200,
                available_seats=200
            ),

            MovieShow(
                movie_id=movies[4].id,
                cinema_id=cinemas[2].id,
                show_date="2026-09-10",
                show_time="10:00 PM",
                screen_name="Screen 4",
                ticket_price=280,
                total_seats=200,
                available_seats=200
            ),

            # -------------------------------------------------
            # GALAXY BEYOND - PUNE
            # -------------------------------------------------

            MovieShow(
                movie_id=movies[5].id,
                cinema_id=cinemas[8].id,
                show_date="2026-09-10",
                show_time="12:00 PM",
                screen_name="Screen 1",
                ticket_price=250,
                total_seats=180,
                available_seats=180
            ),

            MovieShow(
                movie_id=movies[5].id,
                cinema_id=cinemas[8].id,
                show_date="2026-09-10",
                show_time="06:00 PM",
                screen_name="Screen 1",
                ticket_price=320,
                total_seats=180,
                available_seats=180
            ),

            MovieShow(
                movie_id=movies[5].id,
                cinema_id=cinemas[8].id,
                show_date="2026-09-10",
                show_time="09:30 PM",
                screen_name="Screen 1",
                ticket_price=350,
                total_seats=180,
                available_seats=180
            ),

            # -------------------------------------------------
            # HIDDEN KINGDOM - HYDERABAD
            # -------------------------------------------------

            MovieShow(
                movie_id=movies[6].id,
                cinema_id=cinemas[7].id,
                show_date="2026-09-10",
                show_time="02:30 PM",
                screen_name="Screen 2",
                ticket_price=200,
                total_seats=190,
                available_seats=190
            ),

            MovieShow(
                movie_id=movies[6].id,
                cinema_id=cinemas[7].id,
                show_date="2026-09-10",
                show_time="08:00 PM",
                screen_name="Screen 2",
                ticket_price=260,
                total_seats=190,
                available_seats=190
            ),

            # -------------------------------------------------
            # FAMILY FOREVER - DELHI
            # -------------------------------------------------

            MovieShow(
                movie_id=movies[7].id,
                cinema_id=cinemas[4].id,
                show_date="2026-09-10",
                show_time="04:00 PM",
                screen_name="Screen 5",
                ticket_price=180,
                total_seats=180,
                available_seats=180
            ),

            MovieShow(
                movie_id=movies[7].id,
                cinema_id=cinemas[4].id,
                show_date="2026-09-10",
                show_time="08:30 PM",
                screen_name="Screen 5",
                ticket_price=230,
                total_seats=180,
                available_seats=180
            )
        ]

        db.add_all(shows)
        db.commit()

        print("✅ Movie, cinema and show data inserted successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_movies()