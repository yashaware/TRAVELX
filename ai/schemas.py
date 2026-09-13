from pydantic import BaseModel, Field


class TripPlanRequest(BaseModel):
    destination: str = Field(min_length=2, max_length=100)
    days: int = Field(default=3, ge=1, le=30)
    budget: int = Field(default=10000, ge=1000)
    travel_style: str = Field(default="Standard", min_length=2, max_length=30)
    interests: str = Field(
        default="Sightseeing, food, local experiences",
        max_length=500
    )
    travelers: int = Field(default=1, ge=1, le=20)
    starting_city: str = Field(default="", max_length=100)


class TripDay(BaseModel):
    day: int
    title: str
    morning: str
    afternoon: str
    evening: str
    estimated_cost: int


class TripPlanResponse(BaseModel):
    destination: str
    days: int
    budget: int
    travel_style: str
    travelers: int
    estimated_total: int
    budget_status: str
    summary: str
    transport: list[str]
    accommodation: list[str]
    food: list[str]
    tips: list[str]
    itinerary: list[TripDay]
    ai_powered: bool