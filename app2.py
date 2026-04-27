import streamlit as st
import math
import hashlib
import pandas as pd
import random

st.set_page_config(page_title="ODD FATHERS NBA", layout="wide")

# ----------------------------
# LOGIN
# ----------------------------
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

USERS = {"user": hash_pw("user123")}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def clean_username(u):
    return " ".join(u.strip().lower().split())

if not st.session_state.logged_in:
    st.title("🔐 ODD FATHERS NBA LOGIN")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if clean_username(username) in USERS and USERS[clean_username(username)] == hash_pw(password):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.stop()

# ----------------------------
# TITLE
# ----------------------------
st.title("🏀🔥 ODD FATHERS NBA - AI Predictions")

# ----------------------------
# TEAM DATA (IMPROVED)
# ----------------------------
TEAM_STATS = {
    "Lakers": {"off": 113, "def": 112, "pace": 101},
    "Celtics": {"off": 118, "def": 110, "pace": 99},
    "Bucks": {"off": 117, "def": 112, "pace": 100},
    "Nuggets": {"off": 117, "def": 111, "pace": 97},
    "Suns": {"off": 115, "def": 113, "pace": 98},
    "Warriors": {"off": 114, "def": 113, "pace": 102},
    "76ers": {"off": 116, "def": 111, "pace": 99},
    "Knicks": {"off": 115, "def": 112, "pace": 96},
    "Heat": {"off": 112, "def": 111, "pace": 95},
    "Cavaliers": {"off": 113, "def": 110, "pace": 97},
    "Hawks": {"off": 116, "def": 115, "pace": 102},
    "Rockets": {"off": 113, "def": 113, "pace": 100},
    "Thunder": {"off": 117, "def": 111, "pace": 101},
    "Mavericks": {"off": 117, "def": 113, "pace": 99},
}

PLAYER_STATS = {
    "Lakers": ("LeBron James", 27),
    "Celtics": ("Jayson Tatum", 28),
    "Bucks": ("Giannis", 30),
    "Nuggets": ("Jokic", 29),
    "Suns": ("Booker", 27),
    "Warriors": ("Curry", 29),
    "76ers": ("Embiid", 30),
    "Knicks": ("Brunson", 26),
    "Heat": ("Butler", 24),
    "Cavaliers": ("Mitchell", 28),
    "Hawks": ("Trae Young", 27),
    "Rockets": ("Jalen Green", 23),
    "Thunder": ("SGA", 30),
    "Mavericks": ("Luka Doncic", 32),
}

teams = list(TEAM_STATS.keys())

team1 = st.selectbox("Home Team", teams)
team2 = st.selectbox("Away Team", teams)

if team1 == team2:
    st.warning("Select different teams")
    st.stop()

# ----------------------------
# MODEL
# ----------------------------
def normal_prob(mean, std, threshold):
    z = (threshold - mean) / std
    return 100 * (1 - (0.5 * (1 + math.erf(z / math.sqrt(2)))))

def predict(team1, team2):

    t1 = TEAM_STATS[team1]
    t2 = TEAM_STATS[team2]

    off1, def1, pace1 = t1["off"], t1["def"], t1["pace"]
    off2, def2, pace2 = t2["off"], t2["def"], t2["pace"]

    pace = (pace1 + pace2) / 2

    # REALISTIC NBA SCORING
    p1 = (off1 / 100) * pace + random.uniform(-5, 5)
    p2 = (off2 / 100) * pace + random.uniform(-5, 5)

    total = p1 + p2
    diff = p1 - p2

    home_prob = 100 / (1 + math.exp(-diff / 6))
    away_prob = 100 - home_prob

    std = 12
    over220 = normal_prob(total, std, 220)
    over230 = normal_prob(total, std, 230)

    # PLAYER PROPS
    p1_name, p1_avg = PLAYER_STATS[team1]
    p2_name, p2_avg = PLAYER_STATS[team2]

    p1_points = p1_avg + (diff / 8) + random.uniform(-3, 3)
    p2_points = p2_avg - (diff / 8) + random.uniform(-3, 3)

    return {
        "score": f"{int(p1)} - {int(p2)}",
        "home_prob": round(home_prob,1),
        "away_prob": round(away_prob,1),
        "total": round(total,1),
        "spread": round(diff,1),
        "team1_total": round(p1,1),
        "team2_total": round(p2,1),
        "over220": round(over220,1),
        "over230": round(over230,1),
        "p1_name": p1_name,
        "p1_points": round(p1_points,1),
        "p2_name": p2_name,
        "p2_points": round(p2_points,1),
    }

# ----------------------------
# RUN
# ----------------------------
if st.button("🚀 RUN AI ANALYSIS"):

    pred = predict(team1, team2)

    st.subheader(f"{team1} vs {team2}")

    st.write(f"🏀 Score: {pred['score']}")

    st.write("### 📊 Win Probability")
    st.progress(pred["home_prob"]/100)
    st.write(f"{team1}: {pred['home_prob']}%")
    st.write(f"{team2}: {pred['away_prob']}%")

    st.write("### 📈 Totals")
    st.write(f"Game Total: {pred['total']}")
    st.write(f"{team1} Total: {pred['team1_total']}")
    st.write(f"{team2} Total: {pred['team2_total']}")

    st.write("### 🎯 Over/Under")
    st.write(f"Over 220: {pred['over220']}%")
    st.write(f"Over 230: {pred['over230']}%")

    st.write("### 🏀 Spread")
    st.write(f"{team1} {pred['spread']}")

    st.write("### ⭐ Player Props")
    st.write(f"{pred['p1_name']}: {pred['p1_points']} pts")
    st.write(f"{pred['p2_name']}: {pred['p2_points']} pts")

    # Chart
    chart = pd.DataFrame({
        "Team": [team1, team2],
        "Win %": [pred["home_prob"], pred["away_prob"]]
    }).set_index("Team")

    st.bar_chart(chart)
