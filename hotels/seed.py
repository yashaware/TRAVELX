from db.database import SessionLocal
from db.models import Hotel


hotels = [

    # =========================
    # MUMBAI
    # =========================

    {
        "name": "TRAVELX Grand Hotel",
        "city": "Mumbai",
        "address": "Marine Drive, Mumbai",
        "description": "Premium hotel with comfortable rooms and modern facilities.",
        "rating": 4.5,
        "price_per_night": 3500,
        "available_rooms": 20,
        "amenities": "WiFi, Breakfast, Parking, AC, Swimming Pool"
    },

    {
        "name": "Mumbai City Palace",
        "city": "Mumbai",
        "address": "Colaba, Mumbai",
        "description": "Luxury hotel near major Mumbai attractions.",
        "rating": 4.6,
        "price_per_night": 4800,
        "available_rooms": 15,
        "amenities": "WiFi, Breakfast, AC, Pool, Restaurant, Gym"
    },

    {
        "name": "Mumbai Comfort Inn",
        "city": "Mumbai",
        "address": "Andheri East, Mumbai",
        "description": "Affordable and comfortable stay for business travellers.",
        "rating": 4.0,
        "price_per_night": 2100,
        "available_rooms": 30,
        "amenities": "WiFi, AC, Parking, Restaurant"
    },


    # =========================
    # PUNE
    # =========================

    {
        "name": "TRAVELX Royal Palace",
        "city": "Pune",
        "address": "Koregaon Park, Pune",
        "description": "Luxury stay in the heart of Pune.",
        "rating": 4.3,
        "price_per_night": 2800,
        "available_rooms": 15,
        "amenities": "WiFi, Breakfast, Parking, AC"
    },

    {
        "name": "Pune Grand Residency",
        "city": "Pune",
        "address": "Shivajinagar, Pune",
        "description": "Modern hotel with spacious rooms.",
        "rating": 4.4,
        "price_per_night": 3200,
        "available_rooms": 18,
        "amenities": "WiFi, AC, Breakfast, Gym, Restaurant"
    },

    {
        "name": "Pune Budget Stay",
        "city": "Pune",
        "address": "Hinjewadi, Pune",
        "description": "Affordable hotel suitable for business and leisure.",
        "rating": 4.0,
        "price_per_night": 1700,
        "available_rooms": 25,
        "amenities": "WiFi, AC, Parking"
    },


    # =========================
    # DELHI
    # =========================

    {
        "name": "TRAVELX City Inn",
        "city": "Delhi",
        "address": "Connaught Place, Delhi",
        "description": "Comfortable and affordable city hotel.",
        "rating": 4.1,
        "price_per_night": 2200,
        "available_rooms": 25,
        "amenities": "WiFi, AC, Restaurant"
    },

    {
        "name": "Delhi Royal Residency",
        "city": "Delhi",
        "address": "Aerocity, Delhi",
        "description": "Premium hotel near Delhi airport.",
        "rating": 4.6,
        "price_per_night": 4200,
        "available_rooms": 20,
        "amenities": "WiFi, Breakfast, Pool, AC, Gym, Airport Shuttle"
    },

    {
        "name": "Delhi Comfort Hotel",
        "city": "Delhi",
        "address": "Karol Bagh, Delhi",
        "description": "Affordable hotel in central Delhi.",
        "rating": 4.0,
        "price_per_night": 1800,
        "available_rooms": 30,
        "amenities": "WiFi, AC, Parking, Restaurant"
    },


    # =========================
    # HYDERABAD
    # =========================

    {
        "name": "TRAVELX Hyderabad Palace",
        "city": "Hyderabad",
        "address": "Banjara Hills, Hyderabad",
        "description": "Modern hotel with premium rooms and excellent service.",
        "rating": 4.4,
        "price_per_night": 3000,
        "available_rooms": 18,
        "amenities": "WiFi, Breakfast, Parking, AC, Gym"
    },

    {
        "name": "Hyderabad Lake View",
        "city": "Hyderabad",
        "address": "Hussain Sagar, Hyderabad",
        "description": "Beautiful hotel with excellent city views.",
        "rating": 4.5,
        "price_per_night": 3600,
        "available_rooms": 16,
        "amenities": "WiFi, AC, Pool, Restaurant, Breakfast"
    },

    {
        "name": "Hyderabad Budget Inn",
        "city": "Hyderabad",
        "address": "Ameerpet, Hyderabad",
        "description": "Budget-friendly hotel for travellers.",
        "rating": 4.0,
        "price_per_night": 1600,
        "available_rooms": 28,
        "amenities": "WiFi, AC, Parking"
    },


    # =========================
    # BENGALURU
    # =========================

    {
        "name": "TRAVELX Bangalore Suites",
        "city": "Bengaluru",
        "address": "MG Road, Bengaluru",
        "description": "Comfortable business and leisure hotel.",
        "rating": 4.6,
        "price_per_night": 3200,
        "available_rooms": 22,
        "amenities": "WiFi, Breakfast, AC, Gym, Restaurant"
    },

    {
        "name": "Bangalore Tech Residency",
        "city": "Bengaluru",
        "address": "Whitefield, Bengaluru",
        "description": "Modern hotel close to Bengaluru IT hubs.",
        "rating": 4.4,
        "price_per_night": 2900,
        "available_rooms": 20,
        "amenities": "WiFi, Breakfast, AC, Gym, Parking"
    },

    {
        "name": "Bangalore Budget Hotel",
        "city": "Bengaluru",
        "address": "Electronic City, Bengaluru",
        "description": "Affordable stay for business travellers.",
        "rating": 4.0,
        "price_per_night": 1800,
        "available_rooms": 32,
        "amenities": "WiFi, AC, Parking"
    },


    # =========================
    # GOA
    # =========================

    {
        "name": "TRAVELX Beach Resort",
        "city": "Goa",
        "address": "Calangute Beach, Goa",
        "description": "Beautiful beach resort perfect for vacations.",
        "rating": 4.7,
        "price_per_night": 4500,
        "available_rooms": 30,
        "amenities": "WiFi, Breakfast, Pool, Beach Access, AC"
    },

    {
        "name": "Goa Paradise Resort",
        "city": "Goa",
        "address": "Baga Beach, Goa",
        "description": "Premium resort near Baga Beach.",
        "rating": 4.8,
        "price_per_night": 5200,
        "available_rooms": 18,
        "amenities": "WiFi, Pool, Breakfast, Beach Access, Restaurant, Bar"
    },

    {
        "name": "Goa Budget Stay",
        "city": "Goa",
        "address": "Anjuna, Goa",
        "description": "Affordable stay close to popular beaches.",
        "rating": 4.2,
        "price_per_night": 1900,
        "available_rooms": 25,
        "amenities": "WiFi, AC, Parking, Breakfast"
    },


    # =========================
    # JAIPUR
    # =========================

    {
        "name": "TRAVELX Heritage Hotel",
        "city": "Jaipur",
        "address": "MI Road, Jaipur",
        "description": "Traditional Rajasthani style hotel with modern facilities.",
        "rating": 4.5,
        "price_per_night": 2600,
        "available_rooms": 20,
        "amenities": "WiFi, Breakfast, Parking, AC, Restaurant"
    },

    {
        "name": "Jaipur Royal Palace",
        "city": "Jaipur",
        "address": "Amer Road, Jaipur",
        "description": "Royal style hotel near historic attractions.",
        "rating": 4.7,
        "price_per_night": 3900,
        "available_rooms": 14,
        "amenities": "WiFi, Pool, Breakfast, AC, Restaurant, Parking"
    },


    # =========================
    # CHENNAI
    # =========================

    {
        "name": "TRAVELX Marina Hotel",
        "city": "Chennai",
        "address": "Marina Beach Road, Chennai",
        "description": "Modern hotel close to major attractions.",
        "rating": 4.2,
        "price_per_night": 2400,
        "available_rooms": 24,
        "amenities": "WiFi, Breakfast, Parking, AC"
    },

    {
        "name": "Chennai Grand Residency",
        "city": "Chennai",
        "address": "T Nagar, Chennai",
        "description": "Premium city hotel with modern facilities.",
        "rating": 4.5,
        "price_per_night": 3300,
        "available_rooms": 20,
        "amenities": "WiFi, AC, Breakfast, Gym, Restaurant"
    },


    # =========================
    # KOLKATA
    # =========================

    {
        "name": "TRAVELX Kolkata Residency",
        "city": "Kolkata",
        "address": "Park Street, Kolkata",
        "description": "Comfortable city hotel with excellent dining options.",
        "rating": 4.3,
        "price_per_night": 2300,
        "available_rooms": 19,
        "amenities": "WiFi, Restaurant, Breakfast, AC"
    },

    {
        "name": "Kolkata Royal Hotel",
        "city": "Kolkata",
        "address": "Salt Lake, Kolkata",
        "description": "Modern hotel for business and leisure travellers.",
        "rating": 4.4,
        "price_per_night": 2900,
        "available_rooms": 21,
        "amenities": "WiFi, AC, Gym, Breakfast, Parking"
    },


    # =========================
    # AHMEDABAD
    # =========================

    {
        "name": "TRAVELX Ahmedabad Inn",
        "city": "Ahmedabad",
        "address": "Navrangpura, Ahmedabad",
        "description": "Affordable and comfortable hotel for business and leisure.",
        "rating": 4.0,
        "price_per_night": 1900,
        "available_rooms": 28,
        "amenities": "WiFi, Breakfast, Parking, AC"
    },

    {
        "name": "Ahmedabad Grand Hotel",
        "city": "Ahmedabad",
        "address": "SG Highway, Ahmedabad",
        "description": "Premium hotel with modern facilities.",
        "rating": 4.5,
        "price_per_night": 3100,
        "available_rooms": 20,
        "amenities": "WiFi, Pool, Breakfast, AC, Gym"
    },


    # =========================
    # AGRA
    # =========================

    {
        "name": "TRAVELX Taj View Hotel",
        "city": "Agra",
        "address": "Taj East Gate Road, Agra",
        "description": "Comfortable hotel near the Taj Mahal.",
        "rating": 4.6,
        "price_per_night": 2800,
        "available_rooms": 18,
        "amenities": "WiFi, Breakfast, AC, Restaurant, Parking"
    },

    {
        "name": "Agra Heritage Inn",
        "city": "Agra",
        "address": "Fatehabad Road, Agra",
        "description": "Affordable heritage-style hotel.",
        "rating": 4.1,
        "price_per_night": 1700,
        "available_rooms": 25,
        "amenities": "WiFi, AC, Restaurant"
    },


    # =========================
    # VARANASI
    # =========================

    {
        "name": "TRAVELX Ganga View",
        "city": "Varanasi",
        "address": "Assi Ghat, Varanasi",
        "description": "Beautiful stay near the Ganges.",
        "rating": 4.5,
        "price_per_night": 2500,
        "available_rooms": 16,
        "amenities": "WiFi, Breakfast, AC, Restaurant"
    },

    {
        "name": "Varanasi Heritage Stay",
        "city": "Varanasi",
        "address": "Godowlia, Varanasi",
        "description": "Traditional hotel close to famous ghats.",
        "rating": 4.2,
        "price_per_night": 1800,
        "available_rooms": 22,
        "amenities": "WiFi, AC, Breakfast"
    },


    # =========================
    # UDAIPUR
    # =========================

    {
        "name": "TRAVELX Lake Palace",
        "city": "Udaipur",
        "address": "Lake Pichola, Udaipur",
        "description": "Luxury stay with beautiful lake views.",
        "rating": 4.8,
        "price_per_night": 5500,
        "available_rooms": 12,
        "amenities": "WiFi, Pool, Breakfast, AC, Restaurant, Lake View"
    },

    {
        "name": "Udaipur Heritage Resort",
        "city": "Udaipur",
        "address": "Old City, Udaipur",
        "description": "Traditional Rajasthani hotel.",
        "rating": 4.5,
        "price_per_night": 3000,
        "available_rooms": 18,
        "amenities": "WiFi, Breakfast, AC, Restaurant"
    },


    # =========================
    # MANALI
    # =========================

    {
        "name": "TRAVELX Mountain Resort",
        "city": "Manali",
        "address": "Mall Road, Manali",
        "description": "Beautiful mountain resort for vacation stays.",
        "rating": 4.6,
        "price_per_night": 3200,
        "available_rooms": 20,
        "amenities": "WiFi, Breakfast, Parking, Heater, Restaurant"
    },

    {
        "name": "Manali Snow View Hotel",
        "city": "Manali",
        "address": "Old Manali, Manali",
        "description": "Cozy hotel with mountain views.",
        "rating": 4.4,
        "price_per_night": 2600,
        "available_rooms": 17,
        "amenities": "WiFi, Breakfast, Heater, Parking"
    },


    # =========================
    # SHIMLA
    # =========================

    {
        "name": "TRAVELX Shimla Heights",
        "city": "Shimla",
        "address": "Mall Road, Shimla",
        "description": "Premium hill hotel with scenic views.",
        "rating": 4.6,
        "price_per_night": 3400,
        "available_rooms": 18,
        "amenities": "WiFi, Breakfast, Heater, Restaurant, Parking"
    },

    {
        "name": "Shimla Valley Inn",
        "city": "Shimla",
        "address": "Chotta Shimla, Shimla",
        "description": "Comfortable and affordable hill stay.",
        "rating": 4.2,
        "price_per_night": 2200,
        "available_rooms": 24,
        "amenities": "WiFi, Breakfast, Heater"
    },


    # =========================
    # RISHIKESH
    # =========================

    {
        "name": "TRAVELX Ganga Retreat",
        "city": "Rishikesh",
        "address": "Tapovan, Rishikesh",
        "description": "Peaceful stay near the Ganges and adventure activities.",
        "rating": 4.5,
        "price_per_night": 2400,
        "available_rooms": 20,
        "amenities": "WiFi, Breakfast, AC, Restaurant, Parking"
    },

    {
        "name": "Rishikesh Riverside Resort",
        "city": "Rishikesh",
        "address": "Laxman Jhula, Rishikesh",
        "description": "Relaxing riverside resort.",
        "rating": 4.6,
        "price_per_night": 3500,
        "available_rooms": 15,
        "amenities": "WiFi, Breakfast, Pool, Restaurant, River View"
    }

]


