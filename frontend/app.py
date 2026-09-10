import streamlit as st
import requests
from datetime import date


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="TRAVELX",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "bus_results" not in st.session_state:
    st.session_state.bus_results = []

if "selected_bus" not in st.session_state:
    st.session_state.selected_bus = None

if "wallet_selected_amount" not in st.session_state:
    st.session_state.wallet_selected_amount = 0.0

# ============================================================
# TRAIN SESSION STATE
# ============================================================

if "train_results" not in st.session_state:
    st.session_state.train_results = []

if "selected_train" not in st.session_state:
    st.session_state.selected_train = None

# ============================================================
# HOTEL SESSION STATE
# ============================================================

if "hotel_results" not in st.session_state:
    st.session_state.hotel_results = []

if "selected_hotel" not in st.session_state:
    st.session_state.selected_hotel = None

# ============================================================
# FLIGHT SESSION STATE
# ============================================================

if "flight_results" not in st.session_state:
    st.session_state.flight_results = []

if "selected_flight" not in st.session_state:
    st.session_state.selected_flight = None

# ============================================================
# CAB SESSION STATE
# ============================================================

if "cab_results" not in st.session_state:
    st.session_state.cab_results = []

if "selected_cab" not in st.session_state:
    st.session_state.selected_cab = None

# ============================================================
# FOOD SESSION STATE
# ============================================================

if "food_restaurants" not in st.session_state:
    st.session_state.food_restaurants = []

if "selected_restaurant" not in st.session_state:
    st.session_state.selected_restaurant = None

if "food_menu" not in st.session_state:
    st.session_state.food_menu = []

if "food_cart" not in st.session_state:
    st.session_state.food_cart = []

# ============================================================
# MOVIE SESSION STATE
# ============================================================

if "movie_results" not in st.session_state:
    st.session_state.movie_results = []

if "movie_city" not in st.session_state:
    st.session_state.movie_city = ""

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

if "movie_cinemas" not in st.session_state:
    st.session_state.movie_cinemas = []

if "selected_cinema" not in st.session_state:
    st.session_state.selected_cinema = None

if "movie_shows" not in st.session_state:
    st.session_state.movie_shows = []

if "selected_show" not in st.session_state:
    st.session_state.selected_show = None

if "selected_movie_seats" not in st.session_state:
    st.session_state.selected_movie_seats = []

if "movie_booking_lookup_cache" not in st.session_state:
    st.session_state.movie_booking_lookup_cache = {}

# ============================================================
# EVENT SESSION STATE
# ============================================================

if "event_results" not in st.session_state:
    st.session_state.event_results = []

if "event_city" not in st.session_state:
    st.session_state.event_city = ""

if "selected_event" not in st.session_state:
    st.session_state.selected_event = None

if "event_venues" not in st.session_state:
    st.session_state.event_venues = []

if "selected_event_venue" not in st.session_state:
    st.session_state.selected_event_venue = None

if "event_shows" not in st.session_state:
    st.session_state.event_shows = []

if "selected_event_show" not in st.session_state:
    st.session_state.selected_event_show = None

# ============================================================
# AI TRIP PLANNER SESSION STATE
# ============================================================

if "trip_plan" not in st.session_state:
    st.session_state.trip_plan = None

# ============================================================
# CUSTOM CSS
# ============================================================

st.html("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(37, 99, 235, 0.12),
            transparent 30%
        ),
        radial-gradient(
            circle at bottom left,
            rgba(14, 165, 233, 0.06),
            transparent 25%
        ),
        #080c14;
}

.main .block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #f8fafc !important;
}

p, label {
    color: #cbd5e1;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #111827 0%,
            #0f172a 55%,
            #080c14 100%
        );

    border-right: 1px solid #263244;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

.sidebar-brand {
    text-align: center;
    padding: 10px 0 22px 0;
}

.sidebar-logo {
    color: white;
    font-size: 28px;
    font-weight: 900;
}

.sidebar-tagline {
    color: #64748b;
    font-size: 11px;
    margin-top: 4px;
    letter-spacing: 0.5px;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-box {
    position: relative;
    overflow: hidden;

    padding: 42px;
    border-radius: 28px;
    margin-bottom: 30px;

    background:
        radial-gradient(
            circle at 88% 18%,
            rgba(96, 165, 250, 0.35),
            transparent 24%
        ),
        radial-gradient(
            circle at 70% 100%,
            rgba(59, 130, 246, 0.18),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #111827 0%,
            #1d4ed8 55%,
            #2563eb 100%
        );

    border: 1px solid rgba(147, 197, 253, 0.20);

    box-shadow:
        0 20px 55px rgba(0, 0, 0, 0.30);
}

.hero-box::after {
    content: "✈️";
    position: absolute;
    right: 45px;
    bottom: -30px;

    font-size: 140px;
    opacity: 0.07;

    transform: rotate(-10deg);
}

.hero-badge {
    display: inline-block;

    padding: 7px 14px;
    border-radius: 999px;

    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.16);

    color: #dbeafe;
    font-size: 12px;
    font-weight: 700;

    letter-spacing: 0.7px;
    margin-bottom: 15px;
}

.hero-title {
    position: relative;
    z-index: 1;

    color: white;
    font-size: 44px;
    font-weight: 900;

    line-height: 1.15;
    margin-bottom: 12px;
}

.hero-text {
    position: relative;
    z-index: 1;

    color: #dbeafe;
    font-size: 17px;

    max-width: 800px;
    line-height: 1.65;
}


/* ============================================================
   SECTION
   ============================================================ */

.section-heading {
    color: #f8fafc;

    font-size: 28px;
    font-weight: 850;

    margin-top: 15px;
    margin-bottom: 6px;
}

.section-subtitle {
    color: #64748b;

    font-size: 14px;

    margin-bottom: 22px;
}


/* ============================================================
   SERVICE CARDS
   ============================================================ */

.service-card {
    min-height: 165px;

    padding: 22px;
    margin-bottom: 8px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            #111827,
            #0f172a
        );

    border: 1px solid #263244;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.18);
}

.service-icon {
    font-size: 34px;
    margin-bottom: 8px;
}

.service-title {
    color: #f8fafc;

    font-size: 20px;
    font-weight: 800;
}

.service-description {
    color: #94a3b8;

    font-size: 13px;

    line-height: 1.5;

    margin-top: 7px;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

.metric-card {
    padding: 22px;

    border-radius: 19px;

    background:
        linear-gradient(
            145deg,
            #111827,
            #0d1422
        );

    border: 1px solid #263244;

    min-height: 120px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.15);
}

.metric-label {
    color: #64748b;

    font-size: 12px;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: 0.6px;

    margin-bottom: 8px;
}

.metric-value {
    color: #f8fafc;

    font-size: 28px;
    font-weight: 900;
}


/* ============================================================
   WALLET
   ============================================================ */

.wallet-box {
    position: relative;
    overflow: hidden;

    padding: 34px;

    border-radius: 25px;
    margin-bottom: 28px;

    background:
        radial-gradient(
            circle at 88% 15%,
            rgba(96, 165, 250, 0.30),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #111827,
            #172554 50%,
            #1e40af
        );

    border: 1px solid rgba(96,165,250,0.22);

    box-shadow:
        0 20px 50px rgba(0,0,0,0.28);
}

.wallet-label {
    color: #bfdbfe;

    font-size: 13px;
    font-weight: 700;

    letter-spacing: 0.8px;
}

.wallet-balance {
    color: white;

    font-size: 46px;
    font-weight: 900;

    margin: 7px 0;
}

.wallet-subtitle {
    color: #93c5fd;
    font-size: 13px;
}


/* ============================================================
   LOGIN
   ============================================================ */

.login-box {
    padding: 30px;

    border-radius: 22px;

    background: #111827;

    border: 1px solid #263244;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 11px !important;

    font-weight: 700 !important;

    border: 1px solid #374151 !important;

    min-height: 42px;
}


/* ============================================================
   INPUTS
   ============================================================ */

.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background-color: #111827 !important;

    color: #f8fafc !important;

    border: 1px solid #374151 !important;

    border-radius: 10px !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;

    color: #475569;

    padding: 35px 0 10px 0;

    font-size: 12px;
}

</style>
""")


# ============================================================
# API HELPERS
# ============================================================

def auth_headers():

    if not st.session_state.token:
        return {}

    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }


def api_get(endpoint):

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            headers=auth_headers(),
            timeout=10
        )

        return response

    except requests.exceptions.RequestException as e:

        st.error(
            f"Backend connection error: {e}"
        )

        return None


def api_post(endpoint, data):

    try:

        response = requests.post(
            f"{API_URL}{endpoint}",
            json=data,
            headers=auth_headers(),
            timeout=10
        )

        return response

    except requests.exceptions.RequestException as e:

        st.error(
            f"Backend connection error: {e}"
        )

        return None


def get_json(response):

    if response is None:
        return {}

    try:

        return response.json()

    except Exception:

        return {}


# ============================================================
# AUTH FUNCTIONS
# ============================================================

def login_user(email, password):

    try:

        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=10
        )

        if response.status_code != 200:
            return False

        data = response.json()

        st.session_state.token = data["access_token"]

        profile_response = requests.get(
            f"{API_URL}/auth/profile",
            headers=auth_headers(),
            timeout=10
        )

        if profile_response.status_code == 200:

            st.session_state.user = (
                profile_response.json()
            )

        else:

            st.session_state.user = {
                "name": email.split("@")[0],
                "email": email
            }

        return True

    except requests.exceptions.RequestException as e:

        st.error(
            f"Backend connection error: {e}"
        )

        return False


def register_user(
    name,
    email,
    phone,
    password
):

    try:

        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "name": name,
                "email": email,
                "phone": phone,
                "password": password
            },
            timeout=10
        )

        if response.status_code in [200, 201]:

            return True

        detail = get_json(response).get(
            "detail",
            "Registration failed."
        )

        st.error(detail)

        return False

    except requests.exceptions.RequestException as e:

        st.error(
            f"Backend connection error: {e}"
        )

        return False


def logout_user():

    st.session_state.token = None

    st.session_state.user = None

    st.session_state.page = "Home"

    st.session_state.bus_results = []

    st.session_state.selected_bus = None
    st.session_state.train_results = []
    st.session_state.selected_train = None
    st.session_state.hotel_results = []
    st.session_state.selected_hotel = None
    st.session_state.flight_results = []
    st.session_state.selected_flight = None
    st.session_state.cab_results = []
    st.session_state.selected_cab = None

    st.session_state.food_restaurants = []
    st.session_state.selected_restaurant = None
    st.session_state.food_menu = []
    st.session_state.food_cart = []

    st.session_state.movie_results = []
    st.session_state.movie_city = ""
    st.session_state.selected_movie = None
    st.session_state.movie_cinemas = []
    st.session_state.selected_cinema = None
    st.session_state.movie_shows = []
    st.session_state.selected_show = None
    st.session_state.selected_movie_seats = []
    st.session_state.movie_booking_lookup_cache = {}

    st.session_state.event_results = []
    st.session_state.event_city = ""
    st.session_state.selected_event = None
    st.session_state.event_venues = []
    st.session_state.selected_event_venue = None
    st.session_state.event_shows = []
    st.session_state.selected_event_show = None

    st.session_state.trip_plan = None

    st.session_state.wallet_selected_amount = 0.0

    st.rerun()


# ============================================================
# LOGIN / REGISTER
# ============================================================

if not st.session_state.token:

    st.html("""
    <div class="hero-box">

        <div class="hero-badge">
            ✨ ONE PLATFORM • EVERY JOURNEY
        </div>

        <div class="hero-title">
            Welcome to TRAVELX ✈️
        </div>

        <div class="hero-text">
            Your complete travel and lifestyle super app.
            Search, compare and manage your journeys —
            buses, trains, flights, hotels, cabs, food,
            movies and events, all from one powerful platform.
        </div>

    </div>
    """)

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Create Account"
        ]
    )


    # ========================================================
    # LOGIN TAB
    # ========================================================

    with login_tab:

        st.html("""
        <div style="
            text-align:center;
            padding:20px 0 25px 0;
        ">

            <div style="
                font-size:54px;
                margin-bottom:5px;
            ">
                👋
            </div>

            <div style="
                color:#f8fafc;
                font-size:34px;
                font-weight:900;
            ">
                Welcome Back
            </div>

            <div style="
                color:#64748b;
                font-size:14px;
                margin-top:6px;
            ">
                Login to continue your TRAVELX journey.
            </div>

        </div>
        """)

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "🚀 Login to TRAVELX",
            type="primary",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Please enter email and password."
                )

            elif login_user(
                email,
                password
            ):

                st.success(
                    "Login successful! 🎉"
                )

                st.session_state.page = "Home"

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )


    # ========================================================
    # REGISTER TAB
    # ========================================================

    with register_tab:

        st.html("""
        <div style="
            text-align:center;
            padding:20px 0 25px 0;
        ">

            <div style="
                font-size:54px;
            ">
                🚀
            </div>

            <div style="
                color:#f8fafc;
                font-size:34px;
                font-weight:900;
            ">
                Create Your Account
            </div>

            <div style="
                color:#64748b;
                font-size:14px;
                margin-top:6px;
            ">
                Join TRAVELX and manage your journey in one place.
            </div>

        </div>
        """)

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        phone = st.text_input(
            "Phone Number",
            key="register_phone"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button(
            "✨ Create TRAVELX Account",
            type="primary",
            use_container_width=True
        ):

            if (
                not name
                or not email
                or not phone
                or not password
            ):

                st.warning(
                    "Please fill all fields."
                )

            elif register_user(
                name,
                email,
                phone,
                password
            ):

                st.success(
                    "Account created successfully! "
                    "Please login."
                )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div class="sidebar-brand">

        <div class="sidebar-logo">
            ✈️ TRAVELX
        </div>

        <div class="sidebar-tagline">
            TRAVEL • BOOK • EXPLORE
        </div>

    </div>
    """)

    if st.session_state.user:

        user_name = st.session_state.user.get(
            "name",
            "User"
        )

        st.write(
            f"👋 Welcome, **{user_name}**"
        )

    st.divider()

    pages = [
        ("🏠", "Home"),
        ("✈️", "Flights"),
        ("🚆", "Trains"),
        ("🚌", "Buses"),
        ("🏨", "Hotels"),
        ("🚕", "Cabs"),
        ("🍔", "Food"),
        ("🎬", "Movies"),
        ("🎟️", "Events"),
        ("🤖", "AI Trip Planner"),
        ("💰", "Wallet"),
        ("📋", "My Bookings"),
        ("👤", "Profile")
    ]

    for icon, page_name in pages:

        if st.button(
            f"{icon}  {page_name}",
            use_container_width=True,
            key=f"sidebar_{page_name}"
        ):

            st.session_state.page = page_name

            st.rerun()

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout_user()


# ============================================================
# HOME
# ============================================================

