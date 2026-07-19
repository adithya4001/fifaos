import base64
import hashlib
import json
import secrets
import textwrap
from pathlib import Path

import streamlit as st

import random
from deep_translator import GoogleTranslator

LANG_CODES = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de"
}

@st.cache_data(show_spinner=False)
def t(text, target_lang):
    """Dynamic GenAI-powered translation."""
    if target_lang == "English" or not text: 
        return text
    try:
        target_code = LANG_CODES.get(target_lang, "en")
        return GoogleTranslator(source='auto', target=target_code).translate(text)
    except Exception:
        return text


st.set_page_config(
	page_title="FIFA 2026 Smart Stadium Ops",
	layout="wide",
)


USERS_FILE = Path(__file__).with_name("users.json")
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


ORGANIZER_INTRO = {
	"vision": "Run a stadium ecosystem where crowd flow, safety, accessibility, and sustainability stay in sync.",
	"mission": "Convert live signals into instant action for operations teams and volunteers.",
	"roles": [
		"Monitor stadium readiness",
		"Track match-day crowd pressure",
		"Dispatch volunteers by urgency",
		"Review analytics and post-match impact",
	],
}


ORGANIZER_COUNTRIES = [
	("Qatar", "Host nation and operational coordinator"),
	("Brazil", "Top fan base and global following"),
	("Argentina", "High attendance and media interest"),
	("France", "Strong tournament performance history"),
	("Germany", "High operational and crowd planning demand"),
	("Japan", "Large multilingual support requirement"),
]


ORGANIZER_SCHEDULE = [
	{"date": "2026-06-15", "time": "19:00", "fixture": "Brazil vs Spain", "location": "Lusail", "verdict": "High demand"},
	{"date": "2026-06-16", "time": "16:00", "fixture": "Argentina vs Germany", "location": "Al Bayt", "verdict": "Moderate crowd"},
	{"date": "2026-06-17", "time": "21:00", "fixture": "France vs Japan", "location": "Education City", "verdict": "Operational watch"},
]


ORGANIZER_STADIUM_STATUS = [
	{
		"stadium": "Lusail Stadium",
		"capacity": 88966,
		"maintenance": "Green",
		"cleaning": "Green",
		"weather": "Clear, 31°C",
		"ready": "Yes",
		"notes": "Main route open and volunteer coverage complete.",
	},
	{
		"stadium": "Al Bayt Stadium",
		"capacity": 60000,
		"maintenance": "Amber",
		"cleaning": "Green",
		"weather": "Cloudy, 28°C",
		"ready": "Yes",
		"notes": "Crowd inflow monitored at North entry.",
	},
	{
		"stadium": "Education City Stadium",
		"capacity": 44500,
		"maintenance": "Green",
		"cleaning": "Amber",
		"weather": "Windy, 29°C",
		"ready": "No",
		"notes": "Final cleaning pass required before opening.",
	},
]


ORGANIZER_ANALYTICS = {
	"attendance": [62, 74, 81, 79, 88, 91],
	"complaints": [5, 4, 6, 3, 2, 4],
	"transport": [42, 48, 55, 61, 58, 64],
	"volunteer_fill": [73, 76, 80, 85, 89, 92],
}


FEEDBACK = [
	{"category": "navigation", "text": "Gate instructions were clear and fast.", "sentiment": "positive"},
	{"category": "accessibility", "text": "Wheelchair assistance took too long near Gate 4.", "sentiment": "negative"},
	{"category": "transport", "text": "Bus timings were useful but crowded after the match.", "sentiment": "neutral"},
	{"category": "support", "text": "Volunteer help at the food counter was excellent.", "sentiment": "positive"},
	{"category": "cleaning", "text": "Restrooms needed more frequent checks.", "sentiment": "negative"},
]


def analyze_feedback(items):
	sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
	category_counts = {}
	for item in items:
		sentiment = item["sentiment"]
		category = item["category"]
		sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
		category_counts[category] = category_counts.get(category, 0) + 1

	main_issue = max(category_counts, key=category_counts.get)
	recommendation = {
		"navigation": "Improve gate signage and wayfinding assistance.",
		"accessibility": "Dispatch an accessibility volunteer and shorten response time.",
		"transport": "Add more post-match shuttle capacity.",
		"support": "Keep staffing levels high at service counters.",
		"cleaning": "Increase restroom and concourse cleaning frequency.",
	}.get(main_issue, "Review the most reported issue and escalate accordingly.")

	return {
		"sentiment_counts": sentiment_counts,
		"category_counts": category_counts,
		"main_issue": main_issue,
		"recommendation": recommendation,
	}


VOLUNTEER_INTRO = {
	"vision": "Turn small on-ground actions into measurable fan comfort and safety improvements.",
	"mission": "Give volunteers clear tasks, quick feedback, and meaningful recognition.",
	"roles": [
		"Handle support requests",
		"Assist crowd movement",
		"Track issue resolution",
		"Earn points for quality work",
	],
}


VOLUNTEER_QUEUE = [
	{"task": "Guide fans to Gate 3", "priority": "High", "location": "Lusail Stadium", "status": "In progress", "points": 25},
	{"task": "Assist wheelchair user", "priority": "Critical", "location": "Al Bayt Stadium", "status": "Pending", "points": 40},
	{"task": "Collect exit feedback", "priority": "Medium", "location": "Education City Stadium", "status": "Pending", "points": 15},
	{"task": "Refill beverage station", "priority": "High", "location": "Lusail Stadium", "status": "Done", "points": 20},
]


