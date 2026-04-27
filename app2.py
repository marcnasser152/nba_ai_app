import streamlit as st
import math
import hashlib
import pandas as pd

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="ODD FATHERS NBA", layout="wide")

# ----------------------------
# LOGIN (SECURE)
# ----------------------------
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

USERS = {
    "user": hash_pw("user123")
}

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
# TERMS
# ----------------------------
TERMS_TEXT = """
By using this app, you agree that all predictions are for informational purposes only.
No guarantees of profit or success.
"""

if "accepted_terms" not in st.session_state:
    st.session_state.accepted_terms = False

if not st.session_state.accepted_terms:
    st.title("📜 Terms & Conditions")
    st.write(TERMS_TEXT)

    agree = st.checkbox("I agree")

    if st.button("Continue"):
        if agree:
            st.session_state.accepted_terms = True
            st.rerun()
        else:
            st.error("You must agree")

    st.stop()

# ----------------------------
# TITLE
# ----------------------------
st.title("🏀🔥 ODD FATHERS NBA - AI Predictions")

# ----------------------------
# REAL TEAM DATA (STABLE)
# ----------------------------
TEAM_STATS = {
    "Lakers": {"off": 113.2, "def": 112.5, "pace": 101},
    "Celtics": {"off": 118.0, "def": 110.2, "pace": 99},
    "Bucks": {"off": 116.5, "def": 112.0, "pace": 100},
    "Nuggets": {"off": 117.2, "def": 111.8, "pace": 97},
    "Suns": {"off": 115.3, "def": 113.0, "pace": 98},
    "Warriors": {"off": 114.0, "def": 113.5, "pace": 102},
}

teams = list(TEAM_STATS.keys())

# ----------------------------
# SELECT MATCH
# ----------------------------
team1 = st.selectbox("Home Team", teams)
team2 = st.selectbox("Away Team", teams)

# ----------------------------
# MODEL
# ----------------------------
def predict(team1, team2):

    t1 = TEAM_STATS[team1]
    t2 = TEAM_STATS[team2]

    off1, def1, pace1 = t1["off"], t1["def"], t1["pace"]
    off2, def2, pace2 = t2["off"], t2["def"], t2["pace"]

    pace = (pace1 + pace2) / 2

    p1 = (off1 * pace / 100) - (def2 * 0.5)
    p2 = (off2 * pace / 100) - (def1 * 0.5)

    total = p1 + p2
    diff = p1 - p2

    home_prob = 100 / (1 + math.exp(-diff / 5))
    away_prob = 100 - home_prob

    return {
        "score": f"{int(p1)} - {int(p2)}",
        "home_prob": round(home_prob,1),
        "away_prob": round(away_prob,1),
        "total": round(total,1),
        "spread": round(diff,1)
    }

# ----------------------------
# RUN
# ----------------------------
if st.button("🚀 RUN AI ANALYSIS"):

    pred = predict(team1, team2)

    st.subheader(f"{team1} vs {team2}")

    st.write(f"🏀 Score Prediction: {pred['score']}")

    st.write("### 📊 Win Probability")
    st.progress(pred["home_prob"]/100)
    st.write(f"{team1}: {pred['home_prob']}%")
    st.write(f"{team2}: {pred['away_prob']}%")

    st.write("### 📈 Total Points")
    st.write(f"{pred['total']}")

    st.write("### 🎯 Spread")
    st.write(f"{team1} {pred['spread']}")

    chart_data = pd.DataFrame({
        "Team": [team1, team2],
        "Win %": [pred["home_prob"], pred["away_prob"]]
    }).set_index("Team")

    st.bar_chart(chart_data)

    confidence = abs(pred["spread"])

    if confidence > 10:
        st.success("🔥 HIGH CONFIDENCE PICK")
    elif confidence > 5:
        st.warning("⚠️ MEDIUM CONFIDENCE")
    else:
        st.info("❄️ LOW CONFIDENCE")
