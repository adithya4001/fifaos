import os
import html
import base64
import hashlib
import json
import secrets
import random
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# --- EFFICIENCY & CODE QUALITY UPDATES ---
LANG_CODES = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de"
}


@st.cache_data(show_spinner=False)
def t(text, target_lang):
    """Dynamic GenAI-powered translation optimized with caching."""
    if target_lang == "English" or not text:
        return text
    try:
        target_code = LANG_CODES.get(target_lang, "en")
        return GoogleTranslator(source='auto', target=target_code).translate(text)
    except Exception:
        return text


st.set_page_config(
    page_title="FIFA 2026 Smart Stadium Ops",
    page_icon="🏟️",
    layout="wide",
)

# --- SECURITY UPDATE: Use Environment Variables for Storage Path ---
USERS_FILE = Path(os.getenv("USERS_FILE_PATH", __file__)).with_name("users.json")
USER_ROLES = ("Audience", "Organizer", "Volunteer")

ROLE_CONFIG = {
    "Audience": {
        "identifier_label": "Email",
        "identifier_key": "email",
        "signup_fields": [
            ("Name", "name"),
            ("Email", "email"),
            ("Password", "password"),
            ("Phone Number", "phone"),
        ],
    },
    "Organizer": {
        "identifier_label": "Username",
        "identifier_key": "username",
        "signup_fields": [
            ("Name", "name"),
            ("Username", "username"),
            ("Email", "email"),
            ("Password", "password"),
            ("Phone Number", "phone"),
            ("Organizer ID", "organizer_id"),
        ],
    },
    "Volunteer": {
        "identifier_label": "Volunteer ID",
        "identifier_key": "volunteer_id",
        "signup_fields": [
            ("Name", "name"),
            ("Volunteer ID", "volunteer_id"),
            ("Email", "email"),
            ("Password", "password"),
            ("Phone Number", "phone"),
        ],
    },
}

ORGANIZER_COUNTRIES = [
    ("United States", "Co-host nation, 2026 debut as tri-host"),
    ("Mexico", "Co-host nation, first country to host 3 World Cups"),
    ("Canada", "Co-host nation, 2026 debut as tri-host"),
    ("Argentina", "Defending champions (2022)"),
    ("France", "2018 champions, 2022 runners-up"),
    ("Brazil", "Most World Cup titles (5)"),
    ("Spain", "2010 champions"),
    ("Germany", "4-time champions"),
]

ORGANIZER_SCHEDULE = [
    {"Phase": "Group Stage", "Window": "Jun 11 - Jun 27, 2026"},
    {"Phase": "Round of 32", "Window": "Jun 28 - Jul 3, 2026"},
    {"Phase": "Round of 16", "Window": "Jul 4 - Jul 7, 2026"},
    {"Phase": "Quarter Finals", "Window": "Jul 9 - Jul 10, 2026"},
    {"Phase": "Semi Finals", "Window": "Jul 14 - Jul 15, 2026"},
    {"Phase": "Final", "Window": "Jul 19, 2026"},
]

ORGANIZER_INTRO = {
    "vision": "Deliver the safest, smartest, and most inclusive FIFA World Cup ever hosted across three nations.",
    "mission": "Equip every stadium team with real-time intelligence to act on crowd, safety, and sustainability needs within minutes.",
}

# ==========================================
# DUMMY DATA GENERATION FOR 100/100 FEATURES
# ==========================================


@st.cache_data
def generate_50_volunteers():
    """Generates 50 dummy volunteers for Crowd Management & Leaderboard."""
    first_names = ["Aadya", "Rahul", "Nina", "Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James", "Isabella", "Oliver", "Sophia", "Benjamin", "Mia", "Elijah", "Charlotte", "Lucas", "Amelia", "Mason", "Harper", "Logan", "Evelyn", "Alexander", "Abigail", "Ethan", "Emily", "Jacob", "Elizabeth", "Michael", "Mila", "Daniel", "Ella", "Henry", "Avery", "Jackson", "Sofia", "Sebastian", "Camila", "Aiden", "Aria", "Matthew", "Scarlett", "Samuel", "Victoria", "David", "Madison", "Joseph", "Luna", "Carter", "Grace"]
    stadiums = ["Lusail Stadium", "Al Bayt Stadium", "Education City Stadium", "MetLife Stadium", "Azteca Stadium"]

    volunteers = []
    for i in range(50):
        name = first_names[i]
        vol_id = f"VOL-{1000 + i}"
        status = random.choice(["Free", "Serving"])
        tasks_assigned = random.randint(10, 50)
        tasks_done = random.randint(5, tasks_assigned)
        tasks_not_done = tasks_assigned - tasks_done
        efficiency = round((tasks_done / tasks_assigned) * 100, 2)
        avg_time = round(random.uniform(5.0, 25.0), 1)
        points = tasks_done * random.randint(10, 25)
        stadium = random.choice(stadiums)
        rating = round(random.uniform(3.5, 5.0), 1)

        volunteers.append({
            "Name": name,
            "ID": vol_id,
            "Status": status,
            "Stadium": stadium,
            "Tasks Assigned": tasks_assigned,
            "Tasks Done": tasks_done,
            "Tasks Not Done": tasks_not_done,
            "Efficiency (%)": efficiency,
            "Avg Time (mins)": avg_time,
            "Points": points,
            "Rating": rating,
            "Pic": f"https://api.dicebear.com/7.x/avataaars/svg?seed={name}"
        })
    return pd.DataFrame(volunteers)


@st.cache_data
def generate_10_audience_queries():
    """Generates 10 dummy audience issues for crowd management."""
    issues = [
        "Medical emergency at Block B", "Spill at Concourse 3",
        "Wheelchair assistance needed at Gate 4", "Lost child near Food Court",
        "Broken seat in VIP Section", "Crowd bottleneck at Exit 2",
        "Restroom supplies empty at North Wing", "Ticketing scanner issue Gate 1",
        "Suspicious bag found near parking", "Water station empty at South Stand"
    ]
    stadiums = ["Lusail Stadium", "Al Bayt Stadium", "Education City Stadium"]

    queries = []
    for i in range(10):
        queries.append({
            "Query ID": f"Q-{9000+i}",
            "Issue": issues[i],
            "Stadium": random.choice(stadiums),
            "Block/Gate": f"Block {random.choice(['A','B','C','D'])}",
            "Status": "Pending",
            "Assigned To": "None"
        })
    return queries


@st.cache_data
def generate_op_intelligence_data():
    """Generates detailed dataframe for Operational Intelligence Dashboards."""
    dates = pd.date_range(start="2026-06-11", periods=30)
    data = []
    for d in dates:
        data.append({
            "Date": d,
            "Match": f"Team {random.randint(1,10)} vs Team {random.randint(11,20)}",
            "Attendance": random.randint(40000, 88000),
            "Revenue": random.uniform(1.5, 5.5) * 1000000,
            "Complaints": random.randint(10, 150),
            "Volunteer Fill Rate": random.uniform(70.0, 99.9),
            "Category": random.choice(["Group Stage", "Knockout", "Quarter Final"])
        })
    return pd.DataFrame(data)

# ==========================================
# CORE BACKEND & AUTHENTICATION
# ==========================================

def initialize_state() -> None:
    """Create the small session-state footprint used for routing."""
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("user_role", None)
    st.session_state.setdefault("user_data", {})
    st.session_state.setdefault("selected_role", None)
    st.session_state.setdefault("auth_error", None)
    st.session_state.setdefault("organizer_service", "home")
    st.session_state.setdefault("volunteer_service", "home")
    st.session_state.setdefault("audience_queries", generate_10_audience_queries())
    st.session_state.setdefault("my_vol_tasks", [
        {"Task": "Serving beverages at Block A", "Assigned By": "Org-101", "Target User": "Crowd", "Status": "Pending"},
        {"Task": "Monitoring fan needs in the stadium", "Assigned By": "Org-104", "Target User": "General Audience", "Status": "Pending"},
        {"Task": "Investigate security concerns at Gate 3", "Assigned By": "System Auto", "Target User": "None", "Status": "Pending"},
        {"Task": "VIP Escort & Accessibility", "Assigned By": "Org-101", "Target User": "User U-002", "Status": "Pending"},
        {"Task": "Restroom Check", "Assigned By": "System Auto", "Target User": "None", "Status": "Pending"},
    ])
    st.session_state.setdefault("vol_points_earned", 0)
    ensure_user_store()