VOLUNTEER_LEADERBOARD = [
	{"name": "Aadya", "points": 92, "tasks": 14, "quality": 97},
	{"name": "Rahul", "points": 88, "tasks": 13, "quality": 94},
	{"name": "Nina", "points": 84, "tasks": 12, "quality": 91},
	{"name": "You", "points": 20, "tasks": 1, "quality": 88},
]


def initialize_state() -> None:
	"""Create the small session-state footprint used for routing."""

	st.session_state.setdefault("logged_in", False)
	st.session_state.setdefault("user_role", None)
	st.session_state.setdefault("user_data", {})
	st.session_state.setdefault("selected_role", None)
	st.session_state.setdefault("auth_error", None)
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
	digest = hashlib.pbkdf2_hmac(
		"sha256",
		password.encode("utf-8"),
		bytes.fromhex(salt_hex),
		120000,
	)
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

	for record in store[role]:
		if normalize_key(record.get(identifier_key)) == identifier_value:
			return False, f"A {role.lower()} account already exists for this {config['identifier_label'].lower()}.", None
		if email_value and normalize_key(record.get("email")) == email_value:
			return False, f"A {role.lower()} account already exists for this email.", None

	salt, password_hash = hash_password(payload["password"])
	user_record = {
		"role": role,
		"name": normalize_text(payload.get("name")),
		"email": normalize_text(payload.get("email")).lower(),
		"phone": normalize_text(payload.get("phone")),
		identifier_key: normalize_text(payload.get(identifier_key)),
		"password_salt": salt,
		"password_hash": password_hash,
	}
	if role == "Organizer":
		user_record["organizer_id"] = normalize_text(payload.get("organizer_id"))

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

	return False, f"No {role.lower()} account was found for that {ROLE_CONFIG[role]['identifier_label'].lower() }.", None


def submit_account_success(role: str, account: dict) -> None:
	complete_login(
		role,
		{
			"role": role,
			"name": account.get("name", ""),
			"email": account.get("email", ""),
			"phone": account.get("phone", ""),
			ROLE_CONFIG[role]["identifier_key"]: account.get(ROLE_CONFIG[role]["identifier_key"], ""),
		},
	)


