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

        st.error(f"Backend connection error: {e}")

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

        st.error(f"Backend connection error: {e}")

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

    st.session_state.wallet_selected_amount = 0.0

    st.rerun()


# ============================================================
# LOGIN / REGISTER
# ============================================================

if not st.session_state.token:

    # --------------------------------------------------------
    # LOGIN HERO
    # --------------------------------------------------------

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
                Bus Bookings
            </div>

            <div class="metric-value">
                {bus_booking_count}
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
# BUSES
# ============================================================

elif st.session_state.page == "Buses":

    st.title("🚌 Bus Booking")

    st.caption(
        "Search available buses and reserve your seats."
    )

    st.divider()

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

            else:

                response = api_post(
                    "/buses/book",
                    {
                        "bus_id": bus["id"],
                        "passenger_name": passenger_name,
                        "passenger_phone": passenger_phone,
                        "seats": seats
                    }
                )

                if response:

                    if response.status_code in [
                        200,
                        201
                    ]:

                        booking = response.json()

                        st.success(
                            f"Booking confirmed! "
                            f"Booking ID: "
                            f"#{booking['id']}"
                        )

                        st.session_state.selected_bus = None

                        st.session_state.page = (
                            "My Bookings"
                        )

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
# WALLET
# ============================================================

elif st.session_state.page == "Wallet":

    st.title("💰 TRAVELX Wallet")

    st.caption(
        "Manage your TRAVELX balance and transaction history."
    )

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


    # --------------------------------------------------------
    # BUS BOOKINGS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # OTHER BOOKINGS
    # --------------------------------------------------------

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

    st.title("🚆 Trains")

    st.caption(
        "Plan and manage your railway journey."
    )

    st.info(
        "Train booking module is coming next. 🚀"
    )

    st.write(
        "TRAVELX will support train search, "
        "availability and booking."
    )


# ============================================================
# HOTELS
# ============================================================

elif st.session_state.page == "Hotels":

    st.title("🏨 Hotels")

    st.caption(
        "Find comfortable stays for your journey."
    )

    st.info(
        "Hotel booking module is coming next. 🚀"
    )

    st.write(
        "TRAVELX will support hotel search, "
        "rooms, pricing and booking."
    )


# ============================================================
# CABS
# ============================================================

elif st.session_state.page == "Cabs":

    st.title("🚕 Cabs")

    st.caption(
        "Book local and outstation rides."
    )

    st.info(
        "Cab booking module is coming next. 🚀"
    )

    st.write(
        "TRAVELX will support local, airport "
        "and outstation cab booking."
    )


# ============================================================
# FOOD
# ============================================================

elif st.session_state.page == "Food":

    st.title("🍔 Food")

    st.caption(
        "Discover restaurants and order food."
    )

    st.info(
        "Food ordering module is coming next. 🚀"
    )

    st.write(
        "TRAVELX will support restaurant discovery, "
        "menus, ordering and delivery."
    )


# ============================================================
# MOVIES
# ============================================================

elif st.session_state.page == "Movies":

    st.title("🎬 Movies")

    st.caption(
        "Discover movies and book tickets."
    )

    st.info(
        "Movie ticket booking module is coming next. 🚀"
    )

    st.write(
        "TRAVELX will support movie discovery, "
        "theatres, shows and ticket booking."
    )


# ============================================================
# EVENTS
# ============================================================

elif st.session_state.page == "Events":

    st.title("🎟️ Events")

    st.caption(
        "Discover concerts, shows and local events."
    )

    st.info(
        "Events module is coming next. 🚀"
    )

    st.write(
        "TRAVELX will support event discovery "
        "and ticket booking."
    )


# ============================================================
# AI TRIP PLANNER
# ============================================================

elif st.session_state.page == "AI Trip Planner":

    st.title("🤖 AI Trip Planner")

    st.caption(
        "Build a personalized travel plan based on your destination, duration and budget."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        destination = st.text_input(
            "📍 Destination",
            placeholder="Example: Goa",
            key="trip_destination"
        )

        days = st.number_input(
            "📅 Number of Days",
            min_value=1,
            max_value=30,
            value=3,
            key="trip_days"
        )

    with col2:

        budget = st.number_input(
            "💰 Budget",
            min_value=1000,
            value=10000,
            step=1000,
            key="trip_budget"
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

    if st.button(
        "✨ Generate My Trip Plan",
        type="primary",
        use_container_width=True
    ):

        if not destination:

            st.warning(
                "Please enter a destination."
            )

        else:

            st.success(
                "Your trip request has been prepared! 🚀"
            )

            st.markdown(
                "### 🧳 Trip Summary"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Destination",
                    destination
                )

            with col2:

                st.metric(
                    "Duration",
                    f"{days} Days"
                )

            with col3:

                st.metric(
                    "Budget",
                    f"₹{budget:,}"
                )

            with col4:

                st.metric(
                    "Style",
                    travel_style
                )

            st.info(
                "The AI travel-planning backend will be connected here next."
            )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">

    ✈️ <b>TRAVELX</b>
    • Travel Smarter
    • Explore More
    • 2026

</div>
""")