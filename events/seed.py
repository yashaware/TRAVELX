from db.database import SessionLocal
from db.models import Event, EventVenue, EventShow


def seed_events():
    db = SessionLocal()

    try:

        # =====================================================
        # DEMO EVENTS
        # =====================================================

        events_data = [

            {
                "name": "Sunburn Festival",
                "category": "Music",
                "description": "A high-energy electronic music festival featuring DJs, live performances and entertainment.",
                "language": "English",
                "duration_minutes": 360,
                "rating": 4.8,
                "image_url": ""
            },

            {
                "name": "Arijit Singh Live",
                "category": "Concert",
                "description": "A soulful live music concert featuring romantic and popular Hindi songs.",
                "language": "Hindi",
                "duration_minutes": 180,
                "rating": 4.9,
                "image_url": ""
            },

            {
                "name": "Comedy Nights Live",
                "category": "Comedy",
                "description": "A fun-filled stand-up comedy evening featuring popular Indian comedians.",
                "language": "Hindi",
                "duration_minutes": 150,
                "rating": 4.6,
                "image_url": ""
            },

            {
                "name": "IPL Fan Fest",
                "category": "Sports",
                "description": "A cricket celebration with match screenings, fan activities, games and live entertainment.",
                "language": "English",
                "duration_minutes": 300,
                "rating": 4.7,
                "image_url": ""
            },

            {
                "name": "Indian Classical Night",
                "category": "Music",
                "description": "An elegant evening celebrating Indian classical music and traditional performances.",
                "language": "Hindi",
                "duration_minutes": 150,
                "rating": 4.5,
                "image_url": ""
            },

            {
                "name": "The Magic Show",
                "category": "Entertainment",
                "description": "A spectacular family-friendly magic and illusion experience.",
                "language": "English",
                "duration_minutes": 120,
                "rating": 4.4,
                "image_url": ""
            },

            {
                "name": "Startup & Tech Summit",
                "category": "Business",
                "description": "A technology and startup summit connecting founders, developers and entrepreneurs.",
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
                "description": "Experience Indian food, cultural performances, traditional activities and entertainment.",
                "language": "Hindi",
                "duration_minutes": 300,
                "rating": 4.6,
                "image_url": ""
            }
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
        # DEMO VENUES
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
                "city": "Bengaluru",
                "address": "Mahadevapura, Bengaluru",
                "capacity": 4000
            },

            {
                "name": "Palace Grounds",
                "city": "Bengaluru",
                "address": "Jayamahal Road, Bengaluru",
                "capacity": 12000
            },

            {
                "name": "HITEX Exhibition Centre",
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
            }
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
        # MAP EVENTS AND VENUES
        # =====================================================

        event_map = {
            event.name: event
            for event in events
        }

        venue_map = {
            venue.name: venue
            for venue in venues
        }

        # =====================================================
        # DEMO SHOWS
        # All dates are future demo dates
        # =====================================================

        shows_data = [

            # -------------------------------------------------
            # SUNBURN FESTIVAL
            # -------------------------------------------------

            {
                "event": "Sunburn Festival",
                "venue": "Mahalaxmi Racecourse",
                "date": "2026-09-27",
                "time": "04:00 PM",
                "ticket_type": "General",
                "price": 2499,
                "tickets": 8000
            },

            {
                "event": "Sunburn Festival",
                "venue": "Mahalaxmi Racecourse",
                "date": "2026-09-28",
                "time": "04:00 PM",
                "ticket_type": "VIP",
                "price": 4999,
                "tickets": 2000
            },

            # -------------------------------------------------
            # ARIJIT SINGH
            # -------------------------------------------------

            {
                "event": "Arijit Singh Live",
                "venue": "Jio World Convention Centre",
                "date": "2026-09-26",
                "time": "07:00 PM",
                "ticket_type": "Silver",
                "price": 1999,
                "tickets": 2500
            },

            {
                "event": "Arijit Singh Live",
                "venue": "Jio World Convention Centre",
                "date": "2026-09-26",
                "time": "07:00 PM",
                "ticket_type": "Gold",
                "price": 3499,
                "tickets": 1500
            },

            # -------------------------------------------------
            # COMEDY
            # -------------------------------------------------

            {
                "event": "Comedy Nights Live",
                "venue": "Talkatora Indoor Stadium",
                "date": "2026-09-25",
                "time": "07:30 PM",
                "ticket_type": "Regular",
                "price": 799,
                "tickets": 2000
            },

            {
                "event": "Comedy Nights Live",
                "venue": "Talkatora Indoor Stadium",
                "date": "2026-09-26",
                "time": "07:30 PM",
                "ticket_type": "Premium",
                "price": 1299,
                "tickets": 800
            },

            # -------------------------------------------------
            # IPL FAN FEST
            # -------------------------------------------------

            {
                "event": "IPL Fan Fest",
                "venue": "Jawaharlal Nehru Stadium",
                "date": "2026-09-29",
                "time": "03:00 PM",
                "ticket_type": "General",
                "price": 499,
                "tickets": 10000
            },

            {
                "event": "IPL Fan Fest",
                "venue": "Jawaharlal Nehru Stadium",
                "date": "2026-09-29",
                "time": "03:00 PM",
                "ticket_type": "VIP",
                "price": 1499,
                "tickets": 3000
            },

            # -------------------------------------------------
            # CLASSICAL NIGHT
            # -------------------------------------------------

            {
                "event": "Indian Classical Night",
                "venue": "Balgandharva Rangmandir",
                "date": "2026-09-30",
                "time": "06:30 PM",
                "ticket_type": "Regular",
                "price": 599,
                "tickets": 1500
            },

            {
                "event": "Indian Classical Night",
                "venue": "Balgandharva Rangmandir",
                "date": "2026-09-30",
                "time": "06:30 PM",
                "ticket_type": "Premium",
                "price": 999,
                "tickets": 500
            },

            # -------------------------------------------------
            # MAGIC SHOW
            # -------------------------------------------------

            {
                "event": "The Magic Show",
                "venue": "Phoenix Marketcity",
                "date": "2026-10-01",
                "time": "05:00 PM",
                "ticket_type": "Regular",
                "price": 499,
                "tickets": 2500
            },

            {
                "event": "The Magic Show",
                "venue": "Phoenix Marketcity",
                "date": "2026-10-01",
                "time": "08:00 PM",
                "ticket_type": "Premium",
                "price": 799,
                "tickets": 1000
            },

            # -------------------------------------------------
            # STARTUP SUMMIT
            # -------------------------------------------------

            {
                "event": "Startup & Tech Summit",
                "venue": "HITEX Exhibition Centre",
                "date": "2026-10-02",
                "time": "10:00 AM",
                "ticket_type": "Standard",
                "price": 999,
                "tickets": 5000
            },

            {
                "event": "Startup & Tech Summit",
                "venue": "HITEX Exhibition Centre",
                "date": "2026-10-02",
                "time": "10:00 AM",
                "ticket_type": "VIP",
                "price": 2499,
                "tickets": 1000
            },

            # -------------------------------------------------
            # DANCE WORKSHOP
            # -------------------------------------------------

            {
                "event": "Bollywood Dance Workshop",
                "venue": "Balgandharva Rangmandir",
                "date": "2026-10-03",
                "time": "11:00 AM",
                "ticket_type": "Workshop Pass",
                "price": 899,
                "tickets": 500
            },

            {
                "event": "Bollywood Dance Workshop",
                "venue": "Balgandharva Rangmandir",
                "date": "2026-10-04",
                "time": "11:00 AM",
                "ticket_type": "Premium Workshop",
                "price": 1299,
                "tickets": 300
            },

            # -------------------------------------------------
            # ROCK ON
            # -------------------------------------------------

            {
                "event": "Rock On Live",
                "venue": "Palace Grounds",
                "date": "2026-10-05",
                "time": "07:00 PM",
                "ticket_type": "General",
                "price": 1499,
                "tickets": 8000
            },

            {
                "event": "Rock On Live",
                "venue": "Palace Grounds",
                "date": "2026-10-05",
                "time": "07:00 PM",
                "ticket_type": "VIP",
                "price": 2999,
                "tickets": 2000
            },

            # -------------------------------------------------
            # FOOD FESTIVAL
            # -------------------------------------------------

            {
                "event": "Food & Culture Festival",
                "venue": "Ramoji Film City",
                "date": "2026-10-06",
                "time": "12:00 PM",
                "ticket_type": "General",
                "price": 699,
                "tickets": 10000
            },

            {
                "event": "Food & Culture Festival",
                "venue": "Ramoji Film City",
                "date": "2026-10-06",
                "time": "05:00 PM",
                "ticket_type": "Premium",
                "price": 1199,
                "tickets": 3000
            }
        ]

        # =====================================================
        # CREATE SHOWS
        # =====================================================

        created_shows = 0
        skipped_shows = 0

        for data in shows_data:

            event = event_map[data["event"]]
            venue = venue_map[data["venue"]]

            # Safety check:
            # Tickets cannot exceed venue capacity
            if data["tickets"] > venue.capacity:
                print(
                    f"⚠️ Skipping {data['event']} - "
                    f"{data['ticket_type']} because tickets "
                    f"exceed venue capacity."
                )
                skipped_shows += 1
                continue

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
        print("🎟️ TRAVELX EVENTS DEMO SEED COMPLETED")
        print("=" * 60)

        print(f"🎤 Events       : {len(events)}")
        print(f"🏟️ Venues       : {len(venues)}")
        print(f"🎫 Shows Added  : {created_shows}")
        print(f"⏭️ Shows Skipped: {skipped_shows}")

        print("=" * 60)
        print("✅ Demo event database is ready!")
        print("⚠️ Data is synthetic/demo data.")
        print("⚠️ It is NOT real-time event inventory.")
        print("=" * 60)
        print()

    except Exception as e:

        db.rollback()

        print()
        print("=" * 60)
        print("❌ ERROR WHILE SEEDING EVENTS")
        print("=" * 60)
        print(e)
        print()

    finally:
        db.close()


if __name__ == "__main__":
    seed_events()