# ============================================================
# INSERT HOTELS INTO DATABASE
# ============================================================

def seed_hotels():

    db = SessionLocal()

    try:

        added = 0
        skipped = 0

        for hotel_data in hotels:

            # Check if hotel already exists
            existing_hotel = db.query(
                Hotel
            ).filter(
                Hotel.name == hotel_data["name"],
                Hotel.city == hotel_data["city"]
            ).first()

            if existing_hotel:

                skipped += 1
                continue


            hotel = Hotel(
                name=hotel_data["name"],
                city=hotel_data["city"],
                address=hotel_data["address"],
                description=hotel_data["description"],
                rating=hotel_data["rating"],
                price_per_night=hotel_data["price_per_night"],
                available_rooms=hotel_data["available_rooms"],
                amenities=hotel_data["amenities"]
            )

            db.add(hotel)

            added += 1


        db.commit()

        print("=" * 60)
        print("TRAVELX HOTEL DATABASE")
        print("=" * 60)

        print(f"Hotels added   : {added}")
        print(f"Hotels skipped  : {skipped}")
        print(f"Total provided  : {len(hotels)}")

        total_hotels = db.query(Hotel).count()

        print(f"Total in DB     : {total_hotels}")

        print("=" * 60)
        print("Hotel seeding completed successfully!")
        print("=" * 60)


    except Exception as e:

        db.rollback()

        print("Error while seeding hotels:")
        print(e)


    finally:

        db.close()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    seed_hotels()