if st.session_state.page == "Home":

    user_name = (
        st.session_state.user.get(
            "name",
            "Traveler"
        )
        if st.session_state.user
        else "Traveler"
    )


    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.html(f"""
    <div class="hero-box">

        <div class="hero-badge">
            ✨ YOUR JOURNEY STARTS HERE
        </div>

        <div class="hero-title">
            Travel Smarter, {user_name} ✈️
        </div>

        <div class="hero-text">
            Book buses, trains, flights, hotels, cabs,
            food, movies and events — all from one place.
            Let TRAVELX simplify your entire journey.
        </div>

    </div>
    """)


    # --------------------------------------------------------
    # QUICK ACTIONS
    # --------------------------------------------------------

    st.html("""
    <div class="section-heading">
        Quick Actions
    </div>

    <div class="section-subtitle">
        Jump directly to your most-used TRAVELX features.
    </div>
    """)

    quick1, quick2, quick3, quick4 = st.columns(4)

    with quick1:

        if st.button(
            "🚌 Book a Bus",
            use_container_width=True,
            key="quick_bus"
        ):

            st.session_state.page = "Buses"
            st.rerun()

    with quick2:

        if st.button(
            "💰 Add Money",
            use_container_width=True,
            key="quick_wallet"
        ):

            st.session_state.page = "Wallet"
            st.rerun()

    with quick3:

        if st.button(
            "📋 My Bookings",
            use_container_width=True,
            key="quick_bookings"
        ):

            st.session_state.page = "My Bookings"
            st.rerun()

    with quick4:

        if st.button(
            "🤖 Plan a Trip",
            use_container_width=True,
            key="quick_ai"
        ):

            st.session_state.page = "AI Trip Planner"
            st.rerun()


    # --------------------------------------------------------
    # DASHBOARD DATA
    # --------------------------------------------------------

    wallet_balance = 0.0
    booking_count = 0
    bus_booking_count = 0
    train_booking_count = 0
    flight_booking_count = 0
    cab_booking_count = 0
    food_order_count = 0
    event_booking_count = 0


    # ========================================================
    # EVENT BOOKINGS COUNT
    # ========================================================

    event_booking_response = api_get(
        "/events/my-bookings"
    )

    if (
        event_booking_response
        and event_booking_response.status_code == 200
    ):
        event_booking_data = get_json(
            event_booking_response
        )

        if isinstance(event_booking_data, list):
            event_booking_count = len(event_booking_data)


    # ========================================================
    # LIVE WALLET
    # ========================================================

    wallet_response = api_get(
        "/wallet/"
    )

    if (
        wallet_response
        and wallet_response.status_code == 200
    ):

        wallet_data = get_json(
            wallet_response
        )

        wallet_balance = float(
            wallet_data.get(
                "balance",
                0
            )
        )


    # ========================================================
    # MOVIE BOOKINGS COUNT
    # ========================================================

    movie_booking_count = 0

    movie_booking_response = api_get(
        "/movies/my-bookings"
    )

    if (
        movie_booking_response
        and movie_booking_response.status_code == 200
    ):
        movie_booking_data = get_json(
            movie_booking_response
        )

        if isinstance(
            movie_booking_data,
            list
        ):
            movie_booking_count = len(
                movie_booking_data
            )

    elif movie_booking_response:
        st.warning(
            "Unable to load movie booking count."
        )


    # ========================================================
    # BUS BOOKINGS
    # ========================================================

    bus_response = api_get(
        "/buses/my-bookings"
    )

    if (
        bus_response
        and bus_response.status_code == 200
    ):

        bus_booking_data = get_json(
            bus_response
        )

        if isinstance(
            bus_booking_data,
            list
        ):

            bus_booking_count = len(
                bus_booking_data
            )


    # ========================================================
    # TRAIN BOOKINGS COUNT
    # ========================================================

    train_count_response = api_get(
        "/trains/my-bookings"
    )

    if (
        train_count_response
        and train_count_response.status_code == 200
    ):
        train_booking_data = get_json(
            train_count_response
        )

        if isinstance(
            train_booking_data,
            list
        ):
            train_booking_count = len(
                train_booking_data
            )

    # ========================================================
    # FLIGHT BOOKINGS COUNT
    # ========================================================

    flight_count_response = api_get(
        "/flights/my-bookings"
    )

    if (
        flight_count_response
        and flight_count_response.status_code == 200
    ):

        flight_booking_data = get_json(
            flight_count_response
        )

        if isinstance(
            flight_booking_data,
            list
        ):

            flight_booking_count = len(
                flight_booking_data
            )

    # ========================================================
    # CAB BOOKINGS COUNT
    # ========================================================

    cab_count_response = api_get(
        "/cabs/my-bookings"
    )

    if (
        cab_count_response
        and cab_count_response.status_code == 200
    ):

        cab_booking_data = get_json(
            cab_count_response
        )

        if isinstance(
            cab_booking_data,
            list
        ):

            cab_booking_count = len(
                cab_booking_data
            )


    # ========================================================
    # FOOD ORDERS COUNT
    # ========================================================

    food_count_response = api_get(
        "/food/my-orders"
    )

    if (
        food_count_response
        and food_count_response.status_code == 200
    ):

        food_order_data = get_json(
            food_count_response
        )

        if isinstance(
            food_order_data,
            list
        ):

            food_order_count = len(
                food_order_data
            )


    # ========================================================
    # GENERIC BOOKINGS
    # ========================================================

    booking_response = api_get(
        "/bookings/my"
    )

    if (
        booking_response
        and booking_response.status_code == 200
    ):

        booking_data = get_json(
            booking_response
        )

        if isinstance(
            booking_data,
            list
        ):

            booking_count = len(
                booking_data
            )


    total_bookings = (
        bus_booking_count
        + train_booking_count
        + flight_booking_count
        + cab_booking_count
        + food_order_count
        + movie_booking_count
        + event_booking_count
        + booking_count
    )


    # --------------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------------

    st.html("""
    <div class="section-heading">
        Your TRAVELX Overview
    </div>

    <div class="section-subtitle">
        A quick look at your travel activity.
    </div>
    """)

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:

        st.html(f"""
        <div class="metric-card">

            <div class="metric-label">
                Wallet Balance
            </div>

            <div class="metric-value">
                ₹{wallet_balance:,.2f}
            </div>

        </div>
        """)

    with metric2:

        st.html(f"""
        <div class="metric-card">

            <div class="metric-label">
                Total Bookings
            </div>

            <div class="metric-value">
                {total_bookings}
            </div>

        </div>
        """)

    with metric3:

        st.html(f"""
        <div class="metric-card">

            <div class="metric-label">
                Flight Bookings
            </div>

            <div class="metric-value">
                {flight_booking_count}
            </div>

        </div>
        """)

    with metric4:

        st.html("""
        <div class="metric-card">

            <div class="metric-label">
                Smart Planning
            </div>

            <div class="metric-value">
                AI 🤖
            </div>

        </div>
        """)


    # --------------------------------------------------------
    # SERVICES
    # --------------------------------------------------------

    st.html("""
    <div class="section-heading">
        Explore TRAVELX
    </div>

    <div class="section-subtitle">
        Everything you need for your journey, under one roof.
    </div>
    """)

    services = [
        ("✈️", "Flights", "Search and book flights."),
        ("🚆", "Trains", "Plan your railway journey."),
        ("🚌", "Buses", "Book intercity buses."),
        ("🏨", "Hotels", "Find your perfect stay."),
        ("🚕", "Cabs", "Book local and outstation cabs."),
        ("🍔", "Food", "Order food while travelling."),
        ("🎬", "Movies", "Book movie tickets."),
        ("🎟️", "Events", "Discover events."),
        ("🤖", "AI Trip Planner", "Create smart travel plans."),
        ("💰", "Wallet", "Manage your TRAVELX money."),
        ("📋", "My Bookings", "View all your bookings."),
        ("👤", "Profile", "Manage your account.")
    ]

    for row in range(
        0,
        len(services),
        3
    ):

        columns = st.columns(3)

        for index, column in enumerate(columns):

            service_index = row + index

            if service_index >= len(services):
                continue

            icon, title, description = services[
                service_index
            ]

            with column:

                st.html(f"""
                <div class="service-card">

                    <div class="service-icon">
                        {icon}
                    </div>

                    <div class="service-title">
                        {title}
                    </div>

                    <div class="service-description">
                        {description}
                    </div>

                </div>
                """)

                if st.button(
                    f"Open {title}",
                    use_container_width=True,
                    key=f"service_{title}"
                ):

                    st.session_state.page = title
                    st.rerun()


    # --------------------------------------------------------
    # WHY TRAVELX
    # --------------------------------------------------------

    st.html("""
    <div class="section-heading">
        Why TRAVELX?
    </div>

    <div class="section-subtitle">
        One platform designed around your entire journey.
    </div>
    """)

    why1, why2, why3, why4 = st.columns(4)

    with why1:

        st.markdown("### ⚡")
        st.write("**Fast & Simple**")

        st.caption(
            "Manage your journey without switching between multiple applications."
        )

    with why2:

        st.markdown("### 🔐")
        st.write("**Secure Account**")

        st.caption(
            "Your account and bookings are protected through authentication."
        )

    with why3:

        st.markdown("### 💰")
        st.write("**Digital Wallet**")

        st.caption(
            "Keep your TRAVELX balance ready for future bookings."
        )

    with why4:

        st.markdown("### 🤖")
        st.write("**AI Powered**")

        st.caption(
            "Build personalized travel plans with intelligent assistance."
        )


# ============================================================
# FLIGHTS
# ============================================================