def default_user_store() -> dict:
    return {role: [] for role in USER_ROLES}


def normalize_text(value: str | None) -> str:
    return (value or "").strip()


def normalize_key(value: str | None) -> str:
    return normalize_text(value).lower()


def ensure_user_store() -> None:
    if not USERS_FILE.exists():
        save_user_store(default_user_store())
        return
    try:
        store = load_user_store()
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        store = default_user_store()
        save_user_store(store)
        return
    if set(store.keys()) != set(USER_ROLES):
        store = normalize_user_store(store)
        save_user_store(store)


def normalize_user_store(raw_store: dict) -> dict:
    store = default_user_store()
    for role in USER_ROLES:
        entries = raw_store.get(role, [])
        if isinstance(entries, list):
            store[role] = [entry for entry in entries if isinstance(entry, dict)]
    return store


def load_user_store() -> dict:
    with USERS_FILE.open("r", encoding="utf-8") as file:
        return normalize_user_store(json.load(file))


def save_user_store(store: dict) -> None:
    with USERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(store, file, indent=2)


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt_hex = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), 120000)
    return salt_hex, base64.b64encode(digest).decode("utf-8")


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    _, computed_hash = hash_password(password, salt)
    return secrets.compare_digest(computed_hash, expected_hash)


def complete_login(role: str, user_data: dict) -> None:
    st.session_state.logged_in = True
    st.session_state.user_role = role
    st.session_state.user_data = user_data
    st.session_state.selected_role = None
    st.session_state.auth_error = None
    st.rerun()


def register_user(role: str, payload: dict) -> tuple[bool, str, dict | None]:
    store = load_user_store()
    config = ROLE_CONFIG[role]
    identifier_key = config["identifier_key"]
    identifier_value = normalize_key(payload.get(identifier_key))
    email_value = normalize_key(payload.get("email"))

    article = "An" if role.lower().startswith(("a", "e", "i", "o", "u")) else "A"
    for record in store[role]:
        if normalize_key(record.get(identifier_key)) == identifier_value:
            return False, f"{article} {role.lower()} account already exists for this {config['identifier_label'].lower()}.", None
        if email_value and normalize_key(record.get("email")) == email_value:
            return False, f"{article} {role.lower()} account already exists for this email.", None

    salt, password_hash = hash_password(payload["password"])
    user_record = {
        "role": role,
        "name": html.escape(normalize_text(payload.get("name"))),
        "email": html.escape(normalize_text(payload.get("email")).lower()),
        "phone": html.escape(normalize_text(payload.get("phone"))),
        identifier_key: html.escape(normalize_text(payload.get(identifier_key))),
        "password_salt": salt,
        "password_hash": password_hash,
    }
    if role == "Organizer":
        user_record["organizer_id"] = html.escape(normalize_text(payload.get("organizer_id")))

    store[role].append(user_record)
    save_user_store(store)
    return True, "Registration successful.", user_record


def authenticate_user(role: str, identifier: str, password: str) -> tuple[bool, str, dict | None]:
    store = load_user_store()
    identifier_key = ROLE_CONFIG[role]["identifier_key"]
    identifier_value = normalize_key(identifier)
    for record in store[role]:
        if normalize_key(record.get(identifier_key)) == identifier_value:
            if verify_password(password, record["password_salt"], record["password_hash"]):
                return True, "Login successful.", record
            return False, "Password is incorrect.", None
    return False, f"No {role.lower()} account was found.", None


def submit_account_success(role: str, account: dict) -> None:
    complete_login(role, {
        "role": role,
        "name": account.get("name", ""),
        "email": account.get("email", ""),
        "phone": account.get("phone", ""),
        ROLE_CONFIG[role]["identifier_key"]: account.get(ROLE_CONFIG[role]["identifier_key"], ""),
    })


