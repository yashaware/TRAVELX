from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import (
    Restaurant,
    FoodItem,
    FoodOrder,
    FoodOrderItem,
    Wallet,
    WalletTransaction
)

from food.schemas import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantSearch,
    FoodItemCreate,
    FoodItemResponse,
    FoodOrderCreate,
    FoodOrderResponse,
    FoodOrderItemResponse
)

from auth.security import get_current_user


food_router = APIRouter(
    prefix="/food",
    tags=["Food"]
)


# =========================================================
# RESTAURANTS
# =========================================================

@food_router.get(
    "/restaurants",
    response_model=list[RestaurantResponse]
)
def get_all_restaurants(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Restaurant).order_by(Restaurant.rating.desc()).all()


@food_router.post(
    "/restaurants",
    response_model=RestaurantResponse
)
def create_restaurant(
    restaurant_data: RestaurantCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    restaurant = Restaurant(
        name=restaurant_data.name,
        city=restaurant_data.city,
        address=restaurant_data.address,
        cuisine=restaurant_data.cuisine,
        description=restaurant_data.description,
        rating=restaurant_data.rating,
        delivery_time=restaurant_data.delivery_time,
        is_open=restaurant_data.is_open
    )

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return restaurant


@food_router.post(
    "/restaurants/search",
    response_model=list[RestaurantResponse]
)
def search_restaurants(
    search_data: RestaurantSearch,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    city = search_data.city.strip()

    restaurants = db.query(Restaurant).filter(
        Restaurant.city.ilike(city)
    ).order_by(
        Restaurant.rating.desc()
    ).all()

    return restaurants


@food_router.get(
    "/restaurants/{restaurant_id}",
    response_model=RestaurantResponse
)
def get_restaurant(
    restaurant_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found."
        )

    return restaurant


# =========================================================
# FOOD MENU
# =========================================================

@food_router.post(
    "/menu",
    response_model=FoodItemResponse
)
def create_food_item(
    food_data: FoodItemCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == food_data.restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found."
        )

    food_item = FoodItem(
        restaurant_id=food_data.restaurant_id,
        name=food_data.name,
        category=food_data.category,
        description=food_data.description,
        price=food_data.price,
        is_available=food_data.is_available
    )

    db.add(food_item)
    db.commit()
    db.refresh(food_item)

    return food_item


@food_router.get(
    "/menu/{restaurant_id}",
    response_model=list[FoodItemResponse]
)
def get_restaurant_menu(
    restaurant_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found."
        )

    menu = db.query(FoodItem).filter(
        FoodItem.restaurant_id == restaurant_id
    ).order_by(
        FoodItem.category,
        FoodItem.id
    ).all()

    return menu


# =========================================================
# FOOD ORDERS
# =========================================================

@food_router.post(
    "/orders",
    response_model=FoodOrderResponse
)
def create_food_order(
    order_data: FoodOrderCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # Check restaurant
    # -----------------------------------------------------

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == order_data.restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found."
        )

    if not restaurant.is_open:
        raise HTTPException(
            status_code=400,
            detail="Restaurant is currently closed."
        )

    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty."
        )

    # -----------------------------------------------------
    # Calculate total
    # -----------------------------------------------------

    total_price = 0
    order_items_data = []

    for item_data in order_data.items:

        food_item = db.query(FoodItem).filter(
            FoodItem.id == item_data.food_item_id,
            FoodItem.restaurant_id == order_data.restaurant_id
        ).first()

        if not food_item:
            raise HTTPException(
                status_code=404,
                detail=f"Food item {item_data.food_item_id} not found."
            )

        if not food_item.is_available:
            raise HTTPException(
                status_code=400,
                detail=f"{food_item.name} is currently unavailable."
            )

        subtotal = food_item.price * item_data.quantity

        total_price += subtotal

        order_items_data.append({
            "food_item_id": food_item.id,
            "item_name": food_item.name,
            "quantity": item_data.quantity,
            "price": food_item.price,
            "subtotal": subtotal
        })

    # -----------------------------------------------------
    # Payment
    # -----------------------------------------------------

    payment_method = order_data.payment_method.strip().lower()

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
            description=f"Food order - {restaurant.name}",
            balance_after=wallet.balance
        )

        db.add(transaction)

    # -----------------------------------------------------
    # Create order
    # -----------------------------------------------------

    order = FoodOrder(
        user_id=current_user["id"],
        restaurant_id=restaurant.id,
        customer_name=order_data.customer_name,
        customer_phone=order_data.customer_phone,
        delivery_address=order_data.delivery_address,
        total_price=total_price,
        payment_method=payment_method,
        order_status="confirmed"
    )

    db.add(order)
    db.flush()

    # -----------------------------------------------------
    # Create order items
    # -----------------------------------------------------

    for item in order_items_data:

        order_item = FoodOrderItem(
            order_id=order.id,
            food_item_id=item["food_item_id"],
            item_name=item["item_name"],
            quantity=item["quantity"],
            price=item["price"],
            subtotal=item["subtotal"]
        )

        db.add(order_item)

    db.commit()
    db.refresh(order)

    # -----------------------------------------------------
    # Return order with items
    # -----------------------------------------------------

    items = db.query(FoodOrderItem).filter(
        FoodOrderItem.order_id == order.id
    ).all()

    return FoodOrderResponse(
        id=order.id,
        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        delivery_address=order.delivery_address,
        total_price=order.total_price,
        payment_method=order.payment_method,
        order_status=order.order_status,
        items=[
            FoodOrderItemResponse(
                id=item.id,
                food_item_id=item.food_item_id,
                item_name=item.item_name,
                quantity=item.quantity,
                price=item.price,
                subtotal=item.subtotal
            )
            for item in items
        ]
    )


