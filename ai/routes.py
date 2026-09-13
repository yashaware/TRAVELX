import os

from fastapi import APIRouter, Depends, HTTPException

from ai.schemas import (
    TripPlanRequest,
    TripPlanResponse
)

from ai.service import (
    generate_fallback,
    generate_with_gemini
)

from auth.security import get_current_user


ai_router = APIRouter(
    prefix="/ai",
    tags=["AI Trip Planner"]
)


@ai_router.get("/health")
def ai_health(
    current_user=Depends(get_current_user)
):

    return {
        "status": "ready",
        "gemini_configured": bool(
            os.getenv("GEMINI_API_KEY")
        )
    }


@ai_router.post(
    "/trip-plan",
    response_model=TripPlanResponse
)
def create_trip_plan(
    request: TripPlanRequest,
    current_user=Depends(get_current_user)
):

    try:

        result = generate_with_gemini(
            request
        )

        ai_powered = result is not None

        if result is None:

            result = generate_fallback(
                request
            )

        result["destination"] = (
            request.destination.strip()
        )

        result["days"] = request.days

        result["budget"] = request.budget

        result["travel_style"] = (
            request.travel_style.strip()
        )

        result["travelers"] = request.travelers

        result["ai_powered"] = ai_powered

        result.setdefault(
            "estimated_total",
            request.budget
        )

        result.setdefault(
            "budget_status",
            "Within budget"
        )

        result.setdefault(
            "summary",
            "Your TRAVELX trip plan is ready."
        )

        result.setdefault(
            "transport",
            []
        )

        result.setdefault(
            "accommodation",
            []
        )

        result.setdefault(
            "food",
            []
        )

        result.setdefault(
            "tips",
            []
        )

        result.setdefault(
            "itinerary",
            []
        )

        return result

    except Exception as exc:

        try:

            fallback = generate_fallback(
                request
            )

            fallback.update(
                {
                    "destination":
                        request.destination.strip(),

                    "days":
                        request.days,

                    "budget":
                        request.budget,

                    "travel_style":
                        request.travel_style.strip(),

                    "travelers":
                        request.travelers,

                    "ai_powered":
                        False,
                }
            )

            return fallback

        except Exception:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Unable to generate the "
                    "trip plan right now."
                )
            ) from exc