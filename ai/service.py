import json
import os
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# ---------------------------------------------------------
# Load .env from the TRAVELX project root
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE)

# ---------------------------------------------------------
# Gemini configuration
# ---------------------------------------------------------

try:
    from google import genai
except Exception:
    genai = None


MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

API_KEY = os.getenv("GEMINI_API_KEY")


# ---------------------------------------------------------
# Gemini client
# ---------------------------------------------------------

def get_gemini_client():
    """
    Create and return a Gemini client.

    Returns None if Gemini SDK or API key is unavailable.
    """

    if genai is None:
        return None

    if not API_KEY:
        return None

    try:
        return genai.Client(api_key=API_KEY)
    except Exception:
        return None


# ---------------------------------------------------------
# Extract JSON from Gemini response
# ---------------------------------------------------------

def extract_json(text: str) -> dict[str, Any] | None:
    """
    Convert Gemini text response into a Python dictionary.

    Handles:
    - normal JSON
    - JSON inside ```json ... ```
    - JSON surrounded by extra text
    """

    if not text:
        return None

    text = text.strip()

    # Remove markdown code fences
    if text.startswith("```"):
        lines = text.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    # First attempt: complete JSON
    try:
        result = json.loads(text)

        if isinstance(result, dict):
            return result

    except json.JSONDecodeError:
        pass

    # Second attempt: find JSON object inside response
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:

        candidate = text[start:end + 1]

        try:
            result = json.loads(candidate)

            if isinstance(result, dict):
                return result

        except json.JSONDecodeError:
            pass

    return None


# ---------------------------------------------------------
# Gemini prompt
# ---------------------------------------------------------

def build_prompt(request) -> str:
    """
    Build the prompt sent to Gemini.
    """

    starting_city = (
        request.starting_city.strip()
        if getattr(request, "starting_city", "")
        else "Not specified"
    )

    interests = (
        request.interests.strip()
        if request.interests
        else "Sightseeing, food, local experiences"
    )

    return f"""
You are the AI travel planner for TRAVELX, an Indian all-in-one
travel and lifestyle application.

Create a practical and realistic travel plan.

TRIP DETAILS

Starting city:
{starting_city}

Destination:
{request.destination}

Number of days:
{request.days}

Number of travelers:
{request.travelers}

Budget in Indian Rupees:
₹{request.budget}

Travel style:
{request.travel_style}

Interests:
{interests}


IMPORTANT REQUIREMENTS

1. Create a day-by-day itinerary.
2. Keep the total estimated cost close to or below the user's budget.
3. Consider the number of travelers.
4. Suggest realistic transport options.
5. Suggest suitable accommodation.
6. Suggest local food.
7. Include useful travel tips.
8. Use Indian Rupees.
9. Do not invent exact live availability.
10. Do not claim that a booking has been made.
11. Keep recommendations practical for the destination.
12. Return ONLY valid JSON.
13. Do not use markdown.
14. Do not add explanations outside the JSON.


RETURN EXACTLY THIS JSON STRUCTURE:

{{
    "summary": "Short trip summary",
    "estimated_total": 0,
    "budget_status": "Within budget",
    "transport": [
        "transport recommendation"
    ],
    "accommodation": [
        "accommodation recommendation"
    ],
    "food": [
        "food recommendation"
    ],
    "tips": [
        "travel tip"
    ],
    "itinerary": [
        {{
            "day": 1,
            "title": "Day title",
            "morning": "Morning activity",
            "afternoon": "Afternoon activity",
            "evening": "Evening activity",
            "estimated_cost": 0
        }}
    ]
}}
"""


# ---------------------------------------------------------
# Gemini generation
# ---------------------------------------------------------