def inject_css() -> None:
	"""Add a bold stadium-themed landing page treatment."""

	st.markdown(
		"""
		<style>
			* { font-family: 'Times New Roman', serif !important; }

			#MainMenu,
			footer,
			header,
			[data-testid="stHeader"],
			[data-testid="stToolbar"] {
				display: none !important;
			}

			.stApp {
				background:
					linear-gradient(180deg, rgba(3, 8, 16, 0.82) 0%, rgba(5, 12, 22, 0.76) 50%, rgba(4, 9, 17, 0.9) 100%),
					url('https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?q=80&w=2000') center center / cover no-repeat fixed;
				color: #f5f7fb;
				min-height: 100vh;
			}

			[data-testid="stAppViewContainer"] {
				background: transparent;
			}

			.hero {
				max-width: 1040px;
				margin: 0 auto;
				padding: 4rem 2rem 2.5rem;
				text-align: center;
				border: 1px solid rgba(255, 255, 255, 0.12);
				border-radius: 30px;
				background: linear-gradient(135deg, rgba(7, 13, 23, 0.82), rgba(14, 24, 39, 0.56));
				box-shadow: 0 24px 70px rgba(0, 0, 0, 0.48);
				backdrop-filter: blur(16px);
				-webkit-backdrop-filter: blur(16px);
			}

			.eyebrow {
				text-transform: uppercase;
				letter-spacing: 0.28em;
				font-size: 0.78rem;
				color: #8ed8ff;
				margin-bottom: 0.75rem;
			}

			.hero h1 {
				font-size: clamp(2.7rem, 6vw, 5.7rem);
				line-height: 0.98;
				margin: 0 0 0.9rem 0;
				color: #ffffff;
				text-shadow: 0 0 18px rgba(105, 191, 255, 0.28), 0 0 40px rgba(0, 0, 0, 0.28);
				font-weight: 700;
			}

			.hero p {
				max-width: 900px;
				margin: 0 auto;
				font-size: 1.1rem;
				line-height: 1.8;
				color: rgba(245, 247, 251, 0.9);
				text-shadow: 0 1px 10px rgba(0, 0, 0, 0.35);
			}

			div[data-testid="column"] {
				padding-top: 0.35rem;
				padding-bottom: 0.35rem;
			}

			.role-card {
				min-height: 240px;
				padding: 1.5rem;
				border-radius: 24px;
				border: 1px solid rgba(255, 255, 255, 0.16);
				background: linear-gradient(180deg, rgba(0, 0, 0, 0.52), rgba(10, 14, 24, 0.74));
				box-shadow:
					inset 0 1px 0 rgba(255, 255, 255, 0.08),
					0 18px 45px rgba(0, 0, 0, 0.34);
				backdrop-filter: blur(10px);
				-webkit-backdrop-filter: blur(10px);
			}

			.role-card h3 {
				margin: 0 0 0.55rem 0;
				font-size: 1.35rem;
				color: #ffffff;
				text-shadow: 0 0 12px rgba(255, 255, 255, 0.08);
			}

			.role-card p {
				color: rgba(245, 247, 251, 0.8);
				line-height: 1.6;
			}

			.role-chip {
				display: inline-block;
				margin-bottom: 0.9rem;
				padding: 0.35rem 0.75rem;
				border-radius: 999px;
				background: rgba(255, 255, 255, 0.08);
				color: #8ed8ff;
				font-size: 0.8rem;
				letter-spacing: 0.05em;
			}

			.selected-role-banner {
				margin-top: 1.1rem;
				padding: 0.9rem 1rem;
				border-left: 4px solid #ffd24a;
				border-radius: 12px;
				background: rgba(255, 210, 74, 0.1);
				color: #fff4c2;
			}

			div[data-testid="stForm"] {
				border: 1px solid rgba(255, 255, 255, 0.1);
				border-radius: 20px;
				padding: 1rem 1.1rem 0.25rem;
				background: rgba(0, 0, 0, 0.48);
				backdrop-filter: blur(12px);
				-webkit-backdrop-filter: blur(12px);
				box-shadow: 0 18px 45px rgba(0, 0, 0, 0.3);
			}

			div[data-testid="stButton"] button {
				border: 1px solid rgba(255, 255, 255, 0.28) !important;
				border-radius: 18px !important;
				padding: 0.75rem 1.2rem !important;
				font-weight: 700;
				background: rgba(0, 0, 0, 0.6) !important;
				color: #ffffff !important;
				backdrop-filter: blur(10px);
				-webkit-backdrop-filter: blur(10px);
				box-shadow: 0 10px 28px rgba(0, 0, 0, 0.28);
				transition: transform 180ms ease, box-shadow 180ms ease, background 180ms ease, border-color 180ms ease;
			}

			div[data-testid="stButton"] button:hover {
				transform: scale(1.05);
				border-color: rgba(255, 255, 255, 0.45) !important;
				box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.08), 0 0 24px rgba(92, 176, 255, 0.28), 0 12px 30px rgba(0, 0, 0, 0.4);
				background: rgba(18, 18, 18, 0.74) !important;
			}

			div[data-testid="stButton"] button:active {
				transform: scale(0.99);
			}

			div[data-testid="stDialog"] div[role="dialog"],
			div[data-testid="stDialog"] {
				background: rgba(5, 9, 16, 0.9);
			}

			div[data-testid="stModal"] { background-color: rgba(0, 0, 0, 0.4) !important; backdrop-filter: blur(5px) !important; }
			div[data-testid="stModal"] > div { background-color: rgba(20, 20, 20, 0.9) !important; border: 1px solid #444; border-radius: 15px; }
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
	st.session_state.user_data = {}
	st.session_state.selected_role = None
	st.session_state.auth_error = None
	st.rerun()


def audience_dashboard() -> None:
	import urllib.parse
	import uuid
	import streamlit.components.v1 as components

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
			"hero_body": "Un portail premium pour la billetterie, la navigation, l’assistance et l’engagement en direct.",
			"welcome_title": "Centre de commandement des fans",
			"welcome_body": "Préparez votre arrivée, réservez votre siège, explorez le stade et posez vos questions dans votre langue.",
			"services": "VOS SERVICES",
			"book": "Réserver des billets",
			"navigate": "Navigation facile",
			"quiz": "QUIZMELA",
			"query": "Centre de requêtes",
			"back": "Retour à l’accueil",
		},
	}
	lang = st.session_state.audience_language
	localized = translations.get(lang, translations["English"])

	all_languages = [
		"English", "Spanish", "French", "German"
	]

	football_gallery = [
		{"title": "The roar of the crowd", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTK5tN4htmqho7D5FUAVtRNILBn7uGzAuMAyPrn54eIwg&s=10", "points": ["Stadium energy turns every match into a live festival.", "Fans create the atmosphere players remember forever.", "Shared chants make the World Cup feel global in one place."]},
		{"title": "Precision on the pitch", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk8shsHdl9W4bdlkM-AuyAX_xUfzLjSoQdqtXnTZGDOA&s=10", "points": ["Every pass and run matters under pressure.", "Tactical movement is as important as raw speed.", "Small moments can decide a world-class match."]},
		{"title": "The game is universal", "image": "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?q=80&w=1200", "points": ["Football connects different countries and cultures.", "One tournament can bring millions of stories together.", "The World Cup is a shared language for fans."]},
		{"title": "Fans make it iconic", "image": "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=1200", "points": ["Color, flags, and chants define the tournament vibe.", "Supporters convert a stadium into a memory machine.", "Cheering together is half the magic of FIFA."]},
		{"title": "Moments become history", "image": "https://images.unsplash.com/photo-1518091043644-c1d4457512c6?q=80&w=1200", "points": ["Big matches create unforgettable highlights.", "Players become legends through decisive performances.", "Every World Cup adds new records and emotions."]},
	]

	service_cards = [
		{"key": "booking", "title": "Booking Tickets", "desc": "Pick a FIFA 2026 match, choose your seat in a stadium view, see the price instantly, and complete payment in a guided flow.", "image": "https://images.unsplash.com/photo-1547347298-4074fc3086f0?q=80&w=1200"},
		{"key": "navigation", "title": "Easy Navigation", "desc": "Enter your current address and stadium destination, select car/bus/bike, and get a route assistant with map preview and travel guidance.", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6c6BkaAPqIBxyKSE8OQkUpWJw2901VoqpsbdrHurBTw&s=10"},
		{"key": "quizmela", "title": "QUIZMELA", "desc": "Play 5 quizzes, 5 riddles, and 5 football mini-games in a gamified dialog experience with points, hints, and fun facts.", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUJZHxMZpSa7ide0yCaCADuNoGJwh5ib4sTbtZbYdBgQ&s=10"},
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

	def t(key: str) -> str:
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

	def build_map_url(origin: str, destination: str) -> str:
		origin_q = urllib.parse.quote_plus(origin)
		destination_q = urllib.parse.quote_plus(destination)
		return f"https://www.google.com/maps/dir/{origin_q}/{destination_q}"

	def render_home() -> None:
		st.markdown(
			f"""
			<div style="position: relative; overflow: hidden; border-radius: 34px; min-height: 480px; margin-bottom: 1.2rem; border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 28px 80px rgba(0,0,0,0.5); background: #0a0f18;">
				<div style="position:absolute; inset:0; background: linear-gradient(180deg, rgba(4,8,14,0.2) 0%, rgba(4,8,14,0.68) 58%, rgba(4,8,14,0.93) 100%), url('https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=2000') center center / cover no-repeat;"></div>
				<div style="position:relative; z-index:1; padding: 5rem 3rem 4rem; text-align:center; max-width: 980px; margin: 0 auto;">
					<div style="text-transform:uppercase; letter-spacing:0.32em; color:#8ed8ff; font-size:0.8rem; margin-bottom:0.9rem;">FIFA 2026 Audience Portal</div>
					<h1 style="margin:0 0 1rem 0; font-size: clamp(3rem, 7vw, 6.5rem); line-height:0.95; color:#fff; text-shadow:0 0 20px rgba(94,179,255,0.35), 0 0 48px rgba(0,0,0,0.55);">{t('hero_title')}</h1>
					<p style="margin:0 auto; max-width: 920px; font-size: 1.1rem; line-height:1.85; color: rgba(245,247,251,0.94);">{t('hero_body')}</p>
				</div>
			</div>
			""",
			unsafe_allow_html=True,
		)

		st.markdown(
			f"""
			<div style="padding:1.1rem 1.25rem; margin-bottom:1rem; border-radius:20px; border:1px solid rgba(255,255,255,0.14); background: linear-gradient(180deg, rgba(0,0,0,0.52), rgba(12,16,26,0.74)); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);">
				<h3 style="margin:0 0 0.45rem 0; color:#fff;">{t('welcome_title')}</h3>
				<p style="margin:0; color: rgba(245,247,251,0.88); line-height:1.75;">{t('welcome_body')}</p>
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
					# Modern Glassmorphism Card combining Image and Text
					st.markdown(
						f"""
						<div style="background: rgba(12, 18, 28, 0.7); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 1.5rem;">
							<div style="height: 220px; overflow: hidden; border-bottom: 1px solid rgba(255,255,255,0.1);">
								<img src="{item['image']}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'"/>
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

		st.markdown(f"## {t('services')}")
		st.caption("Choose one service to open a dedicated in-app workspace.")
		service_columns = st.columns(4, gap="large")
		for column, card in zip(service_columns, service_cards):
			with column:
				st.markdown(
					f"""
					<div style="min-height: 360px; padding:1rem; border-radius: 24px; border:1px solid rgba(255,255,255,0.14); background: rgba(0,0,0,0.48); box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 20px 44px rgba(0,0,0,0.32);">
						<img src="{card['image']}" style="width:100%; height:140px; object-fit:cover; border-radius:18px; margin-bottom:0.85rem;" />
						<div style="text-transform:uppercase; letter-spacing:0.16em; color:#8ed8ff; font-size:0.72rem; margin-bottom:0.45rem;">Your Service</div>
						<h3 style="margin:0 0 0.5rem 0; color:#fff;">{card['title']}</h3>
						<p style="margin:0 0 0.9rem 0; color:rgba(245,247,251,0.86); line-height:1.65;">{card['desc']}</p>
					</div>
					""",
					unsafe_allow_html=True,
				)
				if st.button(f"Open {card['title']}", key=f"service_open_{card['key']}", use_container_width=True):
					set_service(card["key"])

		if st.session_state.audience_ticket_issue_message:
			st.success(st.session_state.audience_ticket_issue_message)
			st.session_state.audience_ticket_issue_message = ""

		st.markdown(f"### {t('welcome_title')}")
		st.write("This home screen is a fan command center with direct access to ticketing, movement help, games, and support.")

	def render_ticketing() -> None:
		st.markdown(f"## {t('book')}")
		st.caption("Select a FIFA 2026 match, choose a seat in the stadium view, confirm the price, and issue the ticket.")
		if st.button(t("back"), key="back_home_ticketing"):
			set_service("home")
		return

	def render_navigation() -> None:
		st.markdown(f"## {t('navigate')}")
		st.caption("Your journey made easy: enter address, destination, and mode to get an optimal route plan.")
		if st.button(t("back"), key="back_home_navigation"):
			set_service("home")
		return

	def render_quizmela() -> None:
		st.markdown(f"## {t('quiz')}")
		st.caption("Quizzes, riddles, and games that keep fans entertained between matches.")
		if st.button(t("back"), key="back_home_quizmela"):
			set_service("home")
		return

	def render_query_center() -> None:
		st.markdown(f"## {t('query')}")
		st.caption("Raise a ticket, attach proof, and route the issue to the organiser queue.")
		if st.button(t("back"), key="back_home_query"):
			set_service("home")
		return

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

	if service == "home":
		render_home()
		return

	if service == "booking":
		st.markdown("<div style='padding:1rem 1.2rem; border-radius:18px; background: rgba(0,0,0,0.46); border:1px solid rgba(255,255,255,0.12); margin-bottom:1rem;'><b>Booking Tickets</b><br/>Select a FIFA 2026 match from the actual tournament schedule, choose seats from the stadium view, see the fare, then pay through UPI or Net Banking.</div>", unsafe_allow_html=True)
		if st.button(t("back"), key="back_ticketing_top"):
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
						if st.button(seat_label, key=f"seat_{seat_label}", use_container_width=True):
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

		if st.button(t("back"), key="back_ticketing_bottom"):
			set_service("home")
		return

	if service == "navigation":
		st.markdown("<div style='padding:1rem 1.2rem; border-radius:18px; background: rgba(0,0,0,0.46); border:1px solid rgba(255,255,255,0.12); margin-bottom:1rem;'><b>Stadium Navigation</b><br/>Your journey made easy: provide origin, stadium destination, and transport mode; then receive a route plan, map view, and distance estimate.</div>", unsafe_allow_html=True)
		if st.button(t("back"), key="back_navigation_top"):
			set_service("home")

		origin = st.text_input("Your address", key="nav_origin")
		
		# Stadium actual locations for map targeting
		stadiums_info = {
			"Lusail Stadium": "Lusail, Qatar",
			"Al Bayt Stadium": "Al Khor, Qatar",
			"Education City Stadium": "Al Rayyan, Qatar"
		}
		
		destination = st.selectbox("Stadium address", list(stadiums_info.keys()), key="nav_destination")
		mode = st.radio("Way of going", ["Car", "Bus", "Bike"], horizontal=True, key="nav_mode")
		
		if st.button("Proceed", key="nav_proceed"):
			st.session_state.audience_route_generated = True
			# Generate a dynamic mock distance based on string length to simulate an API call
			base_dist = len(origin) * 1.8 if origin else 12.5
			st.session_state.mock_distance = round(base_dist + (len(destination) * 0.5), 1)

		if st.session_state.get("audience_route_generated"):
			map_query = urllib.parse.quote_plus(f"{destination}, {stadiums_info[destination]}")
			# Changing map to terrain/satellite view dynamically
			map_url = f"https://www.google.com/maps?q={map_query}&t=k&output=embed"
			
			dist = st.session_state.get("mock_distance", 24.5)
			# Time multiplier based on mode
			time_mins = int(dist * (1.8 if mode == "Car" else 2.5 if mode == "Bus" else 4.0))

			left, right = st.columns([1.2, 1])
			with left:
				st.markdown("###  Live World Map View")
				components.html(
					f"<iframe src='{map_url}' width='100%' height='450' style='border:0; border-radius:18px;' loading='lazy' referrerpolicy='no-referrer-when-downgrade'></iframe>",
					height=470,
				)
			with right:
				st.markdown("###  Routing Intelligence")
				st.markdown(
					f"""
					<div style="padding: 1.5rem; background: rgba(0,0,0,0.5); border-radius: 16px; border: 1px solid #8ed8ff; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
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

		if st.button(t("back"), key="back_navigation_bottom"):
			set_service("home")
		return

	if service == "quizmela":
		st.markdown("<div style='padding:1rem 1.2rem; border-radius:18px; background: rgba(0,0,0,0.46); border:1px solid rgba(255,255,255,0.12); margin-bottom:1rem;'><b>QUIZMELA</b><br/>Choose quizzes, riddles, or football games. Every game is focused on FIFA facts, football knowledge, and fan engagement.</div>", unsafe_allow_html=True)
		if st.button(t("back"), key="back_quiz_top"):
			set_service("home")

		quiz_tab, riddle_tab, game_tab = st.tabs(["Quizzes", "Riddles", "Games"])
		with quiz_tab:
			st.markdown("### 5 Quizzes")
			quiz_cols = st.columns(5)
			for idx, item in enumerate(quiz_bank):
				with quiz_cols[idx]:
					st.markdown(f"**Q{idx + 1}**")
					st.write(item["question"])
					if st.button("Open", key=f"quiz_open_{idx}"):
						st.session_state.audience_modal = {"type": "quiz", "index": idx}
		with riddle_tab:
			st.markdown("### 5 Riddles")
			riddle_cols = st.columns(5)
			for idx, item in enumerate(riddle_bank):
				with riddle_cols[idx]:
					st.markdown(f"**R{idx + 1}**")
					st.write(item["question"])
					if st.button("Open", key=f"riddle_open_{idx}"):
						st.session_state.audience_modal = {"type": "riddle", "index": idx}
		with game_tab:
			st.markdown("### 5 Games")
			game_cols = st.columns(5)
			for idx, item in enumerate(game_bank):
				with game_cols[idx]:
					st.markdown(f"**Game {idx + 1}**")
					st.write(item["title"])
					if st.button("Play", key=f"game_open_{idx}"):
						st.session_state.audience_modal = {"type": "game", "index": idx}

		if st.session_state.audience_modal:
			modal = st.session_state.audience_modal
			if modal["type"] == "quiz":
				open_game_dialog("quiz", modal["index"])
			elif modal["type"] == "riddle":
				open_game_dialog("riddle", modal["index"])
			elif modal["type"] == "game":
				open_game_dialog("game", modal["index"])

		if st.button(t("back"), key="back_quiz_bottom"):
			set_service("home")
		return

	if service == "query":
		st.markdown("<div style='padding:1rem 1.2rem; border-radius:18px; background: rgba(0,0,0,0.46); border:1px solid rgba(255,255,255,0.12); margin-bottom:1rem;'><b>Query Center</b><br/>Submit the issue with your name, seat number, ticket ID, problem statement, and photo proof. It will be routed to the organiser queue for volunteer assignment.</div>", unsafe_allow_html=True)
		if st.button(t("back"), key="back_query_top"):
			set_service("home")

		with st.form("query_center_form", clear_on_submit=False):
			name = st.text_input("Name")
			seat_no = st.text_input("Seat No")
			ticket_id = st.text_input("Ticket ID")
			problem = st.text_area("Problem facing")
			proof = st.file_uploader("Upload one photo as proof", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
			submitted = st.form_submit_button("Raise Ticket")
		if submitted:
			entry = {
				"name": normalize_text(name),
				"seat_no": normalize_text(seat_no),
				"ticket_id": normalize_text(ticket_id),
				"problem": normalize_text(problem),
				"status": "Queued for organiser review",
			}
			st.session_state.audience_query_tickets.append(entry)
			st.session_state.audience_query_ticket_success = f"Ticket raised for seat {entry['seat_no'] or 'N/A'} and queued for organiser action."
			st.success(st.session_state.audience_query_ticket_success)

		if st.session_state.audience_query_tickets:
			st.markdown("### Recent tickets")
			st.table(st.session_state.audience_query_tickets[-5:])
			st.info("These queries will appear on the organiser side and be assigned to the available volunteer.")

		if st.button(t("back"), key="back_query_bottom"):
			set_service("home")
		return

	st.session_state.audience_service = "home"
	st.rerun()


def organizer_dashboard() -> None:
	st.title(" Organizer Command Center")
	st.success("You are logged in as an Organizer.")
	st.caption("Live stadium intelligence, crowd monitoring, volunteer dispatch, and match-day decision support.")

	intro_left, intro_right = st.columns(2)
	with intro_left:
		st.markdown("#### Vision")
		st.info(ORGANIZER_INTRO["vision"])
	with intro_right:
		st.markdown("#### Mission")
		st.info(ORGANIZER_INTRO["mission"])

	st.markdown("#### Core responsibilities")
	resp_cols = st.columns(4)
	for column, role_text in zip(resp_cols, ORGANIZER_INTRO["roles"]):
		with column:
			st.metric("Organizer focus", role_text, delta=None)

	st.markdown("### Participating countries and FIFA context")
	country_col, schedule_col = st.columns(2)
	with country_col:
		st.table([{ "Country": country, "Reason": note } for country, note in ORGANIZER_COUNTRIES])
	with schedule_col:
		st.table(ORGANIZER_SCHEDULE)

	st.markdown("### Stadium readiness and maintenance")
	stadium_choice = st.selectbox(
		"Select a host stadium",
		[item["stadium"] for item in ORGANIZER_STADIUM_STATUS],
		key="organizer_stadium_choice",
	)
	selected_stadium = next(item for item in ORGANIZER_STADIUM_STATUS if item["stadium"] == stadium_choice)
	readiness_cols = st.columns(4)
	with readiness_cols[0]:
		st.metric("Capacity", f'{selected_stadium["capacity"]:,}')
	with readiness_cols[1]:
		st.metric("Maintenance", selected_stadium["maintenance"])
	with readiness_cols[2]:
		st.metric("Cleaning", selected_stadium["cleaning"])
	with readiness_cols[3]:
		st.metric("Match ready", selected_stadium["ready"])
	st.write(f"Weather: {selected_stadium['weather']}")
	st.write(f"Notes: {selected_stadium['notes']}")

	st.markdown("### Crowd management and real-time decision support")
	crowd_cols = st.columns(3)
	with crowd_cols[0]:
		st.metric("Peak crowd pressure", "87%", delta="High attention")
	with crowd_cols[1]:
		st.metric("Queue intensity", "Moderate", delta="Gate 3 and Gate 4")
	with crowd_cols[2]:
		st.metric("Volunteer coverage", "92%", delta="Improving")
	st.progress(0.87)
	st.caption("AI suggestion: keep extra volunteers near the highest-pressure gate and broadcast a low-crowd exit route after halftime.")

	st.markdown("### Operational intelligence")
	st.line_chart(ORGANIZER_ANALYTICS)
	op_cols = st.columns(4)
	with op_cols[0]:
		st.metric("Average attendance", "80.8%")
	with op_cols[1]:
		st.metric("Average complaints", "4.0")
	with op_cols[2]:
		st.metric("Transport demand", "56.3")
	with op_cols[3]:
		st.metric("Volunteer fill rate", "82.5%")
	st.write("Filter-ready dashboard idea: attendance, crowd, transport, complaints, and volunteer productivity can each be sliced by match or stadium in a production version.")

	st.markdown("### Volunteer dispatch and sustainability/accessibility")
	dispatch_left, dispatch_right = st.columns(2)
	with dispatch_left:
		task_title = st.selectbox("Select a task to assign", [row["task"] for row in VOLUNTEER_QUEUE], key="organizer_task_choice")
		volunteer_name = st.text_input("Volunteer name", key="organizer_volunteer_name")
		if st.button("Assign Task", key="organizer_assign_task"):
			selected_task = next(row for row in VOLUNTEER_QUEUE if row["task"] == task_title)
			st.success(
				f"Assigned {selected_task['task']} to {volunteer_name or 'selected volunteer'} at {selected_task['location']} with priority {selected_task['priority']}."
			)
		st.table([{ "Issue": "Accessible route blocked", "Owner": "Volunteer team", "Status": "Pending" }, { "Issue": "Restroom cleaning", "Owner": "Facility crew", "Status": "In progress" }, { "Issue": "Water refill point", "Owner": "Volunteer team", "Status": "Done" }])
	with dispatch_right:
		st.table([
			{"Metric": "Water usage", "Status": "Stable"},
			{"Metric": "Energy demand", "Status": "Controlled"},
			{"Metric": "Waste sorting", "Status": "On track"},
			{"Metric": "Accessibility checks", "Status": "Needs closer monitoring"},
		])
		st.caption("Sustainability and accessibility recommendations are generated from volunteer status updates and post-match feedback.")

	st.markdown("### AI-generated match-day briefing")
	briefing = textwrap.dedent(
		"""
		- High-demand match detected at Lusail Stadium.
		- Gate 3 and Gate 4 need extra support during arrival and exit windows.
		- Cleaning is the only stadium component still lagging in one venue.
		- Accessibility issues should be escalated before the next fixture.
		- Volunteer coverage is strong enough to handle routine crowd support.
		"""
	).strip()
	st.text_area("Organizer AI summary", briefing, height=160)

	if st.button("Logout", key="organizer_logout"):
		reset_and_logout()


def volunteer_dashboard() -> None:
	st.title(" Volunteer Operations Panel")
	st.success("You are logged in as a Volunteer.")
	st.caption("Handle live tasks, feedback, and points that feed directly into organizer analytics.")

	if "volunteer_tasks" not in st.session_state:
		st.session_state.volunteer_tasks = [dict(item) for item in VOLUNTEER_QUEUE]
	if "volunteer_points" not in st.session_state:
		st.session_state.volunteer_points = sum(item["points"] for item in st.session_state.volunteer_tasks if item["status"] == "Done")

	intro_left, intro_right = st.columns(2)
	with intro_left:
		st.markdown("#### Vision")
		st.info(VOLUNTEER_INTRO["vision"])
	with intro_right:
		st.markdown("#### Mission")
		st.info(VOLUNTEER_INTRO["mission"])

	st.markdown("#### Core responsibilities")
	resp_cols = st.columns(4)
	for column, role_text in zip(resp_cols, VOLUNTEER_INTRO["roles"]):
		with column:
			st.metric("Volunteer focus", role_text, delta=None)

	st.markdown("### Task board")
	task_col, status_col = st.columns(2)
	with task_col:
		st.table(st.session_state.volunteer_tasks)
	with status_col:
		st.metric("Earned points", st.session_state.volunteer_points)
		st.metric("Completed tasks", sum(1 for item in st.session_state.volunteer_tasks if item["status"] == "Done"))
		st.metric("Open tasks", sum(1 for item in st.session_state.volunteer_tasks if item["status"] != "Done"))
		if st.button("Mark highest priority pending task as done", key="volunteer_complete_task"):
			for item in st.session_state.volunteer_tasks:
				if item["status"] != "Done":
					item["status"] = "Done"
					st.session_state.volunteer_points += item["points"]
					st.success(f"Updated {item['task']} to Done and earned {item['points']} points.")
					break

	st.markdown("### Feedback capture and AI insights")
	feedback_summary = analyze_feedback(FEEDBACK)
	feedback_cols = st.columns(3)
	with feedback_cols[0]:
		st.metric("Positive feedback", feedback_summary["sentiment_counts"]["positive"])
	with feedback_cols[1]:
		st.metric("Neutral feedback", feedback_summary["sentiment_counts"]["neutral"])
	with feedback_cols[2]:
		st.metric("Negative feedback", feedback_summary["sentiment_counts"]["negative"])
	st.write(f"Most reported issue: {feedback_summary['main_issue']}")
	st.write(f"AI recommendation: {feedback_summary['recommendation']}")

	st.markdown("### Weekly leaderboard and incentive tracking")
	st.table(VOLUNTEER_LEADERBOARD)
	st.caption("Organizers can use this ranking to review salary, bonuses, or recognition for high-performing volunteers.")

	st.markdown("### Support handoff")
	st.table([
		{"Query": "Lost child", "Escalation": "Security desk"},
		{"Query": "Medical help", "Escalation": "Medical team"},
		{"Query": "Wheelchair assistance", "Escalation": "Accessibility volunteer"},
		{"Query": "Water shortage", "Escalation": "Concourse support"},
	])

	if st.button("Logout", key="volunteer_logout"):
		reset_and_logout()


def render_hero() -> None:
	st.markdown(
		"""
		<div class="hero">
			<div class="eyebrow">FIFA 2026 Smart Operations</div>
			<h1>FIFA 2026 Ultimate Smart-Ops Hub</h1>
			<p>
				A premium operations portal for fans, organizers, and volunteers navigating
				live match-day intelligence, seamless coordination, and elevated stadium
				experiences for FIFA 2026.
			</p>
		</div>
		""",
		unsafe_allow_html=True,
	)


def render_role_cards() -> None:
	col1, col2, col3 = st.columns(3, gap="large")

	with col1:
		st.markdown(
			"""
			<div class="role-card">
				<h3>Audience</h3>
				<p>Step into the ultimate fan experience. Get seamless access to real-time stadium navigation, live transport updates, fast-lane ticketing, and multilingual AI assistance tailored for your FIFA 2026 journey.</p>
			</div>
			""",
			unsafe_allow_html=True,
		)
		if st.button("Continue as Audience", key="pick_audience", use_container_width=True):
			st.session_state.selected_role = "Audience"
			st.session_state.auth_error = None

	with col2:
		st.markdown(
			"""
			<div class="role-card">
				<h3>Organizer</h3>
				<p>Take total control of match-day operations. Monitor live crowd dynamics, track stadium maintenance, and leverage GenAI-powered operational intelligence to make split-second strategic decisions.</p>
			</div>
			""",
			unsafe_allow_html=True,
		)
		if st.button("Continue as Organizer", key="pick_organizer", use_container_width=True):
			st.session_state.selected_role = "Organizer"
			st.session_state.auth_error = None

	with col3:
		st.markdown(
			"""
			<div class="role-card">
				<h3>Volunteer</h3>
				<p>Be the heartbeat of the tournament. Receive automated task allocations, manage dynamic crowd assistance requests, and earn points on the live leaderboard for your critical on-ground support.</p>
			</div>
			""",
			unsafe_allow_html=True,
		)
		if st.button("Continue as Volunteer", key="pick_volunteer", use_container_width=True):
			st.session_state.selected_role = "Volunteer"
			st.session_state.auth_error = None



def dialog_shell(role: str, body_fn) -> None:
	if hasattr(st, "dialog"):

		@st.dialog(f"{role} Access")
		def _dialog() -> None:
			st.caption(f"Secure account access for {role.lower()} operations.")
			if st.session_state.auth_error:
				st.error(st.session_state.auth_error)
			login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
			with login_tab:
				body_fn("login")
			with signup_tab:
				body_fn("signup")
			if st.button("Close", key=f"close_{role.lower()}_dialog"):
				clear_login_dialog()

		_dialog()
		return

	with st.container(border=True):
		st.caption(f"Secure account access for {role.lower()} operations.")
		if st.session_state.auth_error:
			st.error(st.session_state.auth_error)
		login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
		with login_tab:
			body_fn("login")
		with signup_tab:
			body_fn("signup")
		if st.button("Close", key=f"close_{role.lower()}_dialog_fallback"):
			clear_login_dialog()


def render_audience_auth(mode: str) -> None:
	if mode == "login":
		with st.form("audience_login_form", clear_on_submit=False):
			email = st.text_input("Email", key="audience_login_email")
			password = st.text_input("Password", type="password", key="audience_login_password")
			submitted = st.form_submit_button("Login")
		if submitted:
			success, message, account = authenticate_user("Audience", email, password)
			if success and account:
				submit_account_success("Audience", account)
			st.session_state.auth_error = message
		return

	with st.form("audience_signup_form", clear_on_submit=False):
		name = st.text_input("Name", key="audience_signup_name")
		email = st.text_input("Email", key="audience_signup_email")
		password = st.text_input("Password", type="password", key="audience_signup_password")
		phone = st.text_input("Phone Number", key="audience_signup_phone")
		submitted = st.form_submit_button("Create Account")
	if submitted:
		success, message, account = register_user(
			"Audience",
			{
				"name": name,
				"email": email,
				"password": password,
				"phone": phone,
			},
		)
		if success and account:
			submit_account_success("Audience", account)
		st.session_state.auth_error = message


def render_organizer_auth(mode: str) -> None:
	if mode == "login":
		with st.form("organizer_login_form", clear_on_submit=False):
			username = st.text_input("Username", key="organizer_login_username")
			organizer_id = st.text_input("Organizer ID", key="organizer_login_organizer_id")
			submitted = st.form_submit_button("Login")
		if submitted:
			store = load_user_store()
			username_value = normalize_key(username)
			organizer_id_value = normalize_key(organizer_id)
			for account in store["Organizer"]:
				if normalize_key(account.get("username")) == username_value and normalize_key(account.get("organizer_id")) == organizer_id_value:
					submit_account_success("Organizer", account)
					break
			else:
				st.session_state.auth_error = "Organizer login failed. Check the Username and Organizer ID."
		return

	with st.form("organizer_signup_form", clear_on_submit=False):
		name = st.text_input("Name", key="organizer_signup_name")
		username = st.text_input("Username", key="organizer_signup_username")
		email = st.text_input("Email", key="organizer_signup_email")
		password = st.text_input("Password", type="password", key="organizer_signup_password")
		phone = st.text_input("Phone Number", key="organizer_signup_phone")
		organizer_id = st.text_input("Organizer ID", key="organizer_signup_id")
		submitted = st.form_submit_button("Create Account")
	if submitted:
		success, message, account = register_user(
			"Organizer",
			{
				"name": name,
				"username": username,
				"email": email,
				"password": password,
				"phone": phone,
				"organizer_id": organizer_id,
			},
		)
		if success and account:
			submit_account_success("Organizer", account)
		st.session_state.auth_error = message


def render_volunteer_auth(mode: str) -> None:
	if mode == "login":
		with st.form("volunteer_login_form", clear_on_submit=False):
			volunteer_id = st.text_input("Volunteer ID", key="volunteer_login_id")
			password = st.text_input("Password", type="password", key="volunteer_login_password")
			submitted = st.form_submit_button("Login")
		if submitted:
			success, message, account = authenticate_user("Volunteer", volunteer_id, password)
			if success and account:
				submit_account_success("Volunteer", account)
			st.session_state.auth_error = message
		return

	with st.form("volunteer_signup_form", clear_on_submit=False):
		name = st.text_input("Name", key="volunteer_signup_name")
		volunteer_id = st.text_input("Volunteer ID", key="volunteer_signup_id")
		email = st.text_input("Email", key="volunteer_signup_email")
		password = st.text_input("Password", type="password", key="volunteer_signup_password")
		phone = st.text_input("Phone Number", key="volunteer_signup_phone")
		submitted = st.form_submit_button("Create Account")
	if submitted:
		success, message, account = register_user(
			"Volunteer",
			{
				"name": name,
				"volunteer_id": volunteer_id,
				"email": email,
				"password": password,
				"phone": phone,
			},
		)
		if success and account:
			submit_account_success("Volunteer", account)
		st.session_state.auth_error = message


def render_role_dialog(role: str) -> None:
	body_map = {
		"Audience": render_audience_auth,
		"Organizer": render_organizer_auth,
		"Volunteer": render_volunteer_auth,
	}
	dialog_shell(role, body_map[role])


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
