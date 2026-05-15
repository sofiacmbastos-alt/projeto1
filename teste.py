import streamlit as st
from datetime import date
from supabase import create_client, Client

SUPABASE_URL = "https://madsldtymrcyevpmwwup.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

today = str(date.today())

st.set_page_config(page_title="Reminders", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Monsieur+La+Doulaise&display=swap');

    .stApp {
        background-color: #FFF7FA;
    }

    /* MAIN FONT */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #b76b86;
    }

    /* TITLE */
    h1 {
        font-family: 'Monsieur La Doulaise', cursive;
        font-size: 78px;
        text-align: center;
        color: #d48ca3;
        margin-bottom: 0px;
    }

    h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #c77c95;
        font-weight: 600;
    }

    /* REMOVE BLUE */
    * {
        accent-color: #f7a8c4 !important;
    }

    /* INPUT */
    input {
        border-radius: 12px !important;
    }

    /* BUTTON */
    button {
        background-color: #f7a8c4 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
    }

    button:hover {
        background-color: #f28fb6 !important;
    }

    /* CHECKBOX */
    [data-testid="stCheckbox"] label {
        font-size: 18px;
        color: #b76b86 !important;
    }

    /* PROGRESS BAR */
    [data-testid="stProgress"] > div > div {
        background-color: #ffe4ec !important;
    }

    [data-testid="stProgress"] > div > div > div {
        background-color: #f7a8c4 !important;
    }

    /* CARD (Pinterest / Notion style) */
    .card {
        background: white;
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 10px;
        border: 1px solid #ffe4ec;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.04);
        transition: 0.2s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 18px rgba(0,0,0,0.06);
    }

    /* CLEAN TEXT */
    .task-text {
        font-size: 16px;
        font-weight: 500;
        color: #b76b86;
    }

    .status {
        font-size: 13px;
        color: #d48ca3;
        margin-top: 4px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>Sofia’s Reminders</h1>", unsafe_allow_html=True)

st.write("Minimal daily system for focus and consistency")

st.subheader("Add task")

new_task = st.text_input("")

if st.button("Add"):
    if new_task:
        supabase.table("tasks").insert({
            "task": new_task,
            "done": False,
            "day": today
        }).execute()

response = supabase.table("tasks").select("*").eq("day", today).execute()
tasks_data = response.data or []

st.subheader("Today")

done_count = 0

for item in tasks_data:
    checked = st.checkbox(item["task"], value=item["done"], key=item["id"])

    if checked != item["done"]:
        supabase.table("tasks").update({
            "done": checked
        }).eq("id", item["id"]).execute()

    if checked:
        done_count += 1

total = len(tasks_data)
st.progress(done_count / total if total > 0 else 0)
st.write(f"{done_count}/{total} completed")

st.subheader("Dashboard")

all_data = supabase.table("tasks").select("*").order("day", desc=True).execute().data or []

for item in all_data:
    status = "done" if item["done"] else "not done"

    st.markdown(
        f"""
        <div class="card">
            <div class="task-text">{item['task']}</div>
            <div class="status">{item['day']} · {status}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
