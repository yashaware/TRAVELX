from db.database import SessionLocal
from db.models import Flight


flights = [

    # Mumbai → Delhi
    {
        "airline": "IndiGo",
        "flight_number": "6E-2001",
        "source": "Mumbai",
        "destination": "Delhi",
        "departure_time": "06:00 AM",
        "arrival_time": "08:10 AM",
        "economy_price": 4500,
        "premium_economy_price": 6500,
        "business_price": 9500,
        "available_seats": 180
    },
    {
        "airline": "Air India",
        "flight_number": "AI-864",
        "source": "Mumbai",
        "destination": "Delhi",
        "departure_time": "09:30 AM",
        "arrival_time": "11:45 AM",
        "economy_price": 5200,
        "premium_economy_price": 7200,
        "business_price": 10500,
        "available_seats": 160
    },

    # Delhi → Mumbai
    {
        "airline": "IndiGo",
        "flight_number": "6E-2104",
        "source": "Delhi",
        "destination": "Mumbai",
        "departure_time": "07:00 AM",
        "arrival_time": "09:15 AM",
        "economy_price": 4700,
        "premium_economy_price": 6700,
        "business_price": 9800,
        "available_seats": 175
    },
    {
        "airline": "Air India",
        "flight_number": "AI-805",
        "source": "Delhi",
        "destination": "Mumbai",
        "departure_time": "02:00 PM",
        "arrival_time": "04:20 PM",
        "economy_price": 5000,
        "premium_economy_price": 7000,
        "business_price": 10000,
        "available_seats": 150
    },

    # Mumbai → Bangalore
    {
        "airline": "IndiGo",
        "flight_number": "6E-505",
        "source": "Mumbai",
        "destination": "Bangalore",
        "departure_time": "06:30 AM",
        "arrival_time": "08:15 AM",
        "economy_price": 3800,
        "premium_economy_price": 5600,
        "business_price": 8500,
        "available_seats": 170
    },
    {
        "airline": "Akasa Air",
        "flight_number": "QP-1102",
        "source": "Mumbai",
        "destination": "Bangalore",
        "departure_time": "11:00 AM",
        "arrival_time": "12:45 PM",
        "economy_price": 3500,
        "premium_economy_price": 5200,
        "business_price": 8000,
        "available_seats": 165
    },

    # Bangalore → Mumbai
    {
        "airline": "IndiGo",
        "flight_number": "6E-506",
        "source": "Bangalore",
        "destination": "Mumbai",
        "departure_time": "09:00 AM",
        "arrival_time": "10:45 AM",
        "economy_price": 3900,
        "premium_economy_price": 5700,
        "business_price": 8600,
        "available_seats": 175
    },

    # Delhi → Bangalore
    {
        "airline": "Air India",
        "flight_number": "AI-503",
        "source": "Delhi",
        "destination": "Bangalore",
        "departure_time": "08:00 AM",
        "arrival_time": "10:45 AM",
        "economy_price": 5500,
        "premium_economy_price": 7500,
        "business_price": 11000,
        "available_seats": 155
    },

    # Bangalore → Delhi
    {
        "airline": "IndiGo",
        "flight_number": "6E-507",
        "source": "Bangalore",
        "destination": "Delhi",
        "departure_time": "03:30 PM",
        "arrival_time": "06:15 PM",
        "economy_price": 5300,
        "premium_economy_price": 7300,
        "business_price": 10800,
        "available_seats": 160
    },

    # Mumbai → Hyderabad
    {
        "airline": "IndiGo",
        "flight_number": "6E-5201",
        "source": "Mumbai",
        "destination": "Hyderabad",
        "departure_time": "07:30 AM",
        "arrival_time": "09:00 AM",
        "economy_price": 3200,
        "premium_economy_price": 4800,
        "business_price": 7500,
        "available_seats": 180
    },

    # Hyderabad → Mumbai
    {
        "airline": "Akasa Air",
        "flight_number": "QP-1405",
        "source": "Hyderabad",
        "destination": "Mumbai",
        "departure_time": "05:30 PM",
        "arrival_time": "07:00 PM",
        "economy_price": 3400,
        "premium_economy_price": 5000,
        "business_price": 7800,
        "available_seats": 170
    },

    # Delhi → Kolkata
    {
        "airline": "IndiGo",
        "flight_number": "6E-2215",
        "source": "Delhi",
        "destination": "Kolkata",
        "departure_time": "06:45 AM",
        "arrival_time": "09:00 AM",
        "economy_price": 4200,
        "premium_economy_price": 6200,
        "business_price": 9200,
        "available_seats": 165
    },

    # Kolkata → Delhi
    {
        "airline": "Air India",
        "flight_number": "AI-762",
        "source": "Kolkata",
        "destination": "Delhi",
        "departure_time": "04:00 PM",
        "arrival_time": "06:20 PM",
        "economy_price": 4500,
        "premium_economy_price": 6500,
        "business_price": 9500,
        "available_seats": 150
    },

    # Mumbai → Chennai
    {
        "airline": "IndiGo",
        "flight_number": "6E-5304",
        "source": "Mumbai",
        "destination": "Chennai",
        "departure_time": "10:00 AM",
        "arrival_time": "12:00 PM",
        "economy_price": 4100,
        "premium_economy_price": 6000,
        "business_price": 9000,
        "available_seats": 175
    },

    # Chennai → Mumbai
    {
        "airline": "Air India",
        "flight_number": "AI-572",
        "source": "Chennai",
        "destination": "Mumbai",
        "departure_time": "01:30 PM",
        "arrival_time": "03:30 PM",
        "economy_price": 4300,
        "premium_economy_price": 6300,
        "business_price": 9300,
        "available_seats": 160
    },

    # Delhi → Goa
    {
        "airline": "IndiGo",
        "flight_number": "6E-2347",
        "source": "Delhi",
        "destination": "Goa",
        "departure_time": "07:15 AM",
        "arrival_time": "10:00 AM",
        "economy_price": 4800,
        "premium_economy_price": 6800,
        "business_price": 10000,
        "available_seats": 165
    },

    # Mumbai → Goa
    {
        "airline": "Akasa Air",
        "flight_number": "QP-1630",
        "source": "Mumbai",
        "destination": "Goa",
        "departure_time": "08:30 AM",
        "arrival_time": "09:40 AM",
        "economy_price": 2800,
        "premium_economy_price": 4200,
        "business_price": 6500,
        "available_seats": 180
    },

    # Goa → Mumbai
    {
        "airline": "IndiGo",
        "flight_number": "6E-5231",
        "source": "Goa",
        "destination": "Mumbai",
        "departure_time": "06:00 PM",
        "arrival_time": "07:10 PM",
        "economy_price": 2900,
        "premium_economy_price": 4300,
        "business_price": 6600,
        "available_seats": 175
    },

    # Bangalore → Hyderabad
    {
        "airline": "IndiGo",
        "flight_number": "6E-6923",
        "source": "Bangalore",
        "destination": "Hyderabad",
        "departure_time": "08:00 AM",
        "arrival_time": "09:10 AM",
        "economy_price": 2600,
        "premium_economy_price": 4000,
        "business_price": 6200,
        "available_seats": 180
    },

    # Hyderabad → Bangalore
    {
        "airline": "Akasa Air",
        "flight_number": "QP-1410",
        "source": "Hyderabad",
        "destination": "Bangalore",
        "departure_time": "07:00 PM",
        "arrival_time": "08:10 PM",
        "economy_price": 2700,
        "premium_economy_price": 4100,
        "business_price": 6300,
        "available_seats": 175
    },

    # Delhi → Hyderabad
    {
        "airline": "IndiGo",
        "flight_number": "6E-6201",
        "source": "Delhi",
        "destination": "Hyderabad",
        "departure_time": "10:30 AM",
        "arrival_time": "12:45 PM",
        "economy_price": 4400,
        "premium_economy_price": 6400,
        "business_price": 9400,
        "available_seats": 165
    },

    # Hyderabad → Delhi
    {
        "airline": "Air India",
        "flight_number": "AI-542",
        "source": "Hyderabad",
        "destination": "Delhi",
        "departure_time": "03:00 PM",
        "arrival_time": "05:20 PM",
        "economy_price": 4600,
        "premium_economy_price": 6600,
        "business_price": 9600,
        "available_seats": 155
    }
]


def seed_flights():

    db = SessionLocal()

    try:

        added = 0
        skipped = 0

        for data in flights:

            existing = db.query(Flight).filter(
                Flight.flight_number == data["flight_number"]
            ).first()

            if existing:
                skipped += 1
                continue

            flight = Flight(**data)

            db.add(flight)
            added += 1

        db.commit()

        total = db.query(Flight).count()

        print("=" * 50)
        print("FLIGHT SEEDING COMPLETED")
        print("=" * 50)
        print(f"Flights added : {added}")
        print(f"Flights skipped : {skipped}")
        print(f"Total in DB : {total}")
        print("=" * 50)

    finally:
        db.close()


if __name__ == "__main__":
    seed_flights()