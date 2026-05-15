import streamlit as st
from datetime import date, timedelta
from supabase import create_client, Client

SUPABASE_URL = "https://madsldtymrcyevpmwwup.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hZHNsZHR5bXJjeWV2cG13d3VwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyNDcwMjMsImV4cCI6MjA5MzgyMzAyM30.qArWVNfbAJ-Xs4Osnpj2SEK1EvbW_awapIVzhH6xGNU"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

today = date.today()

st.set_page_config(page_title="Pink Habit Tracker", layout="wide")

# ---------------- STYLE ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');

    .stApp {
        background-color: #FFF7FA;
        font-family: 'Inter', sans-serif;
    }

    .title {
        font-size: 90px;
        text-align: center;
        color: #d48ca3;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        margin-bottom: 20px;
    }

    /* iPhone toggle */
    .switch {
      position: relative;
      display: inline-block;
      width: 52px;
      height: 30px;
    }

    .switch input { display: none; }

    .slider {
      position: absolute;
      cursor: pointer;
      top: 0; left: 0; right: 0; bottom: 0;
      background-color: #f3c6d3;
      transition: .4s;
      border-radius: 30px;
    }

    .slider:before {
      position: absolute;
      content: "";
      height: 22px;
      width: 22px;
      left: 4px;
      bottom: 4px;
      background-color: white;
      transition: .4s;
      border-radius: 50%;
    }

    input:checked + .slider {
      background-color: #d48ca3;
    }

    input:checked + .slider:before {
      transform: translateX(22px);
    }

    /* card */
    .card {
        background: white;
        padding: 12px;
        border-radius: 14px;
        margin-bottom: 8px;
        border: 1px solid #ffe4ec;
    }

    /* badge */
    .badge {
        padding: 8px 14px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 10px;
        font-weight: 500;
    }

    .pink { background: #ffd6e7; color: #a85b7a; }
    .silver { background: #f0f0f0; color: #777; }
    .gold { background: #ffe6a7; color: #8a6b00; }

    /* calendar */
    .cal {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        margin-top: 10px;
    }

    .day {
        width: 100%;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-size: 12px;
        background: #ffe4ec;
    }

    .done {
        background: #f7a8c4;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>Sofia’s Habit Tracker</div>", unsafe_allow_html=True)

# ---------------- HABITS ----------------
habits = ["Remedio 1", "Remedio 2", "Academia"]

data = supabase.table("tasks").select("*").execute().data or []

today_str = str(today)

today_data = [d for d in data if d["day"] == today_str]

# ---------------- STREAK ----------------
def get_streak():
    streak = 0
    current = today

    for i in range(30):
        day = str(current - timedelta(days=i))
        day_tasks = [d for d in data if d["day"] == day]

        if not day_tasks:
            break

        if all(d["done"] for d in day_tasks):
            streak += 1
        else:
            break

    return streak

streak = get_streak()

# ---------------- BADGES ----------------
if streak >= 30:
    badge = "gold"
elif streak >= 7:
    badge = "silver"
else:
    badge = "pink"

st.markdown(f"<div class='badge {badge}'>Streak: {streak} days</div>", unsafe_allow_html=True)

# ---------------- TOGGLES ----------------
st.subheader("Today")

done_count = 0

for habit in habits:
    record = next((t for t in today_data if t["task"] == habit), None)
    value = record["done"] if record else False

    col1, col2 = st.columns([1, 8])

    with col1:
        checked = st.checkbox("", value=value, key=habit)

    with col2:
        st.write(habit)

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
                "day": today_str
            }).execute()

    if checked:
        done_count += 1

st.progress(done_count / len(habits))

# ---------------- CALENDAR HEATMAP ----------------
st.subheader("Calendar")

last_days = [today - timedelta(days=i) for i in range(21)][::-1]

cal_html = "<div class='cal'>"

for d in last_days:
    d_str = str(d)
    day_tasks = [x for x in data if x["day"] == d_str]

    if day_tasks and all(x["done"] for x in day_tasks):
        cal_html += f"<div class='day done'>{d.day}</div>"
    else:
        cal_html += f"<div class='day'>{d.day}</div>"

cal_html += "</div>"

st.markdown(cal_html, unsafe_allow_html=True)