elif st.session_state.page == "Flights":

    st.title("✈️ Flight Booking")

    st.caption(
        "Search flights, compare fares and book your journey."
    )

    st.divider()

    # ========================================================
    # SEARCH FLIGHTS
    # ========================================================

    st.subheader("🔎 Search Flights")

    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input(
            "From",
            placeholder="Example: Mumbai",
            key="flight_source"
        )

    with col2:
        destination = st.text_input(
            "To",
            placeholder="Example: Delhi",
            key="flight_destination"
        )

    if st.button(
        "🔎 Search Flights",
        type="primary",
        use_container_width=True,
        key="search_flights_button"
    ):

        if not source.strip() or not destination.strip():

            st.warning("Please enter source and destination.")

        else:

            response = api_post(
                "/flights/search",
                {
                    "source": source.strip(),
                    "destination": destination.strip()
                }
            )

            if response:

                if response.status_code == 200:

                    st.session_state.flight_results = response.json()
                    st.session_state.selected_flight = None

                    if not st.session_state.flight_results:

                        st.warning(
                            f"No flights found from {source.strip()} "
                            f"to {destination.strip()}."
                        )

                else:

                    detail = get_json(response).get(
                        "detail",
                        "Flight search failed."
                    )

                    st.error(detail)

    # ========================================================
    # AVAILABLE FLIGHTS
    # ========================================================

    if st.session_state.flight_results:

        st.divider()

        st.subheader("✈️ Available Flights")

        for flight in st.session_state.flight_results:

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [2.2, 2.5, 2, 1]
                )

                # ------------------------------------------------
                # AIRLINE
                # ------------------------------------------------

                with col1:

                    st.markdown(
                        f"### ✈️ {flight['airline']}"
                    )

                    st.write(
                        f"**{flight['flight_number']}**"
                    )

                # ------------------------------------------------
                # ROUTE + TIME
                # ------------------------------------------------

                with col2:

                    st.write(
                        f"📍 **{flight['source']} → "
                        f"{flight['destination']}**"
                    )

                    st.write(
                        f"🕐 {flight['departure_time']} → "
                        f"{flight['arrival_time']}"
                    )

                # ------------------------------------------------
                # FARE + SEATS
                # ------------------------------------------------

                with col3:

                    st.write(
                        f"💺 Available seats: "
                        f"**{flight['available_seats']}**"
                    )

                    st.write(
                        f"💰 Economy: "
                        f"**₹{flight['economy_price']:,}**"
                    )

                    st.caption(
                        f"Premium ₹{flight['premium_economy_price']:,} "
                        f"• Business ₹{flight['business_price']:,}"
                    )

                # ------------------------------------------------
                # BOOK
                # ------------------------------------------------

                with col4:

                    if st.button(
                        "Book Now",
                        key=f"select_flight_{flight['id']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_flight = flight

                        st.rerun()

    # ========================================================
    # FLIGHT BOOKING FORM
    # ========================================================

    if st.session_state.selected_flight:

        flight = st.session_state.selected_flight

        st.divider()

        st.subheader("🎫 Complete Your Flight Booking")

        st.info(
            f"✈️ **{flight['airline']} {flight['flight_number']}** | "
            f"📍 {flight['source']} → {flight['destination']} | "
            f"🕐 {flight['departure_time']} → "
            f"{flight['arrival_time']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            passenger_name = st.text_input(
                "Passenger Name",
                key="flight_passenger_name"
            )

        with col2:

            passenger_phone = st.text_input(
                "Passenger Phone",
                key="flight_passenger_phone"
            )

        # ====================================================
        # CLASS
        # ====================================================

        travel_class = st.selectbox(
            "💺 Travel Class",
            [
                "Economy",
                "Premium Economy",
                "Business"
            ],
            key="flight_travel_class"
        )

        class_prices = {
            "Economy": flight["economy_price"],
            "Premium Economy": flight["premium_economy_price"],
            "Business": flight["business_price"]
        }

        selected_price = class_prices[travel_class]

        seats = st.number_input(
            "Number of Seats",
            min_value=1,
            max_value=int(flight["available_seats"]),
            value=1,
            step=1,
            key="flight_seats"
        )

        total_price = selected_price * int(seats)

        st.success(
            f"💰 Total Price: **₹{total_price:,}**"
        )

        st.caption(
            f"{travel_class}: ₹{selected_price:,} × {int(seats)} seat(s)"
        )

        # ====================================================
        # LIVE WALLET BALANCE
        # ====================================================

        wallet_response = api_get(
            "/wallet/"
        )

        wallet_balance = 0.0

        if (
            wallet_response
            and wallet_response.status_code == 200
        ):

            wallet_data = get_json(
                wallet_response
            )

            wallet_balance = float(
                wallet_data.get(
                    "balance",
                    0
                )
            )

        # ====================================================
        # PAYMENT
        # ====================================================

        st.subheader("💳 Payment Method")

        payment_method = st.radio(
            "Choose payment method",
            [
                "TRAVELX Wallet",
                "Demo Payment"
            ],
            key="flight_payment_method"
        )

        if payment_method == "TRAVELX Wallet":

            st.info(
                f"💰 Wallet Balance: "
                f"**₹{wallet_balance:,.2f}**"
            )

            if wallet_balance >= total_price:

                remaining_balance = (
                    wallet_balance - total_price
                )

                st.success(
                    f"After payment: "
                    f"**₹{remaining_balance:,.2f}**"
                )

            else:

                shortage = (
                    total_price - wallet_balance
                )

                st.error(
                    f"Insufficient wallet balance. "
                    f"You need ₹{shortage:,.2f} more."
                )

        else:

            st.warning(
                "Demo Payment does not deduct money "
                "from your TRAVELX Wallet."
            )

        # ====================================================
        # CONFIRM BOOKING
        # ====================================================

        if st.button(
            "🎟️ Confirm Flight Booking",
            type="primary",
            use_container_width=True,
            key="confirm_flight_booking"
        ):

            if not passenger_name.strip():

                st.warning(
                    "Please enter passenger name."
                )

            elif not passenger_phone.strip():

                st.warning(
                    "Please enter passenger phone."
                )

            elif (
                payment_method == "TRAVELX Wallet"
                and wallet_balance < total_price
            ):

                st.error(
                    "Insufficient wallet balance. "
                    "Please add money to your wallet."
                )

            else:

                backend_payment_method = (
                    "wallet"
                    if payment_method == "TRAVELX Wallet"
                    else "demo"
                )

                response = api_post(
                    "/flights/book",
                    {
                        "flight_id": flight["id"],
                        "passenger_name": passenger_name.strip(),
                        "passenger_phone": passenger_phone.strip(),
                        "travel_class": travel_class,
                        "seats": int(seats),
                        "payment_method": backend_payment_method
                    }
                )

                if response:

                    if response.status_code in [200, 201]:

                        booking = response.json()

                        st.success(
                            "🎉 Flight Booking Confirmed!"
                        )

                        st.write(
                            f"**Booking ID:** "
                            f"#{booking['id']}"
                        )

                        st.write(
                            f"**Flight:** "
                            f"{flight['airline']} "
                            f"{flight['flight_number']}"
                        )

                        st.write(
                            f"**Passenger:** "
                            f"{booking['passenger_name']}"
                        )

                        st.write(
                            f"**Class:** "
                            f"{booking['travel_class'].title()}"
                        )

                        st.write(
                            f"**Seats:** "
                            f"{booking['seats']}"
                        )

                        st.write(
                            f"**Total Paid:** "
                            f"₹{booking['total_price']:,}"
                        )

                        st.write(
                            f"**Payment:** "
                            f"{booking['payment_method'].upper()}"
                        )

                        if backend_payment_method == "wallet":

                            st.success(
                                "💳 Payment completed "
                                "using TRAVELX Wallet."
                            )

                        else:

                            st.info(
                                "🧪 Demo payment completed."
                            )

                        st.session_state.selected_flight = None
                        st.session_state.flight_results = []
                        st.session_state.page = "My Bookings"

                        st.rerun()

                    else:

                        detail = get_json(
                            response
                        ).get(
                            "detail",
                            "Flight booking failed."
                        )

                        st.error(detail)



# ============================================================
# CABS
# ============================================================

elif st.session_state.page == "Food":

    st.title("🍔 Food Ordering")

    st.caption(
        "Discover restaurants, explore menus and order your favourite food."
    )

    st.divider()

    # ========================================================
    # SEARCH RESTAURANTS
    # ========================================================

    st.subheader("📍 Find Restaurants")

    col1, col2 = st.columns([3, 1])

    with col1:
        city = st.text_input(
            "City",
            placeholder="Example: Mumbai",
            key="food_city"
        )

    with col2:
        st.write("")
        st.write("")
        search_food = st.button(
            "🔎 Search",
            type="primary",
            use_container_width=True,
            key="search_food_restaurants"
        )

    if search_food:

        if not city.strip():
            st.warning("Please enter a city.")
        else:
            response = api_post(
                "/food/restaurants/search",
                {"city": city.strip()}
            )

            if response:
                if response.status_code == 200:
                    st.session_state.food_restaurants = response.json()
                    st.session_state.selected_restaurant = None
                    st.session_state.food_menu = []
                    st.session_state.food_cart = []

                    if not st.session_state.food_restaurants:
                        st.warning(
                            f"No restaurants found in {city.strip()}."
                        )
                else:
                    st.error(
                        get_json(response).get(
                            "detail",
                            "Restaurant search failed."
                        )
                    )

    # ========================================================
    # RESTAURANT LIST
    # ========================================================

    if st.session_state.food_restaurants and not st.session_state.selected_restaurant:

        st.divider()
        st.subheader("🏪 Restaurants")

        for restaurant in st.session_state.food_restaurants:

            with st.container(border=True):

                col1, col2, col3 = st.columns([3, 2, 1])

                with col1:
                    st.markdown(
                        f"### 🍽️ {restaurant['name']}"
                    )
                    st.write(
                        f"🍴 **{restaurant['cuisine']}**"
                    )
                    st.caption(
                        f"📍 {restaurant['address']}"
                    )
                    if restaurant.get("description"):
                        st.caption(restaurant["description"])

                with col2:
                    st.write(
                        f"⭐ Rating: **{restaurant['rating']:.1f}/5**"
                    )
                    st.write(
                        f"⏱️ Delivery: **{restaurant['delivery_time']} min**"
                    )
                    if restaurant.get("is_open"):
                        st.success("🟢 Open")
                    else:
                        st.error("🔴 Closed")

                with col3:
                    if st.button(
                        "View Menu",
                        key=f"view_restaurant_{restaurant['id']}",
                        use_container_width=True,
                        disabled=not restaurant.get("is_open", False)
                    ):
                        response = api_get(
                            f"/food/menu/{restaurant['id']}"
                        )

                        if response and response.status_code == 200:
                            st.session_state.selected_restaurant = restaurant
                            st.session_state.food_menu = response.json()
                            st.session_state.food_cart = []
                            st.rerun()
                        elif response:
                            st.error(
                                get_json(response).get(
                                    "detail",
                                    "Unable to load menu."
                                )
                            )

    # ========================================================
    # RESTAURANT MENU
    # ========================================================

    if st.session_state.selected_restaurant:

        restaurant = st.session_state.selected_restaurant

        st.divider()

        header_col1, header_col2 = st.columns([4, 1])

        with header_col1:
            st.subheader(f"🍽️ {restaurant['name']} - Menu")
            st.caption(
                f"{restaurant['cuisine']} • ⭐ {restaurant['rating']:.1f}/5 • "
                f"⏱️ {restaurant['delivery_time']} min"
            )

        with header_col2:
            if st.button(
                "← Restaurants",
                use_container_width=True,
                key="back_to_food_restaurants"
            ):
                st.session_state.selected_restaurant = None
                st.session_state.food_menu = []
                st.session_state.food_cart = []
                st.rerun()

        available_items = [
            item for item in st.session_state.food_menu
            if item.get("is_available", False)
        ]

        if not available_items:
            st.info("No food items are currently available.")
        else:
            categories = []
            for item in available_items:
                if item["category"] not in categories:
                    categories.append(item["category"])

            for category in categories:

                st.markdown(f"### {category}")

                category_items = [
                    item for item in available_items
                    if item["category"] == category
                ]

                for item in category_items:

                    with st.container(border=True):

                        col1, col2, col3 = st.columns([4, 1.5, 1.2])

                        with col1:
                            st.markdown(
                                f"**{item['name']}**"
                            )
                            if item.get("description"):
                                st.caption(item["description"])

                        with col2:
                            st.write(
                                f"💰 **₹{item['price']:,}**"
                            )

                        with col3:
                            if st.button(
                                "➕ Add",
                                key=f"add_food_{item['id']}",
                                use_container_width=True
                            ):
                                existing = next(
                                    (
                                        cart_item
                                        for cart_item in st.session_state.food_cart
                                        if cart_item["id"] == item["id"]
                                    ),
                                    None
                                )

                                if existing:
                                    existing["quantity"] += 1
                                else:
                                    st.session_state.food_cart.append({
                                        "id": item["id"],
                                        "name": item["name"],
                                        "price": item["price"],
                                        "quantity": 1
                                    })

                                st.rerun()

        # ====================================================
        # CART
        # ====================================================

        st.divider()
        st.subheader("🛒 Your Cart")

        if not st.session_state.food_cart:
            st.info("Your cart is empty. Add some delicious food! 🍕")
        else:

            cart_total = 0

            for cart_item in st.session_state.food_cart:

                subtotal = cart_item["price"] * cart_item["quantity"]
                cart_total += subtotal

                with st.container(border=True):

                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                    with col1:
                        st.write(f"🍽️ **{cart_item['name']}**")
                        st.caption(
                            f"₹{cart_item['price']:,} × {cart_item['quantity']}"
                        )

                    with col2:
                        if st.button(
                            "➖",
                            key=f"minus_food_{cart_item['id']}",
                            use_container_width=True
                        ):
                            cart_item["quantity"] -= 1
                            if cart_item["quantity"] <= 0:
                                st.session_state.food_cart.remove(cart_item)
                            st.rerun()

                    with col3:
                        st.write(f"**{cart_item['quantity']}**")

                    with col4:
                        if st.button(
                            "➕",
                            key=f"plus_food_{cart_item['id']}",
                            use_container_width=True
                        ):
                            cart_item["quantity"] += 1
                            st.rerun()

            st.success(
                f"🧾 Cart Total: **₹{cart_total:,}**"
            )

            # =================================================
            # CHECKOUT
            # =================================================

            st.subheader("🧾 Checkout")

            col1, col2 = st.columns(2)

            with col1:
                customer_name = st.text_input(
                    "Customer Name",
                    value=st.session_state.user.get("name", "") if st.session_state.user else "",
                    key="food_customer_name"
                )

            with col2:
                customer_phone = st.text_input(
                    "Phone Number",
                    key="food_customer_phone"
                )

            delivery_address = st.text_area(
                "📍 Delivery Address",
                placeholder="Enter your complete delivery address",
                key="food_delivery_address"
            )

            wallet_response = api_get("/wallet/")
            wallet_balance = 0.0

            if wallet_response and wallet_response.status_code == 200:
                wallet_data = get_json(wallet_response)
                wallet_balance = float(wallet_data.get("balance", 0))

            st.write(
                f"💳 TRAVELX Wallet Balance: **₹{wallet_balance:,.2f}**"
            )

            payment_method = st.radio(
                "Payment Method",
                ["TRAVELX Wallet", "Demo Payment"],
                horizontal=True,
                key="food_payment_method"
            )

            if payment_method == "TRAVELX Wallet" and wallet_balance < cart_total:
                st.warning(
                    f"Insufficient wallet balance. You need ₹{cart_total - wallet_balance:,.2f} more."
                )

            if st.button(
                "🍔 Place Food Order",
                type="primary",
                use_container_width=True,
                key="place_food_order"
            ):

                if not customer_name.strip():
                    st.warning("Please enter customer name.")
                elif not customer_phone.strip():
                    st.warning("Please enter phone number.")
                elif not delivery_address.strip():
                    st.warning("Please enter delivery address.")
                elif payment_method == "TRAVELX Wallet" and wallet_balance < cart_total:
                    st.error("Insufficient wallet balance. Please add money first.")
                else:

                    backend_payment_method = (
                        "wallet"
                        if payment_method == "TRAVELX Wallet"
                        else "demo"
                    )

                    response = api_post(
                        "/food/orders",
                        {
                            "restaurant_id": restaurant["id"],
                            "customer_name": customer_name.strip(),
                            "customer_phone": customer_phone.strip(),
                            "delivery_address": delivery_address.strip(),
                            "items": [
                                {
                                    "food_item_id": item["id"],
                                    "quantity": item["quantity"]
                                }
                                for item in st.session_state.food_cart
                            ],
                            "payment_method": backend_payment_method
                        }
                    )

                    if response:

                        if response.status_code in [200, 201]:

                            order = response.json()

                            st.success("🎉 Food Order Confirmed!")

                            st.write(
                                f"**Order ID:** #{order['id']}"
                            )
                            st.write(
                                f"**Restaurant:** {restaurant['name']}"
                            )
                            st.write(
                                f"**Customer:** {order['customer_name']}"
                            )
                            st.write(
                                f"**Delivery Address:** {order['delivery_address']}"
                            )
                            st.write(
                                f"**Total Paid:** ₹{order['total_price']:,}"
                            )
                            st.write(
                                f"**Payment:** {order['payment_method'].upper()}"
                            )

                            st.success(
                                "🍔 Your food order has been placed successfully!"
                            )

                            st.session_state.food_cart = []
                            st.session_state.selected_restaurant = None
                            st.session_state.food_menu = []
                            st.session_state.food_restaurants = []
                            st.session_state.page = "My Bookings"
                            st.rerun()

                        else:
                            st.error(
                                get_json(response).get(
                                    "detail",
                                    "Food order failed."
                                )
                            )

elif st.session_state.page == "Movies":

    st.title("🎬 Movie Tickets")
    st.caption("Find movies, choose a cinema and show, select your seats and book your tickets.")
    st.divider()

    # ========================================================
    # MOVIE SEARCH
    # ========================================================

    st.subheader("🔎 Find Movies")

    col1, col2, col3 = st.columns([1.5, 1, 1])

    with col1:
        movie_city = st.text_input(
            "📍 City",
            value=st.session_state.movie_city,
            placeholder="Example: Mumbai",
            key="movie_city_input"
        )

    with col2:
        movie_language = st.selectbox(
            "Language",
            ["All", "Hindi", "English"],
            key="movie_language"
        )

    with col3:
        movie_genre = st.selectbox(
            "Genre",
            ["All", "Action", "Romance", "Comedy", "Thriller", "Sci-Fi", "Adventure", "Drama"],
            key="movie_genre"
        )

    if st.button("🔎 Search Movies", type="primary", use_container_width=True, key="search_movies_button"):
        if not movie_city.strip():
            st.warning("Please enter a city.")
        else:
            response = api_post(
                "/movies/search",
                {
                    "city": movie_city.strip(),
                    "language": None if movie_language == "All" else movie_language,
                    "genre": None if movie_genre == "All" else movie_genre
                }
            )

            if response and response.status_code == 200:
                st.session_state.movie_city = movie_city.strip()
                st.session_state.movie_results = response.json()
                st.session_state.selected_movie = None
                st.session_state.movie_cinemas = []
                st.session_state.selected_cinema = None
                st.session_state.movie_shows = []
                st.session_state.selected_show = None
                st.session_state.selected_movie_seats = []

                # The movie search endpoint filters language/genre.
                # Filter the results again so the selected city only
                # shows movies that have available cinema shows there.
                cinema_response = api_post(
                    "/movies/cinemas/search",
                    {"city": movie_city.strip()}
                )

                if cinema_response and cinema_response.status_code == 200:
                    city_cinemas = cinema_response.json()
                    city_movie_ids = set()

                    for city_cinema in city_cinemas:
                        shows_response = api_get(
                            f"/movies/shows/cinema/{city_cinema['id']}"
                        )

                        if shows_response and shows_response.status_code == 200:
                            for show in get_json(shows_response):
                                city_movie_ids.add(show["movie_id"])

                    st.session_state.movie_results = [
                        movie
                        for movie in st.session_state.movie_results
                        if movie["id"] in city_movie_ids
                    ]

                if not st.session_state.movie_results:
                    st.warning(
                        f"No movies with available shows found in "
                        f"{movie_city.strip()} for the selected filters."
                    )
            elif response:
                st.error(get_json(response).get("detail", "Movie search failed."))

    # ========================================================
    # MOVIE LIST
    # ========================================================

    if st.session_state.movie_results and not st.session_state.selected_movie:
        st.divider()
        st.subheader("🎞️ Now Showing")

        for movie in st.session_state.movie_results:
            with st.container(border=True):
                col1, col2, col3 = st.columns([4, 2, 1])

                with col1:
                    st.markdown(f"### 🎬 {movie['title']}")
                    st.write(f"🎭 **{movie['genre']}**  •  🗣️ **{movie['language']}**")
                    st.caption(movie.get("description", ""))

                with col2:
                    st.write(f"⭐ Rating: **{movie['rating']:.1f}/5**")
                    st.write(f"⏱️ Duration: **{movie['duration_minutes']} min**")
                    if movie.get("release_date"):
                        st.write(f"📅 Release: **{movie['release_date']}**")

                with col3:
                    if st.button("View Shows", key=f"movie_select_{movie['id']}", use_container_width=True):
                        st.session_state.selected_movie = movie

                        # Only show cinemas that have this movie.
                        show_response = api_get(
                            f"/movies/shows/movie/{movie['id']}"
                        )

                        if show_response and show_response.status_code == 200:
                            movie_shows = get_json(show_response)

                            movie_cinema_ids = {
                                show["cinema_id"]
                                for show in movie_shows
                            }

                            cinema_response = api_post(
                                "/movies/cinemas/search",
                                {"city": st.session_state.movie_city}
                            )

                            if cinema_response and cinema_response.status_code == 200:
                                city_cinemas = cinema_response.json()

                                st.session_state.movie_cinemas = [
                                    cinema
                                    for cinema in city_cinemas
                                    if cinema["id"] in movie_cinema_ids
                                ]

                                st.session_state.selected_cinema = None
                                st.session_state.movie_shows = []
                                st.session_state.selected_show = None
                                st.session_state.selected_movie_seats = []
                                st.rerun()

                            elif cinema_response:
                                st.error(
                                    get_json(cinema_response).get(
                                        "detail",
                                        "Unable to load cinemas."
                                    )
                                )

                        elif show_response:
                            st.error(
                                get_json(show_response).get(
                                    "detail",
                                    "Unable to load movie shows."
                                )
                            )

    # ========================================================
    # CINEMA SELECTION
    # ========================================================

    if st.session_state.selected_movie and not st.session_state.selected_cinema:
        movie = st.session_state.selected_movie
        st.divider()
        st.subheader(f"🏢 Select Cinema — {movie['title']}")

        if st.button("← Back to Movies", key="back_to_movies"):
            st.session_state.selected_movie = None
            st.session_state.movie_cinemas = []
            st.rerun()

        if not st.session_state.movie_cinemas:
            st.info("No cinemas found in this city.")
        else:
            for cinema in st.session_state.movie_cinemas:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([4, 3, 1])
                    with col1:
                        st.markdown(f"### 🏢 {cinema['name']}")
                        st.caption(f"📍 {cinema['address']}")
                    with col2:
                        st.write(f"City: **{cinema['city']}**")
                        st.write(f"💺 Seats: **{cinema['total_seats']}**")
                    with col3:
                        if st.button("Show Times", key=f"cinema_select_{cinema['id']}", use_container_width=True):
                            response = api_get(f"/movies/shows/cinema/{cinema['id']}")
                            if response and response.status_code == 200:
                                all_shows = response.json()
                                st.session_state.movie_shows = [
                                    show for show in all_shows if show["movie_id"] == movie["id"]
                                ]
                                st.session_state.selected_cinema = cinema
                                st.session_state.selected_show = None
                                st.session_state.selected_movie_seats = []
                                st.rerun()
                            elif response:
                                st.error(get_json(response).get("detail", "Unable to load shows."))

    # ========================================================
    # SHOW SELECTION
    # ========================================================

    if st.session_state.selected_movie and st.session_state.selected_cinema and not st.session_state.selected_show:
        movie = st.session_state.selected_movie
        cinema = st.session_state.selected_cinema

        st.divider()
        st.subheader(f"🕐 Select Show — {movie['title']}")
        st.caption(f"🏢 {cinema['name']} • 📍 {cinema['city']}")

        if st.button("← Back to Cinemas", key="back_to_cinemas"):
            st.session_state.selected_cinema = None
            st.session_state.movie_shows = []
            st.rerun()

        if not st.session_state.movie_shows:
            st.warning("No available shows for this movie at this cinema.")
        else:
            for show in st.session_state.movie_shows:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([1.4, 1.4, 1.4, 1])
                    with col1:
                        st.write(f"📅 **{show['show_date']}**")
                    with col2:
                        st.write(f"🕐 **{show['show_time']}**")
                    with col3:
                        st.write(f"💺 **{show['available_seats']}** seats")
                        st.write(f"💰 **₹{show['ticket_price']:,}** / ticket")
                    with col4:
                        if st.button("Select", key=f"show_select_{show['id']}", use_container_width=True):
                            st.session_state.selected_show = show
                            st.session_state.selected_movie_seats = []
                            st.rerun()

    # ========================================================
    # SEAT SELECTION
    # ========================================================

    if st.session_state.selected_show:
        movie = st.session_state.selected_movie
        cinema = st.session_state.selected_cinema
        show = st.session_state.selected_show

        st.divider()
        st.subheader("💺 Select Your Seats")
        st.caption(
            f"🎬 {movie['title']} • {cinema['name']} • "
            f"{show['show_date']} • {show['show_time']}"
        )

        if st.button("← Back to Shows", key="back_to_shows"):
            st.session_state.selected_show = None
            st.session_state.selected_movie_seats = []
            st.rerun()

        st.info(
            f"💰 Ticket price: **₹{show['ticket_price']:,}** • "
            f"Available seats: **{show['available_seats']}**"
        )

        # Generate a clean cinema-style seat map from the show's capacity.
        total_seats = int(show.get("total_seats", 0))
        available_seats = int(show.get("available_seats", total_seats))
        seat_labels = []
        row_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for number in range(1, total_seats + 1):
            row_index = (number - 1) // 10
            seat_number = ((number - 1) % 10) + 1
            row_name = row_letters[row_index] if row_index < len(row_letters) else f"R{row_index + 1}"
            seat_labels.append(f"{row_name}{seat_number}")

        # Existing backend currently exposes available_seats as a count.
        # The first available seats are therefore selectable in this UI.
        selectable_labels = seat_labels[:available_seats]

        st.markdown("#### 🎥 SCREEN")
        st.progress(1.0)
        st.caption("Select the seats you want to book. Selected seats are highlighted by Streamlit.")

        for row_start in range(0, len(seat_labels), 10):
            row_seats = seat_labels[row_start:row_start + 10]
            cols = st.columns(10)
            for idx, seat in enumerate(row_seats):
                with cols[idx]:
                    disabled = seat not in selectable_labels
                    selected = seat in st.session_state.selected_movie_seats
                    button_label = f"✅ {seat}" if selected else seat
                    if st.button(
                        button_label,
                        key=f"movie_seat_{show['id']}_{seat}",
                        disabled=disabled,
                        use_container_width=True
                    ):
                        if seat in st.session_state.selected_movie_seats:
                            st.session_state.selected_movie_seats.remove(seat)
                        else:
                            st.session_state.selected_movie_seats.append(seat)
                        st.rerun()

        selected_seats = st.session_state.selected_movie_seats
        total_price = len(selected_seats) * int(show["ticket_price"])

        st.divider()
        if selected_seats:
            st.success(
                f"💺 Selected: **{', '.join(selected_seats)}**  •  "
                f"🎟️ Tickets: **{len(selected_seats)}**  •  "
                f"💰 Total: **₹{total_price:,}**"
            )
        else:
            st.info("Please select at least one seat to continue.")

        # ====================================================
        # PASSENGER + PAYMENT
        # ====================================================

        if selected_seats:
            st.subheader("👤 Passenger Details")
            col1, col2 = st.columns(2)

            with col1:
                movie_customer_name = st.text_input(
                    "Customer Name",
                    value=st.session_state.user.get("name", "") if st.session_state.user else "",
                    key="movie_customer_name"
                )

            with col2:
                movie_customer_phone = st.text_input(
                    "Phone Number",
                    key="movie_customer_phone"
                )

            wallet_response = api_get("/wallet/")
            movie_wallet_balance = 0.0
            if wallet_response and wallet_response.status_code == 200:
                movie_wallet_data = get_json(wallet_response)
                movie_wallet_balance = float(movie_wallet_data.get("balance", 0))

            st.subheader("💳 Payment Method")
            movie_payment_method = st.radio(
                "Choose payment method",
                ["TRAVELX Wallet", "Demo Payment"],
                horizontal=True,
                key="movie_payment_method"
            )

            if movie_payment_method == "TRAVELX Wallet":
                st.info(f"💰 Wallet Balance: **₹{movie_wallet_balance:,.2f}**")
                if movie_wallet_balance >= total_price:
                    st.success(f"After payment: **₹{movie_wallet_balance - total_price:,.2f}**")
                else:
                    st.error(f"Insufficient wallet balance. You need ₹{total_price - movie_wallet_balance:,.2f} more.")
            else:
                st.warning("🧪 Demo Payment does not deduct money from your TRAVELX Wallet.")

            if st.button(
                "🎟️ Confirm Movie Booking",
                type="primary",
                use_container_width=True,
                key="confirm_movie_booking"
            ):
                if not movie_customer_name.strip():
                    st.warning("Please enter customer name.")
                elif not movie_customer_phone.strip():
                    st.warning("Please enter phone number.")
                elif movie_payment_method == "TRAVELX Wallet" and movie_wallet_balance < total_price:
                    st.error("Insufficient wallet balance. Please add money first.")
                else:
                    selected_payment = "wallet" if movie_payment_method == "TRAVELX Wallet" else "demo"
                    response = api_post(
                        "/movies/book",
                        {
                            "movie_id": movie["id"],
                            "cinema_id": cinema["id"],
                            "show_id": show["id"],
                            "customer_name": movie_customer_name.strip(),
                            "customer_phone": movie_customer_phone.strip(),
                            "seats": selected_seats,
                            "payment_method": selected_payment
                        }
                    )

                    if response and response.status_code in [200, 201]:
                        booking = response.json()
                        st.success("🎉 Movie Ticket Booking Confirmed!")
                        st.write(f"**Booking ID:** #{booking['id']}")
                        st.write(f"**Movie:** {movie['title']}")
                        st.write(f"**Cinema:** {cinema['name']}")
                        st.write(f"**Date & Time:** {booking['show_date']} • {booking['show_time']}")
                        st.write(f"**Seats:** {booking['seats']}")
                        st.write(f"**Tickets:** {booking['number_of_seats']}")
                        st.write(f"**Total Paid:** ₹{booking['total_price']:,}")
                        st.write(f"**Payment:** {booking['payment_method'].upper()}")

                        st.session_state.selected_movie = None
                        st.session_state.movie_results = []
                        st.session_state.movie_cinemas = []
                        st.session_state.selected_cinema = None
                        st.session_state.movie_shows = []
                        st.session_state.selected_show = None
                        st.session_state.selected_movie_seats = []
                        st.session_state.page = "My Bookings"
                        st.rerun()
                    elif response:
                        st.error(get_json(response).get("detail", "Movie booking failed."))



# ============================================================
# EVENTS
# ============================================================

elif st.session_state.page == "Events":

    st.title("🎟️ Events")

    st.caption(
        "Discover concerts, comedy shows, festivals, workshops and live experiences."
    )

    st.divider()

    # ========================================================
    # SEARCH EVENTS
    # ========================================================

    st.subheader("🔎 Discover Events")

    col1, col2, col3 = st.columns([1.5, 1, 1])

    with col1:
        event_city = st.text_input(
            "📍 City",
            value=st.session_state.event_city,
            placeholder="Example: Mumbai",
            key="event_city_input"
        )

    with col2:
        event_category = st.selectbox(
            "Category",
            [
                "All",
                "Music",
                "Concert",
                "Comedy",
                "Sports",
                "Entertainment",
                "Business",
                "Workshop",
                "Festival"
            ],
            key="event_category"
        )

    with col3:
        event_language = st.selectbox(
            "Language",
            [
                "All",
                "Hindi",
                "English"
            ],
            key="event_language"
        )

    if st.button(
        "🔎 Search Events",
        type="primary",
        use_container_width=True,
        key="search_events_button"
    ):

        if not event_city.strip():

            st.warning("Please enter a city.")

        else:

            response = api_post(
                "/events/search",
                {
                    "city": event_city.strip(),
                    "category": (
                        None
                        if event_category == "All"
                        else event_category
                    ),
                    "language": (
                        None
                        if event_language == "All"
                        else event_language
                    )
                }
            )

            if response and response.status_code == 200:

                st.session_state.event_city = event_city.strip()

                all_events = response.json()

                # ------------------------------------------------
                # Find events that actually have shows in city
                # ------------------------------------------------

                venue_response = api_post(
                    "/events/venues/search",
                    {
                        "city": event_city.strip()
                    }
                )

                city_event_ids = set()

                if venue_response and venue_response.status_code == 200:

                    city_venues = venue_response.json()

                    for venue in city_venues:

                        shows_response = api_get(
                            f"/events/shows/venue/{venue['id']}"
                        )

                        if (
                            shows_response
                            and shows_response.status_code == 200
                        ):

                            for show in get_json(
                                shows_response
                            ):

                                city_event_ids.add(
                                    show["event_id"]
                                )

                    st.session_state.event_results = [
                        event
                        for event in all_events
                        if event["id"] in city_event_ids
                    ]

                else:

                    st.session_state.event_results = all_events

                st.session_state.selected_event = None
                st.session_state.event_venues = []
                st.session_state.selected_event_venue = None
                st.session_state.event_shows = []
                st.session_state.selected_event_show = None

                if not st.session_state.event_results:

                    st.warning(
                        f"No events with available shows found in "
                        f"{event_city.strip()}."
                    )

            elif response:

                st.error(
                    get_json(response).get(
                        "detail",
                        "Event search failed."
                    )
                )

    # ========================================================
    # EVENT LIST
    # ========================================================

    if (
        st.session_state.event_results
        and not st.session_state.selected_event
    ):

        st.divider()

        st.subheader("🎉 Available Events")

        for event in st.session_state.event_results:

            with st.container(border=True):

                col1, col2, col3 = st.columns([4, 2, 1])

                with col1:

                    st.markdown(
                        f"### 🎟️ {event['name']}"
                    )

                    st.write(
                        f"🎭 **{event['category']}**"
                        f"  •  🗣️ **{event['language']}**"
                    )

                    if event.get("description"):

                        st.caption(
                            event["description"]
                        )

                with col2:

                    st.write(
                        f"⭐ Rating: "
                        f"**{event['rating']:.1f}/5**"
                    )

                    st.write(
                        f"⏱️ Duration: "
                        f"**{event['duration_minutes']} min**"
                    )

                with col3:

                    if st.button(
                        "View Shows",
                        key=f"event_select_{event['id']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_event = event

                        show_response = api_get(
                            f"/events/shows/event/{event['id']}"
                        )

                        if (
                            show_response
                            and show_response.status_code == 200
                        ):

                            event_shows = get_json(
                                show_response
                            )

                            venue_ids = {
                                show["venue_id"]
                                for show in event_shows
                            }

                            venue_response = api_post(
                                "/events/venues/search",
                                {
                                    "city": st.session_state.event_city
                                }
                            )

                            if (
                                venue_response
                                and venue_response.status_code == 200
                            ):

                                city_venues = venue_response.json()

                                st.session_state.event_venues = [
                                    venue
                                    for venue in city_venues
                                    if venue["id"] in venue_ids
                                ]

                                st.session_state.selected_event_venue = None
                                st.session_state.event_shows = []
                                st.session_state.selected_event_show = None

                                st.rerun()

                        elif show_response:

                            st.error(
                                get_json(show_response).get(
                                    "detail",
                                    "Unable to load event shows."
                                )
                            )

    # ========================================================
    # VENUE SELECTION
    # ========================================================

    if (
        st.session_state.selected_event
        and not st.session_state.selected_event_venue
    ):

        event = st.session_state.selected_event

        st.divider()

        st.subheader(
            f"🏟️ Select Venue — {event['name']}"
        )

        if st.button(
            "← Back to Events",
            key="back_to_events"
        ):

            st.session_state.selected_event = None
            st.session_state.event_venues = []
            st.session_state.event_shows = []

            st.rerun()

        if not st.session_state.event_venues:

            st.info(
                "No venues found for this event."
            )

        else:

            for venue in st.session_state.event_venues:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [4, 3, 1]
                    )

                    with col1:

                        st.markdown(
                            f"### 🏟️ {venue['name']}"
                        )

                        st.caption(
                            f"📍 {venue['address']}"
                        )

                    with col2:

                        st.write(
                            f"City: **{venue['city']}**"
                        )

                        st.write(
                            f"👥 Capacity: "
                            f"**{venue['capacity']}**"
                        )

                    with col3:

                        if st.button(
                            "Show Times",
                            key=f"event_venue_{venue['id']}",
                            use_container_width=True
                        ):

                            response = api_get(
                                f"/events/shows/venue/{venue['id']}"
                            )

                            if (
                                response
                                and response.status_code == 200
                            ):

                                all_shows = response.json()

                                st.session_state.event_shows = [
                                    show
                                    for show in all_shows
                                    if show["event_id"] == event["id"]
                                ]

                                st.session_state.selected_event_venue = venue
                                st.session_state.selected_event_show = None

                                st.rerun()

                            elif response:

                                st.error(
                                    get_json(response).get(
                                        "detail",
                                        "Unable to load event shows."
                                    )
                                )

    # ========================================================
    # SHOW / TICKET TYPE SELECTION
    # ========================================================

    if (
        st.session_state.selected_event
        and st.session_state.selected_event_venue
        and not st.session_state.selected_event_show
    ):

        event = st.session_state.selected_event
        venue = st.session_state.selected_event_venue

        st.divider()

        st.subheader(
            f"🎫 Select Show — {event['name']}"
        )

        st.caption(
            f"🏟️ {venue['name']} • 📍 {venue['city']}"
        )

        if st.button(
            "← Back to Venues",
            key="back_to_event_venues"
        ):

            st.session_state.selected_event_venue = None
            st.session_state.event_shows = []

            st.rerun()

        if not st.session_state.event_shows:

            st.warning(
                "No available shows for this event at this venue."
            )

        else:

            for show in st.session_state.event_shows:

                with st.container(border=True):

                    col1, col2, col3, col4 = st.columns(
                        [1.4, 1.4, 1.8, 1]
                    )

                    with col1:

                        st.write(
                            f"📅 **{show['show_date']}**"
                        )

                    with col2:

                        st.write(
                            f"🕐 **{show['show_time']}**"
                        )

                    with col3:

                        st.write(
                            f"🎫 **{show['ticket_type']}**"
                        )

                        st.write(
                            f"💰 **₹{show['ticket_price']:,}** / ticket"
                        )

                        st.caption(
                            f"Available: {show['available_tickets']}"
                        )

                    with col4:

                        if st.button(
                            "Select",
                            key=f"event_show_{show['id']}",
                            use_container_width=True
                        ):

                            st.session_state.selected_event_show = show

                            st.rerun()

    # ========================================================
    # EVENT BOOKING
    # ========================================================

    if (
        st.session_state.selected_event
        and st.session_state.selected_event_venue
        and st.session_state.selected_event_show
    ):

        event = st.session_state.selected_event
        venue = st.session_state.selected_event_venue
        show = st.session_state.selected_event_show

        st.divider()

        st.subheader(
            "🎟️ Complete Your Event Booking"
        )

        st.info(
            f"🎟️ **{event['name']}** | "
            f"🏟️ {venue['name']} | "
            f"📅 {show['show_date']} | "
            f"🕐 {show['show_time']} | "
            f"🎫 {show['ticket_type']}"
        )

        # ----------------------------------------------------
        # CUSTOMER DETAILS
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            event_customer_name = st.text_input(
                "Customer Name",
                value=(
                    st.session_state.user.get("name", "")
                    if st.session_state.user
                    else ""
                ),
                key="event_customer_name"
            )

        with col2:

            event_customer_phone = st.text_input(
                "Phone Number",
                key="event_customer_phone"
            )

        # ----------------------------------------------------
        # NUMBER OF TICKETS
        # ----------------------------------------------------

        event_ticket_count = st.number_input(
            "🎫 Number of Tickets",
            min_value=1,
            max_value=int(show["available_tickets"]),
            value=1,
            step=1,
            key="event_ticket_count"
        )

        event_total_price = (
            show["ticket_price"]
            * int(event_ticket_count)
        )

        st.success(
            f"💰 Total Price: "
            f"**₹{event_total_price:,}**"
        )

        st.caption(
            f"₹{show['ticket_price']:,} × "
            f"{int(event_ticket_count)} ticket(s)"
        )

        # ----------------------------------------------------
        # WALLET
        # ----------------------------------------------------

        wallet_response = api_get(
            "/wallet/"
        )

        wallet_balance = 0.0

        if (
            wallet_response
            and wallet_response.status_code == 200
        ):

            wallet_data = get_json(
                wallet_response
            )

            wallet_balance = float(
                wallet_data.get(
                    "balance",
                    0
                )
            )

        # ----------------------------------------------------
        # PAYMENT
        # ----------------------------------------------------

        st.subheader(
            "💳 Payment Method"
        )

        event_payment_method = st.radio(
            "Choose payment method",
            [
                "TRAVELX Wallet",
                "Demo Payment"
            ],
            key="event_payment_method"
        )

        if event_payment_method == "TRAVELX Wallet":

            st.info(
                f"💰 Wallet Balance: "
                f"**₹{wallet_balance:,.2f}**"
            )

            if wallet_balance >= event_total_price:

                remaining_balance = (
                    wallet_balance
                    - event_total_price
                )

                st.success(
                    f"After payment: "
                    f"**₹{remaining_balance:,.2f}**"
                )

            else:

                shortage = (
                    event_total_price
                    - wallet_balance
                )

                st.error(
                    f"Insufficient wallet balance. "
                    f"You need ₹{shortage:,.2f} more."
                )

        else:

            st.warning(
                "Demo Payment does not deduct money "
                "from your TRAVELX Wallet."
            )

        # ----------------------------------------------------
        # CONFIRM
        # ----------------------------------------------------

        if st.button(
            "🎟️ Confirm Event Booking",
            type="primary",
            use_container_width=True,
            key="confirm_event_booking"
        ):

            if not event_customer_name.strip():

                st.warning(
                    "Please enter customer name."
                )

            elif not event_customer_phone.strip():

                st.warning(
                    "Please enter phone number."
                )

            elif (
                event_payment_method == "TRAVELX Wallet"
                and wallet_balance < event_total_price
            ):

                st.error(
                    "Insufficient wallet balance. "
                    "Please add money first."
                )

            else:

                selected_payment = (
                    "wallet"
                    if event_payment_method == "TRAVELX Wallet"
                    else "demo"
                )

                response = api_post(
                    "/events/book",
                    {
                        "event_id": event["id"],
                        "venue_id": venue["id"],
                        "show_id": show["id"],
                        "customer_name": event_customer_name.strip(),
                        "customer_phone": event_customer_phone.strip(),
                        "number_of_tickets": int(event_ticket_count),
                        "payment_method": selected_payment
                    }
                )

                if (
                    response
                    and response.status_code in [200, 201]
                ):

                    booking = response.json()

                    st.success(
                        "🎉 Event Booking Confirmed!"
                    )

                    st.write(
                        f"**Booking ID:** "
                        f"#{booking['id']}"
                    )

                    st.write(
                        f"**Event:** "
                        f"{event['name']}"
                    )

                    st.write(
                        f"**Venue:** "
                        f"{venue['name']}"
                    )

                    st.write(
                        f"**Date & Time:** "
                        f"{booking['show_date']} • "
                        f"{booking['show_time']}"
                    )

                    st.write(
                        f"**Ticket Type:** "
                        f"{booking['ticket_type']}"
                    )

                    st.write(
                        f"**Tickets:** "
                        f"{booking['number_of_tickets']}"
                    )

                    st.write(
                        f"**Total Paid:** "
                        f"₹{booking['total_price']:,}"
                    )

                    st.write(
                        f"**Payment:** "
                        f"{booking['payment_method'].upper()}"
                    )

                    if selected_payment == "wallet":

                        st.success(
                            "💳 Payment completed "
                            "using TRAVELX Wallet."
                        )

                    else:

                        st.info(
                            "🧪 Demo payment completed."
                        )

                    st.session_state.event_results = []
                    st.session_state.event_city = ""
                    st.session_state.selected_event = None
                    st.session_state.event_venues = []
                    st.session_state.selected_event_venue = None
                    st.session_state.event_shows = []
                    st.session_state.selected_event_show = None

                    st.session_state.page = "My Bookings"

                    st.rerun()

                elif response:

                    st.error(
                        get_json(response).get(
                            "detail",
                            "Event booking failed."
                        )
                    )



# ============================================================
# AI TRIP PLANNER
# ============================================================

elif st.session_state.page == "AI Trip Planner":

    st.title("🤖 AI Trip Planner")

    st.caption(
        "Tell TRAVELX where you want to go, and get a personalized day-by-day travel plan."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        destination = st.text_input(
            "📍 Destination",
            placeholder="Example: Goa",
            key="trip_destination"
        )

        starting_city = st.text_input(
            "🚉 Starting City (optional)",
            placeholder="Example: Mumbai",
            key="trip_starting_city"
        )

        days = st.number_input(
            "📅 Number of Days",
            min_value=1,
            max_value=30,
            value=3,
            step=1,
            key="trip_days"
        )

    with col2:

        budget = st.number_input(
            "💰 Total Budget (₹)",
            min_value=1000,
            max_value=10000000,
            value=25000,
            step=1000,
            key="trip_budget"
        )

        travelers = st.number_input(
            "👥 Travelers",
            min_value=1,
            max_value=20,
            value=1,
            step=1,
            key="trip_travelers"
        )

        travel_style = st.selectbox(
            "🎒 Travel Style",
            [
                "Budget",
                "Standard",
                "Luxury",
                "Adventure",
                "Family",
                "Couple"
            ],
            key="trip_style"
        )

    interests = st.text_input(
        "❤️ What are you interested in?",
        value="Sightseeing, food, local experiences",
        placeholder="Beaches, food, nightlife, temples, shopping...",
        key="trip_interests"
    )

    if st.button(
        "✨ Generate My AI Trip Plan",
        type="primary",
        use_container_width=True,
        key="generate_trip_plan"
    ):

        if not destination.strip():
            st.warning("Please enter a destination.")
        else:

            response = api_post(
                "/ai/trip-plan",
                {
                    "destination": destination.strip(),
                    "starting_city": starting_city.strip(),
                    "days": int(days),
                    "budget": int(budget),
                    "travel_style": travel_style,
                    "interests": interests.strip(),
                    "travelers": int(travelers)
                }
            )

            if response and response.status_code in [200, 201]:
                st.session_state.trip_plan = get_json(response)
                st.success("🎉 Your TRAVELX trip plan is ready!")
            elif response:
                st.error(
                    get_json(response).get(
                        "detail",
                        "Unable to generate trip plan."
                    )
                )

    plan = st.session_state.get("trip_plan")

    if plan:

        st.divider()

        if plan.get("ai_powered"):
            st.success("🧠 Powered by Gemini AI")
        else:
            st.info("⚡ Smart TRAVELX planner is being used. Add GEMINI_API_KEY for Gemini AI generation.")

        st.markdown("## 🧳 Your Trip Summary")

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric("Destination", plan.get("destination", destination))

        with m2:
            st.metric("Duration", f"{plan.get('days', days)} Days")

        with m3:
            st.metric("Budget", f"₹{plan.get('budget', budget):,}")

        with m4:
            st.metric("Estimated Total", f"₹{plan.get('estimated_total', 0):,}")

        st.info(plan.get("summary", "Your personalized trip plan is ready."))

        st.markdown("## 🗺️ Day-by-Day Itinerary")

        for day in plan.get("itinerary", []):

            with st.container(border=True):

                st.markdown(
                    f"### Day {day.get('day')} — {day.get('title', 'Explore')}"
                )

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.write("🌅 **Morning**")
                    st.write(day.get("morning", ""))

                with c2:
                    st.write("☀️ **Afternoon**")
                    st.write(day.get("afternoon", ""))

                with c3:
                    st.write("🌙 **Evening**")
                    st.write(day.get("evening", ""))

                st.caption(
                    f"Estimated day cost: ₹{day.get('estimated_cost', 0):,}"
                )

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("## 🚆 Transport")
            for item in plan.get("transport", []):
                st.write(f"• {item}")

            st.markdown("## 🏨 Accommodation")
            for item in plan.get("accommodation", []):
                st.write(f"• {item}")

        with c2:
            st.markdown("## 🍴 Food")
            for item in plan.get("food", []):
                st.write(f"• {item}")

            st.markdown("## 💡 Smart Tips")
            for item in plan.get("tips", []):
                st.write(f"• {item}")

        st.caption(
            "Planning suggestions only. Verify live prices, timings and availability before booking."
        )

        if st.button(
            "🗑️ Clear Trip Plan",
            key="clear_trip_plan"
        ):
            st.session_state.trip_plan = None
            st.rerun()



elif st.session_state.page == "Cabs":

    st.title("🚕 Cab Booking")

    st.caption(
        "Search cabs, compare fares and book your ride."
    )

    st.divider()

    # ========================================================
    # SEARCH CABS
    # ========================================================

    st.subheader("🔎 Search Cabs")

    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input(
            "From",
            placeholder="Example: Mumbai",
            key="cab_source"
        )

    with col2:
        destination = st.text_input(
            "To",
            placeholder="Example: Pune",
            key="cab_destination"
        )

    if st.button(
        "🔎 Search Cabs",
        type="primary",
        use_container_width=True,
        key="search_cabs_button"
    ):

        if not source.strip() or not destination.strip():

            st.warning(
                "Please enter source and destination."
            )

        else:

            response = api_post(
                "/cabs/search",
                {
                    "source": source.strip(),
                    "destination": destination.strip()
                }
            )

            if response:

                if response.status_code == 200:

                    st.session_state.cab_results = (
                        response.json()
                    )

                    st.session_state.selected_cab = None

                    if not st.session_state.cab_results:

                        st.warning(
                            f"No cabs found from "
                            f"{source.strip()} to "
                            f"{destination.strip()}."
                        )

                else:

                    detail = get_json(response).get(
                        "detail",
                        "Cab search failed."
                    )

                    st.error(detail)

    # ========================================================
    # AVAILABLE CABS
    # ========================================================

    if st.session_state.cab_results:

        st.divider()

        st.subheader("🚕 Available Cabs")

        for cab in st.session_state.cab_results:

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [2.2, 2.5, 2, 1]
                )

                # ------------------------------------------------
                # CAB DETAILS
                # ------------------------------------------------

                with col1:

                    st.markdown(
                        f"### 🚕 {cab['cab_type']}"
                    )

                    st.write(
                        f"👤 Driver: **{cab['driver_name']}**"
                    )

                    st.caption(
                        f"🚘 {cab['vehicle_number']}"
                    )

                # ------------------------------------------------
                # ROUTE
                # ------------------------------------------------

                with col2:

                    st.write(
                        f"📍 **{cab['source']} → "
                        f"{cab['destination']}**"
                    )

                    st.write(
                        f"⭐ Rating: **{cab['rating']:.1f} / 5**"
                    )

                # ------------------------------------------------
                # FARE / SEATS
                # ------------------------------------------------

                with col3:

                    st.write(
                        f"💰 Fare: "
                        f"**₹{cab['fare_per_km']}/km**"
                    )

                    st.write(
                        f"💺 Available seats: "
                        f"**{cab['available_seats']}**"
                    )

                # ------------------------------------------------
                # BOOK
                # ------------------------------------------------

                with col4:

                    if st.button(
                        "Book Now",
                        key=f"select_cab_{cab['id']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_cab = cab

                        st.rerun()

    # ========================================================
    # CAB BOOKING FORM
    # ========================================================

    if st.session_state.selected_cab:

        cab = st.session_state.selected_cab

        st.divider()

        st.subheader("🎫 Complete Your Cab Booking")

        st.info(
            f"🚕 **{cab['cab_type']}** | "
            f"🚘 {cab['vehicle_number']} | "
            f"👤 {cab['driver_name']} | "
            f"📍 {cab['source']} → {cab['destination']} | "
            f"₹{cab['fare_per_km']}/km"
        )

        # ====================================================
        # PASSENGER DETAILS
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            passenger_name = st.text_input(
                "Passenger Name",
                key="cab_passenger_name"
            )

        with col2:

            passenger_phone = st.text_input(
                "Passenger Phone",
                key="cab_passenger_phone"
            )

        # ====================================================
        # PICKUP / DROP
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            pickup_location = st.text_input(
                "📍 Pickup Location",
                placeholder="Example: Mumbai Airport",
                key="cab_pickup_location"
            )

        with col2:

            drop_location = st.text_input(
                "📍 Drop Location",
                placeholder="Example: Pune Station",
                key="cab_drop_location"
            )

        # ====================================================
        # DISTANCE
        # ====================================================

        distance_km = st.number_input(
            "🛣️ Distance (km)",
            min_value=1,
            max_value=2000,
            value=150,
            step=1,
            key="cab_distance_km"
        )

        total_price = (
            cab["fare_per_km"] * int(distance_km)
        )

        st.success(
            f"💰 Total Fare: **₹{total_price:,}**"
        )

        st.caption(
            f"₹{cab['fare_per_km']}/km × "
            f"{int(distance_km)} km"
        )

        # ====================================================
        # LIVE WALLET BALANCE
        # ====================================================

        wallet_response = api_get(
            "/wallet/"
        )

        wallet_balance = 0.0

        if (
            wallet_response
            and wallet_response.status_code == 200
        ):

            wallet_data = get_json(
                wallet_response
            )

            wallet_balance = float(
                wallet_data.get(
                    "balance",
                    0
                )
            )

        # ====================================================
        # PAYMENT
        # ====================================================

        st.subheader("💳 Payment Method")

        payment_method = st.radio(
            "Choose payment method",
            [
                "TRAVELX Wallet",
                "Demo Payment"
            ],
            key="cab_payment_method"
        )

        if payment_method == "TRAVELX Wallet":

            st.info(
                f"💰 Wallet Balance: "
                f"**₹{wallet_balance:,.2f}**"
            )

            if wallet_balance >= total_price:

                remaining_balance = (
                    wallet_balance - total_price
                )

                st.success(
                    f"After payment: "
                    f"**₹{remaining_balance:,.2f}**"
                )

            else:

                shortage = (
                    total_price - wallet_balance
                )

                st.error(
                    f"Insufficient wallet balance. "
                    f"You need ₹{shortage:,.2f} more."
                )

        else:

            st.warning(
                "Demo Payment does not deduct money "
                "from your TRAVELX Wallet."
            )

        # ====================================================
        # CONFIRM BOOKING
        # ====================================================

        if st.button(
            "🎟️ Confirm Cab Booking",
            type="primary",
            use_container_width=True,
            key="confirm_cab_booking"
        ):

            if not passenger_name.strip():

                st.warning(
                    "Please enter passenger name."
                )

            elif not passenger_phone.strip():

                st.warning(
                    "Please enter passenger phone."
                )

            elif not pickup_location.strip():

                st.warning(
                    "Please enter pickup location."
                )

            elif not drop_location.strip():

                st.warning(
                    "Please enter drop location."
                )

            elif (
                payment_method == "TRAVELX Wallet"
                and wallet_balance < total_price
            ):

                st.error(
                    "Insufficient wallet balance. "
                    "Please add money to your wallet."
                )

            else:

                backend_payment_method = (
                    "wallet"
                    if payment_method == "TRAVELX Wallet"
                    else "demo"
                )

                response = api_post(
                    "/cabs/book",
                    {
                        "cab_id": cab["id"],
                        "passenger_name": passenger_name.strip(),
                        "passenger_phone": passenger_phone.strip(),
                        "pickup_location": pickup_location.strip(),
                        "drop_location": drop_location.strip(),
                        "distance_km": int(distance_km),
                        "payment_method": backend_payment_method
                    }
                )

                if response:

                    if response.status_code in [200, 201]:

                        booking = response.json()

                        st.success(
                            "🎉 Cab Booking Confirmed!"
                        )

                        st.write(
                            f"**Booking ID:** "
                            f"#{booking['id']}"
                        )

                        st.write(
                            f"**Cab:** "
                            f"{cab['cab_type']} "
                            f"({cab['vehicle_number']})"
                        )

                        st.write(
                            f"**Driver:** "
                            f"{cab['driver_name']}"
                        )

                        st.write(
                            f"**Passenger:** "
                            f"{booking['passenger_name']}"
                        )

                        st.write(
                            f"**Pickup:** "
                            f"{booking['pickup_location']}"
                        )

                        st.write(
                            f"**Drop:** "
                            f"{booking['drop_location']}"
                        )

                        st.write(
                            f"**Distance:** "
                            f"{booking['distance_km']} km"
                        )

                        st.write(
                            f"**Total Paid:** "
                            f"₹{booking['total_price']:,}"
                        )

                        st.write(
                            f"**Payment:** "
                            f"{booking['payment_method'].upper()}"
                        )

                        if backend_payment_method == "wallet":

                            st.success(
                                "💳 Payment completed "
                                "using TRAVELX Wallet."
                            )

                        else:

                            st.info(
                                "🧪 Demo payment completed."
                            )

                        st.session_state.selected_cab = None
                        st.session_state.cab_results = []
                        st.session_state.page = "My Bookings"

                        st.rerun()

                    else:

                        detail = get_json(
                            response
                        ).get(
                            "detail",
                            "Cab booking failed."
                        )

                        st.error(detail)

# ============================================================
# BUSES
# ============================================================

elif st.session_state.page == "Buses":

    st.title("🚌 Bus Booking")

    st.caption(
        "Search available buses and reserve your seats."
    )

    st.divider()


    # ========================================================
    # SEARCH
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        source = st.text_input(
            "From",
            placeholder="Example: Pune",
            key="bus_source"
        )

    with col2:

        destination = st.text_input(
            "To",
            placeholder="Example: Mumbai",
            key="bus_destination"
        )

    travel_date = st.date_input(
        "Travel Date",
        value=date.today(),
        key="bus_travel_date"
    )


    if st.button(
        "🔎 Search Buses",
        type="primary",
        use_container_width=True
    ):

        if not source or not destination:

            st.warning(
                "Please enter source and destination."
            )

        else:

            response = api_post(
                "/buses/search",
                {
                    "source": source,
                    "destination": destination
                }
            )

            if response:

                if response.status_code == 200:

                    st.session_state.bus_results = (
                        response.json()
                    )

                    if not st.session_state.bus_results:

                        st.warning(
                            "No buses found for this route."
                        )

                else:

                    detail = get_json(
                        response
                    ).get(
                        "detail",
                        "Bus search failed."
                    )

                    st.error(detail)


    # ========================================================
    # AVAILABLE BUSES
    # ========================================================

    if st.session_state.bus_results:

        st.subheader(
            "Available Buses"
        )

        for bus in st.session_state.bus_results:

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [2, 2, 2, 1]
                )

                with col1:

                    st.subheader(
                        bus["operator"]
                    )

                    st.write(
                        f"🚌 {bus['bus_number']}"
                    )

                with col2:

                    st.write(
                        f"📍 {bus['source']} → "
                        f"{bus['destination']}"
                    )

                    st.write(
                        f"🕐 {bus['departure_time']} → "
                        f"{bus['arrival_time']}"
                    )

                with col3:

                    st.write(
                        f"💺 Available: "
                        f"**{bus['available_seats']}**"
                    )

                    st.write(
                        f"💰 Price: "
                        f"**₹{bus['price']}**"
                    )

                with col4:

                    if st.button(
                        "Book",
                        key=f"select_bus_{bus['id']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_bus = bus

                        st.rerun()


    # ========================================================
    # PASSENGER DETAILS
    # ========================================================

    if st.session_state.selected_bus:

        bus = st.session_state.selected_bus

        st.divider()

        st.subheader(
            "🎫 Passenger Details"
        )

        st.info(
            f"{bus['operator']} | "
            f"{bus['source']} → "
            f"{bus['destination']} | "
            f"₹{bus['price']} per seat"
        )


        passenger_name = st.text_input(
            "Passenger Name",
            key="bus_passenger_name"
        )

        passenger_phone = st.text_input(
            "Passenger Phone",
            key="bus_passenger_phone"
        )


        seats = st.number_input(
            "Number of Seats",
            min_value=1,
            max_value=int(
                bus["available_seats"]
            ),
            value=1,
            step=1,
            key="bus_seats"
        )


        total_price = (
            bus["price"] * seats
        )


        st.success(
            f"Total Price: ₹{total_price:,}"
        )


        # ====================================================
        # LIVE WALLET BALANCE
        # ====================================================

        wallet_response = api_get(
            "/wallet/"
        )

        wallet_balance = 0.0

        if (
            wallet_response
            and wallet_response.status_code == 200
        ):

            wallet_data = get_json(
                wallet_response
            )

            wallet_balance = float(
                wallet_data.get(
                    "balance",
                    0
                )
            )


        # ====================================================
        # PAYMENT METHOD
        # ====================================================

        st.subheader(
            "💳 Payment Method"
        )

        payment_method = st.radio(
            "Choose payment method",
            [
                "TRAVELX Wallet",
                "Demo Payment"
            ],
            key="bus_payment_method"
        )


        # ====================================================
        # WALLET PAYMENT
        # ====================================================

        if payment_method == "TRAVELX Wallet":

            st.info(
                f"💰 Wallet Balance: "
                f"**₹{wallet_balance:,.2f}**"
            )

            if wallet_balance >= total_price:

                remaining_balance = (
                    wallet_balance - total_price
                )

                st.success(
                    f"After payment: "
                    f"**₹{remaining_balance:,.2f}**"
                )

            else:

                shortage = (
                    total_price - wallet_balance
                )

                st.error(
                    f"Insufficient wallet balance. "
                    f"You need ₹{shortage:,.2f} more."
                )

        else:

            st.warning(
                "Demo Payment does not deduct money "
                "from your TRAVELX Wallet."
            )


        # ====================================================
        # CONFIRM BOOKING
        # ====================================================

        if st.button(
            "🎟️ Confirm Bus Booking",
            type="primary",
            use_container_width=True
        ):

            if not passenger_name:

                st.warning(
                    "Please enter passenger name."
                )

            elif not passenger_phone:

                st.warning(
                    "Please enter passenger phone."
                )

            elif (
                payment_method == "TRAVELX Wallet"
                and wallet_balance < total_price
            ):

                st.error(
                    "Insufficient wallet balance. "
                    "Please add money to your wallet."
                )

            else:

                backend_payment_method = (
                    "wallet"
                    if payment_method == "TRAVELX Wallet"
                    else "demo"
                )


                # ============================================
                # BOOK BUS
                # ============================================

                response = api_post(
                    "/buses/book",
                    {
                        "bus_id": bus["id"],
                        "passenger_name": passenger_name,
                        "passenger_phone": passenger_phone,
                        "seats": int(seats),
                        "payment_method": backend_payment_method
                    }
                )


                if response:

                    if response.status_code in [
                        200,
                        201
                    ]:

                        booking = response.json()


                        st.success(
                            "🎉 Bus Booking Confirmed!"
                        )


                        st.write(
                            f"**Booking ID:** "
                            f"#{booking['id']}"
                        )

                        st.write(
                            f"**Passenger:** "
                            f"{booking['passenger_name']}"
                        )

                        st.write(
                            f"**Seats:** "
                            f"{booking['seats']}"
                        )

                        st.write(
                            f"**Total Paid:** "
                            f"₹{booking['total_price']:,}"
                        )


                        if backend_payment_method == "wallet":

                            st.success(
                                "💳 Payment completed "
                                "using TRAVELX Wallet."
                            )

                        else:

                            st.info(
                                "🧪 Demo payment completed."
                            )


                        # Clear selected bus

                        st.session_state.selected_bus = None

                        # Clear old search results

                        st.session_state.bus_results = []


                        # Wallet payment
                        # → Go to wallet

                        if backend_payment_method == "wallet":

                            st.session_state.page = "Wallet"

                        else:

                            st.session_state.page = "My Bookings"


                        st.rerun()


                    else:

                        detail = get_json(
                            response
                        ).get(
                            "detail",
                            "Booking failed."
                        )

                        st.error(detail)



# ============================================================
# HOTELS
# ============================================================

elif st.session_state.page == "Hotels":

    st.title("🏨 Hotel Booking")

    st.caption(
        "Search hotels, compare prices and book your perfect stay."
    )

    st.divider()

    # ========================================================
    # SEARCH HOTELS
    # ========================================================

    st.subheader("🔎 Search Hotels")

    city = st.text_input(
        "📍 City",
        placeholder="Example: Mumbai",
        key="hotel_city"
    )

    if st.button(
        "🔎 Search Hotels",
        type="primary",
        use_container_width=True,
        key="search_hotels_button"
    ):

        if not city.strip():

            st.warning("Please enter a city.")

        else:

            response = api_post(
                "/hotels/search",
                {
                    "city": city.strip()
                }
            )

            if response:

                if response.status_code == 200:

                    st.session_state.hotel_results = (
                        response.json()
                    )

                    st.session_state.selected_hotel = None

                    if not st.session_state.hotel_results:

                        st.warning(
                            f"No hotels found in {city.strip()}."
                        )

                else:

                    detail = get_json(
                        response
                    ).get(
                        "detail",
                        "Hotel search failed."
                    )

                    st.error(detail)

    # ========================================================
    # AVAILABLE HOTELS
    # ========================================================

    if st.session_state.hotel_results:

        st.divider()

        st.subheader("🏨 Available Hotels")

        for hotel in st.session_state.hotel_results:

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [2.5, 2, 2, 1]
                )

                # ------------------------------------------------
                # HOTEL DETAILS
                # ------------------------------------------------

                with col1:

                    st.markdown(
                        f"### 🏨 {hotel['name']}"
                    )

                    st.write(
                        f"⭐ **{hotel['rating']:.1f} / 5**"
                    )

                    if hotel.get("address"):

                        st.caption(
                            f"📍 {hotel['address']}"
                        )

                # ------------------------------------------------
                # DESCRIPTION
                # ------------------------------------------------

                with col2:

                    if hotel.get("description"):

                        st.write(
                            hotel["description"]
                        )

                    if hotel.get("amenities"):

                        st.caption(
                            f"✨ {hotel['amenities']}"
                        )

                # ------------------------------------------------
                # PRICE
                # ------------------------------------------------

                with col3:

                    st.write(
                        f"💰 **₹{hotel['price_per_night']:,}**"
                    )

                    st.caption(
                        "per room / night"
                    )

                    st.write(
                        f"🛏️ Available rooms: "
                        f"**{hotel['available_rooms']}**"
                    )

                # ------------------------------------------------
                # BOOK
                # ------------------------------------------------

                with col4:

                    if st.button(
                        "Book Now",
                        key=f"select_hotel_{hotel['id']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_hotel = hotel

                        st.rerun()

    # ========================================================
    # HOTEL BOOKING FORM
    # ========================================================

    if st.session_state.selected_hotel:

        hotel = st.session_state.selected_hotel

        st.divider()

        st.subheader("🛎️ Complete Your Hotel Booking")

        st.info(
            f"🏨 **{hotel['name']}** | "
            f"📍 {hotel['city']} | "
            f"⭐ {hotel['rating']:.1f} | "
            f"₹{hotel['price_per_night']:,} per room/night"
        )

        col1, col2 = st.columns(2)

        with col1:

            guest_name = st.text_input(
                "Guest Name",
                key="hotel_guest_name"
            )

        with col2:

            guest_phone = st.text_input(
                "Guest Phone",
                key="hotel_guest_phone"
            )

        col1, col2 = st.columns(2)

        with col1:

            rooms = st.number_input(
                "Number of Rooms",
                min_value=1,
                max_value=int(hotel["available_rooms"]),
                value=1,
                step=1,
                key="hotel_rooms"
            )

        with col2:

            nights = st.number_input(
                "Number of Nights",
                min_value=1,
                max_value=30,
                value=1,
                step=1,
                key="hotel_nights"
            )

        total_price = (
            hotel["price_per_night"]
            * int(rooms)
            * int(nights)
        )

        st.success(
            f"💰 Total Price: **₹{total_price:,}**"
        )

        # ====================================================
        # LIVE WALLET BALANCE
        # ====================================================

        wallet_response = api_get(
            "/wallet/"
        )

        wallet_balance = 0.0

        if (
            wallet_response
            and wallet_response.status_code == 200
        ):

            wallet_data = get_json(
                wallet_response
            )

            wallet_balance = float(
                wallet_data.get(
                    "balance",
                    0
                )
            )

        # ====================================================
        # PAYMENT
        # ====================================================

        st.subheader("💳 Payment Method")

        payment_method = st.radio(
            "Choose payment method",
            [
                "TRAVELX Wallet",
                "Demo Payment"
            ],
            key="hotel_payment_method"
        )

        if payment_method == "TRAVELX Wallet":

            st.info(
                f"💰 Wallet Balance: "
                f"**₹{wallet_balance:,.2f}**"
            )

            if wallet_balance >= total_price:

                remaining_balance = (
                    wallet_balance - total_price
                )

                st.success(
                    f"After payment: "
                    f"**₹{remaining_balance:,.2f}**"
                )

            else:

                shortage = (
                    total_price - wallet_balance
                )

                st.error(
                    f"Insufficient wallet balance. "
                    f"You need ₹{shortage:,.2f} more."
                )

        else:

            st.warning(
                "Demo Payment does not deduct money "
                "from your TRAVELX Wallet."
            )

        # ====================================================
        # CONFIRM HOTEL BOOKING
        # ====================================================

        if st.button(
            "🏨 Confirm Hotel Booking",
            type="primary",
            use_container_width=True,
            key="confirm_hotel_booking"
        ):

            if not guest_name.strip():

                st.warning(
                    "Please enter guest name."
                )

            elif not guest_phone.strip():

                st.warning(
                    "Please enter guest phone."
                )

            elif (
                payment_method == "TRAVELX Wallet"
                and wallet_balance < total_price
            ):

                st.error(
                    "Insufficient wallet balance. "
                    "Please add money to your wallet."
                )

            else:

                backend_payment_method = (
                    "wallet"
                    if payment_method == "TRAVELX Wallet"
                    else "demo"
                )

                response = api_post(
                    "/hotels/book",
                    {
                        "hotel_id": hotel["id"],
                        "guest_name": guest_name.strip(),
                        "guest_phone": guest_phone.strip(),
                        "rooms": int(rooms),
                        "nights": int(nights),
                        "payment_method": backend_payment_method
                    }
                )

                if response:

                    if response.status_code in [200, 201]:

                        booking = response.json()

                        st.success(
                            "🎉 Hotel Booking Confirmed!"
                        )

                        st.write(
                            f"**Booking ID:** "
                            f"#{booking['id']}"
                        )

                        st.write(
                            f"**Hotel:** "
                            f"{hotel['name']}"
                        )

                        st.write(
                            f"**Guest:** "
                            f"{booking['guest_name']}"
                        )

                        st.write(
                            f"**Rooms:** "
                            f"{booking['rooms']}"
                        )

                        st.write(
                            f"**Nights:** "
                            f"{booking['nights']}"
                        )

                        st.write(
                            f"**Total Paid:** "
                            f"₹{booking['total_price']:,}"
                        )

                        st.write(
                            f"**Payment:** "
                            f"{booking['payment_method'].upper()}"
                        )

                        if backend_payment_method == "wallet":

                            st.success(
                                "💳 Payment completed "
                                "using TRAVELX Wallet."
                            )

                        else:

                            st.info(
                                "🧪 Demo payment completed."
                            )

                        st.session_state.selected_hotel = None

                        st.session_state.hotel_results = []

                        st.session_state.page = "My Bookings"

                        st.rerun()

                    else:

                        detail = get_json(
                            response
                        ).get(
                            "detail",
                            "Hotel booking failed."
                        )

                        st.error(detail)

    # ========================================================
    # MY HOTEL BOOKINGS
    # ========================================================

    st.divider()

    st.subheader("📋 My Hotel Bookings")

    hotel_booking_response = api_get(
        "/hotels/my-bookings"
    )

    if (
        hotel_booking_response
        and hotel_booking_response.status_code == 200
    ):

        hotel_bookings = get_json(
            hotel_booking_response
        )

        if not hotel_bookings:

            st.info(
                "No hotel bookings yet."
            )

        else:

            for booking in hotel_bookings:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [2, 2, 1]
                    )

                    with col1:

                        st.markdown(
                            f"### 🏨 Booking #{booking['id']}"
                        )

                        st.write(
                            f"👤 Guest: "
                            f"**{booking['guest_name']}**"
                        )

                        st.caption(
                            f"📱 {booking['guest_phone']}"
                        )

                    with col2:

                        st.write(
                            f"🏨 Hotel ID: "
                            f"**{booking['hotel_id']}**"
                        )

                        st.write(
                            f"🛏️ Rooms: "
                            f"**{booking['rooms']}**"
                        )

                        st.write(
                            f"🌙 Nights: "
                            f"**{booking['nights']}**"
                        )

                        st.write(
                            f"💳 Payment: "
                            f"**{booking['payment_method'].upper()}**"
                        )

                    with col3:

                        st.write(
                            f"💰 **₹{booking['total_price']:,}**"
                        )

                        if (
                            booking.get("booking_status")
                            == "confirmed"
                        ):

                            st.success("Confirmed")

                        else:

                            st.warning(
                                booking.get(
                                    "booking_status",
                                    "Unknown"
                                )
                            )

    elif hotel_booking_response:

        st.error(
            "Unable to load hotel bookings."
        )


# ============================================================
# WALLET
# ============================================================

elif st.session_state.page == "Wallet":

    st.title("💰 TRAVELX Wallet")

    st.caption(
        "Manage your TRAVELX balance and transaction history."
    )

    st.divider()


    # ========================================================
    # GET WALLET
    # ========================================================

    wallet_response = api_get(
        "/wallet/"
    )


    if (
        wallet_response
        and wallet_response.status_code == 200
    ):

        wallet = get_json(
            wallet_response
        )

        balance = float(
            wallet.get(
                "balance",
                0
            )
        )


        # ====================================================
        # WALLET CARD
        # ====================================================

        st.html(f"""
        <div class="wallet-box">

            <div class="wallet-label">
                AVAILABLE WALLET BALANCE
            </div>

            <div class="wallet-balance">
                ₹{balance:,.2f}
            </div>

            <div class="wallet-subtitle">
                TRAVELX Digital Wallet • Ready for your next journey
            </div>

        </div>
        """)


        # ====================================================
        # ADD MONEY
        # ====================================================

        st.subheader(
            "➕ Add Money"
        )

        st.caption(
            "Choose an amount or enter a custom value."
        )


        col1, col2, col3, col4 = st.columns(4)


        wallet_amounts = [
            (500, "wallet_500"),
            (1000, "wallet_1000"),
            (2000, "wallet_2000"),
            (5000, "wallet_5000")
        ]


        for column, (amount, key) in zip(
            [col1, col2, col3, col4],
            wallet_amounts
        ):

            with column:

                if st.button(
                    f"₹{amount:,}",
                    use_container_width=True,
                    key=key
                ):

                    st.session_state.wallet_selected_amount = amount


        custom_amount = st.number_input(
            "Custom Amount",
            min_value=0.0,
            max_value=1000000.0,
            value=0.0,
            step=100.0,
            key="wallet_custom_amount"
        )


        if custom_amount > 0:

            st.session_state.wallet_selected_amount = (
                custom_amount
            )


        selected_amount = st.session_state.get(
            "wallet_selected_amount",
            0.0
        )


        if selected_amount > 0:

            st.info(
                f"Selected amount: "
                f"**₹{selected_amount:,.2f}**"
            )


            if st.button(
                "💳 Add Money to Wallet",
                type="primary",
                use_container_width=True
            ):

                response = api_post(
                    "/wallet/add-money",
                    {
                        "amount": float(
                            selected_amount
                        )
                    }
                )


                if (
                    response
                    and response.status_code in [200, 201]
                ):

                    st.success(
                        f"₹{selected_amount:,.2f} "
                        "added successfully! 🎉"
                    )

                    st.session_state.wallet_selected_amount = 0.0

                    st.rerun()


                elif response:

                    detail = get_json(
                        response
                    ).get(
                        "detail",
                        "Unable to add money."
                    )

                    st.error(detail)


        st.divider()


        # ====================================================
        # TRANSACTIONS
        # ====================================================

        st.subheader(
            "📜 Transaction History"
        )


        transaction_response = api_get(
            "/wallet/transactions"
        )


        if (
            transaction_response
            and transaction_response.status_code == 200
        ):

            transactions = get_json(
                transaction_response
            )


            if not transactions:

                st.info(
                    "No wallet transactions yet."
                )

            else:

                for transaction in transactions:

                    transaction_type = (
                        transaction.get(
                            "transaction_type",
                            ""
                        ).lower()
                    )


                    if transaction_type == "credit":

                        icon = "🟢"
                        sign = "+"

                    else:

                        icon = "🔴"
                        sign = "-"


                    with st.container(border=True):

                        col1, col2, col3 = st.columns(
                            [2, 4, 2]
                        )


                        with col1:

                            st.write(
                                f"{icon} "
                                f"**{transaction_type.title()}**"
                            )


                        with col2:

                            st.write(
                                transaction.get(
                                    "description",
                                    ""
                                )
                            )


                        with col3:

                            st.write(
                                f"**{sign}₹"
                                f"{float(transaction.get('amount', 0)):,.2f}**"
                            )

                            st.caption(
                                f"Balance: "
                                f"₹{float(transaction.get('balance_after', 0)):,.2f}"
                            )


        elif transaction_response:

            st.error(
                "Unable to load transactions."
            )


    elif wallet_response:

        if wallet_response.status_code == 401:

            st.error(
                "Authentication expired. Please login again."
            )

        else:

            st.error(
                f"Wallet error: "
                f"{wallet_response.status_code}"
            )


# ============================================================
# MY BOOKINGS
# ============================================================

elif st.session_state.page == "My Bookings":

    st.title("📋 My Bookings")

    st.caption(
        "All your TRAVELX reservations in one place."
    )

    st.divider()


    # ========================================================
    # BUS BOOKINGS
    # ========================================================

    st.subheader(
        "🚌 Bus Bookings"
    )


    bus_booking_response = api_get(
        "/buses/my-bookings"
    )


    if (
        bus_booking_response
        and bus_booking_response.status_code == 200
    ):

        bus_bookings = get_json(
            bus_booking_response
        )


        if not bus_bookings:

            st.info(
                "No bus bookings yet."
            )

        else:

            for booking in bus_bookings:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [2, 2, 1]
                    )


                    with col1:

                        st.markdown(
                            f"### 🎫 Booking #{booking['id']}"
                        )

                        st.write(
                            f"**Passenger:** "
                            f"{booking['passenger_name']}"
                        )

                        st.caption(
                            f"Phone: "
                            f"{booking['passenger_phone']}"
                        )


                    with col2:

                        st.write(
                            f"🚌 Bus ID: "
                            f"**{booking['bus_id']}**"
                        )

                        st.write(
                            f"💺 Seats: "
                            f"**{booking['seats']}**"
                        )


                    with col3:

                        st.write(
                            f"💰 **₹{booking['total_price']:,}**"
                        )


                        if booking.get(
                            "booking_status"
                        ) == "confirmed":

                            st.success(
                                "Confirmed"
                            )

                        else:

                            st.warning(
                                booking.get(
                                    "booking_status",
                                    "Unknown"
                                )
                            )


    elif bus_booking_response:

        st.error(
            "Unable to load bus bookings."
        )


    st.divider()


    # ========================================================
    # TRAIN BOOKINGS
    # ========================================================

    st.subheader("🚆 Train Bookings")

    train_booking_response = api_get(
        "/trains/my-bookings"
    )

    if (
        train_booking_response
        and train_booking_response.status_code == 200
    ):
        train_bookings = get_json(
            train_booking_response
        )

        if not train_bookings:
            st.info("No train bookings yet.")
        else:
            for booking in train_bookings:
                with st.container(border=True):
                    col1, col2, col3 = st.columns(
                        [2, 2, 1]
                    )

                    with col1:
                        st.markdown(
                            f"### 🎫 Booking #{booking['id']}"
                        )
                        st.write(
                            f"👤 Passenger: "
                            f"**{booking['passenger_name']}**"
                        )
                        st.caption(
                            f"📱 {booking['passenger_phone']}"
                        )

                    with col2:
                        st.write(
                            f"🚆 Train ID: "
                            f"**{booking['train_id']}**"
                        )
                        st.write(
                            f"🎟️ Class: "
                            f"**{booking['travel_class'].upper()}**"
                        )
                        st.write(
                            f"💺 Seats: "
                            f"**{booking['seats']}**"
                        )
                        st.write(
                            f"💳 Payment: "
                            f"**{booking['payment_method'].upper()}**"
                        )

                    with col3:
                        st.write(
                            f"💰 **₹{booking['total_price']:,}**"
                        )

                        if (
                            booking.get("booking_status")
                            == "confirmed"
                        ):
                            st.success("Confirmed")
                        else:
                            st.warning(
                                booking.get(
                                    "booking_status",
                                    "Unknown"
                                )
                            )

    elif train_booking_response:
        st.error("Unable to load train bookings.")

    st.divider()

    # ========================================================
    # HOTEL BOOKINGS
    # ========================================================

    st.subheader("🏨 Hotel Bookings")

    hotel_booking_response = api_get(
        "/hotels/my-bookings"
    )

    if (
        hotel_booking_response
        and hotel_booking_response.status_code == 200
    ):

        hotel_bookings = get_json(
            hotel_booking_response
        )

        if not hotel_bookings:

            st.info(
                "No hotel bookings yet."
            )

        else:

            for booking in hotel_bookings:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [2, 2, 1]
                    )

                    with col1:

                        st.markdown(
                            f"### 🏨 Booking #{booking['id']}"
                        )

                        st.write(
                            f"**Guest:** "
                            f"{booking['guest_name']}"
                        )

                        st.caption(
                            f"Phone: {booking['guest_phone']}"
                        )

                    with col2:

                        st.write(
                            f"🏨 Hotel ID: "
                            f"**{booking['hotel_id']}**"
                        )

                        st.write(
                            f"🛏️ Rooms: "
                            f"**{booking['rooms']}**"
                        )

                        st.write(
                            f"🌙 Nights: "
                            f"**{booking['nights']}**"
                        )

                        st.write(
                            f"💳 Payment: "
                            f"**{booking['payment_method'].upper()}**"
                        )

                    with col3:

                        st.write(
                            f"💰 **₹{booking['total_price']:,}**"
                        )

                        if (
                            booking.get("booking_status")
                            == "confirmed"
                        ):

                            st.success(
                                "Confirmed"
                            )

                        else:

                            st.warning(
                                booking.get(
                                    "booking_status",
                                    "Unknown"
                                )
                            )

    elif hotel_booking_response:

        st.error(
            "Unable to load hotel bookings."
        )

    st.divider()


    # ========================================================
    # CAB BOOKINGS
    # ========================================================

    st.subheader("🚕 Cab Bookings")

    cab_booking_response = api_get(
        "/cabs/my-bookings"
    )

    if (
        cab_booking_response
        and cab_booking_response.status_code == 200
    ):

        cab_bookings = get_json(
            cab_booking_response
        )

        if not cab_bookings:

            st.info(
                "No cab bookings yet."
            )

        else:

            for booking in cab_bookings:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [2.5, 2.5, 1.5]
                    )

                    with col1:

                        st.markdown(
                            f"### 🚕 Booking #{booking['id']}"
                        )

                        st.write(
                            f"👤 Passenger: "
                            f"**{booking['passenger_name']}**"
                        )

                        st.caption(
                            f"📱 {booking['passenger_phone']}"
                        )

                    with col2:

                        st.write(
                            f"🚕 Cab: "
                            f"**{booking['cab_type']}**"
                        )

                        st.write(
                            f"📍 {booking['pickup_location']} → "
                            f"{booking['drop_location']}"
                        )

                        st.write(
                            f"🛣️ Distance: "
                            f"**{booking['distance_km']} km**"
                        )

                        st.write(
                            f"💳 Payment: "
                            f"**{booking['payment_method'].upper()}**"
                        )

                    with col3:

                        st.write(
                            f"💰 **₹{booking['total_price']:,}**"
                        )

                        if (
                            booking.get("booking_status")
                            == "confirmed"
                        ):

                            st.success(
                                "Confirmed"
                            )

                        else:

                            st.warning(
                                booking.get(
                                    "booking_status",
                                    "Unknown"
                                )
                            )

    elif cab_booking_response:

        st.error(
            "Unable to load cab bookings."
        )

    st.divider()

    # ========================================================
    # FOOD ORDERS
    # ========================================================

    st.subheader("🍔 Food Orders")

    food_orders_response = api_get(
        "/food/my-orders"
    )

    if (
        food_orders_response
        and food_orders_response.status_code == 200
    ):

        food_orders = get_json(
            food_orders_response
        )

        if not food_orders:
            st.info("No food orders yet.")
        else:
            for order in food_orders:

                with st.container(border=True):

                    col1, col2, col3 = st.columns([2.5, 3, 1.5])

                    with col1:
                        st.markdown(
                            f"### 🍔 Order #{order['id']}"
                        )
                        st.write(
                            f"👤 Customer: **{order['customer_name']}**"
                        )
                        st.caption(
                            f"📱 {order['customer_phone']}"
                        )

                    with col2:
                        st.write(
                            f"🏪 Restaurant ID: **{order['restaurant_id']}**"
                        )
                        st.write(
                            f"📍 {order['delivery_address']}"
                        )

                        if order.get("items"):
                            item_text = ", ".join(
                                f"{item['item_name']} × {item['quantity']}"
                                for item in order["items"]
                            )
                            st.caption(
                                f"🍽️ {item_text}"
                            )

                        st.write(
                            f"💳 Payment: **{order['payment_method'].upper()}**"
                        )

                    with col3:
                        st.write(
                            f"💰 **₹{order['total_price']:,}**"
                        )

                        if order.get("order_status") == "confirmed":
                            st.success("Confirmed")
                        else:
                            st.warning(
                                order.get(
                                    "order_status",
                                    "Unknown"
                                )
                            )

    elif food_orders_response:
        st.error("Unable to load food orders.")


    st.divider()
    
    # ========================================================
    # MOVIE BOOKINGS
    # ========================================================

    st.subheader("🎬 Movie Bookings")

    movie_booking_response = api_get(
        "/movies/my-bookings"
    )

    if (
        movie_booking_response
        and movie_booking_response.status_code == 200
    ):
        movie_bookings = get_json(
            movie_booking_response
        )

        if not movie_bookings:
            st.info(
                "No movie bookings yet. Book your first movie ticket from the Movies section. 🎬"
            )

        else:
            for booking in movie_bookings:

                movie_id = booking.get("movie_id")
                cinema_id = booking.get("cinema_id")
                show_id = booking.get("show_id")

                cache = st.session_state.movie_booking_lookup_cache

                movie_cache_key = f"movie_{movie_id}"
                cinema_cache_key = f"cinema_{cinema_id}"
                show_cache_key = f"show_{show_id}"

                # ------------------------------------------------
                # LOAD MOVIE DETAILS
                # ------------------------------------------------

                if movie_cache_key not in cache:
                    movie_response = api_get(
                        f"/movies/{movie_id}"
                    )

                    cache[movie_cache_key] = (
                        get_json(movie_response)
                        if movie_response
                        and movie_response.status_code == 200
                        else {}
                    )

                # ------------------------------------------------
                # LOAD CINEMA DETAILS
                # ------------------------------------------------

                if cinema_cache_key not in cache:
                    cinema_response = api_get(
                        f"/movies/cinemas/{cinema_id}"
                    )

                    cache[cinema_cache_key] = (
                        get_json(cinema_response)
                        if cinema_response
                        and cinema_response.status_code == 200
                        else {}
                    )

                # ------------------------------------------------
                # LOAD SHOW DETAILS
                # ------------------------------------------------

                if show_cache_key not in cache:
                    show_response = api_get(
                        f"/movies/shows/{show_id}"
                    )

                    cache[show_cache_key] = (
                        get_json(show_response)
                        if show_response
                        and show_response.status_code == 200
                        else {}
                    )

                movie_info = cache.get(
                    movie_cache_key,
                    {}
                )

                cinema_info = cache.get(
                    cinema_cache_key,
                    {}
                )

                show_info = cache.get(
                    show_cache_key,
                    {}
                )

                movie_title = movie_info.get(
                    "title",
                    f"Movie ID {movie_id}"
                )

                movie_language = movie_info.get(
                    "language",
                    ""
                )

                movie_genre = movie_info.get(
                    "genre",
                    ""
                )

                cinema_name = cinema_info.get(
                    "name",
                    f"Cinema ID {cinema_id}"
                )

                cinema_address = cinema_info.get(
                    "address",
                    ""
                )

                screen_name = show_info.get(
                    "screen_name",
                    "Screen"
                )

                ticket_price = show_info.get(
                    "ticket_price",
                    0
                )

                booking_status = booking.get(
                    "booking_status",
                    "unknown"
                )

                # ------------------------------------------------
                # MOVIE TICKET CARD
                # ------------------------------------------------

                with st.container(border=True):

                    st.markdown(
                        f"### 🎬 {movie_title}"
                    )

                    st.caption(
                        f"🎫 Booking #{booking['id']} • "
                        f"{movie_genre} • {movie_language}"
                    )

                    col1, col2, col3 = st.columns(
                        [2.5, 3, 1.5]
                    )

                    with col1:

                        st.write(
                            f"👤 Customer: "
                            f"**{booking['customer_name']}**"
                        )

                        st.caption(
                            f"📱 {booking['customer_phone']}"
                        )

                        st.write(
                            f"🏢 Cinema: **{cinema_name}**"
                        )

                        if cinema_address:
                            st.caption(
                                f"📍 {cinema_address}"
                            )

                    with col2:

                        st.write(
                            f"📅 Date: "
                            f"**{booking['show_date']}**"
                        )

                        st.write(
                            f"🕐 Show Time: "
                            f"**{booking['show_time']}**"
                        )

                        st.write(
                            f"🎥 Screen: "
                            f"**{screen_name}**"
                        )

                        st.write(
                            f"💺 Seats: "
                            f"**{booking['seats']}**"
                        )

                        st.write(
                            f"🎟️ Tickets: "
                            f"**{booking['number_of_seats']}**"
                        )

                    with col3:

                        st.write(
                            f"🎟️ Ticket Price: "
                            f"**₹{int(ticket_price):,}**"
                            if ticket_price
                            else "🎟️ Ticket Price: **—**"
                        )

                        st.write(
                            f"💰 Total Paid: "
                            f"**₹{booking['total_price']:,}**"
                        )

                        st.write(
                            f"💳 Payment: "
                            f"**{booking['payment_method'].upper()}**"
                        )

                        if booking_status == "confirmed":

                            st.success(
                                "Confirmed"
                            )

                        else:

                            st.warning(
                                booking_status.title()
                            )

                    # ------------------------------------------------
                    # DIGITAL TICKET SUMMARY
                    # ------------------------------------------------

                    with st.expander(
                        "🎟️ View Ticket Details"
                    ):

                        ticket_col1, ticket_col2 = st.columns(2)

                        with ticket_col1:

                            st.write(
                                f"**Booking ID:** #{booking['id']}"
                            )

                            st.write(
                                f"**Movie:** {movie_title}"
                            )

                            st.write(
                                f"**Cinema:** {cinema_name}"
                            )

                            st.write(
                                f"**Screen:** {screen_name}"
                            )

                        with ticket_col2:

                            st.write(
                                f"**Date:** {booking['show_date']}"
                            )

                            st.write(
                                f"**Time:** {booking['show_time']}"
                            )

                            st.write(
                                f"**Seats:** {booking['seats']}"
                            )

                            st.write(
                                f"**Total:** ₹{booking['total_price']:,}"
                            )

                        st.info(
                            "🎉 Please show this booking information at the cinema."
                        )

    elif movie_booking_response:

        st.error(
            "Unable to load movie bookings."
        )

    st.divider()

    # OTHER BOOKINGS
    # ========================================================

    st.subheader(
        "🎟️ Other Bookings"
    )


    booking_response = api_get(
        "/bookings/my"
    )


    if (
        booking_response
        and booking_response.status_code == 200
    ):

        bookings = get_json(
            booking_response
        )


        if not bookings:

            st.info(
                "No other bookings yet."
            )

        else:

            for booking in bookings:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [2, 3, 1]
                    )


                    with col1:

                        st.markdown(
                            f"### 🎫 #{booking['id']}"
                        )

                        st.write(
                            booking[
                                "booking_type"
                            ].upper()
                        )


                    with col2:

                        st.write(
                            f"**{booking['title']}**"
                        )


                        if booking.get("source"):

                            st.write(
                                f"📍 "
                                f"{booking['source']} → "
                                f"{booking.get('destination', '')}"
                            )


                        if booking.get(
                            "booking_date"
                        ):

                            st.write(
                                f"📅 "
                                f"{booking['booking_date']}"
                            )


                        if booking.get(
                            "details"
                        ):

                            st.caption(
                                booking["details"]
                            )


                    with col3:

                        st.write(
                            f"**₹"
                            f"{float(booking.get('amount', 0)):,.2f}**"
                        )


                        if booking.get(
                            "status"
                        ) == "confirmed":

                            st.success(
                                "Confirmed"
                            )

                        else:

                            st.warning(
                                booking.get(
                                    "status",
                                    "Unknown"
                                )
                            )


    elif booking_response:

        st.error(
            "Unable to load bookings."
        )



    # ========================================================
    # FLIGHT BOOKINGS
    # ========================================================

    flight_response = api_get(
        "/flights/my-bookings"
    )

    if (
        flight_response
        and flight_response.status_code == 200
    ):

        flight_bookings = get_json(
            flight_response
        )

        st.subheader("✈️ Flight Bookings")

        if not flight_bookings:

            st.info("No flight bookings yet.")

        else:

            for booking in flight_bookings:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [2.5, 2.5, 1.5]
                    )

                    with col1:

                        st.markdown(
                            f"### ✈️ Booking #{booking['id']}"
                        )

                        st.write(
                            f"👤 Passenger: "
                            f"**{booking['passenger_name']}**"
                        )

                        st.caption(
                            f"📱 {booking['passenger_phone']}"
                        )

                    with col2:

                        st.write(
                            f"🎫 Flight ID: "
                            f"**{booking['flight_id']}**"
                        )

                        st.write(
                            f"💺 Class: "
                            f"**{booking['travel_class'].title()}**"
                        )

                        st.write(
                            f"💺 Seats: "
                            f"**{booking['seats']}**"
                        )

                        st.write(
                            f"💳 Payment: "
                            f"**{booking['payment_method'].upper()}**"
                        )

                    with col3:

                        st.write(
                            f"💰 **₹{booking['total_price']:,}**"
                        )

                        if booking.get("booking_status") == "confirmed":

                            st.success("Confirmed")

                        else:

                            st.warning(
                                booking.get(
                                    "booking_status",
                                    "Unknown"
                                )
                            )



    # ========================================================
    # EVENT BOOKINGS
    # ========================================================

    st.divider()

    st.subheader("🎟️ Event Bookings")

    event_booking_response = api_get(
        "/events/my-bookings"
    )

    if (
        event_booking_response
        and event_booking_response.status_code == 200
    ):

        event_bookings = get_json(
            event_booking_response
        )

        if not event_bookings:

            st.info(
                "No event bookings yet. "
                "Discover an event and book your tickets! 🎟️"
            )

        else:

            for booking in event_bookings:

                event_id = booking.get("event_id")
                venue_id = booking.get("venue_id")

                event_info = {}
                venue_info = {}

                event_response = api_get(
                    f"/events/{event_id}"
                )

                if (
                    event_response
                    and event_response.status_code == 200
                ):

                    event_info = get_json(
                        event_response
                    )

                venue_response = api_get(
                    "/events/venues/all"
                )

                if (
                    venue_response
                    and venue_response.status_code == 200
                ):

                    venue_info = next(
                        (
                            venue
                            for venue in get_json(venue_response)
                            if venue.get("id") == venue_id
                        ),
                        {}
                    )

                event_name = event_info.get(
                    "name",
                    f"Event ID {event_id}"
                )

                venue_name = venue_info.get(
                    "name",
                    f"Venue ID {venue_id}"
                )

                venue_address = venue_info.get(
                    "address",
                    ""
                )

                with st.container(border=True):

                    st.markdown(
                        f"### 🎟️ {event_name}"
                    )

                    st.caption(
                        f"🎫 Booking #{booking['id']}"
                    )

                    col1, col2, col3 = st.columns(
                        [2.5, 3, 1.5]
                    )

                    with col1:

                        st.write(
                            f"👤 Customer: "
                            f"**{booking['customer_name']}**"
                        )

                        st.caption(
                            f"📱 {booking['customer_phone']}"
                        )

                        st.write(
                            f"🏟️ Venue: "
                            f"**{venue_name}**"
                        )

                        if venue_address:

                            st.caption(
                                f"📍 {venue_address}"
                            )

                    with col2:

                        st.write(
                            f"📅 Date: "
                            f"**{booking['show_date']}**"
                        )

                        st.write(
                            f"🕐 Time: "
                            f"**{booking['show_time']}**"
                        )

                        st.write(
                            f"🎫 Ticket Type: "
                            f"**{booking['ticket_type']}**"
                        )

                        st.write(
                            f"👥 Tickets: "
                            f"**{booking['number_of_tickets']}**"
                        )

                        st.write(
                            f"💳 Payment: "
                            f"**{booking['payment_method'].upper()}**"
                        )

                    with col3:

                        st.write(
                            f"💰 **₹{booking['total_price']:,}**"
                        )

                        if (
                            booking.get("booking_status")
                            == "confirmed"
                        ):

                            st.success(
                                "Confirmed"
                            )

                        else:

                            st.warning(
                                booking.get(
                                    "booking_status",
                                    "Unknown"
                                )
                            )

    elif event_booking_response:

        st.error(
            "Unable to load event bookings."
        )


