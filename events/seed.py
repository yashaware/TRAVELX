from db.database import SessionLocal
from db.models import Event, EventVenue, EventShow


def seed_events():
    db = SessionLocal()

    try:

        # =====================================================
        # EVENTS
        # =====================================================

        events_data = [
            {
                "name": "Sunburn Festival",
                "category": "Music",
                "description": "India's biggest electronic dance music festival featuring top DJs and artists.",
                "language": "English",
                "duration_minutes": 360,
                "rating": 4.8,
                "image_url": ""
            },
            {
                "name": "Arijit Singh Live",
                "category": "Concert",
                "description": "Experience soulful melodies and live performances by one of India's most loved singers.",
                "language": "Hindi",
                "duration_minutes": 180,
                "rating": 4.9,
                "image_url": ""
            },
            {
                "name": "Comedy Nights Live",
                "category": "Comedy",
                "description": "A hilarious evening featuring India's popular stand-up comedians.",
                "language": "Hindi",
                "duration_minutes": 150,
                "rating": 4.6,
                "image_url": ""
            },
            {
                "name": "IPL Fan Fest",
                "category": "Sports",
                "description": "A cricket celebration featuring live match screenings, games, music and fan activities.",
                "language": "English",
                "duration_minutes": 300,
                "rating": 4.7,
                "image_url": ""
            },
            {
                "name": "Indian Classical Night",
                "category": "Music",
                "description": "An elegant evening celebrating India's classical music traditions.",
                "language": "Hindi",
                "duration_minutes": 150,
                "rating": 4.5,
                "image_url": ""
            },
            {
                "name": "The Magic Show",
                "category": "Entertainment",
                "description": "A spectacular family-friendly magic and illusion show.",
                "language": "English",
                "duration_minutes": 120,
                "rating": 4.4,
                "image_url": ""
            },
            {
                "name": "Startup & Tech Summit",
                "category": "Business",
                "description": "Meet founders, entrepreneurs, developers and technology leaders.",
                "language": "English",
                "duration_minutes": 240,
                "rating": 4.6,
                "image_url": ""
            },
            {
                "name": "Bollywood Dance Workshop",
                "category": "Workshop",
                "description": "Learn energetic Bollywood dance moves from professional choreographers.",
                "language": "Hindi",
                "duration_minutes": 120,
                "rating": 4.5,
                "image_url": ""
            },
            {
                "name": "Rock On Live",
                "category": "Concert",
                "description": "An exciting live rock music experience featuring talented Indian bands.",
                "language": "English",
                "duration_minutes": 180,
                "rating": 4.7,
                "image_url": ""
            },
            {
                "name": "Food & Culture Festival",
                "category": "Festival",
                "description": "Explore delicious Indian food, cultural performances and traditional activities.",
                "language": "Hindi",
                "duration_minutes": 300,
                "rating": 4.6,
                "image_url": ""
            },
        ]

        # =====================================================
        # CREATE EVENTS
        # =====================================================

        events = []

        for data in events_data:

            existing = db.query(Event).filter(
                Event.name == data["name"]
            ).first()

            if existing:
                event = existing
            else:
                event = Event(**data)
                db.add(event)
                db.flush()

            events.append(event)

        # =====================================================
        # VENUES
        # =====================================================

        venues_data = [
            {
                "name": "Jio World Convention Centre",
                "city": "Mumbai",
                "address": "Bandra Kurla Complex, Mumbai",
                "capacity": 5000
            },
            {
                "name": "Mahalaxmi Racecourse",
                "city": "Mumbai",
                "address": "Mahalaxmi, Mumbai",
                "capacity": 10000
            },
            {
                "name": "Jawaharlal Nehru Stadium",
                "city": "Delhi",
                "address": "Lodhi Road, New Delhi",
                "capacity": 15000
            },
            {
                "name": "Talkatora Indoor Stadium",
                "city": "Delhi",
                "address": "President's Estate, New Delhi",
                "capacity": 3000
            },
            {
                "name": "Phoenix Marketcity",
                "city": "Bangalore",
                "address": "Mahadevapura, Bangalore",
                "capacity": 4000
            },
            {
                "name": "Palace Grounds",
                "city": "Bangalore",
                "address": "Jayamahal Road, Bangalore",
                "capacity": 12000
            },
            {
                "name": "Hitex Exhibition Centre",
                "city": "Hyderabad",
                "address": "HITEC City, Hyderabad",
                "capacity": 8000
            },
            {
                "name": "Shree Shiv Chhatrapati Sports Complex",
                "city": "Pune",
                "address": "Balewadi, Pune",
                "capacity": 10000
            },
            {
                "name": "Balgandharva Rangmandir",
                "city": "Pune",
                "address": "Shivajinagar, Pune",
                "capacity": 2000
            },
            {
                "name": "Ramoji Film City",
                "city": "Hyderabad",
                "address": "Abdullapurmet, Hyderabad",
                "capacity": 15000
            },
        ]

        # =====================================================
        # CREATE VENUES
        # =====================================================

        venues = []

        for data in venues_data:

            existing = db.query(EventVenue).filter(
                EventVenue.name == data["name"],
                EventVenue.city == data["city"]
            ).first()

            if existing:
                venue = existing
            else:
                venue = EventVenue(**data)
                db.add(venue)
                db.flush()

            venues.append(venue)

        db.commit()

        # =====================================================
        # SHOWS
        # =====================================================

        # Helper dictionary
        event_map = {
            event.name: event
            for event in events
        }

        venue_map = {
            venue.name: venue
            for venue in venues
        }

        shows_data = [

            # -------------------------------------------------
            # SUNBURN FESTIVAL - MUMBAI
            # -------------------------------------------------

            {
                "event": "Sunburn Festival",
                "venue": "Mahalaxmi Racecourse",
                "date": "2026-09-20",
                "time": "04:00 PM",
                "ticket_type": "General",
                "price": 2499,
                "tickets": 8000
            },

            {
                "event": "Sunburn Festival",
                "venue": "Mahalaxmi Racecourse",
                "date": "2026-09-21",
                "time": "04:00 PM",
                "ticket_type": "VIP",
                "price": 4999,
                "tickets": 2000
            },

            # -------------------------------------------------
            # ARIJIT SINGH - MUMBAI
            # -------------------------------------------------

            {
                "event": "Arijit Singh Live",
                "venue": "Jio World Convention Centre",
                "date": "2026-09-15",
                "time": "07:00 PM",
                "ticket_type": "Silver",
                "price": 1999,
                "tickets": 2500
            },

            {
                "event": "Arijit Singh Live",
                "venue": "Jio World Convention Centre",
                "date": "2026-09-15",
                "time": "07:00 PM",
                "ticket_type": "Gold",
                "price": 3499,
                "tickets": 1500
            },

            # -------------------------------------------------
            # COMEDY - DELHI
            # -------------------------------------------------

            {
                "event": "Comedy Nights Live",
                "venue": "Talkatora Indoor Stadium",
                "date": "2026-09-12",
                "time": "07:30 PM",
                "ticket_type": "Regular",
                "price": 799,
                "tickets": 2000
            },

            {
                "event": "Comedy Nights Live",
                "venue": "Talkatora Indoor Stadium",
                "date": "2026-09-13",
                "time": "07:30 PM",
                "ticket_type": "Premium",
                "price": 1299,
                "tickets": 800
            },

            # -------------------------------------------------
            # IPL FAN FEST - DELHI
            # -------------------------------------------------

            {
                "event": "IPL Fan Fest",
                "venue": "Jawaharlal Nehru Stadium",
                "date": "2026-09-18",
                "time": "03:00 PM",
                "ticket_type": "General",
                "price": 499,
                "tickets": 10000
            },

            {
                "event": "IPL Fan Fest",
                "venue": "Jawaharlal Nehru Stadium",
                "date": "2026-09-18",
                "time": "03:00 PM",
                "ticket_type": "VIP",
                "price": 1499,
                "tickets": 3000
            },

            # -------------------------------------------------
            # CLASSICAL NIGHT - PUNE
            # -------------------------------------------------

            {
                "event": "Indian Classical Night",
                "venue": "Balgandharva Rangmandir",
                "date": "2026-09-14",
                "time": "06:30 PM",
                "ticket_type": "Regular",
                "price": 599,
                "tickets": 1500
            },

            {
                "event": "Indian Classical Night",
                "venue": "Balgandharva Rangmandir",
                "date": "2026-09-14",
                "time": "06:30 PM",
                "ticket_type": "Premium",
                "price": 999,
                "tickets": 500
            },

            # -------------------------------------------------
            # MAGIC SHOW - BANGALORE
            # -------------------------------------------------

            {
                "event": "The Magic Show",
                "venue": "Phoenix Marketcity",
                "date": "2026-09-16",
                "time": "05:00 PM",
                "ticket_type": "Regular",
                "price": 499,
                "tickets": 2500
            },

            {
                "event": "The Magic Show",
                "venue": "Phoenix Marketcity",
                "date": "2026-09-16",
                "time": "08:00 PM",
                "ticket_type": "Premium",
                "price": 799,
                "tickets": 1000
            },

            # -------------------------------------------------
            # STARTUP SUMMIT - HYDERABAD
            # -------------------------------------------------

            {
                "event": "Startup & Tech Summit",
                "venue": "Hitex Exhibition Centre",
                "date": "2026-09-22",
                "time": "10:00 AM",
                "ticket_type": "Standard",
                "price": 999,
                "tickets": 5000
            },

            {
                "event": "Startup & Tech Summit",
                "venue": "Hitex Exhibition Centre",
                "date": "2026-09-22",
                "time": "10:00 AM",
                "ticket_type": "VIP",
                "price": 2499,
                "tickets": 1000
            },

            # -------------------------------------------------
            # DANCE WORKSHOP - PUNE
            # -------------------------------------------------

            {
                "event": "Bollywood Dance Workshop",
                "venue": "Balgandharva Rangmandir",
                "date": "2026-09-17",
                "time": "11:00 AM",
                "ticket_type": "Workshop Pass",
                "price": 899,
                "tickets": 500
            },

            # -------------------------------------------------
            # ROCK ON - BANGALORE
            # -------------------------------------------------

            {
                "event": "Rock On Live",
                "venue": "Palace Grounds",
                "date": "2026-09-19",
                "time": "07:00 PM",
                "ticket_type": "General",
                "price": 1499,
                "tickets": 8000
            },

            {
                "event": "Rock On Live",
                "venue": "Palace Grounds",
                "date": "2026-09-19",
                "time": "07:00 PM",
                "ticket_type": "VIP",
                "price": 2999,
                "tickets": 2000
            },

            # -------------------------------------------------
            # FOOD FESTIVAL - HYDERABAD
            # -------------------------------------------------

            {
                "event": "Food & Culture Festival",
                "venue": "Ramoji Film City",
                "date": "2026-09-23",
                "time": "12:00 PM",
                "ticket_type": "General",
                "price": 699,
                "tickets": 10000
            },

            {
                "event": "Food & Culture Festival",
                "venue": "Ramoji Film City",
                "date": "2026-09-23",
                "time": "05:00 PM",
                "ticket_type": "Premium",
                "price": 1199,
                "tickets": 3000
            },
        ]

        # =====================================================
        # CREATE SHOWS
        # =====================================================

        created_shows = 0
        skipped_shows = 0

        for data in shows_data:

            event = event_map[data["event"]]
            venue = venue_map[data["venue"]]

            existing = db.query(EventShow).filter(
                EventShow.event_id == event.id,
                EventShow.venue_id == venue.id,
                EventShow.show_date == data["date"],
                EventShow.show_time == data["time"],
                EventShow.ticket_type == data["ticket_type"]
            ).first()

            if existing:
                skipped_shows += 1
                continue

            show = EventShow(
                event_id=event.id,
                venue_id=venue.id,
                show_date=data["date"],
                show_time=data["time"],
                ticket_type=data["ticket_type"],
                ticket_price=data["price"],
                total_tickets=data["tickets"],
                available_tickets=data["tickets"]
            )

            db.add(show)
            created_shows += 1

        db.commit()

        # =====================================================
        # SUMMARY
        # =====================================================

        print()
        print("=" * 60)
        print("🎟️ TRAVELX EVENTS SEED COMPLETED")
        print("=" * 60)

        print(f"🎤 Events       : {len(events)}")
        print(f"🏟️ Venues       : {len(venues)}")
        print(f"🎫 Shows Added  : {created_shows}")
        print(f"⏭️ Shows Skipped: {skipped_shows}")

        print("=" * 60)
        print("✅ Event database is ready!")
        print("=" * 60)
        print()

    except Exception as e:

        db.rollback()

        print()
        print("❌ ERROR WHILE SEEDING EVENTS")
        print(e)
        print()

    finally:

        db.close()


if __name__ == "__main__":
    seed_events()