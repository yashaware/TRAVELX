from db.database import SessionLocal, engine, Base
from db.models import Cab


# Create tables
Base.metadata.create_all(bind=engine)


def seed_cabs():

    db = SessionLocal()

    try:

        # Don't duplicate data
        if db.query(Cab).count() > 0:

            print("Cabs already exist.")

            return

        cabs = [

            Cab(
                driver_name="Rajesh Kumar",
                vehicle_number="MH12AB1234",
                cab_type="Mini",
                source="Mumbai",
                destination="Pune",
                fare_per_km=12,
                available_seats=4,
                rating=4.5
            ),

            Cab(
                driver_name="Amit Sharma",
                vehicle_number="MH14CD5678",
                cab_type="Sedan",
                source="Mumbai",
                destination="Pune",
                fare_per_km=16,
                available_seats=4,
                rating=4.7
            ),

            Cab(
                driver_name="Suresh Patil",
                vehicle_number="MH12EF9012",
                cab_type="SUV",
                source="Mumbai",
                destination="Pune",
                fare_per_km=22,
                available_seats=6,
                rating=4.8
            ),

            Cab(
                driver_name="Vikas Singh",
                vehicle_number="DL01GH3456",
                cab_type="Mini",
                source="Delhi",
                destination="Agra",
                fare_per_km=13,
                available_seats=4,
                rating=4.4
            ),

            Cab(
                driver_name="Rohit Verma",
                vehicle_number="DL02IJ7890",
                cab_type="Sedan",
                source="Delhi",
                destination="Agra",
                fare_per_km=17,
                available_seats=4,
                rating=4.6
            ),

            Cab(
                driver_name="Arjun Mehta",
                vehicle_number="KA01KL1122",
                cab_type="SUV",
                source="Bangalore",
                destination="Mysore",
                fare_per_km=20,
                available_seats=6,
                rating=4.8
            ),

            Cab(
                driver_name="Manoj Rao",
                vehicle_number="KA05MN3344",
                cab_type="Sedan",
                source="Bangalore",
                destination="Mysore",
                fare_per_km=15,
                available_seats=4,
                rating=4.5
            ),

            Cab(
                driver_name="Prakash Yadav",
                vehicle_number="TS09OP5566",
                cab_type="Mini",
                source="Hyderabad",
                destination="Warangal",
                fare_per_km=12,
                available_seats=4,
                rating=4.3
            ),

            Cab(
                driver_name="Kiran Reddy",
                vehicle_number="TS10QR7788",
                cab_type="SUV",
                source="Hyderabad",
                destination="Warangal",
                fare_per_km=21,
                available_seats=6,
                rating=4.7
            ),

            Cab(
                driver_name="Nitin Joshi",
                vehicle_number="GJ01ST9900",
                cab_type="Sedan",
                source="Ahmedabad",
                destination="Vadodara",
                fare_per_km=15,
                available_seats=4,
                rating=4.6
            )

        ]

        db.add_all(cabs)

        db.commit()

        print("✅ Cab seed data inserted successfully!")

    finally:

        db.close()


if __name__ == "__main__":
    seed_cabs()