# ============================================================
# PROFILE
# ============================================================

elif st.session_state.page == "Profile":

    st.title("👤 My Profile")

    st.caption(
        "View your TRAVELX account information."
    )

    st.divider()


    response = api_get(
        "/auth/profile"
    )


    if (
        response
        and response.status_code == 200
    ):

        profile = get_json(
            response
        )


        col1, col2 = st.columns(2)


        with col1:

            st.subheader(
                "Personal Information"
            )


            st.text_input(
                "Name",
                value=profile.get(
                    "name",
                    ""
                ),
                disabled=True,
                key="profile_name"
            )


            st.text_input(
                "Email",
                value=profile.get(
                    "email",
                    ""
                ),
                disabled=True,
                key="profile_email"
            )


        with col2:

            st.subheader(
                "Account Details"
            )


            st.text_input(
                "Phone",
                value=profile.get(
                    "phone",
                    ""
                ),
                disabled=True,
                key="profile_phone"
            )


            st.text_input(
                "User ID",
                value=str(
                    profile.get(
                        "id",
                        ""
                    )
                ),
                disabled=True,
                key="profile_id"
            )


        st.divider()


        st.success(
            "Your TRAVELX account is active. ✅"
        )


    elif response:

        st.error(
            "Unable to load profile."
        )


