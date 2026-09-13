import streamlit as st
import requests
import pandas as pd
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

if "notification_unread_count" not in st.session_state:
    st.session_state.notification_unread_count = 0
# ============================================================
# ADMIN SESSION STATE
# ============================================================

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "admin_email" not in st.session_state:
    st.session_state.admin_email = ""

if "admin_token" not in st.session_state:
    st.session_state.admin_token = ""

if "admin_edit_bus" not in st.session_state:
    st.session_state.admin_edit_bus = None
if "admin_edit_flight" not in st.session_state:
    st.session_state.admin_edit_flight = None
if "admin_edit_cab" not in st.session_state:
    st.session_state.admin_edit_cab = None
if "admin_edit_restaurant" not in st.session_state:
    st.session_state.admin_edit_restaurant = None
if "admin_edit_food_item" not in st.session_state:
    st.session_state.admin_edit_food_item = None
if "admin_edit_movie" not in st.session_state:
    st.session_state.admin_edit_movie = None
if "admin_edit_cinema" not in st.session_state:
    st.session_state.admin_edit_cinema = None
if "admin_edit_movie_show" not in st.session_state:
    st.session_state.admin_edit_movie_show = None
if "admin_edit_event" not in st.session_state:
    st.session_state.admin_edit_event = None
if "admin_edit_event_venue" not in st.session_state:
    st.session_state.admin_edit_event_venue = None
if "admin_edit_event_show" not in st.session_state:
    st.session_state.admin_edit_event_show = None

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


def api_patch(endpoint, data=None):

    try:

        response = requests.patch(
            f"{API_URL}{endpoint}",
            json=data or {},
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
# ADMIN API HELPERS
# ============================================================

def admin_headers():
    """
    Headers used for all protected admin API requests.

    Admin authentication is now handled through JWT.
    """

    token = st.session_state.get("admin_token", "")

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}"
    }


def admin_api_get(endpoint):
    """
    Send authenticated GET request to an admin endpoint.
    """

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            headers=admin_headers(),
            timeout=10
        )

        return response

    except requests.exceptions.RequestException as e:

        st.error(
            f"Backend connection error: {e}"
        )

        return None


def admin_api_request(
    method,
    endpoint,
    data=None
):
    """
    Send authenticated admin API request.
    """

    try:

        response = requests.request(
            method,
            f"{API_URL}{endpoint}",
            json=data,
            headers=admin_headers(),
            timeout=10
        )

        return response

    except requests.exceptions.RequestException as e:

        st.error(
            f"Backend connection error: {e}"
        )

        return None


