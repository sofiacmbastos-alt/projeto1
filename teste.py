import streamlit as st
from datetime import date
import json
import os

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Monsieur+La+Doulaise&display=swap');

    .stApp {
        background-color: #FFF7FA;
    }

    h1 {
        font-family: 'Monsieur La Doulaise', cursive;
        color: #d48ca3;
        font-size: 75px;
        text-align: center;
    }

    /* CHECKBOX TEXT */
    [data-testid="stCheckbox"] label {
        color: #d48ca3;
        font-weight: 500;
        font-size: 16px;
    }

    /* CHECKBOX COLOR */
    [data-testid="stCheckbox"] input {
        accent-color: #f7a8c4;
    }

    /* PROGRESS BAR BACKGROUND */
    [data-testid="stProgress"] > div > div {
        background-color: #ffe4ec;
    }

    /* PROGRESS BAR FILL */
    [data-testid="stProgress"] > div > div > div {
        background-color: #f7a8c4;
    }

    /* CARD STYLE */
    .card {
        background: white;
        padding: 15px 20px;
        border-radius: 15px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        border: 1px solid #ffe4ec;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>Sofia's Reminders 🌸</h1>", unsafe_allow_html=True)

st.write("things i need to do/be reminded of")

st.image("https://polipet.fbitsstatic.net/media/hollandpopicon.png?v=202501081421")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Netherlandwarf.jpg/330px-Netherlandwarf.jpg")

tasks = ["remedio 1", "remedio 2", "academia"]

today = str(date.today())

ARQUIVO = "historico.json"

if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r") as f:
        historico = json.load(f)
else:
    historico = {}

if today not in historico:
    historico[today] = {task: False for task in tasks}

st.subheader("Today ✨")

for task in tasks:
    historico[today][task] = st.checkbox(
        task,
        value=historico[today][task]
    )

with open(ARQUIVO, "w") as f:
    json.dump(historico, f)

done = sum(historico[today].values())
total = len(tasks)

st.progress(done / total)
st.write(f"{done}/{total} completed 🌸")

st.subheader("Histórico 🌸")

for dia, tarefas in historico.items():
    st.markdown(f"### 📅 {dia}")

    for tarefa, feito in tarefas.items():
        status = "✅ done" if feito else "⬜ not done"

        st.markdown(
            f"""
            <div class="card">
                <b>{tarefa}</b><br>
                <span>{status}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
