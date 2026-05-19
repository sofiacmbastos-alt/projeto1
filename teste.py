import streamlit as st
from datetime import date, timedelta
from supabase import create_client
import calendar

# ---------------- SUPABASE ----------------
SUPABASE_URL = "https://madsldtymrcyevpmwwup.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY_HERE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

today = date.today()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Sofia", layout="centered")

# ---------------- REMOVE STREAMLIT UI ----------------
st.markdown("""
<style>
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

.block-container {
    padding-top: 0rem !important;
}

.stApp {
    background: linear-gradient(to bottom, #ffeef5, #ffdce8);
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MAIN STYLE ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');

.phone {
    width: 390px;
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(14px);
    border-radius: 40px;
    padding: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.title {
    font-size: 52px;
    text-align: center;
    color: #d48ca3;
    font-weight: 600;
    font-family: Inter;
}

.subtitle {
    text-align: center;
    color: #c98aa1;
    font-size: 14px;
    margin-bottom: 10px;
}

.badge {
    text-align: center;
    padding: 6px 12px;
    border-radius: 20px;
    background: #ffd6e7;
    color: #a85b7a;
    font-size: 13px;
    margin-bottom: 10px;
}

.day {
    aspect-ratio: 1/1;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fff4f8;
    color: #b76b86;
    font-size: 13px;
    transition: 0.2s;
}

.day.done {
    background: linear-gradient(135deg, #f8b6cc, #f3c4ff);
    color: white;
    box-shadow: 0 6px 16px rgba(248,182,204,0.35);
}

.day.today {
    border: 2px solid #d48ca3;
    font-weight: bold;
}

.day:hover {
    transform: scale(1.05);
}

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
    margin-top: 10px;
}

.weekday {
    text-align: center;
    font-size: 11px;
    color: #c98aa1;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ---------------- WRAPPER ----------------
st.markdown("<div class='phone'>", unsafe_allow_html=True)

st.markdown("<div class='title'>Sofia</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>habit tracker</div>", unsafe_allow_html=True)

# ---------------- DATA ----------------
habits = ["💊 Remedio 1", "💊 Remedio 2", "🏋️ Academia"]

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
        if all(x["done"] for x in day_tasks):
            streak += 1
        else:
            break

    return streak

st.markdown(
    f"<div class='badge'>🔥 Streak: {streak_calc()} days</div>",
    unsafe_allow_html=True
)

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

cal = calendar.Calendar(firstweekday=0)
month_days = list(cal.itermonthdates(year, month))

weekdays = ["M", "T", "W", "T", "F", "S", "S"]

html = "<div class='calendar-grid'>"

for w in weekdays:
    html += f"<div class='weekday'>{w}</div>"

for d in month_days:

    if d.month != month:
        html += "<div></div>"
        continue

    d_str = str(d)
    day_data = [x for x in data if x["day"] == d_str]

    classes = "day"

    if day_data and all(x["done"] for x in day_data):
        classes += " done"

    if d == today:
        classes += " today"

    html += f"<div class='{classes}'>{d.day}</div>"

html += "</div>"

st.markdown(html, unsafe_allow_html=True)

# ---------------- END ----------------
st.markdown("</div>", unsafe_allow_html=True)
