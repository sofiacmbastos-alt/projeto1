import streamlit as st
from datetime import date
import json
import os

# ----------------- STYLE -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Monsieur+La+Doulaise&display=swap');

    .stApp {
        background-color: #FFF7FA;
    }

    /* REMOVE STREAMLIT BLUE ACCENTS */
    * {
        accent-color: #f7a8c4 !important;
    }

    /* TITLE FONT */
    h1, h2, h3 {
        font-family: 'Monsieur La Doulaise', cursive !important;
        color: #d48ca3 !important;
        text-align: center;
    }

    /* TEXT */
    p, span, label {
        color: #c77c95 !important;
    }

    /* CHECKBOX */
    [data-testid="stCheckbox"] label {
        color: #c77c95 !important;
        font-size: 16px;
    }

    /* BUTTONS (fix blue Streamlit buttons) */
    button {
        background-color: #f7a8c4 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
    }

    button:hover {
        background-color: #f28fb6 !important;
    }

    /* PROGRESS BAR */
    [data-testid="stProgress"] > div > div {
        background-color: #ffe4ec !important;
    }

    [data-testid="stProgress"] > div > div > div {
        background-color: #f7a8c4 !important;
    }

    /* CARD */
    .card {
        background: white;
        padding: 12px 18px;
        border-radius: 16px;
        margin-bottom: 10px;
        border: 1px solid #ffe4ec;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- TITLE -----------------
st.markdown("<h1>Sofia's Reminders 🌸</h1>", unsafe_allow_html=True)

st.write("things i need to do/be reminded of")

st.image("https://polipet.fbitsstatic.net/media/hollandpopicon.png?v=202501081421")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Netherlandwarf.jpg/330px-Netherlandwarf.jpg")

# ----------------- DATA -----------------
tasks = ["remedio 1", "remedio 2", "academia"]
today = str(date.today())

ARQUIVO = "historico.json"

if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r") as f:
        historico = json.load(f)
else:
    historico = {}

if today not in historico:
    historico[today] = {}

# ensure keys exist
for t in tasks:
    if t not in historico[today]:
        historico[today][t] = False

# ----------------- ADD NEW TASK -----------------
st.subheader("Add new task ✨")

new_task = st.text_input("New task")

if st.button("Add 💖"):
    if new_task:
        historico[today][new_task] = False
        st.rerun()

# update task list dynamically
tasks = list(historico[today].keys())

# ----------------- TODAY TASKS -----------------
st.subheader("Today 🌸")

for task in tasks:
    historico[today][task] = st.checkbox(
        task,
        value=historico[today][task]
    )

# save
with open(ARQUIVO, "w") as f:
    json.dump(historico, f)

# ----------------- PROGRESS -----------------
done = sum(historico[today].values())
total = len(tasks)

st.progress(done / total if total > 0 else 0)
st.write(f"{done}/{total} completed 🌸")

# ----------------- CALENDAR VIEW -----------------
st.subheader("Calendar view 📅")

for dia in sorted(historico.keys(), reverse=True):
    with st.expander(f"📅 {dia}"):

        for tarefa, feito in historico[dia].items():
            status = "💖 done" if feito else "🤍 not done"

            st.markdown(
                f"""
                <div class="card">
                    <b>{tarefa}</b><br>
                    {status}
                </div>
                """,
                unsafe_allow_html=True
            )
