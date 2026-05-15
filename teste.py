import streamlit as st
from datetime import date
from supabase import create_client, Client

SUPABASE_URL = "https://madsldtymrcyevpmwwup.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hZHNsZHR5bXJjeWV2cG13d3VwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyNDcwMjMsImV4cCI6MjA5MzgyMzAyM30.qArWVNfbAJ-Xs4Osnpj2SEK1EvbW_awapIVzhH6xGNU"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

today = str(date.today())

st.set_page_config(page_title="Reminders", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Monsieur+La+Doulaise&family=Inter:wght@300;400;500&display=swap');

    .stApp {
        background-color: #FFF7FA;
        font-family: 'Inter', sans-serif;
    }

    .big-title {
        font-family: 'Monsieur La Doulaise', cursive;
        font-size: 150px;
        text-align: center;
        color: #d48ca3;
        line-height: 1;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 18px !important;
        color: #b76b86 !important;
    }

    h2, h3 {
        color: #c77c95 !important;
    }

    .card {
        background: white;
        padding: 14px;
        border-radius: 16px;
        margin-bottom: 10px;
        border: 1px solid #ffe4ec;
    }

    * {
        accent-color: #f7a8c4 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='big-title'>Sofia's Reminders</div>", unsafe_allow_html=True)

# ---------------- FIXED TASKS ----------------
tasks = ["Remedio 1", "Remedio 2", "Academia"]

# ---------------- LOAD DATA ----------------
response = supabase.table("tasks").select("*").execute()
tasks_data = response.data or []

today_tasks = [t for t in tasks_data if t["day"] == today]

# ---------------- TODAY ----------------
st.subheader("Today")

done_count = 0

for task in tasks:
    record = next((t for t in today_tasks if t["task"] == task), None)

    checked_value = record["done"] if record else False

    checked = st.checkbox(task, value=checked_value, key=task)

    if record:
        if checked != record["done"]:
            supabase.table("tasks").update({
                "done": checked
            }).eq("id", record["id"]).execute()
    else:
        if checked:
            supabase.table("tasks").insert({
                "task": task,
                "done": True,
                "day": today
            }).execute()

    if checked:
        done_count += 1

total = len(tasks)

st.progress(done_count / total)
st.write(f"{done_count}/{total} completed")

# ---------------- DASHBOARD ----------------
st.subheader("Dashboard")

for item in reversed(tasks_data):
    st.markdown(
        f"""
        <div class="card">
            <b>{item['task']}</b><br>
            {item['day']} · {'done' if item['done'] else 'not done'}
        </div>
        """,
        unsafe_allow_html=True
    )
