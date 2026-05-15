import streamlit as st
from datetime import date, timedelta
from supabase import create_client, Client

SUPABASE_URL = "https://madsldtymrcyevpmwwup.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hZHNsZHR5bXJjeWV2cG13d3VwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyNDcwMjMsImV4cCI6MjA5MzgyMzAyM30.qArWVNfbAJ-Xs4Osnpj2SEK1EvbW_awapIVzhH6xGNU"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

today = str(date.today())

st.set_page_config(page_title="Pink Habit Tracker", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Monsieur+La+Doulaise&family=Inter:wght@300;400;500&display=swap');

    .stApp {
        background-color: #FFF7FA;
        font-family: 'Inter', sans-serif;
    }

    .title {
        font-family: 'Monsieur La Doulaise', cursive;
        font-size: 140px;
        text-align: center;
        color: #d48ca3;
        margin-bottom: 10px;
    }

    .card {
        background: white;
        padding: 14px;
        border-radius: 16px;
        margin-bottom: 10px;
        border: 1px solid #ffe4ec;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.04);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #b76b86 !important;
        font-size: 18px !important;
    }

    * {
        accent-color: #f7a8c4 !important;
    }

    .stProgress > div > div > div > div {
        background-color: #f7a8c4 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>Sofia’s Habit Tracker</div>", unsafe_allow_html=True)

# ---------------- HABITS ----------------
habits = ["Remedio 1", "Remedio 2", "Academia"]

# ---------------- LOAD DATA ----------------
response = supabase.table("tasks").select("*").execute()
data = response.data or []

today_data = [d for d in data if d["day"] == today]

# ---------------- STREAK CALC ----------------
def get_streak():
    streak = 0
    current_day = date.today()

    for i in range(30):  # check last 30 days
        day_str = str(current_day - timedelta(days=i))
        day_tasks = [d for d in data if d["day"] == day_str]

        if not day_tasks:
            break

        if all(d["done"] for d in day_tasks):
            streak += 1
        else:
            break

    return streak

streak = get_streak()

st.markdown(f"### 🔥 Streak: {streak} days")

# ---------------- TODAY HABITS ----------------
st.subheader("Today")

done_count = 0

for habit in habits:
    record = next((t for t in today_data if t["task"] == habit), None)

    value = record["done"] if record else False

    checked = st.checkbox(habit, value=value, key=habit)

    if record:
        if checked != record["done"]:
            supabase.table("tasks").update({
                "done": checked
            }).eq("id", record["id"]).execute()
    else:
        if checked:
            supabase.table("tasks").insert({
                "task": habit,
                "done": True,
                "day": today
            }).execute()

    if checked:
        done_count += 1

total = len(habits)

st.progress(done_count / total)
st.write(f"{done_count}/{total} completed 💗")

# ---------------- AUTO RESET LOGIC ----------------
st.markdown(
    "<p style='text-align:center;color:#d48ca3;'>resets automatically every midnight 💕</p>",
    unsafe_allow_html=True
)