def admin_error_message(
    response,
    fallback="Request failed."
):

    if response is None:
        return "Backend connection failed."

    try:

        return response.json().get(
            "detail",
            fallback
        )

    except Exception:

        return fallback
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
            profile_data = profile_response.json()

            # Backend returns actual user information inside "user"
            st.session_state.user = profile_data.get(
                "user",
                profile_data
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

    st.session_state.admin_authenticated = False
    st.session_state.admin_email = ""
    st.session_state.admin_token = ""

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

if not st.session_state.token and not st.session_state.admin_authenticated:

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

    login_tab, register_tab, admin_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Create Account",
            "👑 Admin Portal"
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

    # ========================================================
    # ADMIN LOGIN TAB
    # ========================================================

    # ========================================================
    # ADMIN LOGIN TAB
    # ========================================================

    with admin_tab:

        st.html("""
        <div style="
            text-align:center;
            padding:20px 0 25px 0;
        ">
            <div style="
                font-size:54px;
                margin-bottom:5px;
            ">👑</div>

            <div style="
                color:#f8fafc;
                font-size:34px;
                font-weight:900;
            ">
                TRAVELX Admin
            </div>

            <div style="
                color:#64748b;
                font-size:14px;
                margin-top:6px;
            ">
                Secure administrator access.
            </div>
        </div>
        """)

        admin_email_input = st.text_input(
            "Admin Email",
            placeholder="Enter admin email",
            key="admin_login_email"
        )

        admin_password_input = st.text_input(
            "Admin Password",
            type="password",
            placeholder="Enter admin password",
            key="admin_login_password"
        )

        if st.button(
            "👑 Login as Administrator",
            type="primary",
            use_container_width=True,
            key="admin_login_button"
        ):

            if (
                not admin_email_input
                or not admin_password_input
            ):

                st.warning(
                    "Please enter admin email and password."
                )

            else:

                try:

                    # ------------------------------------------------
                    # AUTHENTICATE THROUGH NORMAL JWT LOGIN
                    # ------------------------------------------------

                    admin_login_response = requests.post(
                        f"{API_URL}/auth/login",
                        json={
                            "email": admin_email_input,
                            "password": admin_password_input
                        },
                        timeout=10
                    )

                    # ------------------------------------------------
                    # LOGIN SUCCESS
                    # ------------------------------------------------

                    if admin_login_response.status_code == 200:

                        login_data = admin_login_response.json()

                        access_token = login_data.get(
                            "access_token"
                        )

                        if not access_token:

                            st.error(
                                "Authentication succeeded but "
                                "no access token was returned."
                            )

                        else:

                            # ------------------------------------------------
                            # VERIFY THAT THIS JWT REALLY HAS ADMIN ACCESS
                            # ------------------------------------------------

                            verify_response = requests.get(
                                f"{API_URL}/admin/dashboard",
                                headers={
                                    "Authorization": (
                                        f"Bearer {access_token}"
                                    )
                                },
                                timeout=10
                            )

                            if verify_response.status_code == 200:

                                st.session_state.admin_authenticated = True

                                st.session_state.admin_email = (
                                    admin_email_input
                                )

                                st.session_state.admin_token = (
                                    access_token
                                )

                                st.session_state.page = (
                                    "Admin Dashboard"
                                )

                                st.success(
                                    "Admin login successful! 👑"
                                )

                                st.rerun()

                            elif verify_response.status_code == 403:

                                st.error(
                                    "This account does not have "
                                    "administrator privileges."
                                )

                            else:

                                st.error(
                                    "Unable to verify administrator access."
                                )

                    else:

                        try:

                            detail = (
                                admin_login_response
                                .json()
                                .get(
                                    "detail",
                                    "Invalid email or password."
                                )
                            )

                        except Exception:

                            detail = (
                                "Invalid email or password."
                            )

                        st.error(detail)

                except requests.exceptions.RequestException as e:

                    st.error(
                        "Unable to connect to TRAVELX backend: "
                        f"{e}"
                    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

if st.session_state.admin_authenticated:

    with st.sidebar:
        st.html("""
        <div class="sidebar-brand">
            <div class="sidebar-logo">👑 TRAVELX ADMIN</div>
            <div class="sidebar-tagline">CONTROL • ANALYZE • MANAGE</div>
        </div>
        """)

        st.success("Administrator")
        st.caption(st.session_state.admin_email)
        st.divider()

        if st.button(
            "📊 Dashboard",
            use_container_width=True,
            key="admin_sidebar_dashboard"
        ):
            st.session_state.page = "Admin Dashboard"
            st.rerun()

        if st.button(
            "🚌 Manage Buses",
            use_container_width=True,
            key="admin_sidebar_buses"
        ):
            st.session_state.page = "Admin Buses"
            st.rerun()

        if st.button(
            "🚆 Manage Trains",
            use_container_width=True,
            key="admin_sidebar_trains"
        ):
            st.session_state.page = "Admin Trains"
            st.rerun()

        if st.button(
            "🏨 Manage Hotels",
            use_container_width=True,
            key="admin_sidebar_hotels"
        ):
            st.session_state.page = "Admin Hotels"
            st.rerun()

        if st.button(
            "✈️ Manage Flights",
            use_container_width=True,
            key="admin_sidebar_flights"
        ):
            st.session_state.page = "Admin Flights"
            st.rerun()

        if st.button(
            "🚕 Manage Cabs",
            use_container_width=True,
            key="admin_sidebar_cabs"
        ):
            st.session_state.page = "Admin Cabs"
            st.rerun()

        if st.button(
            "🍔 Manage Food",
            use_container_width=True,
            key="admin_sidebar_food"
        ):
            st.session_state.page = "Admin Food"
            st.rerun()

        if st.button(
            "🎬 Manage Movies",
            use_container_width=True,
            key="admin_sidebar_movies"
        ):
            st.session_state.page = "Admin Movies"
            st.rerun()

        if st.button(
            "🎟️ Manage Events",
            use_container_width=True,
            key="admin_sidebar_events"
        ):
            st.session_state.page = "Admin Events"
            st.rerun()

        if st.button(
            "🔄 Refresh Dashboard",
            use_container_width=True,
            key="admin_sidebar_refresh"
        ):
            st.rerun()

        st.divider()

        if st.button(
            "🚪 Admin Logout",
            use_container_width=True,
            key="admin_logout"
        ):
            st.session_state.admin_authenticated = False
            st.session_state.admin_email = ""
            st.session_state.admin_token = ""
            st.session_state.page = "Home"
            st.rerun()

    if st.session_state.page == "Admin Buses":

        st.title("🚌 Bus Management")
        st.caption("Add, edit, inspect and delete buses from the TRAVELX admin panel.")
        st.divider()

        bus_tab1, bus_tab2, bus_tab3 = st.tabs([
            "📋 All Buses",
            "➕ Add Bus",
            "✏️ Edit / Delete"
        ])

        import pandas as pd

        # -----------------------------------------------------
        # ALL BUSES
        # -----------------------------------------------------
        with bus_tab1:
            col1, col2 = st.columns([5, 1])
            with col1:
                bus_search = st.text_input(
                    "Search buses",
                    placeholder="Operator, bus number, source or destination...",
                    key="admin_bus_search"
                )
            with col2:
                st.write("")
                if st.button(
                    "🔄 Refresh",
                    key="admin_refresh_buses",
                    use_container_width=True
                ):
                    st.rerun()

            response = admin_api_get("/buses/admin/all")

            if response is None:
                st.warning("Unable to load buses.")
            elif response.status_code == 200:
                buses = response.json()

                if bus_search.strip():
                    term = bus_search.strip().lower()
                    buses = [
                        bus for bus in buses
                        if term in str(bus.get("operator", "")).lower()
                        or term in str(bus.get("bus_number", "")).lower()
                        or term in str(bus.get("source", "")).lower()
                        or term in str(bus.get("destination", "")).lower()
                    ]

                if buses:
                    bus_df = pd.DataFrame(buses).rename(columns={
                        "id": "Bus ID",
                        "operator": "Operator",
                        "bus_number": "Bus Number",
                        "source": "Source",
                        "destination": "Destination",
                        "departure_time": "Departure",
                        "arrival_time": "Arrival",
                        "price": "Price",
                        "available_seats": "Available Seats"
                    })

                    if "Price" in bus_df.columns:
                        bus_df["Price"] = bus_df["Price"].apply(
                            lambda x: f"₹{float(x):,.0f}"
                        )

                    st.dataframe(
                        bus_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    st.success(f"Showing {len(buses)} bus(es).")
                else:
                    st.info("No buses found.")
            else:
                st.error(
                    f"Unable to load buses: "
                    f"{admin_error_message(response, 'Request failed.')}"
                )

        # -----------------------------------------------------
        # ADD BUS
        # -----------------------------------------------------
        with bus_tab2:
            st.subheader("➕ Add New Bus")

            with st.form("admin_add_bus_form"):
                c1, c2 = st.columns(2)

                with c1:
                    operator = st.text_input("Operator", placeholder="TSRTC")
                    bus_number = st.text_input("Bus Number", placeholder="TS09AB1234")
                    source = st.text_input("Source", placeholder="Hyderabad")
                    destination = st.text_input("Destination", placeholder="Bangalore")

                with c2:
                    departure_time = st.text_input("Departure Time", placeholder="08:00 AM")
                    arrival_time = st.text_input("Arrival Time", placeholder="04:00 PM")
                    price = st.number_input("Price (₹)", min_value=1, value=500, step=50)
                    available_seats = st.number_input(
                        "Available Seats",
                        min_value=1,
                        value=40,
                        step=1
                    )

                submitted = st.form_submit_button(
                    "🚀 Create Bus",
                    type="primary",
                    use_container_width=True
                )

            if submitted:
                if not all([
                    operator.strip(),
                    bus_number.strip(),
                    source.strip(),
                    destination.strip(),
                    departure_time.strip(),
                    arrival_time.strip()
                ]):
                    st.warning("Please fill all bus fields.")
                else:
                    payload = {
                        "operator": operator.strip(),
                        "bus_number": bus_number.strip(),
                        "source": source.strip(),
                        "destination": destination.strip(),
                        "departure_time": departure_time.strip(),
                        "arrival_time": arrival_time.strip(),
                        "price": int(price),
                        "available_seats": int(available_seats)
                    }

                    response = admin_api_request(
                        "POST",
                        "/buses/admin/create",
                        payload
                    )

                    if response is not None and response.status_code in [200, 201]:
                        st.success("Bus created successfully! 🚌")
                        st.rerun()
                    else:
                        st.error(
                            admin_error_message(
                                response,
                                "Unable to create bus."
                            )
                        )

        # -----------------------------------------------------
        # EDIT / DELETE BUS
        # -----------------------------------------------------
        with bus_tab3:
            st.subheader("✏️ Edit or Delete Bus")

            bus_id = st.number_input(
                "Bus ID",
                min_value=1,
                value=1,
                step=1,
                key="admin_edit_bus_id"
            )

            load_col, delete_col = st.columns(2)

            with load_col:
                load_bus = st.button(
                    "🔎 Load Bus",
                    use_container_width=True,
                    key="admin_load_bus"
                )

            with delete_col:
                delete_bus = st.button(
                    "🗑️ Delete Bus",
                    use_container_width=True,
                    key="admin_delete_bus",
                    type="secondary"
                )

            if load_bus:
                response = admin_api_get(
                    f"/buses/admin/{int(bus_id)}"
                )

                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_bus = response.json()
                else:
                    st.session_state.admin_edit_bus = None
                    st.error(
                        admin_error_message(
                            response,
                            "Bus not found."
                        )
                    )

            bus_data = st.session_state.get("admin_edit_bus")

            if bus_data:
                st.info(
                    f"Editing Bus #{bus_data.get('id')} — "
                    f"{bus_data.get('operator', '')} / "
                    f"{bus_data.get('bus_number', '')}"
                )

                with st.form("admin_edit_bus_form"):
                    e1, e2 = st.columns(2)

                    with e1:
                        edit_operator = st.text_input(
                            "Operator",
                            value=str(bus_data.get("operator", "")),
                            key="edit_bus_operator"
                        )
                        edit_bus_number = st.text_input(
                            "Bus Number",
                            value=str(bus_data.get("bus_number", "")),
                            key="edit_bus_number"
                        )
                        edit_source = st.text_input(
                            "Source",
                            value=str(bus_data.get("source", "")),
                            key="edit_bus_source"
                        )
                        edit_destination = st.text_input(
                            "Destination",
                            value=str(bus_data.get("destination", "")),
                            key="edit_bus_destination"
                        )

                    with e2:
                        edit_departure = st.text_input(
                            "Departure Time",
                            value=str(bus_data.get("departure_time", "")),
                            key="edit_bus_departure"
                        )
                        edit_arrival = st.text_input(
                            "Arrival Time",
                            value=str(bus_data.get("arrival_time", "")),
                            key="edit_bus_arrival"
                        )
                        edit_price = st.number_input(
                            "Price (₹)",
                            min_value=1,
                            value=int(bus_data.get("price", 1)),
                            step=50,
                            key="edit_bus_price"
                        )
                        edit_seats = st.number_input(
                            "Available Seats",
                            min_value=1,
                            value=max(1, int(bus_data.get("available_seats", 1))),
                            step=1,
                            key="edit_bus_seats"
                        )

                    update_bus = st.form_submit_button(
                        "💾 Save Changes",
                        type="primary",
                        use_container_width=True
                    )

                if update_bus:
                    payload = {
                        "operator": edit_operator.strip(),
                        "bus_number": edit_bus_number.strip(),
                        "source": edit_source.strip(),
                        "destination": edit_destination.strip(),
                        "departure_time": edit_departure.strip(),
                        "arrival_time": edit_arrival.strip(),
                        "price": int(edit_price),
                        "available_seats": int(edit_seats)
                    }

                    if not all([
                        payload["operator"],
                        payload["bus_number"],
                        payload["source"],
                        payload["destination"],
                        payload["departure_time"],
                        payload["arrival_time"]
                    ]):
                        st.warning("Please fill all bus fields.")
                    else:
                        response = admin_api_request(
                            "PUT",
                            f"/buses/admin/{int(bus_id)}",
                            payload
                        )

                        if response is not None and response.status_code == 200:
                            st.success("Bus updated successfully! ✅")
                            st.session_state.admin_edit_bus = response.json()
                            st.rerun()
                        else:
                            st.error(
                                admin_error_message(
                                    response,
                                    "Unable to update bus."
                                )
                            )

            if delete_bus:
                response = admin_api_request(
                    "DELETE",
                    f"/buses/admin/{int(bus_id)}"
                )

                if response is not None and response.status_code == 200:
                    st.success("Bus deleted successfully! 🗑️")
                    st.session_state.admin_edit_bus = None
                    st.rerun()
                else:
                    st.error(
                        admin_error_message(
                            response,
                            "Unable to delete bus."
                        )
                    )

    elif st.session_state.page == "Admin Trains":
        st.title("🚆 Train Management")
        st.caption("Add, edit, inspect and delete trains from the TRAVELX admin panel.")
        st.divider()

        train_tab1, train_tab2, train_tab3 = st.tabs([
            "📋 All Trains",
            "➕ Add Train",
            "✏️ Edit / Delete"
        ])

        import pandas as pd

        # -----------------------------------------------------
        # ALL TRAINS
        # -----------------------------------------------------
        with train_tab1:
            col1, col2 = st.columns([5, 1])
            with col1:
                train_search = st.text_input(
                    "Search trains",
                    placeholder="Train name, number, source or destination...",
                    key="admin_train_search"
                )
            with col2:
                st.write("")
                if st.button(
                    "🔄 Refresh",
                    key="admin_refresh_trains",
                    use_container_width=True
                ):
                    st.rerun()

            response = admin_api_get("/trains/admin/all")

            if response is None:
                st.warning("Unable to load trains.")
            elif response.status_code == 200:
                trains = response.json()

                if train_search.strip():
                    term = train_search.strip().lower()
                    trains = [
                        train for train in trains
                        if term in str(train.get("train_name", "")).lower()
                        or term in str(train.get("train_number", "")).lower()
                        or term in str(train.get("source", "")).lower()
                        or term in str(train.get("destination", "")).lower()
                    ]

                if trains:
                    train_df = pd.DataFrame(trains).rename(columns={
                        "id": "Train ID",
                        "train_name": "Train Name",
                        "train_number": "Train Number",
                        "source": "Source",
                        "destination": "Destination",
                        "departure_time": "Departure",
                        "arrival_time": "Arrival",
                        "sleeper_price": "Sleeper",
                        "third_ac_price": "3A",
                        "second_ac_price": "2A",
                        "first_ac_price": "1A",
                        "available_seats": "Available Seats"
                    })

                    for column in ["Sleeper", "3A", "2A", "1A"]:
                        if column in train_df.columns:
                            train_df[column] = train_df[column].apply(
                                lambda x: f"₹{float(x):,.0f}"
                            )

                    st.dataframe(
                        train_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    st.success(f"Showing {len(trains)} train(s).")
                else:
                    st.info("No trains found.")
            else:
                st.error(
                    f"Unable to load trains: "
                    f"{admin_error_message(response, 'Request failed.')}"
                )

        # -----------------------------------------------------
        # ADD TRAIN
        # -----------------------------------------------------
        with train_tab2:
            st.subheader("➕ Add New Train")

            with st.form("admin_add_train_form"):
                c1, c2 = st.columns(2)

                with c1:
                    train_name = st.text_input(
                        "Train Name",
                        placeholder="Hyderabad Express"
                    )
                    train_number = st.text_input(
                        "Train Number",
                        placeholder="12727"
                    )
                    source = st.text_input(
                        "Source",
                        placeholder="Hyderabad"
                    )
                    destination = st.text_input(
                        "Destination",
                        placeholder="Visakhapatnam"
                    )
                    departure_time = st.text_input(
                        "Departure Time",
                        placeholder="06:30 AM"
                    )
                    arrival_time = st.text_input(
                        "Arrival Time",
                        placeholder="02:30 PM"
                    )

                with c2:
                    sleeper_price = st.number_input(
                        "Sleeper Price (₹)",
                        min_value=1,
                        value=500,
                        step=50
                    )
                    third_ac_price = st.number_input(
                        "3A Price (₹)",
                        min_value=1,
                        value=1200,
                        step=50
                    )
                    second_ac_price = st.number_input(
                        "2A Price (₹)",
                        min_value=1,
                        value=1800,
                        step=50
                    )
                    first_ac_price = st.number_input(
                        "1A Price (₹)",
                        min_value=1,
                        value=2500,
                        step=50
                    )
                    available_seats = st.number_input(
                        "Available Seats",
                        min_value=1,
                        value=100,
                        step=1
                    )

                submitted = st.form_submit_button(
                    "🚀 Create Train",
                    type="primary",
                    use_container_width=True
                )

            if submitted:
                if not all([
                    train_name.strip(),
                    train_number.strip(),
                    source.strip(),
                    destination.strip(),
                    departure_time.strip(),
                    arrival_time.strip()
                ]):
                    st.warning("Please fill all train fields.")
                else:
                    payload = {
                        "train_name": train_name.strip(),
                        "train_number": train_number.strip(),
                        "source": source.strip(),
                        "destination": destination.strip(),
                        "departure_time": departure_time.strip(),
                        "arrival_time": arrival_time.strip(),
                        "sleeper_price": int(sleeper_price),
                        "third_ac_price": int(third_ac_price),
                        "second_ac_price": int(second_ac_price),
                        "first_ac_price": int(first_ac_price),
                        "available_seats": int(available_seats)
                    }

                    response = admin_api_request(
                        "POST",
                        "/trains/admin/create",
                        payload
                    )

                    if response is not None and response.status_code in [200, 201]:
                        st.success("Train created successfully! 🚆")
                        st.rerun()
                    else:
                        st.error(
                            admin_error_message(
                                response,
                                "Unable to create train."
                            )
                        )

        # -----------------------------------------------------
        # EDIT / DELETE TRAIN
        # -----------------------------------------------------
        with train_tab3:
            st.subheader("✏️ Edit or Delete Train")

            train_id = st.number_input(
                "Train ID",
                min_value=1,
                value=1,
                step=1,
                key="admin_edit_train_id"
            )

            load_col, delete_col = st.columns(2)

            with load_col:
                load_train = st.button(
                    "🔎 Load Train",
                    use_container_width=True,
                    key="admin_load_train"
                )

            with delete_col:
                delete_train = st.button(
                    "🗑️ Delete Train",
                    use_container_width=True,
                    key="admin_delete_train"
                )

            if load_train:
                response = admin_api_get(
                    f"/trains/admin/{int(train_id)}"
                )

                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_train = response.json()
                else:
                    st.session_state.admin_edit_train = None
                    st.error(
                        admin_error_message(
                            response,
                            "Train not found."
                        )
                    )

            train_data = st.session_state.get("admin_edit_train")

            if train_data:
                st.info(
                    f"Editing Train #{train_data.get('id')} — "
                    f"{train_data.get('train_name', '')} / "
                    f"{train_data.get('train_number', '')}"
                )

                with st.form("admin_edit_train_form"):
                    e1, e2 = st.columns(2)

                    with e1:
                        edit_train_name = st.text_input(
                            "Train Name",
                            value=str(train_data.get("train_name", "")),
                            key="edit_train_name"
                        )
                        edit_train_number = st.text_input(
                            "Train Number",
                            value=str(train_data.get("train_number", "")),
                            key="edit_train_number"
                        )
                        edit_source = st.text_input(
                            "Source",
                            value=str(train_data.get("source", "")),
                            key="edit_train_source"
                        )
                        edit_destination = st.text_input(
                            "Destination",
                            value=str(train_data.get("destination", "")),
                            key="edit_train_destination"
                        )
                        edit_departure = st.text_input(
                            "Departure Time",
                            value=str(train_data.get("departure_time", "")),
                            key="edit_train_departure"
                        )
                        edit_arrival = st.text_input(
                            "Arrival Time",
                            value=str(train_data.get("arrival_time", "")),
                            key="edit_train_arrival"
                        )

                    with e2:
                        edit_sleeper = st.number_input(
                            "Sleeper Price (₹)",
                            min_value=1,
                            value=int(train_data.get("sleeper_price", 1)),
                            step=50,
                            key="edit_train_sleeper"
                        )
                        edit_third_ac = st.number_input(
                            "3A Price (₹)",
                            min_value=1,
                            value=int(train_data.get("third_ac_price", 1)),
                            step=50,
                            key="edit_train_3a"
                        )
                        edit_second_ac = st.number_input(
                            "2A Price (₹)",
                            min_value=1,
                            value=int(train_data.get("second_ac_price", 1)),
                            step=50,
                            key="edit_train_2a"
                        )
                        edit_first_ac = st.number_input(
                            "1A Price (₹)",
                            min_value=1,
                            value=int(train_data.get("first_ac_price", 1)),
                            step=50,
                            key="edit_train_1a"
                        )
                        edit_seats = st.number_input(
                            "Available Seats",
                            min_value=1,
                            value=max(1, int(train_data.get("available_seats", 1))),
                            step=1,
                            key="edit_train_seats"
                        )

                    update_train = st.form_submit_button(
                        "💾 Save Changes",
                        type="primary",
                        use_container_width=True
                    )

                if update_train:
                    payload = {
                        "train_name": edit_train_name.strip(),
                        "train_number": edit_train_number.strip(),
                        "source": edit_source.strip(),
                        "destination": edit_destination.strip(),
                        "departure_time": edit_departure.strip(),
                        "arrival_time": edit_arrival.strip(),
                        "sleeper_price": int(edit_sleeper),
                        "third_ac_price": int(edit_third_ac),
                        "second_ac_price": int(edit_second_ac),
                        "first_ac_price": int(edit_first_ac),
                        "available_seats": int(edit_seats)
                    }

                    if not all([
                        payload["train_name"],
                        payload["train_number"],
                        payload["source"],
                        payload["destination"],
                        payload["departure_time"],
                        payload["arrival_time"]
                    ]):
                        st.warning("Please fill all train fields.")
                    else:
                        response = admin_api_request(
                            "PUT",
                            f"/trains/admin/{int(train_id)}",
                            payload
                        )

                        if response is not None and response.status_code == 200:
                            st.success("Train updated successfully! ✅")
                            st.session_state.admin_edit_train = response.json()
                            st.rerun()
                        else:
                            st.error(
                                admin_error_message(
                                    response,
                                    "Unable to update train."
                                )
                            )

            if delete_train:
                response = admin_api_request(
                    "DELETE",
                    f"/trains/admin/{int(train_id)}"
                )

                if response is not None and response.status_code == 200:
                    st.success("Train deleted successfully! 🗑️")
                    st.session_state.admin_edit_train = None
                    st.rerun()
                else:
                    st.error(
                        admin_error_message(
                            response,
                            "Unable to delete train."
                        )
                    )

    elif st.session_state.page == "Admin Hotels":

        st.title("🏨 Hotel Management")
        st.caption("Add, edit, inspect and delete hotels from the TRAVELX admin panel.")
        st.divider()

        hotel_tab1, hotel_tab2, hotel_tab3 = st.tabs([
            "📋 All Hotels",
            "➕ Add Hotel",
            "✏️ Edit / Delete"
        ])

        import pandas as pd

        # -----------------------------------------------------
        # ALL HOTELS
        # -----------------------------------------------------
        with hotel_tab1:
            col1, col2 = st.columns([5, 1])
            with col1:
                hotel_search = st.text_input(
                    "Search hotels",
                    placeholder="Name, city, address or amenities...",
                    key="admin_hotel_search"
                )
            with col2:
                st.write("")
                if st.button(
                    "🔄 Refresh",
                    key="admin_refresh_hotels",
                    use_container_width=True
                ):
                    st.rerun()

            response = admin_api_get("/hotels/admin/all")

            if response is None:
                st.warning("Unable to load hotels.")
            elif response.status_code == 200:
                hotels = response.json()

                if hotel_search.strip():
                    term = hotel_search.strip().lower()
                    hotels = [
                        hotel for hotel in hotels
                        if term in str(hotel.get("name", "")).lower()
                        or term in str(hotel.get("city", "")).lower()
                        or term in str(hotel.get("address", "")).lower()
                        or term in str(hotel.get("amenities", "")).lower()
                    ]

                if hotels:
                    hotel_df = pd.DataFrame(hotels).rename(columns={
                        "id": "Hotel ID",
                        "name": "Hotel Name",
                        "city": "City",
                        "address": "Address",
                        "description": "Description",
                        "rating": "Rating",
                        "price_per_night": "Price/Night",
                        "available_rooms": "Available Rooms",
                        "amenities": "Amenities"
                    })

                    if "Price/Night" in hotel_df.columns:
                        hotel_df["Price/Night"] = hotel_df["Price/Night"].apply(
                            lambda x: f"₹{float(x):,.0f}"
                        )

                    st.dataframe(
                        hotel_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    st.success(f"Showing {len(hotels)} hotel(s).")
                else:
                    st.info("No hotels found.")
            else:
                st.error(
                    f"Unable to load hotels: "
                    f"{admin_error_message(response, 'Request failed.')}"
                )

        # -----------------------------------------------------
        # ADD HOTEL
        # -----------------------------------------------------
        with hotel_tab2:
            st.subheader("➕ Add New Hotel")

            with st.form("admin_add_hotel_form"):
                c1, c2 = st.columns(2)

                with c1:
                    hotel_name = st.text_input(
                        "Hotel Name",
                        placeholder="TRAVELX Grand Hotel"
                    )
                    hotel_city = st.text_input(
                        "City",
                        placeholder="Hyderabad"
                    )
                    hotel_address = st.text_input(
                        "Address",
                        placeholder="Banjara Hills, Hyderabad"
                    )
                    hotel_rating = st.number_input(
                        "Rating",
                        min_value=0.0,
                        max_value=5.0,
                        value=4.0,
                        step=0.1,
                        format="%.1f"
                    )

                with c2:
                    hotel_description = st.text_area(
                        "Description",
                        placeholder="Comfortable rooms with modern facilities...",
                        height=120
                    )
                    hotel_price = st.number_input(
                        "Price Per Night (₹)",
                        min_value=1,
                        value=2500,
                        step=100
                    )
                    hotel_rooms = st.number_input(
                        "Available Rooms",
                        min_value=1,
                        value=20,
                        step=1
                    )
                    hotel_amenities = st.text_input(
                        "Amenities",
                        placeholder="WiFi, Pool, Breakfast, Parking"
                    )

                submitted = st.form_submit_button(
                    "🚀 Create Hotel",
                    type="primary",
                    use_container_width=True
                )

            if submitted:
                if not all([
                    hotel_name.strip(),
                    hotel_city.strip(),
                    hotel_address.strip(),
                    hotel_description.strip(),
                    hotel_amenities.strip()
                ]):
                    st.warning("Please fill all hotel fields.")
                else:
                    payload = {
                        "name": hotel_name.strip(),
                        "city": hotel_city.strip(),
                        "address": hotel_address.strip(),
                        "description": hotel_description.strip(),
                        "rating": float(hotel_rating),
                        "price_per_night": int(hotel_price),
                        "available_rooms": int(hotel_rooms),
                        "amenities": hotel_amenities.strip()
                    }

                    response = admin_api_request(
                        "POST",
                        "/hotels/admin/create",
                        payload
                    )

                    if response is not None and response.status_code in [200, 201]:
                        st.success("Hotel created successfully! 🏨")
                        st.rerun()
                    else:
                        st.error(
                            admin_error_message(
                                response,
                                "Unable to create hotel."
                            )
                        )

        # -----------------------------------------------------
        # EDIT / DELETE HOTEL
        # -----------------------------------------------------
        with hotel_tab3:
            st.subheader("✏️ Edit or Delete Hotel")

            hotel_id = st.number_input(
                "Hotel ID",
                min_value=1,
                value=1,
                step=1,
                key="admin_edit_hotel_id"
            )

            load_col, delete_col = st.columns(2)

            with load_col:
                load_hotel = st.button(
                    "🔎 Load Hotel",
                    use_container_width=True,
                    key="admin_load_hotel"
                )

            with delete_col:
                delete_hotel = st.button(
                    "🗑️ Delete Hotel",
                    use_container_width=True,
                    key="admin_delete_hotel"
                )

            if load_hotel:
                response = admin_api_get(
                    f"/hotels/admin/{int(hotel_id)}"
                )

                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_hotel = response.json()
                else:
                    st.session_state.admin_edit_hotel = None
                    st.error(
                        admin_error_message(
                            response,
                            "Hotel not found."
                        )
                    )

            hotel_data = st.session_state.get("admin_edit_hotel")

            if hotel_data:
                st.info(
                    f"Editing Hotel #{hotel_data.get('id')} — "
                    f"{hotel_data.get('name', '')} / "
                    f"{hotel_data.get('city', '')}"
                )

                with st.form("admin_edit_hotel_form"):
                    e1, e2 = st.columns(2)

                    with e1:
                        edit_hotel_name = st.text_input(
                            "Hotel Name",
                            value=str(hotel_data.get("name", "")),
                            key="edit_hotel_name"
                        )
                        edit_hotel_city = st.text_input(
                            "City",
                            value=str(hotel_data.get("city", "")),
                            key="edit_hotel_city"
                        )
                        edit_hotel_address = st.text_input(
                            "Address",
                            value=str(hotel_data.get("address", "")),
                            key="edit_hotel_address"
                        )
                        edit_hotel_rating = st.number_input(
                            "Rating",
                            min_value=0.0,
                            max_value=5.0,
                            value=float(hotel_data.get("rating", 0)),
                            step=0.1,
                            format="%.1f",
                            key="edit_hotel_rating"
                        )

                    with e2:
                        edit_hotel_description = st.text_area(
                            "Description",
                            value=str(hotel_data.get("description", "")),
                            height=120,
                            key="edit_hotel_description"
                        )
                        edit_hotel_price = st.number_input(
                            "Price Per Night (₹)",
                            min_value=1,
                            value=max(1, int(hotel_data.get("price_per_night", 1))),
                            step=100,
                            key="edit_hotel_price"
                        )
                        edit_hotel_rooms = st.number_input(
                            "Available Rooms",
                            min_value=1,
                            value=max(1, int(hotel_data.get("available_rooms", 1))),
                            step=1,
                            key="edit_hotel_rooms"
                        )
                        edit_hotel_amenities = st.text_input(
                            "Amenities",
                            value=str(hotel_data.get("amenities", "")),
                            key="edit_hotel_amenities"
                        )

                    update_hotel = st.form_submit_button(
                        "💾 Save Changes",
                        type="primary",
                        use_container_width=True
                    )

                if update_hotel:
                    payload = {
                        "name": edit_hotel_name.strip(),
                        "city": edit_hotel_city.strip(),
                        "address": edit_hotel_address.strip(),
                        "description": edit_hotel_description.strip(),
                        "rating": float(edit_hotel_rating),
                        "price_per_night": int(edit_hotel_price),
                        "available_rooms": int(edit_hotel_rooms),
                        "amenities": edit_hotel_amenities.strip()
                    }

                    if not all([
                        payload["name"],
                        payload["city"],
                        payload["address"],
                        payload["description"],
                        payload["amenities"]
                    ]):
                        st.warning("Please fill all hotel fields.")
                    else:
                        response = admin_api_request(
                            "PUT",
                            f"/hotels/admin/{int(hotel_id)}",
                            payload
                        )

                        if response is not None and response.status_code == 200:
                            st.success("Hotel updated successfully! ✅")
                            st.session_state.admin_edit_hotel = response.json()
                            st.rerun()
                        else:
                            st.error(
                                admin_error_message(
                                    response,
                                    "Unable to update hotel."
                                )
                            )

            if delete_hotel:
                response = admin_api_request(
                    "DELETE",
                    f"/hotels/admin/{int(hotel_id)}"
                )

                if response is not None and response.status_code == 200:
                    st.success("Hotel deleted successfully! 🗑️")
                    st.session_state.admin_edit_hotel = None
                    st.rerun()
                else:
                    st.error(
                        admin_error_message(
                            response,
                            "Unable to delete hotel."
                        )
                    )

    elif st.session_state.page == "Admin Flights":

        st.title("✈️ Flight Management")
        st.caption("Add, edit, inspect and delete flights from the TRAVELX admin panel.")
        st.divider()

        flight_tab1, flight_tab2, flight_tab3 = st.tabs([
            "📋 All Flights",
            "➕ Add Flight",
            "✏️ Edit / Delete"
        ])

        # -----------------------------------------------------
        # ALL FLIGHTS
        # -----------------------------------------------------
        with flight_tab1:
            col1, col2 = st.columns([5, 1])

            with col1:
                flight_search = st.text_input(
                    "Search flights",
                    placeholder="Airline, flight number, source or destination...",
                    key="admin_flight_search"
                )

            with col2:
                st.write("")
                if st.button(
                    "🔄 Refresh",
                    key="admin_refresh_flights",
                    use_container_width=True
                ):
                    st.rerun()

            response = admin_api_get("/flights/admin/all")

            if response is None:
                st.warning("Unable to load flights.")
            elif response.status_code == 200:
                flights = response.json()

                if flight_search.strip():
                    term = flight_search.strip().lower()
                    flights = [
                        flight for flight in flights
                        if term in str(flight.get("airline", "")).lower()
                        or term in str(flight.get("flight_number", "")).lower()
                        or term in str(flight.get("source", "")).lower()
                        or term in str(flight.get("destination", "")).lower()
                    ]

                if flights:
                    flight_df = pd.DataFrame(flights).rename(columns={
                        "id": "Flight ID",
                        "flight_number": "Flight Number",
                        "airline": "Airline",
                        "source": "Source",
                        "destination": "Destination",
                        "departure_time": "Departure",
                        "arrival_time": "Arrival",
                        "economy_price": "Economy Price",
                        "premium_economy_price": "Premium Economy",
                        "business_price": "Business Price",
                        "available_seats": "Available Seats"
                    })

                    for column in ["Economy Price", "Premium Economy", "Business Price"]:
                        if column in flight_df.columns:
                            flight_df[column] = flight_df[column].apply(
                                lambda x: f"₹{float(x):,.0f}"
                            )

                    st.dataframe(
                        flight_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    st.success(f"Showing {len(flights)} flight(s).")
                else:
                    st.info("No flights found.")
            else:
                st.error(
                    f"Unable to load flights: "
                    f"{admin_error_message(response, 'Request failed.')}"
                )

        # -----------------------------------------------------
        # ADD FLIGHT
        # -----------------------------------------------------
        with flight_tab2:
            st.subheader("➕ Add New Flight")

            with st.form("admin_add_flight_form"):
                c1, c2 = st.columns(2)

                with c1:
                    flight_number = st.text_input(
                        "Flight Number",
                        placeholder="6E123"
                    )
                    airline = st.text_input(
                        "Airline",
                        placeholder="IndiGo"
                    )
                    source = st.text_input(
                        "Source",
                        placeholder="Hyderabad"
                    )
                    destination = st.text_input(
                        "Destination",
                        placeholder="Delhi"
                    )
                    departure_time = st.text_input(
                        "Departure Time",
                        placeholder="08:30 AM"
                    )
                    arrival_time = st.text_input(
                        "Arrival Time",
                        placeholder="10:45 AM"
                    )

                with c2:
                    economy_price = st.number_input(
                        "Economy Price (₹)",
                        min_value=1,
                        value=4500,
                        step=100
                    )
                    premium_economy_price = st.number_input(
                        "Premium Economy Price (₹)",
                        min_value=1,
                        value=6500,
                        step=100
                    )
                    business_price = st.number_input(
                        "Business Price (₹)",
                        min_value=1,
                        value=9500,
                        step=100
                    )
                    available_seats = st.number_input(
                        "Available Seats",
                        min_value=1,
                        value=120,
                        step=1
                    )

                submitted = st.form_submit_button(
                    "🚀 Create Flight",
                    type="primary",
                    use_container_width=True
                )

            if submitted:
                if not all([
                    flight_number.strip(),
                    airline.strip(),
                    source.strip(),
                    destination.strip(),
                    departure_time.strip(),
                    arrival_time.strip()
                ]):
                    st.warning("Please fill all flight fields.")
                else:
                    payload = {
                        "flight_number": flight_number.strip(),
                        "airline": airline.strip(),
                        "source": source.strip(),
                        "destination": destination.strip(),
                        "departure_time": departure_time.strip(),
                        "arrival_time": arrival_time.strip(),
                        "economy_price": int(economy_price),
                        "premium_economy_price": int(premium_economy_price),
                        "business_price": int(business_price),
                        "available_seats": int(available_seats)
                    }

                    response = admin_api_request(
                        "POST",
                        "/flights/admin/create",
                        payload
                    )

                    if response is not None and response.status_code in [200, 201]:
                        st.success("Flight created successfully! ✈️")
                        st.rerun()
                    else:
                        st.error(
                            admin_error_message(
                                response,
                                "Unable to create flight."
                            )
                        )

        # -----------------------------------------------------
        # EDIT / DELETE FLIGHT
        # -----------------------------------------------------
        with flight_tab3:
            st.subheader("✏️ Edit or Delete Flight")

            flight_id = st.number_input(
                "Flight ID",
                min_value=1,
                value=1,
                step=1,
                key="admin_edit_flight_id"
            )

            load_col, delete_col = st.columns(2)

            with load_col:
                load_flight = st.button(
                    "🔎 Load Flight",
                    use_container_width=True,
                    key="admin_load_flight"
                )

            with delete_col:
                delete_flight = st.button(
                    "🗑️ Delete Flight",
                    use_container_width=True,
                    key="admin_delete_flight"
                )

            if load_flight:
                response = admin_api_get(
                    f"/flights/admin/{int(flight_id)}"
                )

                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_flight = response.json()
                else:
                    st.session_state.admin_edit_flight = None
                    st.error(
                        admin_error_message(
                            response,
                            "Flight not found."
                        )
                    )

            flight_data = st.session_state.get("admin_edit_flight")

            if flight_data:
                st.info(
                    f"Editing Flight #{flight_data.get('id')} — "
                    f"{flight_data.get('airline', '')} / "
                    f"{flight_data.get('flight_number', '')}"
                )

                with st.form("admin_edit_flight_form"):
                    e1, e2 = st.columns(2)

                    with e1:
                        edit_flight_number = st.text_input(
                            "Flight Number",
                            value=str(flight_data.get("flight_number", "")),
                            key="edit_flight_number"
                        )
                        edit_airline = st.text_input(
                            "Airline",
                            value=str(flight_data.get("airline", "")),
                            key="edit_flight_airline"
                        )
                        edit_source = st.text_input(
                            "Source",
                            value=str(flight_data.get("source", "")),
                            key="edit_flight_source"
                        )
                        edit_destination = st.text_input(
                            "Destination",
                            value=str(flight_data.get("destination", "")),
                            key="edit_flight_destination"
                        )
                        edit_departure = st.text_input(
                            "Departure Time",
                            value=str(flight_data.get("departure_time", "")),
                            key="edit_flight_departure"
                        )
                        edit_arrival = st.text_input(
                            "Arrival Time",
                            value=str(flight_data.get("arrival_time", "")),
                            key="edit_flight_arrival"
                        )

                    with e2:
                        edit_economy = st.number_input(
                            "Economy Price (₹)",
                            min_value=1,
                            value=max(1, int(flight_data.get("economy_price", 1))),
                            step=100,
                            key="edit_flight_economy"
                        )
                        edit_premium = st.number_input(
                            "Premium Economy Price (₹)",
                            min_value=1,
                            value=max(1, int(flight_data.get("premium_economy_price", 1))),
                            step=100,
                            key="edit_flight_premium"
                        )
                        edit_business = st.number_input(
                            "Business Price (₹)",
                            min_value=1,
                            value=max(1, int(flight_data.get("business_price", 1))),
                            step=100,
                            key="edit_flight_business"
                        )
                        edit_seats = st.number_input(
                            "Available Seats",
                            min_value=1,
                            value=max(1, int(flight_data.get("available_seats", 1))),
                            step=1,
                            key="edit_flight_seats"
                        )

                    update_flight = st.form_submit_button(
                        "💾 Save Changes",
                        type="primary",
                        use_container_width=True
                    )

                if update_flight:
                    payload = {
                        "flight_number": edit_flight_number.strip(),
                        "airline": edit_airline.strip(),
                        "source": edit_source.strip(),
                        "destination": edit_destination.strip(),
                        "departure_time": edit_departure.strip(),
                        "arrival_time": edit_arrival.strip(),
                        "economy_price": int(edit_economy),
                        "premium_economy_price": int(edit_premium),
                        "business_price": int(edit_business),
                        "available_seats": int(edit_seats)
                    }

                    if not all([
                        payload["flight_number"],
                        payload["airline"],
                        payload["source"],
                        payload["destination"],
                        payload["departure_time"],
                        payload["arrival_time"]
                    ]):
                        st.warning("Please fill all flight fields.")
                    else:
                        response = admin_api_request(
                            "PUT",
                            f"/flights/admin/{int(flight_id)}",
                            payload
                        )

                        if response is not None and response.status_code == 200:
                            st.success("Flight updated successfully! ✅")
                            st.session_state.admin_edit_flight = response.json()
                            st.rerun()
                        else:
                            st.error(
                                admin_error_message(
                                    response,
                                    "Unable to update flight."
                                )
                            )

            if delete_flight:
                response = admin_api_request(
                    "DELETE",
                    f"/flights/admin/{int(flight_id)}"
                )

                if response is not None and response.status_code == 200:
                    st.success("Flight deleted successfully! 🗑️")
                    st.session_state.admin_edit_flight = None
                    st.rerun()
                else:
                    st.error(
                        admin_error_message(
                            response,
                            "Unable to delete flight."
                        )
                    )

    elif st.session_state.page == "Admin Cabs":

        st.title("🚕 Cab Management")
        st.caption("Add, edit, inspect and delete cabs from the TRAVELX admin panel.")
        st.divider()

        cab_tab1, cab_tab2, cab_tab3 = st.tabs([
            "📋 All Cabs",
            "➕ Add Cab",
            "✏️ Edit / Delete"
        ])

        # ========================================================
        # ALL CABS
        # ========================================================
        with cab_tab1:
            col1, col2 = st.columns([5, 1])
            with col1:
                cab_search = st.text_input(
                    "Search cabs",
                    placeholder="Driver, vehicle number, type, source or destination...",
                    key="admin_cab_search"
                )
            with col2:
                st.write("")
                if st.button(
                    "🔄 Refresh",
                    key="admin_refresh_cabs",
                    use_container_width=True
                ):
                    st.rerun()

            response = admin_api_get("/cabs/admin/all")
            if response is None:
                st.warning("Unable to load cabs.")
            elif response.status_code == 200:
                cabs = response.json()
                if cab_search.strip():
                    term = cab_search.strip().lower()
                    cabs = [
                        cab for cab in cabs
                        if term in str(cab.get("driver_name", "")).lower()
                        or term in str(cab.get("vehicle_number", "")).lower()
                        or term in str(cab.get("cab_type", "")).lower()
                        or term in str(cab.get("source", "")).lower()
                        or term in str(cab.get("destination", "")).lower()
                    ]

                if cabs:
                    cab_df = pd.DataFrame(cabs).rename(columns={
                        "id": "Cab ID",
                        "driver_name": "Driver",
                        "vehicle_number": "Vehicle Number",
                        "cab_type": "Cab Type",
                        "source": "Source",
                        "destination": "Destination",
                        "fare_per_km": "Fare / Km",
                        "available_seats": "Available Seats",
                        "rating": "Rating"
                    })
                    if "Fare / Km" in cab_df.columns:
                        cab_df["Fare / Km"] = cab_df["Fare / Km"].apply(
                            lambda x: f"₹{float(x):,.0f}"
                        )
                    if "Rating" in cab_df.columns:
                        cab_df["Rating"] = cab_df["Rating"].apply(
                            lambda x: f"⭐ {float(x):.1f}"
                        )
                    st.dataframe(
                        cab_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    st.success(f"Showing {len(cabs)} cab(s).")
                else:
                    st.info("No cabs found.")
            else:
                st.error(
                    f"Unable to load cabs: "
                    f"{admin_error_message(response, 'Request failed.')}"
                )

        # ========================================================
        # ADD CAB
        # ========================================================
        with cab_tab2:
            st.subheader("➕ Add New Cab")
            with st.form("admin_add_cab_form"):
                c1, c2 = st.columns(2)
                with c1:
                    driver_name = st.text_input(
                        "Driver Name",
                        placeholder="Rahul Sharma"
                    )
                    vehicle_number = st.text_input(
                        "Vehicle Number",
                        placeholder="TS09AB1234"
                    )
                    cab_type = st.text_input(
                        "Cab Type",
                        placeholder="Sedan"
                    )
                    source = st.text_input(
                        "Source",
                        placeholder="Hyderabad"
                    )
                    destination = st.text_input(
                        "Destination",
                        placeholder="Warangal"
                    )
                with c2:
                    fare_per_km = st.number_input(
                        "Fare per KM (₹)",
                        min_value=1.0,
                        value=15.0,
                        step=1.0
                    )
                    available_seats = st.number_input(
                        "Available Seats",
                        min_value=1,
                        value=4,
                        step=1
                    )
                    rating = st.number_input(
                        "Rating",
                        min_value=0.0,
                        max_value=5.0,
                        value=4.5,
                        step=0.1
                    )

                submitted = st.form_submit_button(
                    "🚀 Create Cab",
                    type="primary",
                    use_container_width=True
                )

            if submitted:
                if not all([
                    driver_name.strip(),
                    vehicle_number.strip(),
                    cab_type.strip(),
                    source.strip(),
                    destination.strip()
                ]):
                    st.warning("Please fill all cab fields.")
                elif rating < 0 or rating > 5:
                    st.warning("Rating must be between 0 and 5.")
                else:
                    payload = {
                        "driver_name": driver_name.strip(),
                        "vehicle_number": vehicle_number.strip(),
                        "cab_type": cab_type.strip(),
                        "source": source.strip(),
                        "destination": destination.strip(),
                        "fare_per_km": float(fare_per_km),
                        "available_seats": int(available_seats),
                        "rating": float(rating)
                    }
                    response = admin_api_request(
                        "POST",
                        "/cabs/admin/create",
                        payload
                    )
                    if response is not None and response.status_code in [200, 201]:
                        st.success("Cab created successfully! 🚕")
                        st.rerun()
                    else:
                        st.error(
                            admin_error_message(
                                response,
                                "Unable to create cab."
                            )
                        )

        # ========================================================
        # EDIT / DELETE CAB
        # ========================================================
        with cab_tab3:
            st.subheader("✏️ Edit or Delete Cab")
            cab_id = st.number_input(
                "Cab ID",
                min_value=1,
                value=1,
                step=1,
                key="admin_edit_cab_id"
            )

            load_col, delete_col = st.columns(2)
            with load_col:
                load_cab = st.button(
                    "🔎 Load Cab",
                    use_container_width=True,
                    key="admin_load_cab"
                )
            with delete_col:
                delete_cab = st.button(
                    "🗑️ Delete Cab",
                    use_container_width=True,
                    key="admin_delete_cab"
                )

            if load_cab:
                response = admin_api_get(
                    f"/cabs/admin/{int(cab_id)}"
                )
                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_cab = response.json()
                else:
                    st.session_state.admin_edit_cab = None
                    st.error(
                        admin_error_message(
                            response,
                            "Cab not found."
                        )
                    )

            cab_data = st.session_state.get("admin_edit_cab")

            if cab_data:
                st.info(
                    f"Editing Cab #{cab_data.get('id')} — "
                    f"{cab_data.get('vehicle_number', '')} / "
                    f"{cab_data.get('cab_type', '')}"
                )

                with st.form("admin_edit_cab_form"):
                    e1, e2 = st.columns(2)
                    with e1:
                        edit_driver_name = st.text_input(
                            "Driver Name",
                            value=str(cab_data.get("driver_name", "")),
                            key="edit_cab_driver_name"
                        )
                        edit_vehicle_number = st.text_input(
                            "Vehicle Number",
                            value=str(cab_data.get("vehicle_number", "")),
                            key="edit_cab_vehicle_number"
                        )
                        edit_cab_type = st.text_input(
                            "Cab Type",
                            value=str(cab_data.get("cab_type", "")),
                            key="edit_cab_type"
                        )
                        edit_source = st.text_input(
                            "Source",
                            value=str(cab_data.get("source", "")),
                            key="edit_cab_source"
                        )
                        edit_destination = st.text_input(
                            "Destination",
                            value=str(cab_data.get("destination", "")),
                            key="edit_cab_destination"
                        )
                    with e2:
                        edit_fare = st.number_input(
                            "Fare per KM (₹)",
                            min_value=1.0,
                            value=max(1.0, float(cab_data.get("fare_per_km", 1))),
                            step=1.0,
                            key="edit_cab_fare"
                        )
                        edit_seats = st.number_input(
                            "Available Seats",
                            min_value=1,
                            value=max(1, int(cab_data.get("available_seats", 1))),
                            step=1,
                            key="edit_cab_seats"
                        )
                        edit_rating = st.number_input(
                            "Rating",
                            min_value=0.0,
                            max_value=5.0,
                            value=min(5.0, max(0.0, float(cab_data.get("rating", 0)))),
                            step=0.1,
                            key="edit_cab_rating"
                        )

                    update_cab = st.form_submit_button(
                        "💾 Save Changes",
                        type="primary",
                        use_container_width=True
                    )

                if update_cab:
                    payload = {
                        "driver_name": edit_driver_name.strip(),
                        "vehicle_number": edit_vehicle_number.strip(),
                        "cab_type": edit_cab_type.strip(),
                        "source": edit_source.strip(),
                        "destination": edit_destination.strip(),
                        "fare_per_km": float(edit_fare),
                        "available_seats": int(edit_seats),
                        "rating": float(edit_rating)
                    }

                    if not all([
                        payload["driver_name"],
                        payload["vehicle_number"],
                        payload["cab_type"],
                        payload["source"],
                        payload["destination"]
                    ]):
                        st.warning("Please fill all cab fields.")
                    else:
                        response = admin_api_request(
                            "PUT",
                            f"/cabs/admin/{int(cab_id)}",
                            payload
                        )
                        if response is not None and response.status_code == 200:
                            st.success("Cab updated successfully! ✅")
                            st.session_state.admin_edit_cab = response.json()
                            st.rerun()
                        else:
                            st.error(
                                admin_error_message(
                                    response,
                                    "Unable to update cab."
                                )
                            )

            if delete_cab:
                response = admin_api_request(
                    "DELETE",
                    f"/cabs/admin/{int(cab_id)}"
                )
                if response is not None and response.status_code == 200:
                    st.success("Cab deleted successfully! 🗑️")
                    st.session_state.admin_edit_cab = None
                    st.rerun()
                else:
                    st.error(
                        admin_error_message(
                            response,
                            "Unable to delete cab."
                        )
                    )

    elif st.session_state.page == "Admin Food":

        st.title("🍔 Food Management")
        st.caption("Manage restaurants and menu items from the TRAVELX admin panel.")
        st.divider()

        food_tab1, food_tab2, food_tab3 = st.tabs([
            "🏪 Restaurants",
            "🍽️ Menu Management",
            "✏️ Edit / Delete"
        ])

        # ========================================================
        # RESTAURANTS
        # ========================================================
        with food_tab1:
            col1, col2 = st.columns([5, 1])
            with col1:
                restaurant_search = st.text_input(
                    "Search restaurants",
                    placeholder="Name, city, cuisine or address...",
                    key="admin_restaurant_search"
                )
            with col2:
                st.write("")
                if st.button(
                    "🔄 Refresh",
                    key="admin_refresh_restaurants",
                    use_container_width=True
                ):
                    st.rerun()

            response = admin_api_get("/food/admin/restaurants")
            if response is None:
                st.warning("Unable to load restaurants.")
            elif response.status_code == 200:
                restaurants = response.json()
                if restaurant_search.strip():
                    term = restaurant_search.strip().lower()
                    restaurants = [
                        r for r in restaurants
                        if term in str(r.get("name", "")).lower()
                        or term in str(r.get("city", "")).lower()
                        or term in str(r.get("cuisine", "")).lower()
                        or term in str(r.get("address", "")).lower()
                    ]
                if restaurants:
                    restaurant_df = pd.DataFrame(restaurants).rename(columns={
                        "id": "Restaurant ID",
                        "name": "Name",
                        "city": "City",
                        "address": "Address",
                        "cuisine": "Cuisine",
                        "description": "Description",
                        "rating": "Rating",
                        "delivery_time": "Delivery (min)",
                        "is_open": "Open"
                    })
                    if "Rating" in restaurant_df.columns:
                        restaurant_df["Rating"] = restaurant_df["Rating"].apply(
                            lambda x: f"{float(x):.1f}/5"
                        )
                    if "Open" in restaurant_df.columns:
                        restaurant_df["Open"] = restaurant_df["Open"].apply(
                            lambda x: "🟢 Open" if x else "🔴 Closed"
                        )
                    st.dataframe(
                        restaurant_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    st.success(f"Showing {len(restaurants)} restaurant(s).")
                else:
                    st.info("No restaurants found.")
            else:
                st.error(
                    f"Unable to load restaurants: "
                    f"{admin_error_message(response, 'Request failed.')}"
                )

        # ========================================================
        # MENU MANAGEMENT
        # ========================================================
        with food_tab2:
            st.subheader("🍽️ Restaurant Menu")

            restaurant_response = admin_api_get("/food/admin/restaurants")
            restaurants = (
                restaurant_response.json()
                if restaurant_response is not None
                and restaurant_response.status_code == 200
                else []
            )

            if not restaurants:
                st.info("No restaurants available. Create a restaurant first.")
            else:
                restaurant_options = {
                    f"#{r['id']} — {r['name']} ({r['city']})": r['id']
                    for r in restaurants
                }
                selected_restaurant_label = st.selectbox(
                    "Select Restaurant",
                    list(restaurant_options.keys()),
                    key="admin_food_restaurant_select"
                )
                selected_restaurant_id = restaurant_options[selected_restaurant_label]

                menu_response = admin_api_get(
                    f"/food/admin/menu/{selected_restaurant_id}"
                )

                if menu_response is not None and menu_response.status_code == 200:
                    menu_items = menu_response.json()
                    if menu_items:
                        menu_df = pd.DataFrame(menu_items).rename(columns={
                            "id": "Item ID",
                            "restaurant_id": "Restaurant ID",
                            "name": "Item Name",
                            "category": "Category",
                            "description": "Description",
                            "price": "Price",
                            "is_available": "Available"
                        })
                        if "Price" in menu_df.columns:
                            menu_df["Price"] = menu_df["Price"].apply(
                                lambda x: f"₹{float(x):,.0f}"
                            )
                        if "Available" in menu_df.columns:
                            menu_df["Available"] = menu_df["Available"].apply(
                                lambda x: "🟢 Yes" if x else "🔴 No"
                            )
                        st.dataframe(
                            menu_df,
                            use_container_width=True,
                            hide_index=True
                        )
                        st.success(f"Showing {len(menu_items)} menu item(s).")
                    else:
                        st.info("No menu items for this restaurant yet.")
                elif menu_response is not None:
                    st.error(
                        admin_error_message(
                            menu_response,
                            "Unable to load restaurant menu."
                        )
                    )

                st.divider()
                st.subheader("➕ Add Menu Item")
                with st.form("admin_add_food_item_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        food_name = st.text_input(
                            "Food Item Name",
                            placeholder="Butter Chicken"
                        )
                        food_category = st.text_input(
                            "Category",
                            placeholder="Main Course"
                        )
                        food_description = st.text_area(
                            "Description",
                            placeholder="Creamy tomato-based chicken curry..."
                        )
                    with c2:
                        food_price = st.number_input(
                            "Price (₹)",
                            min_value=1,
                            value=250,
                            step=10
                        )
                        food_available = st.checkbox(
                            "Available for ordering",
                            value=True
                        )
                    add_food_item = st.form_submit_button(
                        "🚀 Create Menu Item",
                        type="primary",
                        use_container_width=True
                    )

                if add_food_item:
                    if not food_name.strip() or not food_category.strip():
                        st.warning("Please enter food item name and category.")
                    else:
                        payload = {
                            "restaurant_id": int(selected_restaurant_id),
                            "name": food_name.strip(),
                            "category": food_category.strip(),
                            "description": food_description.strip(),
                            "price": float(food_price),
                            "is_available": bool(food_available)
                        }
                        response = admin_api_request(
                            "POST",
                            "/food/admin/menu",
                            payload
                        )
                        if response is not None and response.status_code in [200, 201]:
                            st.success("Menu item created successfully! 🍽️")
                            st.rerun()
                        else:
                            st.error(
                                admin_error_message(
                                    response,
                                    "Unable to create menu item."
                                )
                            )

        # ========================================================
        # EDIT / DELETE RESTAURANTS + FOOD ITEMS
        # ========================================================
        with food_tab3:
            st.subheader("✏️ Edit or Delete Restaurant")
            restaurant_id = st.number_input(
                "Restaurant ID",
                min_value=1,
                value=1,
                step=1,
                key="admin_edit_restaurant_id"
            )
            load_col, delete_col = st.columns(2)
            with load_col:
                load_restaurant = st.button(
                    "🔎 Load Restaurant",
                    use_container_width=True,
                    key="admin_load_restaurant"
                )
            with delete_col:
                delete_restaurant = st.button(
                    "🗑️ Delete Restaurant",
                    use_container_width=True,
                    key="admin_delete_restaurant"
                )

            if load_restaurant:
                response = admin_api_get(
                    f"/food/admin/restaurants/{int(restaurant_id)}"
                )
                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_restaurant = response.json()
                else:
                    st.session_state.admin_edit_restaurant = None
                    st.error(
                        admin_error_message(
                            response,
                            "Restaurant not found."
                        )
                    )

            restaurant_data = st.session_state.get("admin_edit_restaurant")
            if restaurant_data:
                with st.form("admin_edit_restaurant_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        edit_restaurant_name = st.text_input(
                            "Restaurant Name",
                            value=str(restaurant_data.get("name", "")),
                            key="edit_restaurant_name"
                        )
                        edit_restaurant_city = st.text_input(
                            "City",
                            value=str(restaurant_data.get("city", "")),
                            key="edit_restaurant_city"
                        )
                        edit_restaurant_address = st.text_input(
                            "Address",
                            value=str(restaurant_data.get("address", "")),
                            key="edit_restaurant_address"
                        )
                        edit_restaurant_cuisine = st.text_input(
                            "Cuisine",
                            value=str(restaurant_data.get("cuisine", "")),
                            key="edit_restaurant_cuisine"
                        )
                        edit_restaurant_description = st.text_area(
                            "Description",
                            value=str(restaurant_data.get("description", "") or ""),
                            key="edit_restaurant_description"
                        )
                    with c2:
                        edit_restaurant_rating = st.number_input(
                            "Rating",
                            min_value=0.0,
                            max_value=5.0,
                            value=float(restaurant_data.get("rating", 0) or 0),
                            step=0.1,
                            key="edit_restaurant_rating"
                        )
                        edit_delivery_time = st.number_input(
                            "Delivery Time (minutes)",
                            min_value=1,
                            value=max(1, int(restaurant_data.get("delivery_time", 30) or 30)),
                            step=1,
                            key="edit_restaurant_delivery"
                        )
                        edit_is_open = st.checkbox(
                            "Restaurant is open",
                            value=bool(restaurant_data.get("is_open", True)),
                            key="edit_restaurant_open"
                        )

                    update_restaurant = st.form_submit_button(
                        "💾 Save Restaurant Changes",
                        type="primary",
                        use_container_width=True
                    )

                if update_restaurant:
                    payload = {
                        "name": edit_restaurant_name.strip(),
                        "city": edit_restaurant_city.strip(),
                        "address": edit_restaurant_address.strip(),
                        "cuisine": edit_restaurant_cuisine.strip(),
                        "description": edit_restaurant_description.strip(),
                        "rating": float(edit_restaurant_rating),
                        "delivery_time": int(edit_delivery_time),
                        "is_open": bool(edit_is_open)
                    }
                    if not all([
                        payload["name"],
                        payload["city"],
                        payload["address"],
                        payload["cuisine"]
                    ]):
                        st.warning("Please fill all required restaurant fields.")
                    else:
                        response = admin_api_request(
                            "PUT",
                            f"/food/admin/restaurants/{int(restaurant_id)}",
                            payload
                        )
                        if response is not None and response.status_code == 200:
                            st.success("Restaurant updated successfully! ✅")
                            st.session_state.admin_edit_restaurant = response.json()
                            st.rerun()
                        else:
                            st.error(
                                admin_error_message(
                                    response,
                                    "Unable to update restaurant."
                                )
                            )

            if delete_restaurant:
                response = admin_api_request(
                    "DELETE",
                    f"/food/admin/restaurants/{int(restaurant_id)}"
                )
                if response is not None and response.status_code == 200:
                    st.success("Restaurant deleted successfully! 🗑️")
                    st.session_state.admin_edit_restaurant = None
                    st.rerun()
                else:
                    st.error(
                        admin_error_message(
                            response,
                            "Unable to delete restaurant."
                        )
                    )

            st.divider()
            st.subheader("🍽️ Edit or Delete Menu Item")

            item_restaurant_response = admin_api_get("/food/admin/restaurants")
            item_restaurants = (
                item_restaurant_response.json()
                if item_restaurant_response is not None
                and item_restaurant_response.status_code == 200
                else []
            )

            if not item_restaurants:
                st.info("No restaurants available for menu item management.")
            else:
                item_restaurant_options = {
                    f"#{r['id']} — {r['name']} ({r['city']})": r['id']
                    for r in item_restaurants
                }
                edit_menu_restaurant_label = st.selectbox(
                    "Select Restaurant",
                    list(item_restaurant_options.keys()),
                    key="admin_edit_menu_restaurant_select"
                )
                edit_menu_restaurant_id = item_restaurant_options[edit_menu_restaurant_label]

                edit_menu_response = admin_api_get(
                    f"/food/admin/menu/{edit_menu_restaurant_id}"
                )

                if edit_menu_response is not None and edit_menu_response.status_code == 200:
                    edit_menu_items = edit_menu_response.json()

                    if not edit_menu_items:
                        st.info("This restaurant has no menu items yet.")
                    else:
                        item_options = {
                            f"#{item['id']} — {item['name']} (₹{float(item.get('price', 0)):,.0f})": item
                            for item in edit_menu_items
                        }
                        selected_item_label = st.selectbox(
                            "Select Menu Item",
                            list(item_options.keys()),
                            key="admin_food_item_select"
                        )
                        food_item_data = item_options[selected_item_label]
                        selected_item_id = int(food_item_data["id"])

                        with st.form("admin_edit_food_item_form"):
                            e1, e2 = st.columns(2)
                            with e1:
                                edit_item_name = st.text_input(
                                    "Food Item Name",
                                    value=str(food_item_data.get("name", "")),
                                    key="edit_food_item_name"
                                )
                                edit_item_category = st.text_input(
                                    "Category",
                                    value=str(food_item_data.get("category", "")),
                                    key="edit_food_item_category"
                                )
                                edit_item_description = st.text_area(
                                    "Description",
                                    value=str(food_item_data.get("description", "") or ""),
                                    key="edit_food_item_description"
                                )
                            with e2:
                                edit_item_price = st.number_input(
                                    "Price (₹)",
                                    min_value=1,
                                    value=max(1, int(float(food_item_data.get("price", 1) or 1))),
                                    step=10,
                                    key="edit_food_item_price"
                                )
                                edit_item_available = st.checkbox(
                                    "Available for ordering",
                                    value=bool(food_item_data.get("is_available", True)),
                                    key="edit_food_item_available"
                                )

                            update_item = st.form_submit_button(
                                "💾 Save Menu Item Changes",
                                type="primary",
                                use_container_width=True
                            )

                        if update_item:
                            payload = {
                                "restaurant_id": int(edit_menu_restaurant_id),
                                "name": edit_item_name.strip(),
                                "category": edit_item_category.strip(),
                                "description": edit_item_description.strip(),
                                "price": float(edit_item_price),
                                "is_available": bool(edit_item_available)
                            }
                            if not payload["name"] or not payload["category"]:
                                st.warning("Please fill all required menu item fields.")
                            else:
                                response = admin_api_request(
                                    "PUT",
                                    f"/food/admin/menu/{selected_item_id}",
                                    payload
                                )
                                if response is not None and response.status_code == 200:
                                    st.success("Menu item updated successfully! ✅")
                                    st.rerun()
                                else:
                                    st.error(
                                        admin_error_message(
                                            response,
                                            "Unable to update menu item."
                                        )
                                    )

                        if st.button(
                            "🗑️ Delete Selected Menu Item",
                            use_container_width=True,
                            key="admin_delete_selected_food_item"
                        ):
                            response = admin_api_request(
                                "DELETE",
                                f"/food/admin/menu/{selected_item_id}"
                            )
                            if response is not None and response.status_code == 200:
                                st.success("Menu item deleted successfully! 🗑️")
                                st.rerun()
                            else:
                                st.error(
                                    admin_error_message(
                                        response,
                                        "Unable to delete menu item."
                                    )
                                )
                elif edit_menu_response is not None:
                    st.error(
                        admin_error_message(
                            edit_menu_response,
                            "Unable to load menu items."
                        )
                    )


    elif st.session_state.page == "Admin Movies":

        st.title("🎬 Movie Management")
        st.caption("Manage movies, cinemas and movie shows from the TRAVELX admin panel.")
        st.divider()

        movie_tab1, movie_tab2, movie_tab3 = st.tabs([
            "🎬 Movies",
            "🏢 Cinemas",
            "🕒 Shows"
        ])

        # ========================================================
        # MOVIES
        # ========================================================
        with movie_tab1:
            st.subheader("🎬 Movie Catalog")

            movie_search = st.text_input(
                "Search movies",
                placeholder="Title, language, genre...",
                key="admin_movie_search"
            )

            response = admin_api_get("/movies/admin/all")
            if response is None:
                st.warning("Unable to load movies.")
            elif response.status_code == 200:
                movies = response.json()
                if movie_search.strip():
                    term = movie_search.strip().lower()
                    movies = [
                        m for m in movies
                        if term in str(m.get("title", "")).lower()
                        or term in str(m.get("language", "")).lower()
                        or term in str(m.get("genre", "")).lower()
                    ]

                if movies:
                    movie_df = pd.DataFrame(movies).rename(columns={
                        "id": "Movie ID",
                        "title": "Title",
                        "language": "Language",
                        "genre": "Genre",
                        "duration_minutes": "Duration (min)",
                        "rating": "Rating",
                        "description": "Description",
                        "release_date": "Release Date",
                        "is_active": "Active"
                    })
                    if "Rating" in movie_df.columns:
                        movie_df["Rating"] = movie_df["Rating"].apply(
                            lambda x: f"{float(x):.1f}/5"
                        )
                    if "Active" in movie_df.columns:
                        movie_df["Active"] = movie_df["Active"].apply(
                            lambda x: "🟢 Active" if x else "🔴 Inactive"
                        )
                    st.dataframe(movie_df, use_container_width=True, hide_index=True)
                    st.success(f"Showing {len(movies)} movie(s).")
                else:
                    st.info("No movies found.")
            else:
                st.error(admin_error_message(response, "Unable to load movies."))

            st.divider()
            st.subheader("➕ Add Movie")

            with st.form("admin_add_movie_form"):
                c1, c2 = st.columns(2)
                with c1:
                    movie_title = st.text_input("Movie Title", placeholder="Kalki 2898 AD")
                    movie_language = st.text_input("Language", placeholder="Hindi")
                    movie_genre = st.text_input("Genre", placeholder="Sci-Fi")
                    movie_duration = st.number_input(
                        "Duration (minutes)", min_value=1, value=150, step=1
                    )
                with c2:
                    movie_rating = st.number_input(
                        "Rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1
                    )
                    movie_release_date = st.text_input(
                        "Release Date", placeholder="2026-09-13"
                    )
                    movie_description = st.text_area(
                        "Description", placeholder="Movie description..."
                    )
                    movie_active = st.checkbox("Movie is active", value=True)

                create_movie = st.form_submit_button(
                    "🚀 Create Movie", type="primary", use_container_width=True
                )

            if create_movie:
                if not movie_title.strip() or not movie_language.strip() or not movie_genre.strip():
                    st.warning("Please fill title, language and genre.")
                else:
                    payload = {
                        "title": movie_title.strip(),
                        "language": movie_language.strip(),
                        "genre": movie_genre.strip(),
                        "duration_minutes": int(movie_duration),
                        "rating": float(movie_rating),
                        "description": movie_description.strip(),
                        "release_date": movie_release_date.strip() or None,
                        "is_active": bool(movie_active)
                    }
                    response = admin_api_request("POST", "/movies/admin/create", payload)
                    if response is not None and response.status_code in [200, 201]:
                        st.success("Movie created successfully! 🎬")
                        st.rerun()
                    else:
                        st.error(admin_error_message(response, "Unable to create movie."))

            st.divider()
            st.subheader("✏️ Edit / Delete Movie")

            movie_id = st.number_input(
                "Movie ID", min_value=1, value=1, step=1, key="admin_edit_movie_id"
            )
            lc1, lc2 = st.columns(2)
            with lc1:
                load_movie = st.button(
                    "🔎 Load Movie", use_container_width=True, key="admin_load_movie"
                )
            with lc2:
                delete_movie = st.button(
                    "🗑️ Delete Movie", use_container_width=True, key="admin_delete_movie"
                )

            if load_movie:
                response = admin_api_get(f"/movies/admin/{int(movie_id)}")
                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_movie = response.json()
                else:
                    st.session_state.admin_edit_movie = None
                    st.error(admin_error_message(response, "Movie not found."))

            movie_data = st.session_state.get("admin_edit_movie")
            if movie_data:
                with st.form("admin_edit_movie_form"):
                    e1, e2 = st.columns(2)
                    with e1:
                        edit_movie_title = st.text_input(
                            "Movie Title", value=str(movie_data.get("title", "")), key="edit_movie_title"
                        )
                        edit_movie_language = st.text_input(
                            "Language", value=str(movie_data.get("language", "")), key="edit_movie_language"
                        )
                        edit_movie_genre = st.text_input(
                            "Genre", value=str(movie_data.get("genre", "")), key="edit_movie_genre"
                        )
                        edit_movie_duration = st.number_input(
                            "Duration (minutes)", min_value=1,
                            value=max(1, int(movie_data.get("duration_minutes", 1) or 1)),
                            step=1, key="edit_movie_duration"
                        )
                    with e2:
                        edit_movie_rating = st.number_input(
                            "Rating", min_value=0.0, max_value=5.0,
                            value=float(movie_data.get("rating", 0) or 0),
                            step=0.1, key="edit_movie_rating"
                        )
                        edit_movie_release = st.text_input(
                            "Release Date",
                            value=str(movie_data.get("release_date", "") or ""),
                            key="edit_movie_release"
                        )
                        edit_movie_description = st.text_area(
                            "Description",
                            value=str(movie_data.get("description", "") or ""),
                            key="edit_movie_description"
                        )
                        edit_movie_active = st.checkbox(
                            "Movie is active",
                            value=bool(movie_data.get("is_active", True)),
                            key="edit_movie_active"
                        )

                    update_movie = st.form_submit_button(
                        "💾 Save Movie Changes", type="primary", use_container_width=True
                    )

                if update_movie:
                    payload = {
                        "title": edit_movie_title.strip(),
                        "language": edit_movie_language.strip(),
                        "genre": edit_movie_genre.strip(),
                        "duration_minutes": int(edit_movie_duration),
                        "rating": float(edit_movie_rating),
                        "description": edit_movie_description.strip(),
                        "release_date": edit_movie_release.strip() or None,
                        "is_active": bool(edit_movie_active)
                    }
                    if not payload["title"] or not payload["language"] or not payload["genre"]:
                        st.warning("Please fill all required movie fields.")
                    else:
                        response = admin_api_request(
                            "PUT", f"/movies/admin/{int(movie_id)}", payload
                        )
                        if response is not None and response.status_code == 200:
                            st.success("Movie updated successfully! ✅")
                            st.session_state.admin_edit_movie = response.json()
                            st.rerun()
                        else:
                            st.error(admin_error_message(response, "Unable to update movie."))

            if delete_movie:
                response = admin_api_request("DELETE", f"/movies/admin/{int(movie_id)}")
                if response is not None and response.status_code == 200:
                    st.success("Movie deleted successfully! 🗑️")
                    st.session_state.admin_edit_movie = None
                    st.rerun()
                else:
                    st.error(admin_error_message(response, "Unable to delete movie."))

        # ========================================================
        # CINEMAS
        # ========================================================
        with movie_tab2:
            st.subheader("🏢 Cinema Management")

            cinema_response = admin_api_get("/movies/admin/cinemas/all")
            cinemas = (
                cinema_response.json()
                if cinema_response is not None and cinema_response.status_code == 200
                else []
            )

            if cinema_response is not None and cinema_response.status_code != 200:
                st.error(admin_error_message(cinema_response, "Unable to load cinemas."))

            cinema_search = st.text_input(
                "Search cinemas", placeholder="Name, city or address...", key="admin_cinema_search"
            )
            filtered_cinemas = cinemas
            if cinema_search.strip():
                term = cinema_search.strip().lower()
                filtered_cinemas = [
                    c for c in cinemas
                    if term in str(c.get("name", "")).lower()
                    or term in str(c.get("city", "")).lower()
                    or term in str(c.get("address", "")).lower()
                ]

            if filtered_cinemas:
                cinema_df = pd.DataFrame(filtered_cinemas).rename(columns={
                    "id": "Cinema ID",
                    "name": "Name",
                    "city": "City",
                    "address": "Address",
                    "total_seats": "Total Seats"
                })
                st.dataframe(cinema_df, use_container_width=True, hide_index=True)
                st.success(f"Showing {len(filtered_cinemas)} cinema(s).")
            else:
                st.info("No cinemas found.")

            st.divider()
            st.subheader("➕ Add Cinema")
            with st.form("admin_add_cinema_form"):
                c1, c2 = st.columns(2)
                with c1:
                    cinema_name = st.text_input("Cinema Name", placeholder="PVR Cinemas")
                    cinema_city = st.text_input("City", placeholder="Hyderabad")
                with c2:
                    cinema_address = st.text_input("Address", placeholder="Banjara Hills")
                    cinema_total_seats = st.number_input(
                        "Total Seats", min_value=1, value=200, step=10
                    )
                create_cinema = st.form_submit_button(
                    "🚀 Create Cinema", type="primary", use_container_width=True
                )

            if create_cinema:
                if not cinema_name.strip() or not cinema_city.strip() or not cinema_address.strip():
                    st.warning("Please fill all cinema fields.")
                else:
                    payload = {
                        "name": cinema_name.strip(),
                        "city": cinema_city.strip(),
                        "address": cinema_address.strip(),
                        "total_seats": int(cinema_total_seats)
                    }
                    response = admin_api_request(
                        "POST", "/movies/admin/cinemas/create", payload
                    )
                    if response is not None and response.status_code in [200, 201]:
                        st.success("Cinema created successfully! 🏢")
                        st.rerun()
                    else:
                        st.error(admin_error_message(response, "Unable to create cinema."))

            st.divider()
            st.subheader("✏️ Edit / Delete Cinema")
            cinema_id = st.number_input(
                "Cinema ID", min_value=1, value=1, step=1, key="admin_edit_cinema_id"
            )
            cc1, cc2 = st.columns(2)
            with cc1:
                load_cinema = st.button(
                    "🔎 Load Cinema", use_container_width=True, key="admin_load_cinema"
                )
            with cc2:
                delete_cinema = st.button(
                    "🗑️ Delete Cinema", use_container_width=True, key="admin_delete_cinema"
                )

            if load_cinema:
                response = admin_api_get(f"/movies/admin/cinemas/{int(cinema_id)}")
                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_cinema = response.json()
                else:
                    st.session_state.admin_edit_cinema = None
                    st.error(admin_error_message(response, "Cinema not found."))

            cinema_data = st.session_state.get("admin_edit_cinema")
            if cinema_data:
                with st.form("admin_edit_cinema_form"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        edit_cinema_name = st.text_input(
                            "Cinema Name", value=str(cinema_data.get("name", "")), key="edit_cinema_name"
                        )
                        edit_cinema_city = st.text_input(
                            "City", value=str(cinema_data.get("city", "")), key="edit_cinema_city"
                        )
                    with ec2:
                        edit_cinema_address = st.text_input(
                            "Address", value=str(cinema_data.get("address", "")), key="edit_cinema_address"
                        )
                        edit_cinema_seats = st.number_input(
                            "Total Seats", min_value=1,
                            value=max(1, int(cinema_data.get("total_seats", 1) or 1)),
                            step=10, key="edit_cinema_seats"
                        )
                    update_cinema = st.form_submit_button(
                        "💾 Save Cinema Changes", type="primary", use_container_width=True
                    )

                if update_cinema:
                    payload = {
                        "name": edit_cinema_name.strip(),
                        "city": edit_cinema_city.strip(),
                        "address": edit_cinema_address.strip(),
                        "total_seats": int(edit_cinema_seats)
                    }
                    if not all([payload["name"], payload["city"], payload["address"]]):
                        st.warning("Please fill all required cinema fields.")
                    else:
                        response = admin_api_request(
                            "PUT", f"/movies/admin/cinemas/{int(cinema_id)}", payload
                        )
                        if response is not None and response.status_code == 200:
                            st.success("Cinema updated successfully! ✅")
                            st.session_state.admin_edit_cinema = response.json()
                            st.rerun()
                        else:
                            st.error(admin_error_message(response, "Unable to update cinema."))

            if delete_cinema:
                response = admin_api_request(
                    "DELETE", f"/movies/admin/cinemas/{int(cinema_id)}"
                )
                if response is not None and response.status_code == 200:
                    st.success("Cinema deleted successfully! 🗑️")
                    st.session_state.admin_edit_cinema = None
                    st.rerun()
                else:
                    st.error(admin_error_message(response, "Unable to delete cinema."))

        # ========================================================
        # SHOWS
        # ========================================================
        with movie_tab3:
            st.subheader("🕒 Movie Show Management")

            shows_response = admin_api_get("/movies/admin/shows/all")
            shows = (
                shows_response.json()
                if shows_response is not None and shows_response.status_code == 200
                else []
            )

            if shows_response is not None and shows_response.status_code != 200:
                st.error(admin_error_message(shows_response, "Unable to load shows."))

            movies_response = admin_api_get("/movies/admin/all")
            movies = (
                movies_response.json()
                if movies_response is not None and movies_response.status_code == 200
                else []
            )
            cinemas_response = admin_api_get("/movies/admin/cinemas/all")
            cinemas = (
                cinemas_response.json()
                if cinemas_response is not None and cinemas_response.status_code == 200
                else []
            )

            if shows:
                movie_lookup = {m["id"]: m.get("title", "") for m in movies}
                cinema_lookup = {c["id"]: c.get("name", "") for c in cinemas}
                display_shows = []
                for show in shows:
                    row = dict(show)
                    row["movie"] = movie_lookup.get(show.get("movie_id"), f"Movie #{show.get('movie_id')}")
                    row["cinema"] = cinema_lookup.get(show.get("cinema_id"), f"Cinema #{show.get('cinema_id')}")
                    display_shows.append(row)

                show_df = pd.DataFrame(display_shows).rename(columns={
                    "id": "Show ID",
                    "movie": "Movie",
                    "cinema": "Cinema",
                    "movie_id": "Movie ID",
                    "cinema_id": "Cinema ID",
                    "show_date": "Date",
                    "show_time": "Time",
                    "screen_name": "Screen",
                    "ticket_price": "Ticket Price",
                    "total_seats": "Total Seats",
                    "available_seats": "Available Seats"
                })
                if "Ticket Price" in show_df.columns:
                    show_df["Ticket Price"] = show_df["Ticket Price"].apply(
                        lambda x: f"₹{float(x):,.0f}"
                    )
                st.dataframe(show_df, use_container_width=True, hide_index=True)
                st.success(f"Showing {len(shows)} show(s).")
            else:
                st.info("No movie shows found.")

            if not movies or not cinemas:
                st.warning("Create at least one movie and one cinema before adding a show.")
            else:
                st.divider()
                st.subheader("➕ Add Movie Show")

                movie_options = {
                    f"#{m['id']} — {m['title']}": m['id'] for m in movies
                }
                cinema_options = {
                    f"#{c['id']} — {c['name']} ({c['city']})": c['id'] for c in cinemas
                }

                with st.form("admin_add_movie_show_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        add_show_movie_label = st.selectbox(
                            "Movie", list(movie_options.keys()), key="admin_add_show_movie"
                        )
                        add_show_cinema_label = st.selectbox(
                            "Cinema", list(cinema_options.keys()), key="admin_add_show_cinema"
                        )
                        add_show_date = st.text_input(
                            "Show Date", placeholder="2026-09-20"
                        )
                        add_show_time = st.text_input(
                            "Show Time", placeholder="19:30"
                        )
                    with c2:
                        add_show_screen = st.text_input(
                            "Screen Name", placeholder="Screen 1"
                        )
                        add_show_price = st.number_input(
                            "Ticket Price (₹)", min_value=1, value=250, step=10
                        )
                        add_show_total = st.number_input(
                            "Total Seats", min_value=1, value=200, step=10
                        )
                        add_show_available = st.number_input(
                            "Available Seats", min_value=0, value=200, step=10
                        )

                    create_show = st.form_submit_button(
                        "🚀 Create Show", type="primary", use_container_width=True
                    )

                if create_show:
                    if not add_show_date.strip() or not add_show_time.strip() or not add_show_screen.strip():
                        st.warning("Please enter date, time and screen name.")
                    elif int(add_show_available) > int(add_show_total):
                        st.warning("Available seats cannot exceed total seats.")
                    else:
                        payload = {
                            "movie_id": int(movie_options[add_show_movie_label]),
                            "cinema_id": int(cinema_options[add_show_cinema_label]),
                            "show_date": add_show_date.strip(),
                            "show_time": add_show_time.strip(),
                            "screen_name": add_show_screen.strip(),
                            "ticket_price": float(add_show_price),
                            "total_seats": int(add_show_total),
                            "available_seats": int(add_show_available)
                        }
                        response = admin_api_request(
                            "POST", "/movies/admin/shows/create", payload
                        )
                        if response is not None and response.status_code in [200, 201]:
                            st.success("Movie show created successfully! 🕒")
                            st.rerun()
                        else:
                            st.error(admin_error_message(response, "Unable to create movie show."))

            st.divider()
            st.subheader("✏️ Edit / Delete Show")
            show_id = st.number_input(
                "Show ID", min_value=1, value=1, step=1, key="admin_edit_show_id"
            )
            sc1, sc2 = st.columns(2)
            with sc1:
                load_show = st.button(
                    "🔎 Load Show", use_container_width=True, key="admin_load_show"
                )
            with sc2:
                delete_show = st.button(
                    "🗑️ Delete Show", use_container_width=True, key="admin_delete_show"
                )

            if load_show:
                response = admin_api_get(f"/movies/admin/shows/{int(show_id)}")
                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_movie_show = response.json()
                else:
                    st.session_state.admin_edit_movie_show = None
                    st.error(admin_error_message(response, "Movie show not found."))

            show_data = st.session_state.get("admin_edit_movie_show")
            if show_data:
                movie_options_edit = {f"#{m['id']} — {m['title']}": m['id'] for m in movies}
                cinema_options_edit = {f"#{c['id']} — {c['name']} ({c['city']})": c['id'] for c in cinemas}
                movie_label_by_id = {v: k for k, v in movie_options_edit.items()}
                cinema_label_by_id = {v: k for k, v in cinema_options_edit.items()}

                with st.form("admin_edit_movie_show_form"):
                    e1, e2 = st.columns(2)
                    with e1:
                        current_movie_id = int(show_data.get("movie_id", 0))
                        current_cinema_id = int(show_data.get("cinema_id", 0))
                        edit_show_movie = st.selectbox(
                            "Movie",
                            list(movie_options_edit.keys()),
                            index=list(movie_options_edit.keys()).index(movie_label_by_id[current_movie_id])
                            if current_movie_id in movie_label_by_id else 0,
                            key="edit_show_movie"
                        )
                        edit_show_cinema = st.selectbox(
                            "Cinema",
                            list(cinema_options_edit.keys()),
                            index=list(cinema_options_edit.keys()).index(cinema_label_by_id[current_cinema_id])
                            if current_cinema_id in cinema_label_by_id else 0,
                            key="edit_show_cinema"
                        )
                        edit_show_date = st.text_input(
                            "Show Date", value=str(show_data.get("show_date", "")), key="edit_show_date"
                        )
                        edit_show_time = st.text_input(
                            "Show Time", value=str(show_data.get("show_time", "")), key="edit_show_time"
                        )
                    with e2:
                        edit_show_screen = st.text_input(
                            "Screen Name", value=str(show_data.get("screen_name", "")), key="edit_show_screen"
                        )
                        edit_show_price = st.number_input(
                            "Ticket Price (₹)", min_value=1,
                            value=max(1, int(float(show_data.get("ticket_price", 1) or 1))),
                            step=10, key="edit_show_price"
                        )
                        edit_show_total = st.number_input(
                            "Total Seats", min_value=1,
                            value=max(1, int(show_data.get("total_seats", 1) or 1)),
                            step=10, key="edit_show_total"
                        )
                        edit_show_available = st.number_input(
                            "Available Seats", min_value=0,
                            value=max(0, int(show_data.get("available_seats", 0) or 0)),
                            step=10, key="edit_show_available"
                        )

                    update_show = st.form_submit_button(
                        "💾 Save Show Changes", type="primary", use_container_width=True
                    )

                if update_show:
                    if not edit_show_date.strip() or not edit_show_time.strip() or not edit_show_screen.strip():
                        st.warning("Please fill date, time and screen name.")
                    elif int(edit_show_available) > int(edit_show_total):
                        st.warning("Available seats cannot exceed total seats.")
                    else:
                        payload = {
                            "movie_id": int(movie_options_edit[edit_show_movie]),
                            "cinema_id": int(cinema_options_edit[edit_show_cinema]),
                            "show_date": edit_show_date.strip(),
                            "show_time": edit_show_time.strip(),
                            "screen_name": edit_show_screen.strip(),
                            "ticket_price": float(edit_show_price),
                            "total_seats": int(edit_show_total),
                            "available_seats": int(edit_show_available)
                        }
                        response = admin_api_request(
                            "PUT", f"/movies/admin/shows/{int(show_id)}", payload
                        )
                        if response is not None and response.status_code == 200:
                            st.success("Movie show updated successfully! ✅")
                            st.session_state.admin_edit_movie_show = response.json()
                            st.rerun()
                        else:
                            st.error(admin_error_message(response, "Unable to update movie show."))

            if delete_show:
                response = admin_api_request(
                    "DELETE", f"/movies/admin/shows/{int(show_id)}"
                )
                if response is not None and response.status_code == 200:
                    st.success("Movie show deleted successfully! 🗑️")
                    st.session_state.admin_edit_movie_show = None
                    st.rerun()
                else:
                    st.error(admin_error_message(response, "Unable to delete movie show."))


    elif st.session_state.page == "Admin Events":

        st.title("🎟️ Event Management")
        st.caption("Manage events, venues and event shows from the TRAVELX admin panel.")
        st.divider()

        event_tab1, event_tab2, event_tab3 = st.tabs([
            "🎟️ Events",
            "🏟️ Venues",
            "🕒 Shows"
        ])

        # ========================================================
        # EVENTS
        # ========================================================
        with event_tab1:
            st.subheader("🎟️ Event Management")

            events_response = admin_api_get("/events/admin/all")
            events = (
                events_response.json()
                if events_response is not None and events_response.status_code == 200
                else []
            )

            if events_response is not None and events_response.status_code != 200:
                st.error(admin_error_message(events_response, "Unable to load events."))

            col1, col2 = st.columns([5, 1])
            with col1:
                event_search = st.text_input(
                    "Search events",
                    placeholder="Name, category or language...",
                    key="admin_event_search"
                )
            with col2:
                st.write("")
                if st.button("🔄 Refresh", key="admin_refresh_events", use_container_width=True):
                    st.rerun()

            filtered_events = events
            if event_search.strip():
                term = event_search.strip().lower()
                filtered_events = [
                    e for e in events
                    if term in str(e.get("name", "")).lower()
                    or term in str(e.get("category", "")).lower()
                    or term in str(e.get("language", "")).lower()
                    or term in str(e.get("description", "")).lower()
                ]

            if filtered_events:
                event_df = pd.DataFrame(filtered_events).rename(columns={
                    "id": "Event ID",
                    "name": "Name",
                    "category": "Category",
                    "description": "Description",
                    "language": "Language",
                    "duration_minutes": "Duration (min)",
                    "rating": "Rating",
                    "image_url": "Image URL",
                    "created_at": "Created At"
                })
                st.dataframe(event_df, use_container_width=True, hide_index=True)
                st.success(f"Showing {len(filtered_events)} event(s).")
            else:
                st.info("No events found.")

            st.divider()
            st.subheader("➕ Add New Event")

            with st.form("admin_add_event_form"):
                c1, c2 = st.columns(2)
                with c1:
                    event_name = st.text_input("Event Name", placeholder="Sunburn Festival")
                    event_category = st.text_input("Category", placeholder="Music")
                    event_language = st.text_input("Language", placeholder="English")
                    event_duration = st.number_input(
                        "Duration (minutes)", min_value=1, value=120, step=10
                    )
                with c2:
                    event_rating = st.number_input(
                        "Rating", min_value=0.0, max_value=5.0, value=4.5, step=0.1
                    )
                    event_image = st.text_input("Image URL", placeholder="https://...")
                    event_description = st.text_area(
                        "Description", placeholder="Event description..."
                    )

                create_event = st.form_submit_button(
                    "🚀 Create Event", type="primary", use_container_width=True
                )

            if create_event:
                payload = {
                    "name": event_name.strip(),
                    "category": event_category.strip(),
                    "description": event_description.strip() or None,
                    "language": event_language.strip() or None,
                    "duration_minutes": int(event_duration),
                    "rating": float(event_rating),
                    "image_url": event_image.strip() or None
                }
                if not payload["name"] or not payload["category"]:
                    st.warning("Please fill Event Name and Category.")
                else:
                    response = admin_api_request("POST", "/events/admin/create", payload)
                    if response is not None and response.status_code in [200, 201]:
                        st.success("Event created successfully! 🎟️")
                        st.rerun()
                    else:
                        st.error(admin_error_message(response, "Unable to create event."))

            st.divider()
            st.subheader("✏️ Edit / Delete Event")
            event_id = st.number_input(
                "Event ID", min_value=1, value=1, step=1, key="admin_edit_event_id"
            )
            load_col, delete_col = st.columns(2)
            with load_col:
                load_event = st.button("🔎 Load Event", use_container_width=True, key="admin_load_event")
            with delete_col:
                delete_event = st.button("🗑️ Delete Event", use_container_width=True, key="admin_delete_event")

            if load_event:
                response = admin_api_get(f"/events/admin/{int(event_id)}")
                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_event = response.json()
                else:
                    st.session_state.admin_edit_event = None
                    st.error(admin_error_message(response, "Event not found."))

            event_data = st.session_state.get("admin_edit_event")
            if event_data:
                st.info(f"Editing Event #{event_data.get('id')} — {event_data.get('name', '')}")
                with st.form("admin_edit_event_form"):
                    e1, e2 = st.columns(2)
                    with e1:
                        edit_event_name = st.text_input(
                            "Event Name", value=str(event_data.get("name", "")), key="edit_event_name"
                        )
                        edit_event_category = st.text_input(
                            "Category", value=str(event_data.get("category", "")), key="edit_event_category"
                        )
                        edit_event_language = st.text_input(
                            "Language", value=str(event_data.get("language", "") or ""), key="edit_event_language"
                        )
                        edit_event_duration = st.number_input(
                            "Duration (minutes)", min_value=1,
                            value=max(1, int(event_data.get("duration_minutes", 1) or 1)),
                            step=10, key="edit_event_duration"
                        )
                    with e2:
                        edit_event_rating = st.number_input(
                            "Rating", min_value=0.0, max_value=5.0,
                            value=min(5.0, max(0.0, float(event_data.get("rating", 0) or 0))),
                            step=0.1, key="edit_event_rating"
                        )
                        edit_event_image = st.text_input(
                            "Image URL", value=str(event_data.get("image_url", "") or ""), key="edit_event_image"
                        )
                        edit_event_description = st.text_area(
                            "Description", value=str(event_data.get("description", "") or ""), key="edit_event_description"
                        )

                    update_event = st.form_submit_button(
                        "💾 Save Event Changes", type="primary", use_container_width=True
                    )

                if update_event:
                    payload = {
                        "name": edit_event_name.strip(),
                        "category": edit_event_category.strip(),
                        "description": edit_event_description.strip() or None,
                        "language": edit_event_language.strip() or None,
                        "duration_minutes": int(edit_event_duration),
                        "rating": float(edit_event_rating),
                        "image_url": edit_event_image.strip() or None
                    }
                    if not payload["name"] or not payload["category"]:
                        st.warning("Please fill Event Name and Category.")
                    else:
                        response = admin_api_request(
                            "PUT", f"/events/admin/{int(event_id)}", payload
                        )
                        if response is not None and response.status_code == 200:
                            st.success("Event updated successfully! ✅")
                            st.session_state.admin_edit_event = response.json()
                            st.rerun()
                        else:
                            st.error(admin_error_message(response, "Unable to update event."))

            if delete_event:
                response = admin_api_request("DELETE", f"/events/admin/{int(event_id)}")
                if response is not None and response.status_code == 200:
                    st.success("Event deleted successfully! 🗑️")
                    st.session_state.admin_edit_event = None
                    st.rerun()
                else:
                    st.error(admin_error_message(response, "Unable to delete event."))

        # ========================================================
        # VENUES
        # ========================================================
        with event_tab2:
            st.subheader("🏟️ Event Venue Management")
            venues_response = admin_api_get("/events/admin/venues/all")
            venues = (
                venues_response.json()
                if venues_response is not None and venues_response.status_code == 200
                else []
            )
            if venues_response is not None and venues_response.status_code != 200:
                st.error(admin_error_message(venues_response, "Unable to load venues."))

            venue_search = st.text_input(
                "Search venues", placeholder="Name, city or address...", key="admin_event_venue_search"
            )
            filtered_venues = venues
            if venue_search.strip():
                term = venue_search.strip().lower()
                filtered_venues = [
                    v for v in venues
                    if term in str(v.get("name", "")).lower()
                    or term in str(v.get("city", "")).lower()
                    or term in str(v.get("address", "")).lower()
                ]

            if filtered_venues:
                venue_df = pd.DataFrame(filtered_venues).rename(columns={
                    "id": "Venue ID", "name": "Name", "city": "City",
                    "address": "Address", "capacity": "Capacity", "created_at": "Created At"
                })
                st.dataframe(venue_df, use_container_width=True, hide_index=True)
                st.success(f"Showing {len(filtered_venues)} venue(s).")
            else:
                st.info("No venues found.")

            st.divider()
            st.subheader("➕ Add New Venue")
            with st.form("admin_add_event_venue_form"):
                c1, c2 = st.columns(2)
                with c1:
                    venue_name = st.text_input("Venue Name", placeholder="Gachibowli Stadium")
                    venue_city = st.text_input("City", placeholder="Hyderabad")
                with c2:
                    venue_address = st.text_input("Address", placeholder="Gachibowli, Hyderabad")
                    venue_capacity = st.number_input("Capacity", min_value=1, value=1000, step=100)
                create_venue = st.form_submit_button(
                    "🚀 Create Venue", type="primary", use_container_width=True
                )

            if create_venue:
                payload = {
                    "name": venue_name.strip(),
                    "city": venue_city.strip(),
                    "address": venue_address.strip(),
                    "capacity": int(venue_capacity)
                }
                if not all([payload["name"], payload["city"], payload["address"]]):
                    st.warning("Please fill all venue fields.")
                else:
                    response = admin_api_request("POST", "/events/admin/venues/create", payload)
                    if response is not None and response.status_code in [200, 201]:
                        st.success("Venue created successfully! 🏟️")
                        st.rerun()
                    else:
                        st.error(admin_error_message(response, "Unable to create venue."))

            st.divider()
            st.subheader("✏️ Edit / Delete Venue")
            venue_id = st.number_input(
                "Venue ID", min_value=1, value=1, step=1, key="admin_edit_event_venue_id"
            )
            load_col, delete_col = st.columns(2)
            with load_col:
                load_venue = st.button("🔎 Load Venue", use_container_width=True, key="admin_load_event_venue")
            with delete_col:
                delete_venue = st.button("🗑️ Delete Venue", use_container_width=True, key="admin_delete_event_venue")

            if load_venue:
                response = admin_api_get(f"/events/admin/venues/{int(venue_id)}")
                if response is not None and response.status_code == 200:
                    st.session_state.admin_edit_event_venue = response.json()
                else:
                    st.session_state.admin_edit_event_venue = None
                    st.error(admin_error_message(response, "Venue not found."))

            venue_data = st.session_state.get("admin_edit_event_venue")
            if venue_data:
                st.info(f"Editing Venue #{venue_data.get('id')} — {venue_data.get('name', '')}")
                with st.form("admin_edit_event_venue_form"):
                    e1, e2 = st.columns(2)
                    with e1:
                        edit_venue_name = st.text_input(
                            "Venue Name", value=str(venue_data.get("name", "")), key="edit_event_venue_name"
                        )
                        edit_venue_city = st.text_input(
                            "City", value=str(venue_data.get("city", "")), key="edit_event_venue_city"
                        )
                    with e2:
                        edit_venue_address = st.text_input(
                            "Address", value=str(venue_data.get("address", "")), key="edit_event_venue_address"
                        )
                        edit_venue_capacity = st.number_input(
                            "Capacity", min_value=1,
                            value=max(1, int(venue_data.get("capacity", 1) or 1)),
                            step=100, key="edit_event_venue_capacity"
                        )
                    update_venue = st.form_submit_button(
                        "💾 Save Venue Changes", type="primary", use_container_width=True
                    )

                if update_venue:
                    payload = {
                        "name": edit_venue_name.strip(),
                        "city": edit_venue_city.strip(),
                        "address": edit_venue_address.strip(),
                        "capacity": int(edit_venue_capacity)
                    }
                    if not all([payload["name"], payload["city"], payload["address"]]):
                        st.warning("Please fill all venue fields.")
                    else:
                        response = admin_api_request(
                            "PUT", f"/events/admin/venues/{int(venue_id)}", payload
                        )
                        if response is not None and response.status_code == 200:
                            st.success("Venue updated successfully! ✅")
                            st.session_state.admin_edit_event_venue = response.json()
                            st.rerun()
                        else:
                            st.error(admin_error_message(response, "Unable to update venue."))

            if delete_venue:
                response = admin_api_request(
                    "DELETE", f"/events/admin/venues/{int(venue_id)}"
                )
                if response is not None and response.status_code == 200:
                    st.success("Venue deleted successfully! 🗑️")
                    st.session_state.admin_edit_event_venue = None
                    st.rerun()
                else:
                    st.error(admin_error_message(response, "Unable to delete venue."))

        # ========================================================
        # SHOWS
        # ========================================================
        with event_tab3:
            st.subheader("🕒 Event Show Management")
            shows_response = admin_api_get("/events/admin/shows/all")
            shows = (
                shows_response.json()
                if shows_response is not None and shows_response.status_code == 200
                else []
            )
            if shows_response is not None and shows_response.status_code != 200:
                st.error(admin_error_message(shows_response, "Unable to load event shows."))

            events_response = admin_api_get("/events/admin/all")
            events_for_show = (
                events_response.json()
                if events_response is not None and events_response.status_code == 200
                else []
            )
            venues_response = admin_api_get("/events/admin/venues/all")
            venues_for_show = (
                venues_response.json()
                if venues_response is not None and venues_response.status_code == 200
                else []
            )

            event_lookup = {e["id"]: e.get("name", "") for e in events_for_show}
            venue_lookup = {v["id"]: v.get("name", "") for v in venues_for_show}

            if shows:
                display_shows = []
                for show in shows:
                    row = dict(show)
                    row["event"] = event_lookup.get(show.get("event_id"), f"Event #{show.get('event_id')}")
                    row["venue"] = venue_lookup.get(show.get("venue_id"), f"Venue #{show.get('venue_id')}")
                    display_shows.append(row)

                show_df = pd.DataFrame(display_shows).rename(columns={
                    "id": "Show ID",
                    "event": "Event",
                    "venue": "Venue",
                    "event_id": "Event ID",
                    "venue_id": "Venue ID",
                    "show_date": "Date",
                    "show_time": "Time",
                    "ticket_type": "Ticket Type",
                    "ticket_price": "Ticket Price",
                    "total_tickets": "Total Tickets",
                    "available_tickets": "Available Tickets",
                    "created_at": "Created At"
                })
                if "Ticket Price" in show_df.columns:
                    show_df["Ticket Price"] = show_df["Ticket Price"].apply(
                        lambda x: f"₹{float(x):,.0f}"
                    )
                st.dataframe(show_df, use_container_width=True, hide_index=True)
                st.success(f"Showing {len(shows)} show(s).")
            else:
                st.info("No event shows found.")

            if not events_for_show or not venues_for_show:
                st.warning("Create at least one event and one venue before adding a show.")
            else:
                event_options = {
                    f"#{e['id']} — {e.get('name', '')}": e["id"] for e in events_for_show
                }
                venue_options = {
                    f"#{v['id']} — {v.get('name', '')} ({v.get('city', '')})": v["id"] for v in venues_for_show
                }

                st.divider()
                st.subheader("➕ Add Event Show")
                with st.form("admin_add_event_show_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        add_show_event = st.selectbox("Event", list(event_options.keys()), key="add_event_show_event")
                        add_show_venue = st.selectbox("Venue", list(venue_options.keys()), key="add_event_show_venue")
                        add_show_date = st.text_input("Show Date", placeholder="2026-12-25", key="add_event_show_date")
                        add_show_time = st.text_input("Show Time", placeholder="07:00 PM", key="add_event_show_time")
                    with c2:
                        add_show_ticket_type = st.text_input("Ticket Type", placeholder="VIP", key="add_event_show_ticket_type")
                        add_show_price = st.number_input("Ticket Price (₹)", min_value=1, value=999, step=50, key="add_event_show_price")
                        add_show_total = st.number_input("Total Tickets", min_value=1, value=500, step=50, key="add_event_show_total")
                        add_show_available = st.number_input("Available Tickets", min_value=0, value=500, step=50, key="add_event_show_available")

                    create_show = st.form_submit_button(
                        "🚀 Create Event Show", type="primary", use_container_width=True
                    )

                if create_show:
                    if not add_show_date.strip() or not add_show_time.strip() or not add_show_ticket_type.strip():
                        st.warning("Please fill date, time and ticket type.")
                    elif int(add_show_available) > int(add_show_total):
                        st.warning("Available tickets cannot exceed total tickets.")
                    else:
                        payload = {
                            "event_id": int(event_options[add_show_event]),
                            "venue_id": int(venue_options[add_show_venue]),
                            "show_date": add_show_date.strip(),
                            "show_time": add_show_time.strip(),
                            "ticket_type": add_show_ticket_type.strip(),
                            "ticket_price": int(add_show_price),
                            "total_tickets": int(add_show_total),
                            "available_tickets": int(add_show_available)
                        }
                        response = admin_api_request("POST", "/events/admin/shows/create", payload)
                        if response is not None and response.status_code in [200, 201]:
                            st.success("Event show created successfully! 🕒")
                            st.rerun()
                        else:
                            st.error(admin_error_message(response, "Unable to create event show."))

                st.divider()
                st.subheader("✏️ Edit / Delete Event Show")
                show_id = st.number_input(
                    "Show ID", min_value=1, value=1, step=1, key="admin_edit_event_show_id"
                )
                load_col, delete_col = st.columns(2)
                with load_col:
                    load_show = st.button("🔎 Load Show", use_container_width=True, key="admin_load_event_show")
                with delete_col:
                    delete_show = st.button("🗑️ Delete Show", use_container_width=True, key="admin_delete_event_show")

                if load_show:
                    response = admin_api_get(f"/events/admin/shows/{int(show_id)}")
                    if response is not None and response.status_code == 200:
                        st.session_state.admin_edit_event_show = response.json()
                    else:
                        st.session_state.admin_edit_event_show = None
                        st.error(admin_error_message(response, "Event show not found."))

                show_data = st.session_state.get("admin_edit_event_show")
                if show_data:
                    st.info(f"Editing Show #{show_data.get('id')}")
                    event_label_by_id = {v: k for k, v in event_options.items()}
                    venue_label_by_id = {v: k for k, v in venue_options.items()}
                    current_event_id = int(show_data.get("event_id", 0))
                    current_venue_id = int(show_data.get("venue_id", 0))

                    with st.form("admin_edit_event_show_form"):
                        e1, e2 = st.columns(2)
                        with e1:
                            edit_show_event = st.selectbox(
                                "Event", list(event_options.keys()),
                                index=list(event_options.keys()).index(event_label_by_id[current_event_id])
                                if current_event_id in event_label_by_id else 0,
                                key="edit_event_show_event"
                            )
                            edit_show_venue = st.selectbox(
                                "Venue", list(venue_options.keys()),
                                index=list(venue_options.keys()).index(venue_label_by_id[current_venue_id])
                                if current_venue_id in venue_label_by_id else 0,
                                key="edit_event_show_venue"
                            )
                            edit_show_date = st.text_input(
                                "Show Date", value=str(show_data.get("show_date", "")), key="edit_event_show_date"
                            )
                            edit_show_time = st.text_input(
                                "Show Time", value=str(show_data.get("show_time", "")), key="edit_event_show_time"
                            )
                        with e2:
                            edit_show_ticket_type = st.text_input(
                                "Ticket Type", value=str(show_data.get("ticket_type", "")), key="edit_event_show_ticket_type"
                            )
                            edit_show_price = st.number_input(
                                "Ticket Price (₹)", min_value=1,
                                value=max(1, int(float(show_data.get("ticket_price", 1) or 1))),
                                step=50, key="edit_event_show_price"
                            )
                            edit_show_total = st.number_input(
                                "Total Tickets", min_value=1,
                                value=max(1, int(show_data.get("total_tickets", 1) or 1)),
                                step=50, key="edit_event_show_total"
                            )
                            edit_show_available = st.number_input(
                                "Available Tickets", min_value=0,
                                value=max(0, int(show_data.get("available_tickets", 0) or 0)),
                                step=50, key="edit_event_show_available"
                            )

                        update_show = st.form_submit_button(
                            "💾 Save Show Changes", type="primary", use_container_width=True
                        )

                    if update_show:
                        if not edit_show_date.strip() or not edit_show_time.strip() or not edit_show_ticket_type.strip():
                            st.warning("Please fill date, time and ticket type.")
                        elif int(edit_show_available) > int(edit_show_total):
                            st.warning("Available tickets cannot exceed total tickets.")
                        else:
                            payload = {
                                "event_id": int(event_options[edit_show_event]),
                                "venue_id": int(venue_options[edit_show_venue]),
                                "show_date": edit_show_date.strip(),
                                "show_time": edit_show_time.strip(),
                                "ticket_type": edit_show_ticket_type.strip(),
                                "ticket_price": int(edit_show_price),
                                "total_tickets": int(edit_show_total),
                                "available_tickets": int(edit_show_available)
                            }
                            response = admin_api_request(
                                "PUT", f"/events/admin/shows/{int(show_id)}", payload
                            )
                            if response is not None and response.status_code == 200:
                                st.success("Event show updated successfully! ✅")
                                st.session_state.admin_edit_event_show = response.json()
                                st.rerun()
                            else:
                                st.error(admin_error_message(response, "Unable to update event show."))

                if delete_show:
                    response = admin_api_request(
                        "DELETE", f"/events/admin/shows/{int(show_id)}"
                    )
                    if response is not None and response.status_code == 200:
                        st.success("Event show deleted successfully! 🗑️")
                        st.session_state.admin_edit_event_show = None
                        st.rerun()
                    else:
                        st.error(admin_error_message(response, "Unable to delete event show."))


    elif st.session_state.page == "Admin Dashboard":

        # ========================================================
        # ADMIN DASHBOARD 2.0
        # ========================================================

        st.html("""
        <div style="padding:28px;border-radius:24px;margin-bottom:24px;
                    border:1px solid rgba(148,163,184,.18);
                    background:linear-gradient(135deg,rgba(30,41,59,.96),rgba(15,23,42,.98));
                    box-shadow:0 18px 45px rgba(0,0,0,.20);">
            <div style="font-size:12px;font-weight:800;letter-spacing:1.5px;opacity:.65;">
                TRAVELX • ADMIN CONTROL CENTER
            </div>
            <div style="font-size:34px;font-weight:900;margin:8px 0;">
                👑 Welcome to TRAVELX Admin
            </div>
            <div style="font-size:15px;opacity:.72;line-height:1.6;">
                Monitor users, bookings, revenue and every TRAVELX service from one place.
            </div>
        </div>
        """)

        dashboard_response = admin_api_get("/admin/dashboard")

        if dashboard_response is None:
            st.error("Unable to connect to the TRAVELX backend.")
            st.stop()

        if dashboard_response.status_code != 200:
            st.error(
                f"Unable to load admin dashboard. Status: {dashboard_response.status_code}"
            )
            st.stop()

        dashboard_data = get_json(dashboard_response)

        total_users = int(dashboard_data.get("total_users", 0) or 0)
        total_bookings = int(dashboard_data.get("total_bookings", 0) or 0)
        total_revenue = float(dashboard_data.get("total_revenue", 0) or 0)
        total_cancelled = int(dashboard_data.get("total_cancelled", 0) or 0)
        wallet_transactions = int(dashboard_data.get("wallet_transactions", 0) or 0)

        active_bookings = max(total_bookings - total_cancelled, 0)
        cancellation_rate = (
            (total_cancelled / total_bookings) * 100
            if total_bookings else 0
        )
        average_booking = (
            total_revenue / total_bookings
            if total_bookings else 0
        )

        # KPI cards
        st.subheader("📊 Business Overview")
        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric("👥 Total Users", f"{total_users:,}")
        with c2:
            st.metric("📋 Total Bookings", f"{total_bookings:,}")
        with c3:
            st.metric("💰 Revenue", f"₹{total_revenue:,.0f}")
        with c4:
            st.metric("❌ Cancelled", f"{total_cancelled:,}")
        with c5:
            st.metric("💳 Wallet Transactions", f"{wallet_transactions:,}")

        st.divider()

        p1, p2, p3, p4 = st.columns(4)
        with p1:
            st.metric("🟢 Active Bookings", f"{active_bookings:,}")
        with p2:
            st.metric("📉 Cancellation Rate", f"{cancellation_rate:.1f}%")
        with p3:
            st.metric("💵 Avg Booking Value", f"₹{average_booking:,.0f}")
        with p4:
            services_for_top = dashboard_data.get("services", []) or []
            top_service = "—"
            if services_for_top:
                top_service_row = max(
                    services_for_top,
                    key=lambda x: float(x.get("bookings", 0) or 0)
                )
                top_service = str(top_service_row.get("service", "—"))
            st.metric("🏆 Top Service", top_service)

        st.divider()

        admin_tab1, admin_tab2, admin_tab3 = st.tabs([
            "📊 Analytics",
            "👥 Customers",
            "📋 Bookings",
        ])

        with admin_tab1:
            st.subheader("📈 Service Performance")

            services = dashboard_data.get("services", []) or []

            if services:
                service_df = pd.DataFrame(services)

                if "bookings" in service_df.columns:
                    service_df["bookings"] = pd.to_numeric(
                        service_df["bookings"], errors="coerce"
                    ).fillna(0)

                if "revenue" in service_df.columns:
                    service_df["revenue"] = pd.to_numeric(
                        service_df["revenue"], errors="coerce"
                    ).fillna(0)

                if "service" not in service_df.columns:
                    service_df["service"] = "Unknown"

                chart1, chart2 = st.columns(2)

                with chart1:
                    st.markdown("### 📈 Bookings by Service")
                    if "bookings" in service_df.columns:
                        st.bar_chart(
                            service_df[["service", "bookings"]].set_index("service"),
                            use_container_width=True
                        )

                with chart2:
                    st.markdown("### 💰 Revenue by Service")
                    if "revenue" in service_df.columns:
                        st.bar_chart(
                            service_df[["service", "revenue"]].set_index("service"),
                            use_container_width=True
                        )

                st.markdown("### 📋 Service Breakdown")
                display_df = service_df.copy()
                if "revenue" in display_df.columns:
                    display_df["revenue"] = display_df["revenue"].apply(
                        lambda value: f"₹{float(value):,.2f}"
                    )
                display_df = display_df.rename(columns={
                    "service": "Service",
                    "bookings": "Bookings",
                    "revenue": "Revenue",
                })
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No service analytics available yet.")

        with admin_tab2:
            st.subheader("👥 Customer Management")
            st.caption("Search and inspect registered TRAVELX customers.")

            search_col, refresh_col = st.columns([5, 1])

            with search_col:
                user_search = st.text_input(
                    "Search users",
                    placeholder="Name, email or phone...",
                    key="step8_admin_user_search"
                )

            with refresh_col:
                st.write("")
                if st.button(
                    "🔄 Refresh",
                    key="step8_admin_refresh_users",
                    use_container_width=True
                ):
                    st.rerun()

            endpoint = "/admin/users"
            if user_search.strip():
                from urllib.parse import quote
                endpoint += "?search=" + quote(user_search.strip())

            users_response = admin_api_get(endpoint)

            if users_response is None:
                st.warning("Unable to load users.")
            elif users_response.status_code == 200:
                users_data = get_json(users_response)

                if users_data:
                    users_df = pd.DataFrame(users_data).rename(columns={
                        "id": "User ID",
                        "name": "Name",
                        "email": "Email",
                        "phone": "Phone",
                        "created_at": "Registered",
                    })
                    st.dataframe(
                        users_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    st.success(f"Showing {len(users_data)} user(s).")
                else:
                    st.info("No users matched your search.")
            else:
                st.error(
                    f"Unable to load users. Status: {users_response.status_code}"
                )

        with admin_tab3:
            st.subheader("📋 Booking Management")
            st.caption("View bookings across every TRAVELX service from one place.")

            filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 4])

            with filter_col1:
                service_filter = st.selectbox(
                    "Service",
                    ["All", "Bus", "Train", "Hotel", "Flight", "Cab", "Food", "Movies", "Events", "General"],
                    key="step8_admin_service_filter"
                )

            with filter_col2:
                status_filter = st.selectbox(
                    "Status",
                    ["All", "confirmed", "booked", "pending", "cancelled"],
                    key="step8_admin_status_filter"
                )

            with filter_col3:
                booking_search = st.text_input(
                    "Search bookings",
                    placeholder="Booking ID, user name or email...",
                    key="step8_admin_booking_search"
                )

            from urllib.parse import quote
            params = [
                "service=" + quote(service_filter),
                "status=" + quote(status_filter),
            ]
            if booking_search.strip():
                params.append("search=" + quote(booking_search.strip()))

            bookings_response = admin_api_get(
                "/admin/bookings?" + "&".join(params)
            )

            if bookings_response is None:
                st.warning("Unable to load bookings.")
            elif bookings_response.status_code == 200:
                bookings_data = get_json(bookings_response)

                if bookings_data:
                    booking_df = pd.DataFrame(bookings_data).rename(columns={
                        "id": "Booking ID",
                        "service": "Service",
                        "user_id": "User ID",
                        "user_name": "Customer",
                        "user_email": "Email",
                        "amount": "Amount",
                        "status": "Status",
                        "payment_method": "Payment",
                        "created_at": "Created",
                    })

                    if "Amount" in booking_df.columns:
                        booking_df["Amount"] = booking_df["Amount"].apply(
                            lambda value: f"₹{float(value):,.2f}"
                        )

                    st.dataframe(
                        booking_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    st.success(f"Showing {len(bookings_data)} booking(s).")
                else:
                    st.info("No bookings matched the selected filters.")
            else:
                st.error(
                    f"Unable to load bookings. Status: {bookings_response.status_code}"
                )

        st.divider()
        st.subheader("⚡ Quick Actions")

        q1, q2, q3, q4 = st.columns(4)

        quick_actions = [
            (q1, "🚌 Manage Buses", "Admin Buses", "step8_quick_buses"),
            (q2, "✈️ Manage Flights", "Admin Flights", "step8_quick_flights"),
            (q3, "🏨 Manage Hotels", "Admin Hotels", "step8_quick_hotels"),
            (q4, "🎟️ Manage Events", "Admin Events", "step8_quick_events"),
        ]

        for column, label, page_name, button_key in quick_actions:
            with column:
                if st.button(label, use_container_width=True, key=button_key):
                    st.session_state.page = page_name
                    st.rerun()

        st.caption("TRAVELX Admin • Control • Analyze • Manage")

    else:
        st.session_state.page = "Admin Dashboard"
        st.rerun()

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
        (
            "🔔",
            (
                f"Notifications "
                f"({st.session_state.notification_unread_count})"
                if st.session_state.notification_unread_count > 0
                else "Notifications"
            )
        ),
        ("📋", "My Bookings"),
        ("👤", "Profile")
    ]

    for icon, page_name in pages:

        if st.button(
            f"{icon}  {page_name}",
            use_container_width=True,
            key=f"sidebar_{page_name}"
        ):

            if page_name.startswith("Notifications"):
                st.session_state.page = "Notifications"
            else:
                st.session_state.page = page_name

            st.rerun()

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout_user()


# ============================================================
# HOME — STEP 7 PREMIUM DASHBOARD
# ============================================================

if st.session_state.page == "Home":

    user_name = (
        st.session_state.user.get("name", "Traveler")
        if st.session_state.user
        else "Traveler"
    )

    # --------------------------------------------------------
    # DATA HELPERS
    # --------------------------------------------------------
    def _home_list(endpoint):
        response = api_get(endpoint)
        if response and response.status_code == 200:
            data = get_json(response)
            if isinstance(data, list):
                return data
        return []

    def _home_first(item, *keys, default=""):
        if not isinstance(item, dict):
            return default
        for key in keys:
            value = item.get(key)
            if value not in (None, ""):
                return value
        return default

    def _home_status(item):
        return str(_home_first(item, "status", "booking_status", "order_status", default="Confirmed")).replace("_", " ").title()

    def _home_amount(item):
        value = _home_first(
            item,
            "total_amount", "amount", "price", "fare", "total_price",
            "total_fare", "booking_amount", "grand_total",
            default=0
        )
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0

    def _home_date(item):
        value = _home_first(
            item,
            "travel_date", "journey_date", "booking_date", "show_date",
            "event_date", "date", "check_in", "checkin", "departure_date",
            "start_date", default=""
        )
        return str(value) if value else ""

    def _home_date_label(value):
        if not value:
            return "Date not available"
        raw = str(value).strip()
        try:
            parsed = date.fromisoformat(raw[:10])
            return parsed.strftime("%d %b %Y")
        except Exception:
            return raw[:16].replace("T", " ")

    def _home_sort_value(item):
        value = _home_first(item, "created_at", "booking_date", "travel_date", "journey_date", "show_date", "event_date", "date", default="")
        return str(value or "")

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------
    st.html(f"""
    <div class="hero-box" style="padding:34px 38px; margin-bottom:18px;">
        <div style="display:flex; justify-content:space-between; gap:24px; align-items:center; flex-wrap:wrap;">
            <div style="flex:1; min-width:280px;">
                <div class="hero-badge">✨ YOUR JOURNEY STARTS HERE</div>
                <div class="hero-title" style="font-size:42px; margin-top:12px;">
                    Welcome back, {user_name} ✈️
                </div>
                <div class="hero-text" style="max-width:760px; margin-top:10px;">
                    Plan, book and manage your complete journey from one powerful travel dashboard.
                    Flights, trains, buses, hotels, cabs, food, movies, events and AI — all in TRAVELX.
                </div>
            </div>
            <div style="min-width:210px; text-align:center; padding:20px; border-radius:20px; background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.10);">
                <div style="font-size:42px;">🌍</div>
                <div style="font-size:13px; opacity:.75; margin-top:6px;">YOUR ALL-IN-ONE</div>
                <div style="font-size:20px; font-weight:700;">TRAVEL COMPANION</div>
            </div>
        </div>
    </div>
    """)

    # --------------------------------------------------------
    # DESTINATION SEARCH
    # --------------------------------------------------------
    st.html("""
    <div class="section-heading">Where do you want to go?</div>
    <div class="section-subtitle">Start with a destination and let TRAVELX take you from discovery to booking.</div>
    """)

    destination_col, destination_btn = st.columns([5, 1.25])
    with destination_col:
        destination = st.text_input(
            "",
            placeholder="Search a destination — Hyderabad, Goa, Delhi, Mumbai...",
            key="home_destination_search",
            label_visibility="collapsed"
        )
    with destination_btn:
        if st.button("🔎 Explore", use_container_width=True, key="home_explore_destination"):
            if destination.strip():
                st.session_state.hotel_city = destination.strip()
                st.session_state.page = "Hotels"
                st.rerun()
            else:
                st.warning("Enter a destination first.")

    # --------------------------------------------------------
    # QUICK BOOKING GRID
    # --------------------------------------------------------
    st.html("""
    <div class="section-heading">Book in One Tap</div>
    <div class="section-subtitle">Your most important TRAVELX services, right at your fingertips.</div>
    """)

    quick_services = [
        ("✈️", "Flights", "Compare and book flights."),
        ("🚆", "Trains", "Plan your railway journey."),
        ("🚌", "Buses", "Book intercity buses."),
        ("🏨", "Hotels", "Find a comfortable stay."),
        ("🚕", "Cabs", "Book local and outstation rides."),
        ("🍔", "Food", "Order food on the go."),
        ("🎬", "Movies", "Book your next movie."),
        ("🎟️", "Events", "Discover live experiences."),
    ]

    for row in range(0, len(quick_services), 4):
        cols = st.columns(4)
        for index, col in enumerate(cols):
            service_index = row + index
            if service_index >= len(quick_services):
                continue
            icon, title, description = quick_services[service_index]
            with col:
                st.html(f"""
                <div class="service-card" style="min-height:150px;">
                    <div class="service-icon">{icon}</div>
                    <div class="service-title">{title}</div>
                    <div class="service-description">{description}</div>
                </div>
                """)
                if st.button(f"Open {title}", use_container_width=True, key=f"home_quick_{title}"):
                    st.session_state.page = title
                    st.rerun()

    # --------------------------------------------------------
    # LOAD DASHBOARD ACTIVITY
    # --------------------------------------------------------
    endpoint_map = {
        "Flights": "/flights/my-bookings",
        "Trains": "/trains/my-bookings",
        "Buses": "/buses/my-bookings",
        "Hotels": "/hotels/my-bookings",
        "Cabs": "/cabs/my-bookings",
        "Food": "/food/my-orders",
        "Movies": "/movies/my-bookings",
        "Events": "/events/my-bookings",
        "Other": "/bookings/my",
    }

    home_activity = []
    service_data = {}
    for service_name, endpoint in endpoint_map.items():
        items = _home_list(endpoint)
        service_data[service_name] = items
        for item in items:
            if isinstance(item, dict):
                item_copy = dict(item)
                item_copy["_service"] = service_name
                home_activity.append(item_copy)

    wallet_balance = 0.0
    wallet_response = api_get("/wallet/")
    if wallet_response and wallet_response.status_code == 200:
        wallet_data = get_json(wallet_response)
        if isinstance(wallet_data, dict):
            try:
                wallet_balance = float(wallet_data.get("balance", 0) or 0)
            except (TypeError, ValueError):
                wallet_balance = 0.0

    total_bookings = len(home_activity)
    active_journeys = sum(
        1 for item in home_activity
        if _home_status(item).lower() in {"confirmed", "pending", "booked", "active"}
    )
    total_spend = sum(_home_amount(item) for item in home_activity if _home_status(item).lower() != "cancelled")

    # --------------------------------------------------------
    # SNAPSHOT METRICS
    # --------------------------------------------------------
    st.html("""
    <div class="section-heading">Your Travel Snapshot</div>
    <div class="section-subtitle">A live overview of your TRAVELX activity.</div>
    """)

    m1, m2, m3, m4 = st.columns(4)
    metric_values = [
        ("💰", "Wallet Balance", f"₹{wallet_balance:,.2f}"),
        ("📋", "Total Activity", str(total_bookings)),
        ("🧳", "Active Journeys", str(active_journeys)),
        ("💳", "Travel Spend", f"₹{total_spend:,.2f}"),
    ]
    for col, (icon, label, value) in zip((m1, m2, m3, m4), metric_values):
        with col:
            st.html(f"""
            <div class="metric-card" style="min-height:130px;">
                <div style="font-size:22px; margin-bottom:5px;">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """)

    # --------------------------------------------------------
    # WALLET + AI PROMO
    # --------------------------------------------------------
    wallet_col, ai_col = st.columns(2)
    with wallet_col:
        st.html(f"""
        <div class="service-card" style="min-height:180px; padding:24px;">
            <div style="font-size:30px;">💰</div>
            <div style="font-size:22px; font-weight:800; margin-top:5px;">TRAVELX Wallet</div>
            <div style="opacity:.7; margin:5px 0 14px;">Ready for your next booking.</div>
            <div style="font-size:30px; font-weight:800;">₹{wallet_balance:,.2f}</div>
        </div>
        """)
        if st.button("💳 Manage Wallet", use_container_width=True, key="home_manage_wallet"):
            st.session_state.page = "Wallet"
            st.rerun()

    with ai_col:
        st.html("""
        <div class="service-card" style="min-height:180px; padding:24px;">
            <div style="font-size:30px;">🤖</div>
            <div style="font-size:22px; font-weight:800; margin-top:5px;">AI Trip Planner</div>
            <div style="opacity:.7; margin:5px 0 14px;">Build a smarter itinerary around your destination, time and budget.</div>
            <div style="font-size:16px; font-weight:700;">Plan less. Explore more. ✨</div>
        </div>
        """)
        if st.button("🤖 Plan My Trip", use_container_width=True, key="home_plan_trip"):
            st.session_state.page = "AI Trip Planner"
            st.rerun()

    # --------------------------------------------------------
    # UPCOMING / RECENT ACTIVITY
    # --------------------------------------------------------
    st.html("""
    <div class="section-heading">Your Journey Activity</div>
    <div class="section-subtitle">Your latest bookings and orders across TRAVELX.</div>
    """)

    recent_items = sorted(home_activity, key=_home_sort_value, reverse=True)[:6]
    if recent_items:
        for row in range(0, len(recent_items), 2):
            cols = st.columns(2)
            for index, col in enumerate(cols):
                item_index = row + index
                if item_index >= len(recent_items):
                    continue
                item = recent_items[item_index]
                service = item.get("_service", "Booking")
                status = _home_status(item)
                booking_id = _home_first(item, "id", "booking_id", "order_id", default="—")
                amount = _home_amount(item)
                activity_date = _home_date(item)
                location = _home_first(item, "route", "source", "destination", "city", "hotel_name", "restaurant_name", "movie_title", "event_name", default="TRAVELX booking")
                icon_map = {"Flights":"✈️", "Trains":"🚆", "Buses":"🚌", "Hotels":"🏨", "Cabs":"🚕", "Food":"🍔", "Movies":"🎬", "Events":"🎟️", "Other":"📋"}
                icon = icon_map.get(service, "📋")
                with col:
                    st.html(f"""
                    <div class="service-card" style="min-height:155px; padding:20px;">
                        <div style="display:flex; justify-content:space-between; gap:10px; align-items:flex-start;">
                            <div>
                                <div style="font-size:27px;">{icon}</div>
                                <div style="font-size:19px; font-weight:800; margin-top:5px;">{service}</div>
                            </div>
                            <div style="font-size:12px; padding:6px 10px; border-radius:999px; background:rgba(255,255,255,.08);">{status}</div>
                        </div>
                        <div style="margin-top:10px; opacity:.75;">Booking #{booking_id}</div>
                        <div style="margin-top:4px; font-weight:600;">{str(location)[:70]}</div>
                        <div style="display:flex; justify-content:space-between; margin-top:10px; opacity:.8; font-size:13px;">
                            <span>{_home_date_label(activity_date)}</span>
                            <span>₹{amount:,.2f}</span>
                        </div>
                    </div>
                    """)
    else:
        st.html("""
        <div class="service-card" style="padding:28px; text-align:center;">
            <div style="font-size:38px;">🧳</div>
            <div style="font-size:22px; font-weight:800; margin-top:8px;">Your journey starts here</div>
            <div style="opacity:.7; margin-top:6px;">You don't have any activity yet. Pick a service above and make your first booking.</div>
        </div>
        """)

    if st.button("📋 View All My Bookings", use_container_width=True, key="home_view_all_bookings"):
        st.session_state.page = "My Bookings"
        st.rerun()

    # --------------------------------------------------------
    # SERVICE BREAKDOWN
    # --------------------------------------------------------
    st.html("""
    <div class="section-heading">Service Breakdown</div>
    <div class="section-subtitle">See where you've been using TRAVELX.</div>
    """)

    service_counts = [
        ("✈️", "Flights", len(service_data["Flights"])),
        ("🚆", "Trains", len(service_data["Trains"])),
        ("🚌", "Buses", len(service_data["Buses"])),
        ("🏨", "Hotels", len(service_data["Hotels"])),
        ("🚕", "Cabs", len(service_data["Cabs"])),
        ("🍔", "Food", len(service_data["Food"])),
        ("🎬", "Movies", len(service_data["Movies"])),
        ("🎟️", "Events", len(service_data["Events"])),
    ]

    for row in range(0, len(service_counts), 4):
        cols = st.columns(4)
        for index, col in enumerate(cols):
            item_index = row + index
            if item_index >= len(service_counts):
                continue
            icon, label, count = service_counts[item_index]
            with col:
                st.html(f"""
                <div class="metric-card" style="min-height:105px;">
                    <div style="font-size:20px;">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="font-size:28px;">{count}</div>
                </div>
                """)

    # --------------------------------------------------------
    # DISCOVER MORE
    # --------------------------------------------------------
    st.html("""
    <div class="section-heading">Discover More</div>
    <div class="section-subtitle">Tools that make TRAVELX more than a booking app.</div>
    """)

    discover = [
        ("🤖", "AI Trip Planner", "Create a personalized itinerary in seconds.", "AI Trip Planner"),
        ("💰", "TRAVELX Wallet", "Keep money ready and simplify payments.", "Wallet"),
        ("🔔", "Notifications", "Stay updated about bookings and payments.", "Notifications"),
        ("📋", "My Bookings", "Manage every booking from one place.", "My Bookings"),
    ]

    cols = st.columns(4)
    for col, (icon, title, description, target) in zip(cols, discover):
        with col:
            st.html(f"""
            <div class="service-card" style="min-height:150px;">
                <div class="service-icon">{icon}</div>
                <div class="service-title">{title}</div>
                <div class="service-description">{description}</div>
            </div>
            """)
            if st.button(f"Open {title}", use_container_width=True, key=f"home_discover_{title}"):
                st.session_state.page = target
                st.rerun()

    # --------------------------------------------------------
    # WHY TRAVELX
    # --------------------------------------------------------
    st.html("""
    <div class="section-heading">Why TRAVELX?</div>
    <div class="section-subtitle">One platform designed around your entire journey.</div>
    """)

    why1, why2, why3, why4 = st.columns(4)
    why_items = [
        (why1, "⚡", "Fast & Simple", "Plan and manage your journey without switching between multiple applications."),
        (why2, "🔐", "Secure Account", "Your account, bookings and payments are managed through the TRAVELX platform."),
        (why3, "💰", "Digital Wallet", "Keep your TRAVELX balance ready for future bookings and refunds."),
        (why4, "🤖", "AI Powered", "Use intelligent trip planning to turn your travel ideas into practical itineraries."),
    ]
    for col, icon, title, description in why_items:
        with col:
            st.markdown(f"### {icon}")
            st.write(f"**{title}**")
            st.caption(description)


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
# MY BOOKINGS - UNIFIED DASHBOARD
# ============================================================


elif st.session_state.page == "Notifications":

    st.title("🔔 TRAVELX Notifications")
    st.caption("Stay updated with your bookings, payments, cancellations and refunds.")

    notifications_response = api_get("/notifications/")
    unread_response = api_get("/notifications/unread-count")

    notifications = []

    if notifications_response and notifications_response.status_code == 200:
        data = get_json(notifications_response)
        if isinstance(data, list):
            notifications = data
    elif notifications_response:
        st.error("Unable to load notifications.")

    if unread_response and unread_response.status_code == 200:
        unread_data = get_json(unread_response)
        st.session_state.notification_unread_count = int(
            unread_data.get("unread_count", 0)
        )

    unread_count = st.session_state.notification_unread_count

    header_left, header_right = st.columns([3, 1])

    with header_left:
        if unread_count > 0:
            st.info(f"🔵 {unread_count} unread notification(s)")
        else:
            st.success("✅ You're all caught up.")

    with header_right:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
            key="refresh_notifications"
        ):
            st.rerun()

    st.divider()

    # ------------------------------------------------------------
    # MARK ALL AS READ
    # ------------------------------------------------------------
    if notifications and unread_count > 0:
        if st.button(
            "✓✓ Mark All as Read",
            use_container_width=True,
            key="mark_all_notifications"
        ):
            response = api_patch("/notifications/read-all")

            if response and response.status_code == 200:
                st.session_state.notification_unread_count = 0
                st.success("All notifications marked as read. ✅")
                st.rerun()
            elif response:
                st.error(
                    get_json(response).get(
                        "detail",
                        "Unable to mark all notifications as read."
                    )
                )

    notification_icons = {
        "success": "🎉",
        "booking": "🎫",
        "payment": "💳",
        "refund": "💰",
        "cancel": "❌",
        "cancellation": "❌",
        "wallet": "💰",
        "warning": "⚠️",
        "info": "ℹ️",
    }

    service_icons = {
        "Bus": "🚌",
        "Train": "🚆",
        "Flight": "✈️",
        "Hotel": "🏨",
        "Cab": "🚕",
        "Food": "🍔",
        "Movies": "🎬",
        "Movie": "🎬",
        "Events": "🎟️",
        "Event": "🎟️",
        "Wallet": "💰",
        "TRAVELX": "✈️",
    }

    if not notifications:
        st.html("""
        <div style="
            padding:50px 25px;
            text-align:center;
            border:1px solid rgba(148,163,184,.18);
            border-radius:20px;
            background:rgba(15,23,42,.45);
        ">
            <div style="font-size:55px;">🔔</div>
            <div style="font-size:24px;font-weight:900;margin-top:10px;">
                No Notifications Yet
            </div>
            <div style="opacity:.65;margin-top:8px;">
                Booking confirmations, refunds and important
                TRAVELX updates will appear here.
            </div>
        </div>
        """)

    else:
        for notification in notifications:
            notification_id = notification.get("id", "-")
            notification_type = str(
                notification.get("notification_type", "info")
            ).lower()
            title = notification.get(
                "title", "TRAVELX Notification"
            )
            message = notification.get("message", "")
            service = notification.get("service")
            booking_id = notification.get("booking_id")
            amount = notification.get("amount")
            is_read = bool(notification.get("is_read", False))
            created_at = notification.get("created_at", "")

            icon = notification_icons.get(notification_type, "🔔")
            service_icon = service_icons.get(str(service), "🔔")

            # Format timestamp without changing the backend value.
            formatted_time = str(created_at).replace("T", " ")
            if "." in formatted_time:
                formatted_time = formatted_time.split(".")[0]
            if "+" in formatted_time:
                formatted_time = formatted_time.split("+")[0]
            formatted_time = formatted_time[:19]

            # --------------------------------------------------------
            # POLISHED NOTIFICATION CARD
            # --------------------------------------------------------
            if not is_read:
                card_background = "rgba(30,64,175,.18)"
                card_border = "rgba(96,165,250,.40)"
                status_text = "🔵 Unread"
            else:
                card_background = "rgba(15,23,42,.35)"
                card_border = "rgba(148,163,184,.16)"
                status_text = "✓ Read"

            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="
                        padding:4px 2px 8px 2px;
                        border-radius:14px;
                        background:{card_background};
                        border:1px solid {card_border};
                        padding:16px;
                        margin-bottom:4px;
                    ">
                        <div style="
                            display:flex;
                            align-items:center;
                            gap:10px;
                            font-size:18px;
                            font-weight:800;
                            color:#f8fafc;
                        ">
                            <span style="font-size:26px;">{icon}</span>
                            <span>{title}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                left, right = st.columns([5, 1])

                with left:
                    st.write(message)

                    meta_parts = []

                    if service:
                        meta_parts.append(
                            f"{service_icon} {str(service)}"
                        )

                    if booking_id:
                        meta_parts.append(
                            f"🎫 Booking #{booking_id}"
                        )

                    if amount is not None:
                        try:
                            meta_parts.append(
                                f"💰 ₹{float(amount):,.2f}"
                            )
                        except (TypeError, ValueError):
                            pass

                    if formatted_time:
                        meta_parts.append(
                            f"🕐 {formatted_time}"
                        )

                    if meta_parts:
                        st.caption("  •  ".join(meta_parts))

                    st.caption(status_text)

                with right:
                    if not is_read:
                        if st.button(
                            "✓ Read",
                            use_container_width=True,
                            key=f"read_notification_{notification_id}"
                        ):
                            response = api_patch(
                                f"/notifications/{notification_id}/read"
                            )

                            if response and response.status_code == 200:
                                st.rerun()
                            elif response:
                                st.error(
                                    get_json(response).get(
                                        "detail",
                                        "Unable to mark notification as read."
                                    )
                                )

    # ------------------------------------------------------------
    # DEVELOPMENT TEST TOOL
    # ------------------------------------------------------------
    with st.expander("🧪 Notification System Test"):
        st.caption(
            "Development tool: create a test notification for the logged-in user."
        )

        test_type = st.selectbox(
            "Notification Type",
            [
                "info",
                "success",
                "booking",
                "payment",
                "refund",
                "cancel",
                "warning"
            ],
            key="notification_test_type"
        )

        if st.button(
            "➕ Create Test Notification",
            use_container_width=True,
            key="create_test_notification"
        ):
            response = api_post(
                "/notifications/test",
                {
                    "notification_type": test_type,
                    "title": "TRAVELX Notification Test",
                    "message": (
                        "Your TRAVELX notification center "
                        "is working perfectly! 🚀"
                    ),
                    "service": "TRAVELX"
                }
            )

            if response and response.status_code in [200, 201]:
                st.success("Test notification created. 🎉")
                st.rerun()
            elif response:
                st.error(
                    get_json(response).get(
                        "detail",
                        "Unable to create test notification."
                    )
                )


elif st.session_state.page == "My Bookings":

    # ============================================================
    # STEP 6 — MY BOOKINGS 2.0
    # ============================================================

    st.title("📋 My Bookings")
    st.caption(
        "Your complete TRAVELX booking history — travel, stays, rides, food, "
        "movies and events."
    )

    # ------------------------------------------------------------
    # SAFE SESSION STATE
    # ------------------------------------------------------------
    if "selected_booking" not in st.session_state:
        st.session_state.selected_booking = None

    if "cancel_target" not in st.session_state:
        st.session_state.cancel_target = None

    # ------------------------------------------------------------
    # TOP ACTIONS
    # ------------------------------------------------------------
    action_left, action_right = st.columns([5, 1])

    with action_left:
        st.markdown(
            """
            <div style="
                padding:14px 18px;
                border:1px solid rgba(96,165,250,.18);
                border-radius:16px;
                background:rgba(15,23,42,.55);
                color:#94a3b8;
                font-size:13px;
            ">
                🎯 <b style="color:#e2e8f0;">Everything in one place.</b>
                Track booking status, payment method, amount and cancellation
                details from one unified dashboard.
            </div>
            """,
            unsafe_allow_html=True
        )

    with action_right:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
            key="refresh_unified_bookings_step6"
        ):
            st.session_state.selected_booking = None
            st.session_state.cancel_target = None
            st.rerun()

    # ------------------------------------------------------------
    # UNIFIED BOOKING COLLECTION
    # ------------------------------------------------------------
    unified_bookings = []
    booking_errors = []

    def add_booking(
        response,
        service,
        icon,
        title_builder,
        subtitle_builder,
        details_builder,
        amount_key,
        status_key,
        payment_key,
    ):
        if response is None:
            booking_errors.append(service)
            return

        if response.status_code != 200:
            booking_errors.append(service)
            return

        data = get_json(response)

        if not isinstance(data, list):
            return

        for item in data:
            try:
                amount = float(item.get(amount_key, 0) or 0)
            except (TypeError, ValueError):
                amount = 0.0

            status = str(
                item.get(status_key, "unknown") or "unknown"
            ).strip().lower()

            payment = str(
                item.get(payment_key, "demo") or "demo"
            ).strip().lower()

            booking_id = item.get("id", "-")

            try:
                numeric_id = int(booking_id)
            except (TypeError, ValueError):
                numeric_id = 0

            unified_bookings.append(
                {
                    "service": service,
                    "icon": icon,
                    "booking_id": booking_id,
                    "numeric_id": numeric_id,
                    "title": title_builder(item),
                    "subtitle": subtitle_builder(item),
                    "details": details_builder(item),
                    "amount": amount,
                    "payment": payment,
                    "status": status,
                    "raw": item,
                }
            )

    # ------------------------------------------------------------
    # BUS
    # ------------------------------------------------------------
    add_booking(
        api_get("/buses/my-bookings"),
        "Bus",
        "🚌",
        lambda x: f"Bus Booking #{x.get('id', '-')}",
        lambda x: f"Bus ID: {x.get('bus_id', '-')}",
        lambda x: [
            ("💺 Seats", x.get("seats", "-")),
            ("👤 Passenger", x.get("passenger_name", "-")),
            ("📱 Phone", x.get("passenger_phone", "-")),
        ],
        "total_price",
        "booking_status",
        "payment_method",
    )

    # ------------------------------------------------------------
    # TRAIN
    # ------------------------------------------------------------
    add_booking(
        api_get("/trains/my-bookings"),
        "Train",
        "🚆",
        lambda x: f"Train Booking #{x.get('id', '-')}",
        lambda x: f"Train ID: {x.get('train_id', '-')}",
        lambda x: [
            ("🎟️ Class", str(x.get("travel_class", "-")).upper()),
            ("💺 Seats", x.get("seats", "-")),
            ("👤 Passenger", x.get("passenger_name", "-")),
            ("📱 Phone", x.get("passenger_phone", "-")),
        ],
        "total_price",
        "booking_status",
        "payment_method",
    )

    # ------------------------------------------------------------
    # FLIGHT
    # ------------------------------------------------------------
    add_booking(
        api_get("/flights/my-bookings"),
        "Flight",
        "✈️",
        lambda x: f"Flight Booking #{x.get('id', '-')}",
        lambda x: f"Flight ID: {x.get('flight_id', '-')}",
        lambda x: [
            ("💺 Class", str(x.get("travel_class", "-")).title()),
            ("💺 Seats", x.get("seats", "-")),
            ("👤 Passenger", x.get("passenger_name", "-")),
            ("📱 Phone", x.get("passenger_phone", "-")),
        ],
        "total_price",
        "booking_status",
        "payment_method",
    )

    # ------------------------------------------------------------
    # HOTEL
    # ------------------------------------------------------------
    add_booking(
        api_get("/hotels/my-bookings"),
        "Hotel",
        "🏨",
        lambda x: f"Hotel Booking #{x.get('id', '-')}",
        lambda x: f"Hotel ID: {x.get('hotel_id', '-')}",
        lambda x: [
            ("🛏️ Rooms", x.get("rooms", "-")),
            ("🌙 Nights", x.get("nights", "-")),
            ("👤 Guest", x.get("guest_name", "-")),
            ("📱 Phone", x.get("guest_phone", "-")),
        ],
        "total_price",
        "booking_status",
        "payment_method",
    )

    # ------------------------------------------------------------
    # CAB
    # ------------------------------------------------------------
    add_booking(
        api_get("/cabs/my-bookings"),
        "Cab",
        "🚕",
        lambda x: f"{x.get('cab_type', 'Cab')} Booking #{x.get('id', '-')}",
        lambda x: (
            f"{x.get('pickup_location', '-')} → "
            f"{x.get('drop_location', '-')}"
        ),
        lambda x: [
            ("🛣️ Distance", f"{x.get('distance_km', '-')} km"),
            ("👤 Passenger", x.get("passenger_name", "-")),
            ("📱 Phone", x.get("passenger_phone", "-")),
        ],
        "total_price",
        "booking_status",
        "payment_method",
    )

    # ------------------------------------------------------------
    # FOOD
    # ------------------------------------------------------------
    add_booking(
        api_get("/food/my-orders"),
        "Food",
        "🍔",
        lambda x: f"Food Order #{x.get('id', '-')}",
        lambda x: f"Restaurant ID: {x.get('restaurant_id', '-')}",
        lambda x: [
            ("👤 Customer", x.get("customer_name", "-")),
            ("📍 Address", x.get("delivery_address", "-")),
        ],
        "total_price",
        "order_status",
        "payment_method",
    )

    # ------------------------------------------------------------
    # MOVIES
    # ------------------------------------------------------------
    add_booking(
        api_get("/movies/my-bookings"),
        "Movie",
        "🎬",
        lambda x: f"Movie Booking #{x.get('id', '-')}",
        lambda x: f"Cinema ID: {x.get('cinema_id', '-')}",
        lambda x: [
            (
                "🎟️ Tickets",
                x.get(
                    "number_of_tickets",
                    x.get("number_of_seats", "-")
                ),
            ),
            ("💺 Seats", x.get("seats", "-")),
            ("📅 Date", x.get("show_date", "-")),
            ("🕐 Time", x.get("show_time", "-")),
        ],
        "total_price",
        "booking_status",
        "payment_method",
    )

    # ------------------------------------------------------------
    # EVENTS
    # ------------------------------------------------------------
    add_booking(
        api_get("/events/my-bookings"),
        "Event",
        "🎟️",
        lambda x: f"Event Booking #{x.get('id', '-')}",
        lambda x: f"Show ID: {x.get('show_id', '-')}",
        lambda x: [
            ("🎫 Ticket Type", x.get("ticket_type", "-")),
            ("👥 Tickets", x.get("number_of_tickets", "-")),
            (
                "📱 Phone",
                x.get(
                    "customer_phone",
                    x.get("passenger_phone", "-")
                ),
            ),
        ],
        "total_price",
        "booking_status",
        "payment_method",
    )

    # ------------------------------------------------------------
    # GENERIC BOOKINGS
    # ------------------------------------------------------------
    generic_response = api_get("/bookings/my")

    if generic_response and generic_response.status_code == 200:
        generic_data = get_json(generic_response)

        if isinstance(generic_data, list):
            for item in generic_data:
                try:
                    amount = float(item.get("amount", 0) or 0)
                except (TypeError, ValueError):
                    amount = 0.0

                booking_id = item.get("id", "-")

                try:
                    numeric_id = int(booking_id)
                except (TypeError, ValueError):
                    numeric_id = 0

                unified_bookings.append(
                    {
                        "service": str(
                            item.get("booking_type", "Other")
                        ).title(),
                        "icon": "🎫",
                        "booking_id": booking_id,
                        "numeric_id": numeric_id,
                        "title": item.get(
                            "title",
                            "TRAVELX Booking"
                        ),
                        "subtitle": (
                            f"{item.get('source', '')} → "
                            f"{item.get('destination', '')}"
                        ).strip(" →"),
                        "details": [
                            (
                                "📅 Date",
                                item.get("booking_date", "-")
                            ),
                            (
                                "📝 Details",
                                item.get("details", "-")
                            ),
                        ],
                        "amount": amount,
                        "payment": str(
                            item.get(
                                "payment_method",
                                "demo"
                            ) or "demo"
                        ).strip().lower(),
                        "status": str(
                            item.get(
                                "status",
                                "unknown"
                            ) or "unknown"
                        ).strip().lower(),
                        "raw": item,
                    }
                )
    elif generic_response:
        booking_errors.append("Other")

    # ------------------------------------------------------------
    # SORT LATEST FIRST
    # ------------------------------------------------------------
    unified_bookings.sort(
        key=lambda x: x.get("numeric_id", 0),
        reverse=True
    )

    # ------------------------------------------------------------
    # SEARCH + FILTERS
    # ------------------------------------------------------------
    st.divider()

    st.subheader("🔎 Find a Booking")

    search_col, service_col, status_col, payment_col = st.columns(
        [3.2, 1.6, 1.6, 1.6]
    )

    with search_col:
        booking_search = st.text_input(
            "Search",
            placeholder=(
                "Booking ID, passenger, location, service..."
            ),
            key="step6_booking_search",
        )

    all_services = [
        "All",
        "Bus",
        "Train",
        "Flight",
        "Hotel",
        "Cab",
        "Food",
        "Movie",
        "Event",
        "Other",
    ]

    with service_col:
        selected_service = st.selectbox(
            "Service",
            all_services,
            key="step6_booking_service_filter",
        )

    with status_col:
        selected_status = st.selectbox(
            "Status",
            ["All", "Confirmed", "Pending", "Cancelled"],
            key="step6_booking_status_filter",
        )

    with payment_col:
        selected_payment_filter = st.selectbox(
            "Payment",
            ["All", "Wallet", "Demo"],
            key="step6_booking_payment_filter",
        )

    filtered_bookings = list(unified_bookings)

    search_term = booking_search.strip().lower()

    if search_term:
        def matches_search(booking):
            searchable_parts = [
                booking.get("service", ""),
                booking.get("title", ""),
                booking.get("subtitle", ""),
                str(booking.get("booking_id", "")),
                booking.get("payment", ""),
                booking.get("status", ""),
            ]

            for label, value in booking.get("details", []):
                searchable_parts.append(str(label))
                searchable_parts.append(str(value))

            searchable_text = " ".join(
                str(part).lower()
                for part in searchable_parts
            )

            return search_term in searchable_text

        filtered_bookings = [
            booking
            for booking in filtered_bookings
            if matches_search(booking)
        ]

    if selected_service != "All":
        filtered_bookings = [
            booking
            for booking in filtered_bookings
            if booking["service"] == selected_service
        ]

    if selected_status != "All":
        wanted_status = selected_status.lower()

        filtered_bookings = [
            booking
            for booking in filtered_bookings
            if (
                booking["status"] == wanted_status
                or (
                    wanted_status == "cancelled"
                    and booking["status"] == "canceled"
                )
            )
        ]

    if selected_payment_filter != "All":
        wanted_payment = selected_payment_filter.lower()

        filtered_bookings = [
            booking
            for booking in filtered_bookings
            if booking["payment"] == wanted_payment
        ]

    # ------------------------------------------------------------
    # SUMMARY METRICS
    # ------------------------------------------------------------
    total_count = len(filtered_bookings)

    confirmed_count = sum(
        1
        for booking in filtered_bookings
        if booking["status"] == "confirmed"
    )

    pending_count = sum(
        1
        for booking in filtered_bookings
        if booking["status"] == "pending"
    )

    cancelled_count = sum(
        1
        for booking in filtered_bookings
        if booking["status"] in ("cancelled", "canceled")
    )

    confirmed_spend = sum(
        booking["amount"]
        for booking in filtered_bookings
        if booking["status"] != "cancelled"
        and booking["status"] != "canceled"
    )

    total_value = sum(
        booking["amount"]
        for booking in filtered_bookings
    )

    services_used = len(
        set(
            booking["service"]
            for booking in filtered_bookings
        )
    )

    st.subheader("📊 Booking Overview")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.html(
            f"""
            <div class="metric-card">
                <div class="metric-label">Bookings</div>
                <div class="metric-value">{total_count}</div>
            </div>
            """
        )

    with m2:
        st.html(
            f"""
            <div class="metric-card">
                <div class="metric-label">Confirmed Spend</div>
                <div class="metric-value">₹{confirmed_spend:,.0f}</div>
            </div>
            """
        )

    with m3:
        st.html(
            f"""
            <div class="metric-card">
                <div class="metric-label">Active</div>
                <div class="metric-value">{confirmed_count + pending_count}</div>
            </div>
            """
        )

    with m4:
        st.html(
            f"""
            <div class="metric-card">
                <div class="metric-label">Services Used</div>
                <div class="metric-value">{services_used}</div>
            </div>
            """
        )

    # ------------------------------------------------------------
    # STATUS SUMMARY
    # ------------------------------------------------------------
    status_summary = st.columns(3)

    with status_summary[0]:
        st.success(
            f"✅ Confirmed: {confirmed_count}"
        )

    with status_summary[1]:
        st.warning(
            f"⏳ Pending: {pending_count}"
        )

    with status_summary[2]:
        st.error(
            f"❌ Cancelled: {cancelled_count}"
        )

    if total_value > 0 and cancelled_count > 0:
        st.caption(
            f"Booking value in current view: ₹{total_value:,.0f}"
        )

    # ------------------------------------------------------------
    # SERVICE BREAKDOWN
    # ------------------------------------------------------------
    if filtered_bookings:
        service_counts = {}

        service_icons = {
            "Bus": "🚌",
            "Train": "🚆",
            "Flight": "✈️",
            "Hotel": "🏨",
            "Cab": "🚕",
            "Food": "🍔",
            "Movie": "🎬",
            "Event": "🎟️",
            "Other": "🎫",
        }

        for booking in filtered_bookings:
            service = booking["service"]
            service_counts[service] = (
                service_counts.get(service, 0) + 1
            )

        st.divider()
        st.subheader("🧩 Services in This View")

        breakdown_columns = st.columns(
            min(4, max(1, len(service_counts)))
        )

        for index, (service, count) in enumerate(
            service_counts.items()
        ):
            with breakdown_columns[
                index % len(breakdown_columns)
            ]:
                st.html(
                    f"""
                    <div class="metric-card">
                        <div style="font-size:30px;">
                            {service_icons.get(service, "🎫")}
                        </div>
                        <div class="metric-label">
                            {service}
                        </div>
                        <div class="metric-value">
                            {count}
                        </div>
                    </div>
                    """
                )

    # ------------------------------------------------------------
    # CANCELLATION HELPER
    # ------------------------------------------------------------
    def cancel_booking(service, booking_id):

        endpoint_map = {
            "Bus": f"/buses/bookings/{booking_id}/cancel",
            "Train": f"/trains/bookings/{booking_id}/cancel",
            "Flight": f"/flights/bookings/{booking_id}/cancel",
            "Hotel": f"/hotels/bookings/{booking_id}/cancel",
            "Cab": f"/cabs/bookings/{booking_id}/cancel",
            "Food": f"/food/orders/{booking_id}/cancel",
            "Movie": f"/movies/bookings/{booking_id}/cancel",
            "Event": f"/events/bookings/{booking_id}/cancel",
        }

        endpoint = endpoint_map.get(service)

        if not endpoint:
            st.error(
                f"Cancellation is not available for "
                f"{service} bookings."
            )
            return False

        response = api_post(endpoint, {})

        if response is None:
            return False

        if response.status_code in [200, 201]:
            st.success(
                f"✅ {service} booking #{booking_id} "
                f"cancelled successfully."
            )
            return True

        st.error(
            get_json(response).get(
                "detail",
                "Unable to cancel booking."
            )
        )
        return False

    # ------------------------------------------------------------
    # BOOKING HISTORY
    # ------------------------------------------------------------
    st.divider()
    st.subheader("📜 Booking History")

    if booking_errors:
        st.warning(
            "Some booking services could not be loaded: "
            + ", ".join(sorted(set(booking_errors)))
        )

    if not filtered_bookings:

        if unified_bookings:
            st.info(
                "🔍 No bookings match your current search or filters."
            )
        else:
            st.html(
                """
                <div style="
                    padding:55px 25px;
                    text-align:center;
                    border:1px solid rgba(148,163,184,.18);
                    border-radius:22px;
                    background:rgba(15,23,42,.45);
                ">
                    <div style="font-size:58px;">🎫</div>
                    <div style="
                        font-size:25px;
                        font-weight:900;
                        margin-top:10px;
                    ">
                        No Bookings Yet
                    </div>
                    <div style="
                        opacity:.65;
                        margin-top:8px;
                    ">
                        Your buses, trains, flights, hotels, cabs,
                        food, movies and event bookings will appear here.
                    </div>
                </div>
                """
            )

    else:

        for booking in filtered_bookings:

            status = booking["status"]
            service = booking["service"]
            amount = booking["amount"]
            payment = booking["payment"]

            is_cancelled = status in (
                "cancelled",
                "canceled",
            )

            is_confirmed = status == "confirmed"
            is_pending = status == "pending"

            if is_confirmed:
                status_label = "✅ Confirmed"
            elif is_pending:
                status_label = "⏳ Pending"
            elif is_cancelled:
                status_label = "❌ Cancelled"
            else:
                status_label = f"ℹ️ {status.title()}"

            with st.container(border=True):

                top_left, top_mid, top_right = st.columns(
                    [4.8, 1.5, 1.5]
                )

                with top_left:
                    st.markdown(
                        f"### {booking['icon']} {booking['title']}"
                    )

                    st.caption(
                        f"{service}  •  "
                        f"Booking #{booking['booking_id']}"
                    )

                    st.write(
                        f"📍 {booking['subtitle']}"
                    )

                with top_mid:
                    if is_confirmed:
                        st.success(status_label)
                    elif is_cancelled:
                        st.error(status_label)
                    elif is_pending:
                        st.warning(status_label)
                    else:
                        st.info(status_label)

                with top_right:
                    st.markdown(
                        f"""
                        <div style="
                            text-align:right;
                            padding-top:5px;
                        ">
                            <div style="
                                font-size:11px;
                                opacity:.60;
                                font-weight:800;
                                letter-spacing:.8px;
                            ">
                                TOTAL
                            </div>
                            <div style="
                                font-size:27px;
                                font-weight:900;
                            ">
                                ₹{amount:,.0f}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.divider()

                details = booking.get("details", [])

                if details:
                    detail_count = min(
                        4,
                        len(details)
                    )

                    detail_columns = st.columns(
                        detail_count
                    )

                    for index, (label, value) in enumerate(
                        details[:4]
                    ):
                        with detail_columns[
                            index % detail_count
                        ]:
                            st.caption(label)
                            st.markdown(
                                f"**{str(value)}**"
                            )

                st.divider()

                payment_left, payment_mid, action_area = st.columns(
                    [2.4, 3.2, 2]
                )

                with payment_left:

                    payment_icon = (
                        "💰"
                        if payment == "wallet"
                        else "🧪"
                    )

                    payment_label = (
                        "TRAVELX Wallet"
                        if payment == "wallet"
                        else "Demo Payment"
                    )

                    st.caption(
                        f"{payment_icon} Payment Method"
                    )

                    st.write(payment_label)

                with payment_mid:

                    if is_cancelled:

                        if payment == "wallet":
                            st.success(
                                f"💰 ₹{amount:,.0f} "
                                "refunded to TRAVELX Wallet"
                            )
                        else:
                            st.info(
                                "🧪 Demo payment — "
                                "no wallet refund was required."
                            )

                    elif is_confirmed:
                        st.caption("🛡️ Booking Protection")
                        st.write(
                            "Cancellation available"
                        )

                    elif is_pending:
                        st.caption("⏳ Booking Status")
                        st.write(
                            "Waiting for confirmation"
                        )

                    else:
                        st.caption("TRAVELX")
                        st.write(
                            status.title()
                        )

                with action_area:

                    view_key = (
                        "step6_view_booking_"
                        f"{service.lower()}_"
                        f"{booking['booking_id']}"
                    )

                    if st.button(
                        "🎫 View Details",
                        use_container_width=True,
                        key=view_key,
                    ):
                        st.session_state.selected_booking = booking
                        st.rerun()

                    if is_confirmed:

                        cancel_key = (
                            "step6_cancel_booking_"
                            f"{service.lower()}_"
                            f"{booking['booking_id']}"
                        )

                        if st.button(
                            "❌ Cancel",
                            use_container_width=True,
                            key=cancel_key,
                        ):
                            st.session_state.cancel_target = {
                                "service": service,
                                "booking_id": booking["booking_id"],
                                "amount": amount,
                                "payment": payment,
                                "title": booking["title"],
                            }
                            st.rerun()

                    elif is_cancelled:
                        st.caption("Cancellation completed")

    # ------------------------------------------------------------
    # DIGITAL TICKET / DETAILS
    # ------------------------------------------------------------
    selected_booking = st.session_state.get(
        "selected_booking"
    )

    if selected_booking:

        st.divider()
        st.subheader("🎫 Booking Details")

        selected_status = str(
            selected_booking.get(
                "status",
                "unknown"
            )
        ).lower()

        selected_service = selected_booking.get(
            "service",
            "TRAVELX"
        )

        selected_payment = str(
            selected_booking.get(
                "payment",
                "demo"
            )
        ).lower()

        try:
            selected_amount = float(
                selected_booking.get(
                    "amount",
                    0
                ) or 0
            )
        except (TypeError, ValueError):
            selected_amount = 0.0

        ticket_left, ticket_right = st.columns(
            [2.5, 1]
        )

        with ticket_left:

            st.html(
                f"""
                <div style="
                    padding:28px;
                    border-radius:22px;
                    border:1px solid rgba(96,165,250,.22);
                    background:
                        radial-gradient(
                            circle at 90% 10%,
                            rgba(59,130,246,.18),
                            transparent 28%
                        ),
                        linear-gradient(
                            145deg,
                            rgba(30,41,59,.90),
                            rgba(15,23,42,.96)
                        );
                ">

                    <div style="
                        font-size:12px;
                        opacity:.60;
                        font-weight:800;
                        letter-spacing:1.4px;
                    ">
                        TRAVELX DIGITAL TICKET
                    </div>

                    <div style="
                        font-size:29px;
                        font-weight:900;
                        margin-top:10px;
                    ">
                        {selected_booking.get("icon", "🎫")}
                        {selected_booking.get(
                            "title",
                            "TRAVELX Booking"
                        )}
                    </div>

                    <div style="
                        opacity:.68;
                        margin-top:7px;
                        font-size:14px;
                    ">
                        {selected_service}
                        • Booking #
                        {selected_booking.get(
                            "booking_id",
                            "-"
                        )}
                    </div>

                    <hr style="
                        border:0;
                        border-top:
                            1px solid
                            rgba(148,163,184,.18);
                        margin:22px 0;
                    ">

                    <div style="
                        font-size:12px;
                        opacity:.60;
                        font-weight:800;
                        letter-spacing:.8px;
                    ">
                        JOURNEY / ORDER
                    </div>

                    <div style="
                        font-size:20px;
                        font-weight:800;
                        margin-top:7px;
                    ">
                        {selected_booking.get(
                            "subtitle",
                            "TRAVELX"
                        )}
                    </div>

                </div>
                """
            )

            details = selected_booking.get(
                "details",
                []
            )

            if details:
                st.write("")

                detail_columns = st.columns(
                    min(4, len(details))
                )

                for index, (label, value) in enumerate(
                    details[:4]
                ):
                    with detail_columns[
                        index % len(detail_columns)
                    ]:
                        st.caption(label)
                        st.write(str(value))

        with ticket_right:

            st.markdown("### 💳 Payment")

            st.metric(
                "Amount",
                f"₹{selected_amount:,.0f}"
            )

            st.caption(
                "Method: "
                + (
                    "TRAVELX WALLET"
                    if selected_payment == "wallet"
                    else "DEMO PAYMENT"
                )
            )

            if selected_status == "confirmed":
                st.success("✅ Booking Confirmed")

            elif selected_status in (
                "cancelled",
                "canceled",
            ):
                st.error("❌ Booking Cancelled")

                if selected_payment == "wallet":
                    st.success(
                        f"₹{selected_amount:,.0f} "
                        "refunded to Wallet"
                    )

            elif selected_status == "pending":
                st.warning("⏳ Booking Pending")

            close_ticket_key = (
                "step6_close_ticket_"
                f"{str(selected_service).lower()}_"
                f"{str(selected_booking.get('booking_id', '-'))}"
            )

            if st.button(
                "✖️ Close Details",
                use_container_width=True,
                key=close_ticket_key,
            ):
                st.session_state.selected_booking = None
                st.rerun()

    # ------------------------------------------------------------
    # CANCELLATION CONFIRMATION
    # ------------------------------------------------------------
    cancel_target = st.session_state.get(
        "cancel_target"
    )

    if cancel_target:

        st.divider()
        st.subheader("⚠️ Confirm Cancellation")

        st.warning(
            "Please confirm that you want to cancel this booking."
        )

        confirm_left, confirm_right = st.columns(2)

        with confirm_left:
            st.markdown(
                f"""
                **Service:** {cancel_target["service"]}

                **Booking:** {cancel_target["title"]}

                **Booking ID:** #{cancel_target["booking_id"]}

                **Amount:** ₹{cancel_target["amount"]:,.0f}

                **Payment:** {
                    "TRAVELX WALLET"
                    if str(cancel_target["payment"]).lower() == "wallet"
                    else "DEMO PAYMENT"
                }
                """
            )

        with confirm_right:

            if (
                str(
                    cancel_target["payment"]
                ).lower()
                == "wallet"
            ):
                st.info(
                    f"💰 ₹{cancel_target['amount']:,.0f} "
                    "will be refunded to your TRAVELX Wallet."
                )
            else:
                st.info(
                    "🧪 This booking used Demo Payment. "
                    "No wallet refund will be created."
                )

        confirm_button, keep_button = st.columns(2)

        with confirm_button:

            if st.button(
                "✅ Yes, Cancel Booking",
                type="primary",
                use_container_width=True,
                key="step6_confirm_cancel_booking",
            ):

                service = cancel_target["service"]
                booking_id = cancel_target["booking_id"]

                if cancel_booking(
                    service,
                    booking_id
                ):
                    st.session_state.cancel_target = None
                    st.session_state.selected_booking = None
                    st.rerun()

        with keep_button:

            if st.button(
                "↩️ Keep Booking",
                use_container_width=True,
                key="step6_keep_booking",
            ):
                st.session_state.cancel_target = None
                st.rerun()
# ============================================================
# PROFILE
# ============================================================

elif st.session_state.page == "Profile":

    st.title("👤 My Profile")

    st.caption(
        "Manage your TRAVELX account and view your activity overview."
    )

    st.divider()

    # --------------------------------------------------------
    # LOAD PROFILE
    # --------------------------------------------------------

    response = api_get("/auth/profile")

    if response and response.status_code == 200:

        profile = get_json(response)

    # Backend returns profile data inside the "user" object
        profile_user = profile.get("user", profile)

        name = profile_user.get("name", "User")
        email = profile_user.get("email", "")
        phone = profile_user.get("phone", "")
        user_id = profile_user.get("id", "")
        # ----------------------------------------------------
        # PROFILE HERO
        # ----------------------------------------------------

        st.html(f"""
        <div style="
            padding:30px;
            border-radius:24px;
            background:
                radial-gradient(circle at 90% 20%, rgba(96,165,250,.28), transparent 25%),
                linear-gradient(135deg,#111827,#172554,#1d4ed8);
            border:1px solid rgba(147,197,253,.20);
            box-shadow:0 18px 45px rgba(0,0,0,.25);
            margin-bottom:25px;
        ">
            <div style="font-size:52px; margin-bottom:8px;">👋</div>
            <div style="font-size:32px; font-weight:900; color:white;">
                Hello, {name}!
            </div>
            <div style="font-size:15px; color:#dbeafe; margin-top:8px;">
                Welcome to your TRAVELX account dashboard.
            </div>
        </div>
        """)

        # ----------------------------------------------------
        # ACCOUNT INFORMATION
        # ----------------------------------------------------

        st.subheader("🪪 Account Information")

        col1, col2 = st.columns(2)

        with col1:
            st.text_input(
                "Full Name",
                value=name,
                disabled=True,
                key="profile_name"
            )

            st.text_input(
                "Email Address",
                value=email,
                disabled=True,
                key="profile_email"
            )

        with col2:
            st.text_input(
                "Phone Number",
                value=phone,
                disabled=True,
                key="profile_phone"
            )

            st.text_input(
                "TRAVELX User ID",
                value=str(user_id),
                disabled=True,
                key="profile_id"
            )

        st.divider()

        # ----------------------------------------------------
        # LIVE ACCOUNT STATS
        # ----------------------------------------------------

        st.subheader("📊 Account Activity")

        endpoints = {
            "Bus": "/buses/my-bookings",
            "Train": "/trains/my-bookings",
            "Flight": "/flights/my-bookings",
            "Hotel": "/hotels/my-bookings",
            "Cab": "/cabs/my-bookings",
            "Food": "/food/my-orders",
            "Movie": "/movies/my-bookings",
            "Event": "/events/my-bookings",
            "Other": "/bookings/my",
        }

        activity_counts = {}
        activity_total = 0
        activity_spent = 0.0
        activity_confirmed = 0

        for service, endpoint in endpoints.items():
            service_response = api_get(endpoint)

            if not service_response or service_response.status_code != 200:
                continue

            service_data = get_json(service_response)

            if not isinstance(service_data, list):
                continue

            count = len(service_data)

            if count:
                activity_counts[service] = count
                activity_total += count

            for item in service_data:
                amount = item.get("total_price", 0)

                try:
                    activity_spent += float(amount or 0)
                except (TypeError, ValueError):
                    pass

                status = str(
                    item.get(
                        "booking_status",
                        item.get("order_status", "")
                    )
                ).lower()

                if status == "confirmed":
                    activity_confirmed += 1

        wallet_balance = 0.0
        wallet_response = api_get("/wallet/")

        if wallet_response and wallet_response.status_code == 200:
            wallet_data = get_json(wallet_response)
            try:
                wallet_balance = float(wallet_data.get("balance", 0) or 0)
            except (TypeError, ValueError):
                wallet_balance = 0.0

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:
            st.html(f"""
            <div class="metric-card">
                <div class="metric-label">Wallet Balance</div>
                <div class="metric-value">₹{wallet_balance:,.2f}</div>
            </div>
            """)

        with metric2:
            st.html(f"""
            <div class="metric-card">
                <div class="metric-label">Total Bookings</div>
                <div class="metric-value">{activity_total}</div>
            </div>
            """)

        with metric3:
            st.html(f"""
            <div class="metric-card">
                <div class="metric-label">Total Spent</div>
                <div class="metric-value">₹{activity_spent:,.0f}</div>
            </div>
            """)

        with metric4:
            st.html(f"""
            <div class="metric-card">
                <div class="metric-label">Confirmed</div>
                <div class="metric-value">{activity_confirmed}</div>
            </div>
            """)

        # ----------------------------------------------------
        # SERVICE ACTIVITY
        # ----------------------------------------------------

        if activity_counts:
            st.divider()
            st.subheader("🧩 Services Used")

            service_items = list(activity_counts.items())

            for row in range(0, len(service_items), 4):
                columns = st.columns(4)

                for index, column in enumerate(columns):
                    item_index = row + index

                    if item_index >= len(service_items):
                        continue

                    service, count = service_items[item_index]

                    icons = {
                        "Bus": "🚌",
                        "Train": "🚆",
                        "Flight": "✈️",
                        "Hotel": "🏨",
                        "Cab": "🚕",
                        "Food": "🍔",
                        "Movie": "🎬",
                        "Event": "🎟️",
                        "Other": "📦",
                    }

                    with column:
                        st.html(f"""
                        <div class="metric-card">
                            <div style="font-size:28px;">{icons.get(service, '📦')}</div>
                            <div class="metric-label">{service}</div>
                            <div class="metric-value">{count}</div>
                        </div>
                        """)

        st.divider()

        # ----------------------------------------------------
        # ACCOUNT STATUS
        # ----------------------------------------------------

        st.subheader("🔐 Account Status")

        st.success("Your TRAVELX account is active and authenticated. ✅")

        st.caption(
            "Your profile information is currently displayed from the TRAVELX backend. "
            "Profile editing can be added when the account-update API is enabled."
        )

        # ----------------------------------------------------
        # QUICK ACTIONS
        # ----------------------------------------------------

        st.subheader("⚡ Quick Actions")

        action1, action2, action3 = st.columns(3)

        with action1:
            if st.button(
                "📋 My Bookings",
                use_container_width=True,
                key="profile_bookings"
            ):
                st.session_state.page = "My Bookings"
                st.rerun()

        with action2:
            if st.button(
                "💰 Open Wallet",
                use_container_width=True,
                key="profile_wallet"
            ):
                st.session_state.page = "Wallet"
                st.rerun()

        with action3:
            if st.button(
                "🏠 Dashboard",
                use_container_width=True,
                key="profile_home"
            ):
                st.session_state.page = "Home"
                st.rerun()

        st.divider()

        if st.button(
            "🚪 Logout",
            type="secondary",
            use_container_width=True,
            key="profile_logout"
        ):
            logout_user()

    elif response:
        st.error(
            get_json(response).get(
                "detail",
                "Unable to load profile."
            )
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