# =========================================================
# MY FOOD ORDERS
# =========================================================

@food_router.get(
    "/my-orders",
    response_model=list[FoodOrderResponse]
)
def get_my_food_orders(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(FoodOrder).filter(
        FoodOrder.user_id == current_user["id"]
    ).order_by(
        FoodOrder.id.desc()
    ).all()

    result = []

    for order in orders:

        items = db.query(FoodOrderItem).filter(
            FoodOrderItem.order_id == order.id
        ).all()

        result.append(
            FoodOrderResponse(
                id=order.id,
                user_id=order.user_id,
                restaurant_id=order.restaurant_id,
                customer_name=order.customer_name,
                customer_phone=order.customer_phone,
                delivery_address=order.delivery_address,
                total_price=order.total_price,
                payment_method=order.payment_method,
                order_status=order.order_status,
                items=[
                    FoodOrderItemResponse(
                        id=item.id,
                        food_item_id=item.food_item_id,
                        item_name=item.item_name,
                        quantity=item.quantity,
                        price=item.price,
                        subtotal=item.subtotal
                    )
                    for item in items
                ]
            )
        )

    return result


# =========================================================
# SINGLE ORDER
# =========================================================

@food_router.get(
    "/orders/{order_id}",
    response_model=FoodOrderResponse
)
def get_food_order(
    order_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(FoodOrder).filter(
        FoodOrder.id == order_id,
        FoodOrder.user_id == current_user["id"]
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Food order not found."
        )

    items = db.query(FoodOrderItem).filter(
        FoodOrderItem.order_id == order.id
    ).all()

    return FoodOrderResponse(
        id=order.id,
        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        delivery_address=order.delivery_address,
        total_price=order.total_price,
        payment_method=order.payment_method,
        order_status=order.order_status,
        items=[
            FoodOrderItemResponse(
                id=item.id,
                food_item_id=item.food_item_id,
                item_name=item.item_name,
                quantity=item.quantity,
                price=item.price,
                subtotal=item.subtotal
            )
            for item in items
        ]
    )