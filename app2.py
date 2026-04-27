import streamlit as st
import pandas as pd
import numpy as np
import math
from nba_api.stats.endpoints import leaguedashteamstats
import hashlib

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
TERMS_TEXT = """By using this app, you acknowledge this is analysis only. No guarantees."""

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
st.title("🏀🔥 ODD FATHERS NBA - REAL AI MODEL")

# ----------------------------
# LOAD REAL TEAM STATS
# ----------------------------
@st.cache_data
def load_team_data():
    df = leaguedashteamstats.LeagueDashTeamStats(
        season='2024-25',
        measure_type_detailed_defense='Advanced'
    ).get_data_frames()[0]

    df = df[[
        "TEAM_NAME",
        "OFF_RATING",
        "DEF_RATING",
        "PACE",
        "NET_RATING"
    ]]
    return df

teams_df = load_team_data()

# ----------------------------
# MATCH SELECTOR
# ----------------------------
teams = teams_df["TEAM_NAME"].tolist()

team1 = st.selectbox("Home Team", teams)
team2 = st.selectbox("Away Team", teams)

# ----------------------------
# MODEL
# ----------------------------
def predict_real(team1, team2):

    t1 = teams_df[teams_df["TEAM_NAME"] == team1].iloc[0]
    t2 = teams_df[teams_df["TEAM_NAME"] == team2].iloc[0]

    # Ratings
    off1, def1, pace1 = t1["OFF_RATING"], t1["DEF_RATING"], t1["PACE"]
    off2, def2, pace2 = t2["OFF_RATING"], t2["DEF_RATING"], t2["PACE"]

    # Combined pace
    pace = (pace1 + pace2) / 2

    # Expected points
    p1 = (off1 * pace / 100) - (def2 * 0.5)
    p2 = (off2 * pace / 100) - (def1 * 0.5)

    # Total
    total = p1 + p2
    diff = p1 - p2

    # Logistic win probability
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
if st.button("🚀 RUN REAL AI ANALYSIS"):

    pred = predict_real(team1, team2)

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

    # Chart
    chart_data = pd.DataFrame({
        "Team": [team1, team2],
        "Win %": [pred["home_prob"], pred["away_prob"]]
    }).set_index("Team")

    st.bar_chart(chart_data)

    # Confidence
    confidence = abs(pred["spread"])

    if confidence > 10:
        st.success("🔥 HIGH CONFIDENCE PICK")
    elif confidence > 5:
        st.warning("⚠️ MEDIUM CONFIDENCE")
    else:
        st.info("❄️ LOW CONFIDENCE")
