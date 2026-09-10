from pydantic import BaseModel, Field


# =========================
# RESTAURANT SCHEMAS
# =========================

class RestaurantCreate(BaseModel):
    name: str
    city: str
    address: str
    cuisine: str
    description: str = ""
    rating: float = Field(default=0.0, ge=0, le=5)
    delivery_time: int = Field(default=30, gt=0)
    is_open: bool = True


class RestaurantResponse(BaseModel):
    id: int
    name: str
    city: str
    address: str
    cuisine: str
    description: str
    rating: float
    delivery_time: int
    is_open: bool


class RestaurantSearch(BaseModel):
    city: str


# =========================
# FOOD ITEM SCHEMAS
# =========================

class FoodItemCreate(BaseModel):
    restaurant_id: int
    name: str
    category: str
    description: str = ""
    price: int = Field(gt=0)
    is_available: bool = True


class FoodItemResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str
    category: str
    description: str
    price: int
    is_available: bool


# =========================
# FOOD ORDER SCHEMAS
# =========================

class FoodOrderItemCreate(BaseModel):
    food_item_id: int
    quantity: int = Field(gt=0)


class FoodOrderCreate(BaseModel):
    restaurant_id: int

    customer_name: str
    customer_phone: str

    delivery_address: str

    items: list[FoodOrderItemCreate]

    payment_method: str = "demo"


class FoodOrderItemResponse(BaseModel):
    id: int
    food_item_id: int
    item_name: str
    quantity: int
    price: int
    subtotal: int


class FoodOrderResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int

    customer_name: str
    customer_phone: str

    delivery_address: str

    total_price: int

    payment_method: str
    order_status: str

    items: list[FoodOrderItemResponse] = []