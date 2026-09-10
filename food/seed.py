from db.database import SessionLocal, engine, Base
from db.models import Restaurant, FoodItem


Base.metadata.create_all(bind=engine)


def seed_food():

    db = SessionLocal()

    try:

        if db.query(Restaurant).count() > 0:
            print("Food data already exists.")
            return

        # =====================================================
        # RESTAURANTS
        # =====================================================

        restaurants = [

            Restaurant(
                name="Spice Garden",
                city="Mumbai",
                address="Andheri West, Mumbai",
                cuisine="North Indian",
                description="Authentic Indian meals, biryani and delicious curries.",
                rating=4.6,
                delivery_time=30,
                is_open=True
            ),

            Restaurant(
                name="Pizza Paradise",
                city="Mumbai",
                address="Bandra West, Mumbai",
                cuisine="Pizza, Italian",
                description="Fresh cheesy pizzas and Italian favourites.",
                rating=4.5,
                delivery_time=35,
                is_open=True
            ),

            Restaurant(
                name="Burger Hub",
                city="Delhi",
                address="Connaught Place, Delhi",
                cuisine="Burgers, Fast Food",
                description="Juicy burgers, fries and refreshing beverages.",
                rating=4.4,
                delivery_time=25,
                is_open=True
            ),

            Restaurant(
                name="Royal Biryani House",
                city="Hyderabad",
                address="Banjara Hills, Hyderabad",
                cuisine="Biryani, Indian",
                description="Authentic Hyderabadi biryani and traditional dishes.",
                rating=4.8,
                delivery_time=30,
                is_open=True
            ),

            Restaurant(
                name="South Indian Delight",
                city="Bangalore",
                address="Indiranagar, Bangalore",
                cuisine="South Indian",
                description="Fresh dosa, idli, vada and traditional South Indian meals.",
                rating=4.7,
                delivery_time=25,
                is_open=True
            ),

            Restaurant(
                name="Cafe Coffee Corner",
                city="Pune",
                address="Koregaon Park, Pune",
                cuisine="Cafe, Beverages",
                description="Coffee, sandwiches, desserts and snacks.",
                rating=4.3,
                delivery_time=20,
                is_open=True
            )
        ]

        db.add_all(restaurants)
        db.commit()

        # Refresh IDs
        for restaurant in restaurants:
            db.refresh(restaurant)

        # =====================================================
        # FOOD ITEMS
        # =====================================================

        food_items = [

            # -------------------------------------------------
            # SPICE GARDEN - MUMBAI
            # -------------------------------------------------

            FoodItem(
                restaurant_id=restaurants[0].id,
                name="Butter Chicken",
                category="Main Course",
                description="Creamy Indian chicken curry.",
                price=320,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[0].id,
                name="Paneer Butter Masala",
                category="Main Course",
                description="Paneer cooked in rich tomato gravy.",
                price=280,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[0].id,
                name="Chicken Biryani",
                category="Biryani",
                description="Aromatic basmati rice with spicy chicken.",
                price=300,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[0].id,
                name="Garlic Naan",
                category="Bread",
                description="Soft naan topped with garlic and butter.",
                price=80,
                is_available=True
            ),

            # -------------------------------------------------
            # PIZZA PARADISE - MUMBAI
            # -------------------------------------------------

            FoodItem(
                restaurant_id=restaurants[1].id,
                name="Margherita Pizza",
                category="Pizza",
                description="Classic pizza with tomato, mozzarella and basil.",
                price=249,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[1].id,
                name="Farmhouse Pizza",
                category="Pizza",
                description="Loaded with fresh vegetables and cheese.",
                price=349,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[1].id,
                name="Cheese Garlic Bread",
                category="Sides",
                description="Crispy garlic bread loaded with cheese.",
                price=149,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[1].id,
                name="Cold Coffee",
                category="Beverages",
                description="Chilled creamy coffee.",
                price=129,
                is_available=True
            ),

            # -------------------------------------------------
            # BURGER HUB - DELHI
            # -------------------------------------------------

            FoodItem(
                restaurant_id=restaurants[2].id,
                name="Classic Chicken Burger",
                category="Burgers",
                description="Crispy chicken patty with fresh vegetables.",
                price=199,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[2].id,
                name="Veg Cheese Burger",
                category="Burgers",
                description="Crispy veg patty with melted cheese.",
                price=169,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[2].id,
                name="French Fries",
                category="Sides",
                description="Golden crispy French fries.",
                price=99,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[2].id,
                name="Chocolate Shake",
                category="Beverages",
                description="Rich chocolate milkshake.",
                price=149,
                is_available=True
            ),

            # -------------------------------------------------
            # ROYAL BIRYANI HOUSE - HYDERABAD
            # -------------------------------------------------

            FoodItem(
                restaurant_id=restaurants[3].id,
                name="Hyderabadi Chicken Biryani",
                category="Biryani",
                description="Traditional dum-cooked Hyderabadi chicken biryani.",
                price=299,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[3].id,
                name="Mutton Biryani",
                category="Biryani",
                description="Tender mutton cooked with aromatic basmati rice.",
                price=399,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[3].id,
                name="Chicken 65",
                category="Starters",
                description="Spicy crispy South Indian chicken starter.",
                price=249,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[3].id,
                name="Double Ka Meetha",
                category="Dessert",
                description="Traditional Hyderabadi bread dessert.",
                price=129,
                is_available=True
            ),

            # -------------------------------------------------
            # SOUTH INDIAN DELIGHT - BANGALORE
            # -------------------------------------------------

            FoodItem(
                restaurant_id=restaurants[4].id,
                name="Masala Dosa",
                category="Dosa",
                description="Crispy dosa filled with spicy potato masala.",
                price=120,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[4].id,
                name="Idli Sambar",
                category="Breakfast",
                description="Soft idlis served with hot sambar.",
                price=90,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[4].id,
                name="Medu Vada",
                category="Breakfast",
                description="Crispy South Indian lentil fritters.",
                price=100,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[4].id,
                name="Filter Coffee",
                category="Beverages",
                description="Traditional South Indian filter coffee.",
                price=70,
                is_available=True
            ),

            # -------------------------------------------------
            # CAFE COFFEE CORNER - PUNE
            # -------------------------------------------------

            FoodItem(
                restaurant_id=restaurants[5].id,
                name="Cappuccino",
                category="Coffee",
                description="Classic creamy cappuccino.",
                price=140,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[5].id,
                name="Veg Grilled Sandwich",
                category="Sandwich",
                description="Grilled sandwich with fresh vegetables and cheese.",
                price=180,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[5].id,
                name="Chocolate Brownie",
                category="Dessert",
                description="Warm chocolate brownie.",
                price=160,
                is_available=True
            ),

            FoodItem(
                restaurant_id=restaurants[5].id,
                name="Cold Coffee",
                category="Beverages",
                description="Cold and creamy coffee.",
                price=150,
                is_available=True
            )
        ]

        db.add_all(food_items)
        db.commit()

        print("✅ Food restaurants and menu data inserted successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_food()