def generate_with_gemini(request) -> dict[str, Any] | None:
    """
    Generate a trip plan using Gemini.

    Temporary Gemini 503 errors are retried automatically.

    Returns:
        dict -> successful Gemini response
        None -> Gemini unavailable / unsuccessful
    """

    client = get_gemini_client()

    if client is None:
        print("Gemini client is not configured.")
        return None

    prompt = build_prompt(request)

    # Number of attempts
    max_attempts = 3

    # Small delays between attempts
    retry_delays = [3, 7, 12]

    for attempt in range(max_attempts):

        try:

            print(
                f"Gemini request attempt "
                f"{attempt + 1}/{max_attempts} "
                f"using {MODEL_NAME}..."
            )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if response is None:
                print("Gemini returned an empty response.")
                return None

            # Gemini SDK response text
            text = getattr(response, "text", None)

            if not text:
                print("Gemini response did not contain text.")
                return None

            result = extract_json(text)

            if result is None:
                print("Gemini returned invalid JSON.")
                print("Gemini response:")
                print(text)
                return None

            print("Gemini response successfully parsed.")

            return result

        except Exception as exc:

            error_text = str(exc)

            print(
                f"Gemini attempt {attempt + 1} failed:"
            )
            print(error_text)

            # Retry temporary server/capacity errors
            temporary_error = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text
                or "temporarily" in error_text.lower()
                or "timeout" in error_text.lower()
            )

            if temporary_error and attempt < max_attempts - 1:

                delay = retry_delays[attempt]

                print(
                    f"Temporary Gemini error. "
                    f"Retrying in {delay} seconds..."
                )

                time.sleep(delay)

                continue

            # Do not repeatedly retry permanent errors
            print(
                "Gemini generation failed. "
                "TRAVELX will use the fallback planner."
            )

            return None

    return None


# ---------------------------------------------------------
# Fallback planner
# ---------------------------------------------------------

def generate_fallback(request) -> dict[str, Any]:
    """
    Reliable local fallback planner.

    This allows TRAVELX to continue working even when
    Gemini is temporarily unavailable.
    """

    destination = request.destination.strip()
    days = request.days
    budget = request.budget
    travelers = request.travelers
    travel_style = request.travel_style.strip()

    interests = (
        request.interests.strip()
        if request.interests
        else "Sightseeing, food, local experiences"
    )

    # Basic budget allocation
    transport_budget = int(budget * 0.20)
    accommodation_budget = int(budget * 0.30)
    food_budget = int(budget * 0.20)
    activities_budget = int(budget * 0.20)
    buffer_budget = int(budget * 0.10)

    estimated_total = (
        transport_budget
        + accommodation_budget
        + food_budget
        + activities_budget
        + buffer_budget
    )

    itinerary = []

    daily_budget = max(
        500,
        int(budget / days)
    )

    for day_number in range(1, days + 1):

        if day_number == 1:

            title = f"Arrive & explore {destination}"

            morning = (
                "Arrive at the destination, "
                "check in and take some rest."
            )

            afternoon = (
                "Explore a popular local attraction "
                "and nearby market or area."
            )

            evening = (
                "Try a popular local food spot "
                "and enjoy a relaxed evening."
            )

        elif day_number == days:

            title = f"Highlights & departure"

            morning = (
                "Visit one final landmark or "
                "scenic location."
            )

            afternoon = (
                "Have lunch, shop for souvenirs "
                "and complete check-out."
            )

            evening = (
                "Start your return journey with "
                "enough buffer time."
            )

        else:

            title = (
                f"Explore {destination} — "
                f"Day {day_number}"
            )

            morning = (
                "Start with a major attraction "
                "or guided local experience."
            )

            afternoon = (
                "Have local lunch and explore "
                "another nearby attraction."
            )

            evening = (
                "Enjoy a cultural, scenic or "
                "entertainment activity."
            )

        itinerary.append(
            {
                "day": day_number,
                "title": title,
                "morning": morning,
                "afternoon": afternoon,
                "evening": evening,
                "estimated_cost": daily_budget
            }
        )

    if estimated_total <= budget:
        budget_status = "Within budget"
    else:
        budget_status = "Slightly above budget"

    return {
        "summary": (
            f"A {days}-day {travel_style.lower()} trip "
            f"to {destination}, focused on {interests}."
        ),

        "estimated_total": estimated_total,

        "budget_status": budget_status,

        "transport": [
            "Mix local public transport with app cabs "
            "depending on distance.",
            "Keep a small buffer for last-mile travel "
            "and transfers."
        ],

        "accommodation": [
            "Choose a well-rated hotel in a central "
            "and convenient area.",
            "Compare location, rating and cancellation "
            "policy before booking."
        ],

        "food": [
            "Try local specialties instead of eating "
            "only at tourist-focused restaurants.",
            "Keep one flexible meal slot each day "
            "for spontaneous discoveries."
        ],

        "tips": [
            "Check attraction timings and holiday "
            "closures before leaving.",
            "Keep identification, emergency contacts "
            "and essential medicines with you.",
            "TRAVELX recommendations are planning "
            "suggestions; verify live availability "
            "before booking."
        ],

        "itinerary": itinerary
    }