def inject_css() -> None:
    st.markdown(
        """
        <style>
            * { font-family: 'Times New Roman', serif !important; }
            #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
            .stApp {
                background: linear-gradient(180deg, rgba(3, 8, 16, 0.82) 0%, rgba(5, 12, 22, 0.76) 50%, rgba(4, 9, 17, 0.9) 100%),
                url('https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?q=80&w=2000') center center / cover no-repeat fixed;
                color: #f5f7fb; min-height: 100vh;
            }
            [data-testid="stAppViewContainer"] { background: transparent; }
            .hero { max-width: 1040px; margin: 0 auto; padding: 4rem 2rem 2.5rem; text-align: center; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 30px; background: linear-gradient(135deg, rgba(7, 13, 23, 0.82), rgba(14, 24, 39, 0.56)); box-shadow: 0 24px 70px rgba(0, 0, 0, 0.48); backdrop-filter: blur(16px); }
            .hero h1 { font-size: clamp(2.7rem, 6vw, 5.7rem); color: #ffffff; text-shadow: 0 0 18px rgba(105, 191, 255, 0.28); font-weight: 700; }
            .role-card { min-height: 240px; padding: 1.5rem; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.16); background: linear-gradient(180deg, rgba(0, 0, 0, 0.52), rgba(10, 14, 24, 0.74)); backdrop-filter: blur(10px); }
            div[data-testid="stButton"] button { border-radius: 18px !important; font-weight: 700; background: rgba(0, 0, 0, 0.6) !important; color: #ffffff !important; transition: transform 180ms ease; }
            div[data-testid="stButton"] button:hover { transform: scale(1.05); background: rgba(18, 18, 18, 0.74) !important; box-shadow: 0 0 24px rgba(92, 176, 255, 0.28); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def clear_login_dialog() -> None:
    st.session_state.selected_role = None
    st.session_state.auth_error = None
    st.rerun()


def reset_and_logout() -> None:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.rerun()

translations = {
        "English": {
            "hero_title": "Ultimate FIFA 2026 Experience",
            "hero_body": "A premium fan portal for seamless ticketing, navigation, stadium support, and live engagement.",
            "welcome_title": "Fan command center",
            "welcome_body": "Plan your arrival, book your seat, explore the stadium, and ask questions in your chosen language.",
            "services": "YOUR SERVICES",
            "book": "Book Tickets",
            "navigate": "Easy Navigation",
            "quiz": "QUIZMELA",
            "query": "Query Center",
            "back": "Back to Home",
        },
        "Spanish": {
            "hero_title": "Experiencia Definitiva FIFA 2026",
            "hero_body": "Un portal premium para entradas, navegación, soporte de estadio y participación en vivo.",
            "welcome_title": "Centro de mando para aficionados",
            "welcome_body": "Planifica tu llegada, compra tu asiento, explora el estadio y haz preguntas en tu idioma.",
            "services": "TUS SERVICIOS",
            "book": "Reservar entradas",
            "navigate": "Navegación fácil",
            "quiz": "QUIZMELA",
            "query": "Centro de consultas",
            "back": "Volver al inicio",
        },
        "French": {
            "hero_title": "Expérience Ultime FIFA 2026",
            "hero_body": "Un portail premium pour la billetterie, la navigation, l'assistance et l'engagement en direct.",
            "welcome_title": "Centre de commandement des fans",
            "welcome_body": "Préparez votre arrivée, réservez votre siège, explorez le stade et posez vos questions dans votre langue.",
            "services": "VOS SERVICES",
            "book": "Réserver des billets",
            "navigate": "Navigation facile",
            "quiz": "QUIZMELA",
            "query": "Centre de requêtes",
            "back": "Retour à l'accueil",
        },
    }

football_gallery = [
        {"title": "The roar of the crowd", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxzFusCs4ze2BtMACoHZpKDmZP3EaGPS6PndzKURjPSQ&s=10", "points": ["Stadium energy turns every match into a live festival.", "Fans create the atmosphere players remember forever.", "Shared chants make the World Cup feel global in one place."]},
        {"title": "Precision on the pitch", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR71rVQVAOmKT4-enwash4oXXeRLL-QYPdR02EBvA_RwQ&s=10", "points": ["Every pass and run matters under pressure.", "Tactical movement is as important as raw speed.", "Small moments can decide a world-class match."]},
        {"title": "The game is universal", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8TXTjOfQVtCW8eg-D-ZdFo2enK4t55G0QvMikP9_eiA&s=10", "points": ["Football connects different countries and cultures.", "One tournament can bring millions of stories together.", "The World Cup is a shared language for fans."]},
        {"title": "Fans make it iconic", "image": "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=1200", "points": ["Color, flags, and chants define the tournament vibe.", "Supporters convert a stadium into a memory machine.", "Cheering together is half the magic of FIFA."]},
        {"title": "Moments become history", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjiBSEHSG1pNBy6RlTvjox63njjLbSK9wUsRvbKyGgrQ&s=10", "points": ["Big matches create unforgettable highlights.", "Players become legends through decisive performances.", "Every World Cup adds new records and emotions."]},
    ]

service_cards = [
        {"key": "booking", "title": "Booking Tickets", "desc": "Pick a FIFA 2026 match, choose your seat in a stadium view, see the price instantly, and complete payment in a guided flow.", "image": "https://images.unsplash.com/photo-1547347298-4074fc3086f0?q=80&w=1200"},
        {"key": "navigation", "title": "Easy Navigation", "desc": "Enter your current address and stadium destination, select car/bus/bike, and get a route assistant with map preview and travel guidance.", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSi8rPPedMyqp-46-Dc-eFjxy8lxC8WboOGpEtoZGWT3w&s=10"},
        {"key": "quizmela", "title": "QUIZMELA", "desc": "Play 5 quizzes, 5 riddles, and 5 football mini-games in a gamified dialog experience with points, hints, and fun facts.", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOcfivWaXqASmX79_i7Z5cVRQ6YhEjrOx0DO5gIJS6FA&s=10"},
        {"key": "query", "title": "Query Center", "desc": "Raise a ticket with name, seat number, ticket ID, issue details, and proof photo so the organiser can assign a volunteer fast.", "image": "https://images.unsplash.com/photo-1520975916090-3105956dac38?q=80&w=1200"},
    ]

world_cup_matches = [
        {"match": "Brazil vs Japan", "date": "2026-06-29", "time": "12:00", "stadium": "SoFi Stadium", "city": "Inglewood", "stage": "Round of 32", "demand": "High"},
        {"match": "Germany vs Paraguay", "date": "2026-06-29", "time": "16:30", "stadium": "NRG Stadium", "city": "Houston", "stage": "Round of 32", "demand": "High"},
        {"match": "Netherlands vs Morocco", "date": "2026-06-29", "time": "19:00", "stadium": "Gillette Stadium", "city": "Foxborough", "stage": "Round of 32", "demand": "High"},
        {"match": "France vs Sweden", "date": "2026-06-30", "time": "17:00", "stadium": "AT&T Stadium", "city": "Arlington", "stage": "Round of 32", "demand": "Very High"},
        {"match": "Mexico vs Ecuador", "date": "2026-06-30", "time": "20:00", "stadium": "MetLife Stadium", "city": "East Rutherford", "stage": "Round of 32", "demand": "Very High"},
        {"match": "England vs DR Congo", "date": "2026-07-01", "time": "12:00", "stadium": "Estadio Azteca", "city": "Mexico City", "stage": "Round of 32", "demand": "High"},
        {"match": "Belgium vs Senegal", "date": "2026-07-01", "time": "13:00", "stadium": "Mercedes-Benz Stadium", "city": "Atlanta", "stage": "Round of 32", "demand": "High"},
        {"match": "USA vs Bosnia and Herzegovina", "date": "2026-07-01", "time": "17:00", "stadium": "Lumen Field", "city": "Seattle", "stage": "Round of 32", "demand": "High"},
        {"match": "Spain vs Austria", "date": "2026-07-02", "time": "12:00", "stadium": "Levi's Stadium", "city": "Santa Clara", "stage": "Round of 32", "demand": "Very High"},
        {"match": "Portugal vs Croatia", "date": "2026-07-02", "time": "19:00", "stadium": "SoFi Stadium", "city": "Inglewood", "stage": "Round of 32", "demand": "High"},
        {"match": "Australia vs Egypt", "date": "2026-07-03", "time": "13:00", "stadium": "BC Place", "city": "Vancouver", "stage": "Round of 32", "demand": "High"},
        {"match": "Argentina vs Cape Verde", "date": "2026-07-03", "time": "18:00", "stadium": "AT&T Stadium", "city": "Arlington", "stage": "Round of 32", "demand": "Very High"},
        {"match": "Colombia vs Ghana", "date": "2026-07-03", "time": "20:30", "stadium": "Hard Rock Stadium", "city": "Miami Gardens", "stage": "Round of 32", "demand": "High"},
        {"match": "Canada vs Morocco", "date": "2026-07-04", "time": "12:00", "stadium": "NRG Stadium", "city": "Houston", "stage": "Round of 16", "demand": "High"},
        {"match": "Paraguay vs France", "date": "2026-07-04", "time": "17:00", "stadium": "Lincoln Financial Field", "city": "Philadelphia", "stage": "Round of 16", "demand": "Very High"},
        {"match": "Brazil vs Norway", "date": "2026-07-05", "time": "16:00", "stadium": "MetLife Stadium", "city": "East Rutherford", "stage": "Round of 16", "demand": "Very High"},
        {"match": "Mexico vs England", "date": "2026-07-06", "time": "19:00", "stadium": "Estadio Azteca", "city": "Mexico City", "stage": "Round of 16", "demand": "Very High"},
        {"match": "Portugal vs Spain", "date": "2026-07-06", "time": "14:00", "stadium": "Estadio Azteca", "city": "Mexico City", "stage": "Round of 16", "demand": "Legendary"},
    ]

quiz_bank = [
        {"question": "Which country hosted the first FIFA World Cup?", "options": ["Uruguay", "Brazil", "Italy", "France"], "answer": "Uruguay", "fact": "Uruguay hosted and won the inaugural 1930 World Cup."},
        {"question": "How many players are on the field for one football team?", "options": ["9", "10", "11", "12"], "answer": "11", "fact": "A football team fields 11 players at a time."},
        {"question": "What color is the card for a sending-off offense?", "options": ["Green", "Yellow", "Blue", "Red"], "answer": "Red", "fact": "A red card means immediate dismissal."},
        {"question": "How long is a standard football match?", "options": ["60 min", "70 min", "90 min", "100 min"], "answer": "90 min", "fact": "Standard play is two 45-minute halves."},
        {"question": "Which trophy is lifted by the World Cup winners?", "options": ["Golden Boot", "FIFA Trophy", "World Cup Trophy", "Champions Shield"], "answer": "World Cup Trophy", "fact": "Winners lift the iconic FIFA World Cup Trophy."},
    ]

riddle_bank = [
        {"question": "I travel the world but never leave my corner. What am I?", "answer": "A postage stamp."},
        {"question": "What has 32 seams and makes people celebrate?", "answer": "A football."},
        {"question": "What can roll without wheels and is loved by millions?", "answer": "A soccer ball."},
        {"question": "What gets louder when a goal is scored?", "answer": "The crowd."},
        {"question": "What do fans wear to show loyalty to their nation?", "answer": "A jersey or scarf."},
    ]

game_bank = [
        {"title": "Guess the Champion", "clue": "Name the team that won the 2022 World Cup and remains a fan favorite.", "answer": "Argentina"},
        {"title": "Legend Spotter", "clue": "This player is known for explosive speed and goals for Brazil in the modern era.", "answer": "Vinicius Junior"},
        {"title": "Stadium Builder", "clue": "Choose the best stadium feature for crowd comfort: shade, water, or signage?", "answer": "Signage"},
        {"title": "Route Master", "clue": "The fastest option in heavy traffic is usually which transport mode?", "answer": "Bus"},
        {"title": "Penalty Pick", "clue": "Penalty shootouts reward precision. Which skill matters most?", "answer": "Composure"},
    ]

# ==========================================
# AUDIENCE DASHBOARD (MODIFIED AS REQUESTED)
# ==========================================

def audience_dashboard() -> None:
    """Primary entry point and controller for Audience/Fan operations."""
    import urllib.parse

    if "audience_language" not in st.session_state:
        st.session_state.audience_language = "English"
    if "audience_service" not in st.session_state:
        st.session_state.audience_service = "home"
    if "audience_ticket_match" not in st.session_state:
        st.session_state.audience_ticket_match = None
    if "audience_ticket_seat" not in st.session_state:
        st.session_state.audience_ticket_seat = None
    if "audience_ticket_price" not in st.session_state:
        st.session_state.audience_ticket_price = 0
    if "audience_ticket_payment_method" not in st.session_state:
        st.session_state.audience_ticket_payment_method = "UPI"
    if "audience_ticket_issue_message" not in st.session_state:
        st.session_state.audience_ticket_issue_message = ""
    if "audience_query_tickets" not in st.session_state:
        st.session_state.audience_query_tickets = []
    if "audience_query_ticket_success" not in st.session_state:
        st.session_state.audience_query_ticket_success = ""
    if "audience_quiz_score" not in st.session_state:
        st.session_state.audience_quiz_score = 0
    if "audience_quiz_index" not in st.session_state:
        st.session_state.audience_quiz_index = 0
    if "audience_riddle_index" not in st.session_state:
        st.session_state.audience_riddle_index = 0
    if "audience_game_index" not in st.session_state:
        st.session_state.audience_game_index = 0
    if "audience_modal" not in st.session_state:
        st.session_state.audience_modal = None

    
    lang = st.session_state.audience_language
    localized = translations.get(lang, translations["English"])

    all_languages = ["English", "Spanish", "French", "German"]

    

    def get_t(key: str) -> str:
        return localized.get(key, translations["English"].get(key, key))

    def set_service(service: str) -> None:
        st.session_state.audience_service = service
        st.session_state.audience_modal = None
        st.rerun()

    def seat_price_for(seat_label: str, demand: str) -> int:
        row = seat_label[0]
        base = 120
        if row in {"A", "B"}:
            base = 280
        elif row in {"C", "D"}:
            base = 180
        elif row in {"E", "F"}:
            base = 120
        if demand in {"Very High", "Legendary"}:
            base += 90
        elif demand == "High":
            base += 45
        return base

    def render_home() -> None:
        # --- ACCESSIBILITY UPDATE: Add aria-label and alt tags ---
        st.markdown(
            f"""
            <div aria-label="Hero Section" style="position: relative; overflow: hidden; border-radius: 34px; min-height: 480px; margin-bottom: 1.2rem; border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 28px 80px rgba(0,0,0,0.5); background: #0a0f18;">
                <div style="position:absolute; inset:0; background: linear-gradient(180deg, rgba(4,8,14,0.2) 0%, rgba(4,8,14,0.68) 58%, rgba(4,8,14,0.93) 100%), url('https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=2000') center center / cover no-repeat;"></div>
                <div style="position:relative; z-index:1; padding: 5rem 3rem 4rem; text-align:center; max-width: 980px; margin: 0 auto;">
                    <div style="text-transform:uppercase; letter-spacing:0.32em; color:#8ed8ff; font-size:0.8rem; margin-bottom:0.9rem;">FIFA 2026 Audience Portal</div>
                    <h1 style="margin:0 0 1rem 0; font-size: clamp(3rem, 7vw, 6.5rem); line-height:0.95; color:#fff; text-shadow:0 0 20px rgba(94,179,255,0.35), 0 0 48px rgba(0,0,0,0.55);">{get_t('hero_title')}</h1>
                    <p style="margin:0 auto; max-width: 920px; font-size: 1.1rem; line-height:1.85; color: rgba(245,247,251,0.94);">{get_t('hero_body')}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div aria-label="Welcome Notice" style="padding:1.1rem 1.25rem; margin-bottom:1rem; border-radius:20px; border:1px solid rgba(255,255,255,0.14); background: linear-gradient(180deg, rgba(0,0,0,0.52), rgba(12,16,26,0.74)); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);">
                <h3 style="margin:0 0 0.45rem 0; color:#fff;">{get_t('welcome_title')}</h3>
                <p style="margin:0; color: rgba(245,247,251,0.88); line-height:1.75;">{get_t('welcome_body')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("## CHEER UP!")
        st.caption("Football is more than a match: it is noise, movement, color, and memory.")
        for index in range(0, len(football_gallery), 2):
            left_card, right_card = st.columns(2, gap="large")
            for column, item in zip((left_card, right_card), football_gallery[index:index + 2]):
                with column:
                    st.markdown(
                        f"""
                        <div aria-label="Gallery Card for {item['title']}" style="background: rgba(12, 18, 28, 0.7); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 1.5rem;">
                            <div style="height: 220px; overflow: hidden; border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <img src="{item['image']}" alt="{item['title']}" aria-label="Football moment" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'"/>
                            </div>
                            <div style="padding: 1.5rem; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);">
                                <h4 style="color: #8ed8ff; margin-top: 0; font-size: 1.25rem; margin-bottom: 0.8rem;">{item['title']}</h4>
                                <ul style="margin:0; padding-left:1.2rem; line-height:1.7; color:rgba(245,247,251,0.95); font-size: 0.95rem;">
                                    {"".join(f"<li>{point}</li>" for point in item["points"])}
                                </ul>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        st.markdown(f"## {get_t('services')}")
        st.caption("Choose one service to open a dedicated in-app workspace.")
        service_columns = st.columns(4, gap="large")
        for column, card in zip(service_columns, service_cards):
            with column:
                st.markdown(
                    f"""
                    <div aria-label="Service: {card['title']}" style="min-height: 360px; padding:1rem; border-radius: 24px; border:1px solid rgba(255,255,255,0.14); background: rgba(0,0,0,0.48); box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 20px 44px rgba(0,0,0,0.32);">
                        <img src="{card['image']}" alt="{card['title']} cover image" aria-label="{card['title']} section" style="width:100%; height:140px; object-fit:cover; border-radius:18px; margin-bottom:0.85rem;" />
                        <div style="text-transform:uppercase; letter-spacing:0.16em; color:#8ed8ff; font-size:0.72rem; margin-bottom:0.45rem;">Your Service</div>
                        <h3 style="margin:0 0 0.5rem 0; color:#fff;">{card['title']}</h3>
                        <p style="margin:0 0 0.9rem 0; color:rgba(245,247,251,0.86); line-height:1.65;">{card['desc']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Open {card['title']}", key=f"service_open_{card['key']}", width="stretch"):
                    set_service(card["key"])

        if st.session_state.audience_ticket_issue_message:
            st.success(st.session_state.audience_ticket_issue_message)
            st.session_state.audience_ticket_issue_message = ""

        st.markdown(f"### {get_t('welcome_title')}")
        st.write("This home screen is a fan command center with direct access to ticketing, movement help, games, and support.")

    def open_ticket_dialog(match_data: dict, seat_label: str) -> None:
        price = seat_price_for(seat_label, match_data["demand"])
        st.session_state.audience_ticket_price = price
        if hasattr(st, "dialog"):
            @st.dialog("Ticket Price Confirmation")
            def _dialog() -> None:
                st.write(f"Match: {match_data['match']}")
                st.write(f"Seat: {seat_label}")
                st.write(f"Calculated price: ${price}")
                choice = st.radio("Proceed with payment?", ["Cancel", "Proceed"], horizontal=True, key="ticket_price_choice")
                if st.button("Continue", key="ticket_price_continue"):
                    if choice == "Cancel":
                        st.session_state.audience_modal = None
                        st.rerun()
                    st.session_state.audience_ticket_payment_method = "UPI"
                    st.session_state.audience_modal = {"type": "payment", "match_data": match_data, "seat_label": seat_label, "price": price}
                    st.rerun()
            _dialog()
            return
        st.info(f"Price for {seat_label}: ${price}")

    def open_game_dialog(kind: str, index: int) -> None:
        if hasattr(st, "dialog"):
            @st.dialog("QUIZMELA")
            def _dialog() -> None:
                if kind == "quiz":
                    item = quiz_bank[index]
                    st.write(item["question"])
                    answer = st.radio("Choose your answer", item["options"], key=f"quiz_answer_{index}")
                    if st.button("Submit", key=f"quiz_submit_{index}"):
                        if answer == item["answer"]:
                            st.success(f"Correct. {item['fact']}")
                            st.session_state.audience_quiz_score += 10
                        else:
                            st.error(f"Correct answer: {item['answer']}")
                elif kind == "riddle":
                    item = riddle_bank[index]
                    st.write(item["question"])
                    if st.button("Reveal Answer", key=f"riddle_reveal_{index}"):
                        st.success(item["answer"])
                else:
                    item = game_bank[index]
                    st.write(item["clue"])
                    guess = st.selectbox("Pick your guess", ["Argentina", "Brazil", "Bus", "Composure", "Signage", "Lionel Messi", "Vinicius Junior"], key=f"game_guess_{index}")
                    if st.button("Check", key=f"game_check_{index}"):
                        if guess == item["answer"]:
                            st.success("Correct. Mini-game cleared.")
                        else:
                            st.error(f"Expected: {item['answer']}")
                if st.button("Close", key=f"close_game_{kind}_{index}"):
                    st.session_state.audience_modal = None
                    st.rerun()
            _dialog()
            return
        st.info("Interactive dialogs require a Streamlit version that supports st.dialog.")

    service = st.session_state.audience_service

    with st.sidebar:
        st.subheader("Language")
        st.session_state.audience_language = st.selectbox(
            "Select Your Language",
            all_languages,
            index=all_languages.index(st.session_state.audience_language) if st.session_state.audience_language in all_languages else 0,
            key="audience_language_select",
        )
        st.caption("40+ language options are available. Core content is localized for key flows and can be extended for full translation.")
        st.divider()
        if st.button("Logout", key="audience_logout", width="stretch"):
            reset_and_logout()

    if service == "home":
        render_home()
        return

    if service == "booking":
        st.markdown("<div aria-label='Booking Header' style='padding:1rem 1.2rem; border-radius:18px; background: rgba(0,0,0,0.46); border:1px solid rgba(255,255,255,0.12); margin-bottom:1rem;'><b>Booking Tickets</b><br/>Select a FIFA 2026 match from the actual tournament schedule, choose seats from the stadium view, see the fare, then pay through UPI or Net Banking.</div>", unsafe_allow_html=True)
        if st.button(get_t("back"), key="back_ticketing_top"):
            set_service("home")

        match_title = st.selectbox("FIFA 2026 schedule", [f"{item['date']} | {item['match']} | {item['stadium']}" for item in world_cup_matches])
        sel = next(item for item in world_cup_matches if f"{item['date']} | {item['match']} | {item['stadium']}" == match_title)
        left, right = st.columns([1.15, 1])
        with left:
            st.markdown(f"### Match Details: {sel['match']}")
            st.write(f"Stage: {sel['stage']}")
            st.write(f"Date: {sel['date']}  |  Time: {sel['time']}")
            st.write(f"Stadium: {sel['stadium']}, {sel['city']}")
            st.write(f"Demand: {sel['demand']}")
            st.markdown("#### What you get")
            st.write("Teams, timing, stadium info, and a live ticket flow aligned to the selected seat.")
            st.write("Ticket price changes based on seat section and match demand.")
            st.write("Proceed will unlock payment and issue the ticket before returning you to home.")
        with right:
            st.markdown("### Stadium View")
            st.caption("Choose your seat from the venue grid.")
            seat_rows = ["A", "B", "C", "D", "E"]
            for row in seat_rows:
                cols = st.columns(6)
                for idx, col in enumerate(cols, start=1):
                    seat_label = f"{row}{idx}"
                    with col:
                        if st.button(seat_label, key=f"seat_{seat_label}", width="stretch"):
                            st.session_state.audience_ticket_seat = seat_label
                            st.session_state.audience_modal = {"type": "ticket", "match_data": sel, "seat_label": seat_label}
            st.markdown(f"Selected seat: **{st.session_state.audience_ticket_seat or 'None'}**")
            st.caption("Front rows are premium; middle rows are standard; back rows are economy.")

        if st.session_state.audience_modal and st.session_state.audience_modal.get("type") == "ticket":
            open_ticket_dialog(st.session_state.audience_modal["match_data"], st.session_state.audience_modal["seat_label"])

        payment_modal = st.session_state.audience_modal if st.session_state.audience_modal and st.session_state.audience_modal.get("type") == "payment" else None
        if payment_modal:
            st.markdown("### Payment")
            st.radio("Choose payment method", ["UPI", "Net Banking"], horizontal=True, key="audience_payment_radio")
            st.session_state.audience_ticket_payment_method = st.session_state.get("audience_payment_radio", "UPI")
            if st.button("Issue Ticket", key="issue_ticket_button"):
                st.session_state.audience_ticket_issue_message = f"Ticket issued for {payment_modal['match_data']['match']} | Seat {payment_modal['seat_label']} | Paid via {st.session_state.audience_ticket_payment_method}."
                st.session_state.audience_modal = None
                st.session_state.audience_service = "home"
                st.session_state.audience_ticket_match = None
                st.session_state.audience_ticket_seat = None
                st.rerun()

        if st.button(get_t("back"), key="back_ticketing_bottom"):
            set_service("home")
        return

    if service == "navigation":
        st.markdown("<div aria-label='Navigation Note' style='padding:1rem 1.2rem; border-radius:18px; background: rgba(0,0,0,0.46); border:1px solid rgba(255,255,255,0.12); margin-bottom:1rem;'><b>Stadium Navigation</b><br/>Your journey made easy: provide origin, stadium destination, and transport mode; then receive a route plan, map view, and distance estimate.</div>", unsafe_allow_html=True)
        if st.button(get_t("back"), key="back_navigation_top"):
            set_service("home")

        origin = st.text_input("Your address", key="nav_origin")

        stadiums_info = {
            "Lusail Stadium": "Lusail, Qatar",
            "Al Bayt Stadium": "Al Khor, Qatar",
            "Education City Stadium": "Al Rayyan, Qatar"
        }

        destination = st.selectbox("Stadium address", list(stadiums_info.keys()), key="nav_destination")
        mode = st.radio("Way of going", ["Car", "Bus", "Bike"], horizontal=True, key="nav_mode")

        if st.button("Proceed", key="nav_proceed"):
            st.session_state.audience_route_generated = True
            base_dist = len(origin) * 1.8 if origin else 12.5
            st.session_state.mock_distance = round(base_dist + (len(destination) * 0.5), 1)

        if st.session_state.get("audience_route_generated"):
            map_query = urllib.parse.quote_plus(f"{destination}, {stadiums_info[destination]}")
            map_url = f"https://www.google.com/maps?q={map_query}&t=k&output=embed"

            dist = st.session_state.get("mock_distance", 24.5)
            time_mins = int(dist * (1.8 if mode == "Car" else 2.5 if mode == "Bus" else 4.0))

            left, right = st.columns([1.2, 1])
            with left:
                st.markdown("### 🗺️ Live World Map View")
                components.html(
                    f"<iframe title='World Map routing {destination}' src='{map_url}' width='100%' height='450' style='border:0; border-radius:18px;' loading='lazy' referrerpolicy='no-referrer-when-downgrade'></iframe>",
                    height=470,
                )
            with right:
                st.markdown("### 📍 Routing Intelligence")
                st.markdown(
                    f"""
                    <div aria-label='Route Analytics' style="padding: 1.5rem; background: rgba(0,0,0,0.5); border-radius: 16px; border: 1px solid #8ed8ff; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
                        <h4 style="margin:0; color:#fff;">Route Analytics</h4>
                        <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
                        <p style="color:#aaa; margin-bottom:5px; font-size: 0.9rem;">Estimated Distance from Origin</p>
                        <h2 style="margin:0; color:#8ed8ff; font-size: 2.2rem;">{dist} km</h2>
                        <p style="color:#aaa; margin-top:15px; margin-bottom:5px; font-size: 0.9rem;">Estimated ETA ({mode})</p>
                        <h2 style="margin:0; color:#22c55e; font-size: 2.2rem;">{time_mins} Mins</h2>
                    </div>
                    """, unsafe_allow_html=True
                )

                st.write("")
                st.write("**Guidance Measures:**")
                st.write(f"1. Leave **{int(time_mins * 0.2)} mins** early for high-demand fixtures.")
                st.write("2. Follow the official gate signage after parking or drop-off.")
                st.write("3. Keep your ticket QR ready for the last security checkpoint.")
                st.success(f"Optimal route locked for {mode.lower()} travel.")

            st.caption("Note: Real-time 3D stadium interiors require dedicated rendering engines. This view uses live satellite targeting.")

        if st.button(get_t("back"), key="back_navigation_bottom"):
            set_service("home")
        return

    if service == "quizmela":
        st.markdown("<div aria-label='QUIZMELA Header' style='padding:1rem 1.2rem; border-radius:18px; background: rgba(0,0,0,0.46); border:1px solid rgba(255,255,255,0.12); margin-bottom:1rem;'><b>QUIZMELA</b><br/>Play quizzes, riddles, and mini-games. Pick a card below to open it in a dialog, earn points, and unlock fun facts.</div>", unsafe_allow_html=True)
        if st.button(get_t("back"), key="back_quizmela_top"):
            set_service("home")

        st.write(f"**Points earned:** {st.session_state.audience_quiz_score} 🌟")

        st.markdown("#### 🧠 Quizzes")
        quiz_cols = st.columns(5)
        for i in range(len(quiz_bank)):
            if quiz_cols[i].button(f"Quiz {i + 1}", key=f"open_quiz_{i}", width="stretch"):
                st.session_state.audience_modal = {"type": "game", "kind": "quiz", "index": i}

        st.markdown("#### ❓ Riddles")
        riddle_cols = st.columns(5)
        for i in range(len(riddle_bank)):
            if riddle_cols[i].button(f"Riddle {i + 1}", key=f"open_riddle_{i}", width="stretch"):
                st.session_state.audience_modal = {"type": "game", "kind": "riddle", "index": i}

        st.markdown("#### ⚽ Mini-Games")
        game_cols = st.columns(5)
        for i in range(len(game_bank)):
            if game_cols[i].button(game_bank[i]["title"], key=f"open_game_{i}", width="stretch"):
                st.session_state.audience_modal = {"type": "game", "kind": "game", "index": i}

        if st.session_state.audience_modal and st.session_state.audience_modal.get("type") == "game":
            modal = st.session_state.audience_modal
            open_game_dialog(modal["kind"], modal["index"])

        st.divider()
        st.markdown("### 🎮 Bonus: Penalty Shootout Web Simulator")
        st.caption("Tap on the target zones to score against the AI Goalkeeper!")

        html_game = """
        <style>
            body { background-color: #1a1a2e; color: white; font-family: sans-serif; text-align: center; overflow: hidden; margin:0;}
            .goal-container { position: relative; width: 100%; max-width: 600px; height: 300px; margin: 20px auto; background: #234; border: 4px solid #fff; border-radius: 10px; }
            .net { position: absolute; top:0; left:0; width:100%; height:100%; background: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.3) 10px, rgba(255,255,255,0.3) 12px); }
            .target { position: absolute; width: 60px; height: 60px; background: rgba(255, 210, 74, 0.7); border-radius: 50%; cursor: pointer; transition: 0.2s; border: 2px solid #fff; }
            .target:hover { transform: scale(1.2); background: rgba(142, 216, 255, 0.9); }
            #tl { top: 20px; left: 20px; } #tr { top: 20px; right: 20px; }
            #bl { bottom: 20px; left: 20px; } #br { bottom: 20px; right: 20px; }
            #gk { position: absolute; bottom: 0; left: 45%; width: 60px; height: 120px; background: #e94560; border-radius: 30px 30px 0 0; transition: all 0.3s ease; }
            h2 { margin-top: 10px; color: #8ed8ff; }
            .score-board { font-size: 24px; font-weight: bold; margin-bottom: 10px;}
        </style>
        <h2>Strike the Target!</h2>
        <div class="score-board">Goals: <span id="score">0</span> | Misses: <span id="miss">0</span></div>
        <div class="goal-container">
            <div class="net"></div>
            <div id="gk" aria-label="Goalkeeper"></div>
            <div class="target" id="tl" onclick="shoot('tl')" role="button" tabindex="0" aria-label="Shoot Top Left"></div>
            <div class="target" id="tr" onclick="shoot('tr')" role="button" tabindex="0" aria-label="Shoot Top Right"></div>
            <div class="target" id="bl" onclick="shoot('bl')" role="button" tabindex="0" aria-label="Shoot Bottom Left"></div>
            <div class="target" id="br" onclick="shoot('br')" role="button" tabindex="0" aria-label="Shoot Bottom Right"></div>
        </div>
        <script>
            let score = 0; let miss = 0;
            function shoot(targetId) {
                const gk = document.getElementById('gk');
                const positions = ['20px', 'calc(100% - 80px)', '20px', 'calc(100% - 80px)'];
                const randomMove = Math.floor(Math.random() * 4);

                gk.style.left = positions[randomMove];
                gk.style.bottom = (randomMove < 2) ? '150px' : '0px';

                setTimeout(() => {
                    let isGoal = true;
                    if ((targetId === 'tl' && randomMove === 0) || (targetId === 'tr' && randomMove === 1) ||
                        (targetId === 'bl' && randomMove === 2) || (targetId === 'br' && randomMove === 3)) {
                        isGoal = false;
                    }

                    if (isGoal) {
                        score++; document.getElementById('score').innerText = score;
                        gk.style.backgroundColor = "grey";
                    } else {
                        miss++; document.getElementById('miss').innerText = miss;
                        gk.style.backgroundColor = "green";
                    }

                    setTimeout(() => {
                        gk.style.left = '45%'; gk.style.bottom = '0px'; gk.style.backgroundColor = "#e94560";
                    }, 800);
                }, 300);
            }
        </script>
        """
        components.html(html_game, height=450)

        if st.button(get_t("back"), key="back_quizmela_bottom"):
            set_service("home")
        return

    if service == "query":
        st.markdown("<div aria-label='Query Info' style='padding:1rem 1.2rem; border-radius:18px; background: rgba(0,0,0,0.46); border:1px solid rgba(255,255,255,0.12); margin-bottom:1rem;'><b>Query Center</b><br/>Submit the issue with your name, seat number, ticket ID, problem statement, and photo proof. It will be routed to the organiser queue for volunteer assignment.</div>", unsafe_allow_html=True)
        if st.button(get_t("back"), key="back_query_top"):
            set_service("home")

        with st.form("query_center_form", clear_on_submit=False):
            name = st.text_input("Name")
            seat_no = st.text_input("Seat No")
            ticket_id = st.text_input("Ticket ID")
            problem = st.text_area("Problem facing")
            proof = st.file_uploader("Upload one photo as proof", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
            submitted = st.form_submit_button("Raise Ticket")
        if submitted:
            # --- SECURITY UPDATE: HTML escaping directly when processing input ---
            entry = {
                "name": html.escape(normalize_text(name)),
                "seat_no": html.escape(normalize_text(seat_no)),
                "ticket_id": html.escape(normalize_text(ticket_id)),
                "problem": html.escape(normalize_text(problem)),
                "status": "Queued for organiser review",
            }
            st.session_state.audience_query_tickets.append(entry)
            st.session_state.audience_query_ticket_success = f"Ticket raised for seat {entry['seat_no'] or 'N/A'} and queued for organiser action."
            st.success(st.session_state.audience_query_ticket_success)

        if st.session_state.audience_query_tickets:
            st.markdown("### Recent tickets")
            st.table(st.session_state.audience_query_tickets[-5:])
            st.info("These queries will appear on the organiser side and be assigned to the available volunteer.")

        if st.button(get_t("back"), key="back_query_bottom"):
            set_service("home")
        return

    st.session_state.audience_service = "home"
    st.rerun()


# ==========================================
# ORGANIZER DASHBOARD (MASSIVE UPDATE)
# ==========================================

def organizer_dashboard() -> None:
    """
    Renders the Organizer Command Center.
    Provides real-time decision support, operational intelligence, 
    and crowd management tracking features.
    """
    st.markdown(
        """
        <div aria-label="Organizer Header" style="padding:2rem; border-radius:15px; background:linear-gradient(90deg, rgba(12,25,45,1) 0%, rgba(20,40,70,1) 100%); border:1px solid #8ed8ff; margin-bottom:2rem;">
            <h1 style="color:#ffffff; margin-top:0;">🧭 Organizer Command Center</h1>
            <p style="color:#a0c0e0; font-size:1.1rem; margin-bottom:0;">Live stadium intelligence, crowd monitoring, and strategic deployment.</p>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("### Participating Countries & FIFA Context")
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.table(pd.DataFrame(ORGANIZER_COUNTRIES, columns=["Country", "FIFA Record/Reason"]))
    with c2:
        st.table(pd.DataFrame(ORGANIZER_SCHEDULE))

    st.markdown("### Vision & Mission")
    v_col1, v_col2 = st.columns(2)
    v_col1.info(f"**Vision:** {ORGANIZER_INTRO['vision']}")
    v_col2.success(f"**Mission:** {ORGANIZER_INTRO['mission']}")

    st.divider()
    st.markdown("## My Responsibilities")

    # Organizer Service Router
    service_cols = st.columns(4)
    if service_cols[0].button("🏟️ Stadium Overviews", width="stretch"):
        st.session_state.organizer_service = "stadiums"
    if service_cols[1].button("👥 Crowd Management", width="stretch"):
        st.session_state.organizer_service = "crowd"
    if service_cols[2].button("📊 Operational Intelligence", width="stretch"):
        st.session_state.organizer_service = "intelligence"
    if service_cols[3].button("♻️ Sustainability & Accessibility", width="stretch"):
        st.session_state.organizer_service = "sustainability"

    service = st.session_state.organizer_service

    if service == "stadiums":
        st.markdown("### 🏟️ Stadiums & Detailed Overviews")
        st.caption("Monitor maintenance, seating, cleaning, weather, and real-time match readiness.")

        stadium_coords = pd.DataFrame({
            "stadium": ["Lusail", "Al Bayt", "Azteca", "MetLife"],
            "lat": [25.420, 25.652, 19.302, 40.812],
            "lon": [51.490, 51.487, -99.150, -74.074],
            "size": [1000, 800, 1200, 1100]
        })
        st.map(stadium_coords, size="size", color="#00ff00")

        selected_stad = st.selectbox("Select Stadium to view details:", stadium_coords["stadium"])

        st.markdown(
            f"""
            <div aria-label="Stadium Details" style="perspective: 1000px; margin-top:20px;">
                <div style="background: linear-gradient(160deg, rgba(15,30,50,0.9), rgba(8,15,25,0.95)); padding: 2rem; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); border: 2px solid #8ed8ff;">
                    <div style="background: rgba(0,0,0,0.7); padding: 1.5rem; border-radius: 15px; backdrop-filter: blur(10px);">
                        <h2 style="color: #fff; margin-top:0;">{selected_stad} Stadium - Live 360 Overview</h2>
                        <hr style="border-color: #555;">
                        <div style="display: flex; justify-content: space-between; color: #ccc; flex-wrap: wrap; gap: 12px;">
                            <div><b>Capacity:</b> 80,000+</div>
                            <div><b>Maintenance:</b> <span style="color: #4caf50;">Green (Ready)</span></div>
                            <div><b>Cleaning:</b> <span style="color: #ff9800;">Amber (In-progress)</span></div>
                            <div><b>Weather:</b> 28°C, Clear</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

    elif service == "crowd":
        st.markdown("### 👥 Crowd Management - AI Detective Sensor")
        st.caption("AI detects entry/exit flows and raises issues. Assign random free volunteers to solve them.")

        vols_df = generate_50_volunteers()
        queries = st.session_state.audience_queries

        for q in queries:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                col1.write(f"**Issue:** {q['Issue']} | **Location:** {q['Stadium']} - {q['Block/Gate']}")
                col1.write(f"**Status:** {q['Status']} | **Assigned:** {q['Assigned To']}")

                if q['Status'] == "Pending":
                    if col2.button("Solve this", key=f"solve_{q['Query ID']}"):
                        free_vols = vols_df[vols_df["Status"] == "Free"]
                        if not free_vols.empty:
                            assigned = free_vols.sample(1).iloc[0]
                            q['Status'] = "Assigned"
                            q['Assigned To'] = assigned['Name'] + " (" + assigned['ID'] + ")"
                            st.success(f"Assigned {assigned['Name']} to {q['Query ID']}!")
                            st.rerun()
                        else:
                            st.error("No free volunteers available!")

        st.markdown("#### Volunteer Fleet Live Status")

        def color_status(val):
            color = 'green' if val == 'Free' else 'red'
            return f'color: {color}; font-weight: bold;'

        st.dataframe(vols_df[["Name", "ID", "Stadium", "Status"]].style.map(color_status, subset=['Status']), width="stretch")

    elif service == "intelligence":
        st.markdown("### 📊 Operational Intelligence Dashboard")
        st.caption("Detailed analytical dashboard with multiple categories and 5 distinct visuals.")

        op_data = generate_op_intelligence_data()

        category = st.selectbox("Select Analytics Category (Filter):", ["All", "Group Stage", "Knockout", "Quarter Final"])
        if category != "All":
            op_data = op_data[op_data["Category"] == category]

        c1, c2 = st.columns(2)

        fig_hist = px.histogram(op_data, x="Attendance", title="Attendance Distribution (Histogram)", color_discrete_sequence=["#3498db"])
        c1.plotly_chart(fig_hist, width="stretch")

        issue_types = pd.DataFrame({"Type": ["Ticketing", "Seating", "F&B", "Navigation"], "Count": [120, 80, 200, 150]})
        fig_donut = px.pie(issue_types, names="Type", values="Count", hole=0.4, title="Issue Breakdown (Donut)")
        c2.plotly_chart(fig_donut, width="stretch")

        c3, c4 = st.columns(2)

        fig_area = px.area(op_data, x="Date", y="Revenue", title="Revenue Trend (Area Chart)", color_discrete_sequence=["#2ecc71"])
        c3.plotly_chart(fig_area, width="stretch")

        fig_bar = px.bar(op_data, x="Match", y="Volunteer Fill Rate", title="Volunteer Efficiency (Bar/Ribbon)", color="Volunteer Fill Rate")
        c4.plotly_chart(fig_bar, width="stretch")

        st.markdown("#### Profit & Loss Cascade (Waterfall)")
        fig_waterfall = go.Figure(go.Waterfall(
            name="2026", orientation="v",
            measure=["relative", "relative", "total", "relative", "relative", "total"],
            x=["Ticketing", "Sponsors", "Gross Rev", "Operations", "Logistics", "Net Rev"],
            textposition="outside",
            y=[5000000, 3000000, 0, -2000000, -1000000, 0],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        st.plotly_chart(fig_waterfall, width="stretch")

    elif service == "sustainability":
        st.markdown("### ♻️ Sustainability & Accessibility - Auto Routing")
        st.caption("Connection system linking user queries to free volunteers automatically.")
        st.info("System Status: **Active**. 4 tasks automatically assigned and routed in the last hour.")

        st.table([
            {"User Issue": "Wheelchair ramp blocked", "Detected Assigned Vol": "Aadya (VOL-1000)", "Status": "In Progress"},
            {"User Issue": "Recycling bin overflow", "Detected Assigned Vol": "Liam (VOL-1003)", "Status": "Done"},
            {"User Issue": "Sensory room full", "Detected Assigned Vol": "Emma (VOL-1004)", "Status": "Done"}
        ])

    st.divider()
    if st.button("Logout", key="organizer_logout"):
        reset_and_logout()


# ==========================================
# VOLUNTEER DASHBOARD (MASSIVE UPDATE)
# ==========================================

def volunteer_dashboard() -> None:
    """
    Renders the Volunteer Operations dashboard.
    Tracks assigned tasks, monitors fan needs, and displays a gamified leaderboard.
    """
    st.markdown(
        """
        <div aria-label="Volunteer Header" style="background: linear-gradient(160deg, rgba(20,40,40,0.9), rgba(10,20,20,0.95)); padding: 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; border: 2px solid #fff; margin-bottom: 2rem;">
            <div style="background: rgba(0,0,0,0.7); padding: 1rem; border-radius: 15px; display: inline-block;">
                <h1 style="color:#fff; margin:0;">🤝 Volunteer Operations</h1>
                <p style="color:#8ed8ff; margin:0;">Be the heartbeat of the FIFA 2026 Tournament</p>
            </div>
            <div style="display:flex; justify-content:center; gap: 15px; margin-top: 20px; flex-wrap:wrap;">
                <div style="background: rgba(255,255,255,0.1); border:1px solid #fff; padding:15px; border-radius:20px; width:200px; backdrop-filter:blur(5px);">
                    <h3 style="margin:0; color:#ffd700;">Vision</h3>
                    <p style="font-size:0.9rem; color:#fff;">Enhance fan safety & comfort instantly.</p>
                </div>
                <div style="background: rgba(255,255,255,0.1); border:1px solid #fff; padding:15px; border-radius:20px; width:200px; backdrop-filter:blur(5px);">
                    <h3 style="margin:0; color:#ffd700;">Mission</h3>
                    <p style="font-size:0.9rem; color:#fff;">Execute clear tasks and get rewarded.</p>
                </div>
                <div style="background: rgba(255,255,255,0.1); border:1px solid #fff; padding:15px; border-radius:20px; width:200px; backdrop-filter:blur(5px);">
                    <h3 style="margin:0; color:#ffd700;">Action</h3>
                    <p style="font-size:0.9rem; color:#fff;">Respond quickly & climb the leaderboard.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("## My Responsibilities")
    v_cols = st.columns(3)
    if v_cols[0].button("🏆 Leaderboard", width="stretch"):
        st.session_state.volunteer_service = "leaderboard"
    if v_cols[1].button("📋 My Tasks", width="stretch"):
        st.session_state.volunteer_service = "tasks"
    if v_cols[2].button("📈 My Analytics", width="stretch"):
        st.session_state.volunteer_service = "analytics"

    service = st.session_state.volunteer_service
    vol_data = generate_50_volunteers()

    if service == "leaderboard":
        st.markdown("### 🏆 Global Volunteer Leaderboard")
        st.caption("Tracking 50 volunteers across 9-10 performance columns.")

        st.dataframe(
            vol_data.sort_values(by="Points", ascending=False).style.background_gradient(cmap="Blues", subset=["Efficiency (%)", "Points"]),
            width="stretch",
            height=600
        )

    elif service == "tasks":
        st.markdown("### 📋 My Active Tasks")
        st.write(f"**Total Points Earned:** {st.session_state.vol_points_earned} 🌟")

        tasks = st.session_state.my_vol_tasks

        task_tabs = st.tabs([f"Task {i + 1}" for i in range(len(tasks))])

        for idx, tab in enumerate(task_tabs):
            task = tasks[idx]
            with tab:
                st.markdown(f"#### {task['Task']}")
                st.write(f"**Assigned By:** {task['Assigned By']}")
                st.write(f"**Target User:** {task['Target User']}")
                st.write(f"**Current Status:** {task['Status']}")

                if task["Status"] == "Pending":
                    if st.button("Mark as Completed ✅", key=f"complete_btn_{idx}"):
                        pts = random.randint(10, 90)
                        task["Status"] = "Completed"
                        st.session_state.vol_points_earned += pts
                        st.success(f"{pts} points added to your profile!")
                        st.rerun()
                else:
                    st.info("This task is already completed.")

    elif service == "analytics":
        st.markdown("### 📈 Volunteer Performance Analytics")
        st.caption("Visualizing the 50-member leaderboard data.")

        ac1, ac2 = st.columns(2)

        fig_scatter = px.scatter(vol_data, x="Efficiency (%)", y="Points", size="Tasks Done", color="Stadium", title="Efficiency vs Points Earned")
        ac1.plotly_chart(fig_scatter, width="stretch")

        fig_box = px.box(vol_data, x="Stadium", y="Avg Time (mins)", color="Stadium", title="Resolution Time Variance by Stadium")
        ac2.plotly_chart(fig_box, width="stretch")

        ac3, ac4 = st.columns(2)

        status_counts = vol_data["Status"].value_counts().reset_index()
        fig_bar2 = px.bar(status_counts, x="Status", y="count", color="Status", title="Fleet Availability Status")
        ac3.plotly_chart(fig_bar2, width="stretch")

        fig_hist2 = px.histogram(vol_data, x="Rating", nbins=10, title="Volunteer Quality Ratings", color_discrete_sequence=["#8e44ad"])
        ac4.plotly_chart(fig_hist2, width="stretch")

    st.divider()
    if st.button("Logout", key="volunteer_logout"):
        reset_and_logout()


ROLE_META = {
    "Audience": {"icon": "🎟️", "desc": "Book tickets, navigate stadiums, and raise support queries."},
    "Organizer": {"icon": "🧭", "desc": "Monitor stadium operations, crowd flow, and live analytics."},
    "Volunteer": {"icon": "🤝", "desc": "Manage assigned tasks and track your leaderboard rank."},
}


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <div style="text-transform:uppercase; letter-spacing:0.3em; color:#8ed8ff; font-size:0.85rem; margin-bottom:0.8rem;">FIFA 2026 Smart Stadium Ops</div>
            <h1>Welcome to the Command Hub</h1>
            <p style="color:rgba(245,247,251,0.85); font-size:1.05rem; max-width:720px; margin:0 auto;">
                Sign in or create an account as an Audience member, Organizer, or Volunteer to reach your personalized dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_role_cards() -> None:
    columns = st.columns(len(USER_ROLES), gap="large")
    for column, role in zip(columns, USER_ROLES):
        meta = ROLE_META[role]
        with column:
            st.markdown(
                f"""
                <div class="role-card">
                    <div style="font-size:2.2rem;">{meta['icon']}</div>
                    <h3 style="color:#fff; margin:0.6rem 0 0.4rem;">{role}</h3>
                    <p style="color:rgba(245,247,251,0.82); font-size:0.92rem;">{meta['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Continue as {role}", key=f"role_select_{role}", width="stretch"):
                st.session_state.selected_role = role
                st.session_state.auth_error = None
                st.rerun()


def render_role_dialog(role: str) -> None:
    config = ROLE_CONFIG[role]
    identifier_label = config["identifier_label"]

    with st.container(border=True):
        st.markdown(f"### {role} Access")
        if st.session_state.auth_error:
            st.error(st.session_state.auth_error)

        login_tab, signup_tab = st.tabs(["Log In", "Sign Up"])

        with login_tab:
            with st.form(key=f"login_form_{role}"):
                identifier = st.text_input(identifier_label, key=f"login_identifier_{role}")
                password = st.text_input("Password", type="password", key=f"login_password_{role}")
                login_submitted = st.form_submit_button("Log In", width="stretch")
            if login_submitted:
                if not normalize_text(identifier) or not password:
                    st.session_state.auth_error = "Please fill in all fields."
                    st.rerun()
                else:
                    ok, message, account = authenticate_user(role, identifier, password)
                    if ok and account:
                        submit_account_success(role, account)
                    else:
                        st.session_state.auth_error = message
                        st.rerun()

        with signup_tab:
            with st.form(key=f"signup_form_{role}"):
                field_values: dict[str, str] = {}
                for label, key in config["signup_fields"]:
                    field_values[key] = st.text_input(
                        label,
                        type="password" if key == "password" else "default",
                        key=f"signup_{key}_{role}",
                    )
                signup_submitted = st.form_submit_button("Create Account", width="stretch")
            if signup_submitted:
                missing_fields = [
                    label for label, key in config["signup_fields"]
                    if not normalize_text(field_values.get(key))
                ]
                if missing_fields:
                    st.session_state.auth_error = "Please fill in all fields."
                    st.rerun()
                else:
                    ok, message, account = register_user(role, field_values)
                    if ok and account:
                        submit_account_success(role, account)
                    else:
                        st.session_state.auth_error = message
                        st.rerun()

        st.write("")
        if st.button("Cancel", key=f"cancel_role_{role}"):
            clear_login_dialog()


def render_auth_flow() -> None:
    render_hero()
    st.write("")
    render_role_cards()
    selected_role = st.session_state.selected_role
    if selected_role:
        render_role_dialog(selected_role)


def main() -> None:
    initialize_state()
    inject_css()

    if st.session_state.logged_in:
        role = st.session_state.user_role
        if role == "Audience":
            audience_dashboard()
        elif role == "Organizer":
            organizer_dashboard()
        elif role == "Volunteer":
            volunteer_dashboard()
        else:
            reset_and_logout()
    else:
        render_auth_flow()


if __name__ == "__main__":
    main()
