import streamlit as st
from datetime import date
from supabase import create_client, Client

# ---------------- SUPABASE SETUP ----------------
SUPABASE_URL = "https://madsldtymrcyevpmwwup.supabase.co"
SUPABASE_KEY = "sb_publishable_TZvbGUtBqfmIQIWB_XMWhQ_-y6Bd1un"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

today = str(date.today())

# ---------------- STYLE ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Monsieur+La+Doulaise&display=swap');

    .stApp {
        background-color: #FFF7FA;
    }

    h1, h2 {
        font-family: 'Monsieur La Doulaise', cursive;
        color: #d48ca3 !important;
        text-align: center;
    }

    * {
        accent-color: #f7a8c4 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>Sofia's Reminders 🌸</h1>", unsafe_allow_html=True)

# ---------------- ADD TASK ----------------
st.subheader("Add new task ✨")

new_task = st.text_input("New task")

if st.button("Add 💖") and new_task:
    supabase.table("tasks").insert({
        "task": new_task,
        "done": False,
        "day": today
    }).execute()

# ---------------- LOAD TASKS ----------------
response = supabase.table("tasks").select("*").eq("day", today).execute()
tasks_data = response.data

# ---------------- DISPLAY TASKS ----------------
st.subheader("Today 🌸")

done_count = 0

for item in tasks_data:
    checked = st.checkbox(item["task"], value=item["done"], key=item["id"])

    if checked != item["done"]:
        supabase.table("tasks").update({
            "done": checked
        }).eq("id", item["id"]).execute()

    if checked:
        done_count += 1

# ---------------- PROGRESS ----------------
total = len(tasks_data)

st.progress(done_count / total if total > 0 else 0)
st.write(f"{done_count}/{total} completed 🌸")

# ---------------- HISTORY ----------------
st.subheader("Calendar view 📅")

all_data = supabase.table("tasks").select("*").order("day", desc=True).execute().data

for item in all_data:
    status = "💖 done" if item["done"] else "🤍 not done"

    st.markdown(
        f"""
        <div style="
            background:white;
            padding:12px;
            border-radius:14px;
            margin-bottom:8px;
            border:1px solid #ffe4ec;">
            <b>{item['day']}</b><br>
            {item['task']} — {status}
        </div>
        """,
        unsafe_allow_html=True
    )
