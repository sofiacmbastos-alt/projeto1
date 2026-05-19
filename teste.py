import streamlit as st
from datetime import date, timedelta
from supabase import create_client, Client
import calendar

SUPABASE_URL = "https://madsldtymrcyevpmwwup.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hZHNsZHR5bXJjeWV2cG13d3VwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyNDcwMjMsImV4cCI6MjA5MzgyMzAyM30.qArWVNfbAJ-Xs4Osnpj2SEK1EvbW_awapIVzhH6xGNU"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

today = date.today()

st.set_page_config(page_title="Habit", layout="centered")

# ---------------- STYLE FIX ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Monsieur+La+Doulaise&family=Inter:wght@300;400;500&display=swap');

    .stApp {
        background: #ffeef5;
        font-family: 'Inter', sans-serif;
        display: flex;
        justify-content: center;
    }

    /* PHONE FRAME */
    .phone {
        width: 390px;
        background: #fff7fa;
        border-radius: 40px;
        padding: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        margin-top: 20px;
    }

    /* BIG PINK TITLE (RESTORED FONT) */
    .title {
        font-family: 'Monsieur La Doulaise', cursive;
        font-size: 90px;
        text-align: center;
        color: #d48ca3;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #d48ca3;
        font-size: 14px;
        margin-bottom: 10px;
    }

    /* TEXT FIX (PREVENT BLACK TEXT) */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #b76b86 !important;
    }

    /* CARD */
    .card {
        background: white;
        border-radius: 18px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid #ffe4ec;
    }

    /* STREAK BADGE */
    .badge {
        text-align: center;
        padding: 6px 12px;
        border-radius: 20px;
        background: #ffd6e7;
        color: #a85b7a;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* CALENDAR */
    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        margin-top: 10px;
    }

    .day {
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        font-size: 12px;
        background: #ffe4ec;
        color: #b76b86;
    }

    .done {
        background: #f7a8c4;
        color: white;
    }

    /* PROGRESS PINK */
    .stProgress > div > div > div > div {
        background-color: #f7a8c4 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- PHONE WRAPPER ----------------
st.markdown("<div class='phone'>", unsafe_allow_html=True)

st.markdown("<div class='title'>Sofia</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>habit tracker</div>", unsafe_allow_html=True)

# ---------------- DATA ----------------
habits = ["Remedio 1", "Remedio 2", "Academia"]

data = supabase.table("tasks").select("*").execute().data or []

today_str = str(today)

today_data = [d for d in data if d["day"] == today_str]

# ---------------- STREAK ----------------
def streak_calc():
    streak = 0
    current = today

    for i in range(60):
        day = str(current - timedelta(days=i))
        day_tasks = [d for d in data if d["day"] == day]

        if not day_tasks:
            break

        if all(d["done"] for d in day_tasks):
            streak += 1
        else:
            break

    return streak

streak = streak_calc()

st.markdown(f"<div class='badge'>Streak: {streak} days</div>", unsafe_allow_html=True)

# ---------------- HABITS ----------------
st.subheader("Today")

done = 0

for h in habits:
    record = next((x for x in today_data if x["task"] == h), None)
    value = record["done"] if record else False

    checked = st.checkbox(h, value=value, key=h)

    if record:
        if checked != record["done"]:
            supabase.table("tasks").update({"done": checked}).eq("id", record["id"]).execute()
    else:
        if checked:
            supabase.table("tasks").insert({
                "task": h,
                "done": True,
                "day": today_str
            }).execute()

    if checked:
        done += 1

st.progress(done / len(habits))

# ---------------- CALENDAR ----------------
st.subheader("Calendar")

year = today.year
month = today.month

month_name = calendar.month_name[month]

# WEEKDAY LABELS
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

cal = calendar.Calendar(firstweekday=0)
month_days = list(cal.itermonthdates(year, month))

html = f"""
<style>
.calendar-wrapper {{
    margin-top: 10px;
}}

.calendar-title {{
    text-align: center;
    font-size: 18px;
    color: #c77995;
    margin-bottom: 12px;
    font-weight: 600;
}}

.calendar-grid {{
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
}}

.weekday {{
    text-align: center;
    font-size: 11px;
    color: #c98aa1;
    margin-bottom: 4px;
    font-weight: 600;
}}

.day {{
    aspect-ratio: 1 / 1;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ffe8f0;
    color: #b76b86;
    font-size: 13px;
    transition: 0.2s;
    border: 1px solid transparent;
}}

.day:hover {{
    transform: scale(1.05);
}}

.done {{
    background: linear-gradient(135deg, #f7a8c4, #f3bfd1);
    color: white;
    box-shadow: 0 4px 12px rgba(247,168,196,0.35);
}}

.today {{
    border: 2px solid #d48ca3;
    font-weight: bold;
}}

.empty {{
    visibility: hidden;
}}
</style>

<div class="calendar-wrapper">
<div class="calendar-title">{month_name} {year}</div>

<div class="calendar-grid">
"""

# WEEKDAY ROW
for w in weekdays:
    html += f"<div class='weekday'>{w}</div>"

# DAYS
for d in month_days:

    if d.month != month:
        html += "<div class='day empty'></div>"
        continue

    d_str = str(d)
    day_data = [x for x in data if x["day"] == d_str]

    classes = "day"

    # completed day
    if day_data and all(x["done"] for x in day_data):
        classes += " done"

    # today highlight
    if d == today:
        classes += " today"

    html += f"<div class='{classes}'>{d.day}</div>"

html += "</div></div>"

st.markdown(html, unsafe_allow_html=True)
