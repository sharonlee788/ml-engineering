import streamlit as st
import requests
import json

st.title("Headline Scorer")
st.markdown(
    "Use this app to send headlines to headline scoring web service."
    )

score_url = "http://localhost:9083/score_headlines"

# session state setup
if "headlines" not in st.session_state:
    st.session_state.headlines = []

def add_new():
    st.session_state.headlines.append("")

def delete_idx(i):
    st.session_state.headlines.pop(i)

def move_up(i):
    if i > 0:
        a = st.session_state.headlines
        a[i-1], a[i] = a[i], a[i-1]

def move_down(i):
    if i < len(st.session_state.headlines) - 1:
        a = st.session_state.headlines
        a[i+1], a[i] = a[i], a[i+1]

# you can add new text box or clear all
col_top = st.columns([1, 1, 5])
with col_top[0]:
    if st.button("Add new"):
        add_new()
with col_top[1]:
    if st.button("Clear all"):
        st.session_state.headlines = [""]

# remove or reorder specific text boxes
for i, val in enumerate(list(st.session_state.headlines)):
    cols = st.columns([6, 1, 1, 2])
    new_val = cols[0].text_input(f"Headline {i+1}", value=val)
    st.session_state.headlines[i] = new_val

    if cols[1].button("▲", key=f"up_{i}"):
        move_up(i)
        st.rerun()
    if cols[2].button("▼", key=f"down_{i}"):
        move_down(i)
        st.rerun()
    if cols[3].button("Delete", key=f"del_{i}"):
        delete_idx(i)
        st.rerun()

st.markdown("---")

# score button
st.write(f"Headlines count: {len([h for h in st.session_state.headlines if h.strip()])}")
if st.button("Score"):
    input_lines = [h for h in st.session_state.headlines if h.strip()]
    st.write(f"We're sending {len(input_lines)} headlines..")
    if not input_lines:
        st.warning("Enter at least one headline.")
    else:
        response = requests.post(score_url, json={"headlines": input_lines})
        st.write(response.json())

### fastapi dev score_headlines_api.py --port 9083
### streamlit run score_headlines_gui.py