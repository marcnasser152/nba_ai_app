import streamlit as st
import random
import math

# ----------------------------
# LOGIN
# ----------------------------
USERS = {"user": "user123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def clean_username(u):
    return " ".join(u.strip().lower().split())

if not st.session_state.logged_in:
    st.title("🔐 ODD FATHERS NBA LOGIN")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if clean_username(username) in USERS and USERS[clean_username(username)] == password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.stop()

# ----------------------------
# PAGE
# ----------------------------
st.set_page_config(page_title="ODD FATHERS NBA", layout="wide")
st.title("🏀🔥 ODD FATHERS NBA - AI Predictions")

# ----------------------------
# FULL TERMS (FROM YOUR PDF)
# ----------------------------
TERMS_TEXT = """
ODD FATHERS VIP Channel Terms & Conditions Agreement

By joining, subscribing, or accessing this VIP channel, the member agrees to the following Terms & Conditions:

1. All content provided is for informational, educational, and entertainment purposes only and consists of sports analysis, statistical observations, and personal opinions.
2. We do not promote, encourage, operate, or facilitate gambling in any way, shape, or form.
3. We do not operate any betting platform and we do not accept bets, deposits, or withdrawals for any member.
4. We do not guarantee any wins, profits, success, or financial benefit. There are no guaranteed outcomes.
5. Members acknowledge that betting and financial decisions involve risk and may result in partial or total financial loss.
6. Members are fully responsible for any decisions, actions, bets, or financial activities they make.
7. We are not responsible for any losses, damages, claims, or financial consequences.
8. Nothing provided should be considered financial advice, investment advice, or professional advice.
9. Subscription fees are for access to informational content only and are non-refundable.
10. Sharing, distributing, forwarding, copying, or reselling VIP content is strictly prohibited.
11. We reserve the right to remove any member at any time if rules are violated.
12. The member agrees not to hold the channel owners or administrators liable for any financial losses or legal issues.
13. By agreeing, the member confirms that they have read, understood, and accepted all terms.
"""  # :contentReference[oaicite:0]{index=0}

if "accepted_terms" not in st.session_state:
    st.session_state.accepted_terms = False

if not st.session_state.accepted_terms:
    st.title("📜 Terms & Conditions")

    st.markdown("### ODD FATHERS VIP Terms & Conditions")

    st.markdown(f"""
    <div style="
        height:420px;
        overflow-y:auto;
        padding:20px;
        border-radius:10px;
        background-color:#111;
        color:white;
        font-size:15px;
        line-height:1.6;
        border:1px solid #333;
    ">
    {TERMS_TEXT}
    </div>
    """, unsafe_allow_html=True)

    agree = st.checkbox("I have read and agree to the Terms & Conditions")

    if st.button("Continue"):
        if agree:
            st.session_state.accepted_terms = True
            st.rerun()
        else:
            st.error("You must agree before continuing")

    st.stop()

# ----------------------------
# MATCHES
# ----------------------------
def get_matches():
    return [
        {"home":"Knicks","away":"Hawks"},
        {"home":"Lakers","away":"Rockets"},
        {"home":"Celtics","away":"76ers"},
        {"home":"Thunder","away":"Suns"},
    ]

# ----------------------------
# PLAYER DATA
# ----------------------------
PLAYER_STATS = {
    "Knicks": ("Brunson", 26),
    "Hawks": ("Trae Young", 27),
    "Lakers": ("LeBron James", 27),
    "Rockets": ("Jalen Green", 23),
    "Celtics": ("Jayson Tatum", 28),
    "76ers": ("Joel Embiid", 30),
    "Thunder": ("SGA", 30),
    "Suns": ("Devin Booker", 27),
}

# ----------------------------
# TEAM STRENGTH
# ----------------------------
def get_team_strength(name):
    base = sum(ord(c) for c in name)
    random.seed(base)

    offense = random.uniform(108, 118)
    defense = random.uniform(105, 115)

    return offense, defense

# ----------------------------
# NORMAL DISTRIBUTION
# ----------------------------
def normal_prob(mean, std, threshold):
    z = (threshold - mean) / std
    return 100 * (1 - (0.5 * (1 + math.erf(z / math.sqrt(2)))))

# ----------------------------
# PREDICT
# ----------------------------
def predict(team1, team2):

    off1, def1 = get_team_strength(team1)
    off2, def2 = get_team_strength(team2)

    p1 = (off1 + def2) / 2 + random.uniform(-3, 3)
    p2 = (off2 + def1) / 2 + random.uniform(-3, 3)

    total = p1 + p2
    diff = p1 - p2

    home_prob = max(35, min(65, 50 + diff*2))
    away_prob = 100 - home_prob

    # realistic totals probability
    std = 12
    over220 = normal_prob(total, std, 220)
    over230 = normal_prob(total, std, 230)

    # ----------------------------
    # REALISTIC PLAYER PROPS
    # ----------------------------
    p1_name, p1_avg = PLAYER_STATS.get(team1, ("Star", 25))
    p2_name, p2_avg = PLAYER_STATS.get(team2, ("Star", 25))

    pace = total / 220
    boost1 = diff / 10
    boost2 = -diff / 10

    p1_points = p1_avg * pace + boost1 + random.uniform(-2, 2)
    p2_points = p2_avg * pace + boost2 + random.uniform(-2, 2)

    return {
        "score": f"{int(p1)} - {int(p2)}",
        "home": round(home_prob,1),
        "away": round(away_prob,1),
        "total": round(total,1),
        "spread": round(diff,1),
        "over220": round(over220,1),
        "over230": round(over230,1),
        "p1_name": p1_name,
        "p1_points": round(p1_points,1),
        "p2_name": p2_name,
        "p2_points": round(p2_points,1),
    }

# ----------------------------
# UI
# ----------------------------
matches = get_matches()

options = [f"{m['home']} vs {m['away']}" for m in matches]

selected = st.selectbox("Select Game", options)

match = matches[options.index(selected)]

# ----------------------------
# RUN
# ----------------------------
if st.button("🚀 RUN AI ANALYSIS"):

    pred = predict(match["home"], match["away"])

    st.subheader(f"{match['home']} vs {match['away']}")
    st.write(f"🏀 Score: {pred['score']}")

    st.write("### 📊 Win Probability")
    st.write(f"{match['home']}: {pred['home']}%")
    st.write(f"{match['away']}: {pred['away']}%")

    st.write("### 📈 Totals")
    st.write(f"Total Points: {pred['total']}")
    st.write(f"Over 220: {pred['over220']}%")
    st.write(f"Over 230: {pred['over230']}%")

    st.write("### 🎯 Spread")
    st.write(f"{match['home']} {pred['spread']}")

    st.write("### ⭐ Player Props")
    st.write(f"{pred['p1_name']}: {pred['p1_points']} pts")
    st.write(f"{pred['p2_name']}: {pred['p2_points']} pts")