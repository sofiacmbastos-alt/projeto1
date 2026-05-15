import streamlit as st
from datetime import date
from supabase import create_client, Client

SUPABASE_URL = "https://madsldtymrcyevpmwwup.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hZHNsZHR5bXJjeWV2cG13d3VwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyNDcwMjMsImV4cCI6MjA5MzgyMzAyM30.qArWVNfbAJ-Xs4Osnpj2SEK1EvbW_awapIVzhH6xGNU"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

today = str(date.today())

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Monsieur+La+Doulaise&family=Inter:wght@300;400;500&display=swap');

    .stApp {
        background-color: #FFF7FA;
        font-family: 'Inter', sans-serif;
    }

    h1 {
        font-family: 'Monsieur La Doulaise', cursive;
        font-size: 75px;
        text-align: center;
        color: #d48ca3;
    }

    h2, h3, p, label {
        color: #b76b86 !important;
    }

    * {
        accent-color: #f7a8c4 !important;
    }

    .card {
        background: white;
        padding: 14px;
        border-radius: 16px;
        margin-bottom: 10px;
        border: 1px solid #ffe4ec;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.04);
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>Sofia's Reminders</h1>", unsafe_allow_html=True)

st.subheader("Add task")

new_task = st.text_input(" ")

if st.button("Add") and new_task:
    supabase.table("tasks").insert({
        "task": new_task,
        "done": False,
        "day": today
    }).execute()
    st.rerun()

response = supabase.table("tasks").select("*").execute()
tasks_data = response.data or []

today_tasks = [t for t in tasks_data if t["day"] == today]

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

st.subheader("Dashboard")

for item in reversed(tasks_data):
    status = "done" if item["done"] else "not done"

    st.markdown(
        f"""
        <div class="card">
            <b>{item['task']}</b><br>
            {item['day']} · {status}
        </div>
        """,
        unsafe_allow_html=True
    )
