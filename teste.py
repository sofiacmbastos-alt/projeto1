import streamlit as st
from datetime import date

st.markdown(
    "<h1 style='color:#FFD1DC;'>Sofia's Reminders 🌸</h1>",
    unsafe_allow_html=True
)

st.write("things i need to do/be reminded of")

st.image("https://polipet.fbitsstatic.net/media/hollandpopicon.png?v=202501081421")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Netherlandwarf.jpg/330px-Netherlandwarf.jpg")

tasks = ["remedio 1", "remedio 2", "academia"]

today = str(date.today())

if "last_reset" not in st.session_state or st.session_state.last_reset != today:
    st.session_state.task_state = {task: False for task in tasks}
    st.session_state.last_reset = today

if "task_state" not in st.session_state:
    st.session_state.task_state = {task: False for task in tasks}

for task in tasks:
    st.session_state.task_state[task] = st.checkbox(
        task,
        value=st.session_state.task_state[task]
    )

done = sum(st.session_state.task_state.values())
total = len(tasks)

st.progress(done / total)
st.write(f"{done}/{total} completed 🌸")
