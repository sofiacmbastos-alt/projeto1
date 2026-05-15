import streamlit as st
from datetime import date
from supabase import create_client, Client

SUPABASE_URL = "https://madsldtymrcyevpmwwup.supabase.co"
SUPABASE_KEY = "YOUR_ANON_KEY_HERE"

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

    /* BIG TITLE */
    .big-title {
        font-family: 'Monsieur La Doulaise', cursive;
        font-size: 150px;
        text-align: center;
        color: #d48ca3;
        line-height: 1;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    /* FORCE TEXT COLOR BACK */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 18px !important;
        color: #b76b86 !important;
    }

    /* HEADINGS */
    h1, h2, h3 {
        color: #c77c95 !important;
    }

    /* BUTTON */
    button {
        background-color: #f7a8c4 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
    }

    /* CARD */
    .card {
        background: white;
        padding: 14px;
        border-radius: 16px;
        margin-bottom: 10px;
        border: 1px solid #ffe4ec;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE (ONLY ONCE) ----------------
st.markdown("<div class='big-title'>Sofia's Reminders</div>", unsafe_allow_html=True)

# ---------------- ADD TASK ----------------
st.subheader("Add task")

new_task = st.text_input("")

if st.button("Add") and new_task:
    supabase.table("tasks").insert({
        "task": new_task,
        "done": False,
        "day": today
    }).execute()
    st.rerun()

# ---------------- LOAD DATA ----------------
response = supabase.table("tasks").select("*").execute()
tasks_data = response.data or []

today_tasks = [t for t in tasks_data if t["day"] == today]

# ---------------- TODAY ----------------
st.subheader("Today")

done_count = 0

for item in today_tasks:
    checked = st.checkbox(item["task"], value=item["done"], key=item["id"])

    if checked != item["done"]:
        supabase.table("tasks").update({
            "done": checked
        }).eq("id", item["id"]).execute()

    if checked:
        done_count += 1

total = len(today_tasks)

st.progress(done_count / total if total > 0 else 0)
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