# ============================================================
# FLIGHTS
# ============================================================

elif st.session_state.page == "Flights":

    st.title("✈️ Flights")

    st.caption(
        "Search, compare and book flights."
    )

    st.info(
        "Flight booking module is coming next. 🚀"
    )

    st.write(
        "TRAVELX will support flight search, "
        "comparison, pricing and booking."
    )


# ============================================================
# TRAINS
# ============================================================

elif st.session_state.page == "Trains":

    st.title("🚆 Train Booking")

    st.caption(
        "Search trains, choose your class and book your journey."
    )

    # ========================================================
    # SEARCH SECTION
    # ========================================================

    st.subheader("🔎 Search Trains")

    col1, col2 = st.columns(2)

    with col1:

        source = st.text_input(
            "From",
            placeholder="e.g. Pune",
            key="train_source"
        )

    with col2:

        destination = st.text_input(
            "To",
            placeholder="e.g. Mumbai",
            key="train_destination"
        )

    if st.button(
        "🔎 Search Trains",
        type="primary",
        use_container_width=True
    ):

        if not source or not destination:

            st.warning(
                "Please enter source and destination."
            )

        else:

            response = api_post(
                "/trains/search",
                {
                    "source": source.strip(),
                    "destination": destination.strip()
                }
            )

            if response:

                if response.status_code == 200:

                    st.session_state.train_results = (
                        response.json()
                    )

                    st.session_state.selected_train = None

                    if not st.session_state.train_results:

                        st.warning(
                            "No trains found for this route."
                        )

                else:

                    detail = get_json(
                        response
                    ).get(
                        "detail",
                        "Train search failed."
                    )

                    st.error(detail)


    # ========================================================
    # AVAILABLE TRAINS
    # ========================================================

    if st.session_state.train_results:

        st.divider()

        st.subheader("🚆 Available Trains")

        for train in st.session_state.train_results:

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [2, 2, 2, 1]
                )

                # ------------------------------------------------
                # TRAIN NAME
                # ------------------------------------------------

                with col1:

                    st.markdown(
                        f"### 🚆 {train['train_name']}"
                    )

                    st.write(
                        f"Train No: **{train['train_number']}**"
                    )


                # ------------------------------------------------
                # ROUTE / TIME
                # ------------------------------------------------

                with col2:

                    st.write(
                        f"📍 **{train['source']} → "
                        f"{train['destination']}**"
                    )

                    st.write(
                        f"🕐 {train['departure_time']} → "
                        f"{train['arrival_time']}"
                    )


                # ------------------------------------------------
                # SEATS / PRICES
                # ------------------------------------------------

                with col3:

                    st.write(
                        f"💺 Available Seats: "
                        f"**{train['available_seats']}**"
                    )

                    st.write(
                        f"🛏️ Sleeper: "
                        f"**₹{train['sleeper_price']:,}**"
                    )

                    st.write(
                        f"❄️ 3A: "
                        f"**₹{train['third_ac_price']:,}**"
                    )


                # ------------------------------------------------
                # SELECT BUTTON
                # ------------------------------------------------

                with col4:

                    if st.button(
                        "Book",
                        key=f"select_train_{train['id']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_train = train

                        st.rerun()


    # ========================================================
    # BOOKING FORM
    # ========================================================

    if st.session_state.selected_train:

        train = st.session_state.selected_train

        st.divider()

        st.subheader("🎫 Passenger Details")

        st.info(
            f"🚆 **{train['train_name']}** "
            f"({train['train_number']})\n\n"
            f"📍 {train['source']} → "
            f"{train['destination']}\n\n"
            f"🕐 {train['departure_time']} → "
            f"{train['arrival_time']}"
        )


        # ====================================================
        # PASSENGER DETAILS
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            passenger_name = st.text_input(
                "Passenger Name",
                key="train_passenger_name"
            )

        with col2:

            passenger_phone = st.text_input(
                "Passenger Phone",
                key="train_passenger_phone"
            )


        # ====================================================
        # CLASS + SEATS
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            travel_class = st.selectbox(
                "Travel Class",
                [
                    "Sleeper",
                    "3A",
                    "2A",
                    "1A"
                ],
                key="train_travel_class"
            )


        with col2:

            seats = st.number_input(
                "Number of Seats",
                min_value=1,
                max_value=int(
                    train["available_seats"]
                ),
                value=1,
                step=1,
                key="train_seats"
            )


        # ====================================================
        # CLASS PRICE
        # ====================================================

        class_prices = {

            "Sleeper": train["sleeper_price"],

            "3A": train["third_ac_price"],

            "2A": train["second_ac_price"],

            "1A": train["first_ac_price"]
        }


        price_per_seat = class_prices[
            travel_class
        ]

        total_price = (
            price_per_seat * seats
        )


        # ====================================================
        # PRICE DISPLAY
        # ====================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Class",
                travel_class
            )

        with col2:

            st.metric(
                "Price / Seat",
                f"₹{price_per_seat:,}"
            )

        with col3:

            st.metric(
                "Total",
                f"₹{total_price:,}"
            )


        st.divider()


        # ====================================================
        # WALLET BALANCE
        # ====================================================

        wallet_response = api_get(
            "/wallet/"
        )

        wallet_balance = 0.0

        if (
            wallet_response
            and wallet_response.status_code == 200
        ):

            wallet_data = get_json(
                wallet_response
            )

            wallet_balance = float(
                wallet_data.get(
                    "balance",
                    0
                )
            )

        st.info(
            f"💰 TRAVELX Wallet Balance: "
            f"**₹{wallet_balance:,.2f}**"
        )


        # ====================================================
        # PAYMENT METHOD
        # ====================================================

        payment_method = st.radio(
            "Payment Method",
            [
                "TRAVELX Wallet",
                "Demo Payment"
            ],
            horizontal=True,
            key="train_payment_method"
        )


        if payment_method == "TRAVELX Wallet":

            if wallet_balance >= total_price:

                st.success(
                    f"Wallet payment available. "
                    f"₹{total_price:,} will be deducted."
                )

            else:

                st.warning(
                    f"Insufficient wallet balance. "
                    f"Available ₹{wallet_balance:,.2f}, "
                    f"Required ₹{total_price:,.2f}"
                )


        # ====================================================
        # CONFIRM BOOKING
        # ====================================================

        if st.button(
            "🎟️ Confirm Train Booking",
            type="primary",
            use_container_width=True
        ):

            if not passenger_name:

                st.warning(
                    "Please enter passenger name."
                )

            elif not passenger_phone:

                st.warning(
                    "Please enter passenger phone."
                )

            elif (
                payment_method == "TRAVELX Wallet"
                and wallet_balance < total_price
            ):

                st.error(
                    "Insufficient wallet balance."
                )

            else:

                selected_payment = (
                    "wallet"
                    if payment_method == "TRAVELX Wallet"
                    else "demo"
                )


                response = api_post(
                    "/trains/book",
                    {
                        "train_id": train["id"],

                        "passenger_name":
                            passenger_name,

                        "passenger_phone":
                            passenger_phone,

                        "travel_class":
                            travel_class.lower(),

                        "seats":
                            seats,

                        "payment_method":
                            selected_payment
                    }
                )


                if response:

                    if response.status_code in [
                        200,
                        201
                    ]:

                        booking = response.json()

                        st.success(
                            f"🎉 Train booking confirmed! "
                            f"Booking ID: "
                            f"#{booking['id']}"
                        )

                        st.session_state.selected_train = None

                        st.session_state.train_results = []

                        st.session_state.page = (
                            "My Bookings"
                        )

                        st.rerun()

                    else:

                        detail = get_json(
                            response
                        ).get(
                            "detail",
                            "Train booking failed."
                        )

                        st.error(detail)


    # ========================================================
    # MY TRAIN BOOKINGS
    # ========================================================

    st.divider()

    st.subheader("📋 My Train Bookings")

    train_booking_response = api_get(
        "/trains/my-bookings"
    )


    if (
        train_booking_response
        and train_booking_response.status_code == 200
    ):

        train_bookings = get_json(
            train_booking_response
        )


        if not train_bookings:

            st.info(
                "No train bookings yet."
            )

        else:

            for booking in train_bookings:

                with st.container(
                    border=True
                ):

                    col1, col2, col3 = st.columns(
                        [2, 2, 1]
                    )


                    with col1:

                        st.markdown(
                            f"### 🎫 Booking "
                            f"#{booking['id']}"
                        )

                        st.write(
                            f"👤 Passenger: "
                            f"**{booking['passenger_name']}**"
                        )

                        st.write(
                            f"📱 "
                            f"{booking['passenger_phone']}"
                        )


                    with col2:

                        st.write(
                            f"🚆 Train ID: "
                            f"**{booking['train_id']}**"
                        )

                        st.write(
                            f"💺 Seats: "
                            f"**{booking['seats']}**"
                        )

                        st.write(
                            f"🎟️ Class: "
                            f"**{booking['travel_class'].upper()}**"
                        )

                        st.write(
                            f"💳 Payment: "
                            f"**{booking['payment_method'].upper()}**"
                        )


                    with col3:

                        st.write(
                            f"💰 **₹{booking['total_price']:,}**"
                        )

                        if (
                            booking["booking_status"]
                            == "confirmed"
                        ):

                            st.success(
                                "Confirmed"
                            )

                        else:

                            st.warning(
                                booking[
                                    "booking_status"
                                ]
                            )


    elif train_booking_response:

        st.error(
            "Unable to load train bookings."
        )


    # ========================================================
    # BACK TO HOME
    # ========================================================

    st.divider()

    if st.button(
        "🏠 Back to Dashboard",
        use_container_width=True
    ):

        st.session_state.page = "Home"

        st.rerun()