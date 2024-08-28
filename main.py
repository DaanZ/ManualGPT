
import streamlit as st
from dotenv import load_dotenv

from history import History
from query import query_dataset

load_dotenv()

machine = "CNC"
purpose = "configuring the CNC machine for the operator"
st.set_page_config(
    page_title=f"{machine} GPT",
    page_icon="⚙️",
    layout="wide"
)

st.title(f"{machine} GPT")

# check for messages in session and create if not exists
if "history" not in st.session_state.keys():
    st.session_state.history = History()
    st.session_state.history.system(f"""You are helping the user with information about a {machine} machine using access to the manual. You are
    currently having a conversation with a person. Answer the questions in a kind and friendly 
    with you being the expert for {purpose} to answer any questions about life.""")
    st.session_state.history.assistant("Hello there, how can I help you? ⚙️")


# Display all messages
for message in st.session_state.history.logs:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.history.user(user_prompt)
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.history.logs[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            chat = query_dataset("data/Manual", st.session_state.history.logs[-1]["content"] +
                                 f" Give your answer highlighting {purpose} in one paragraph:", 10)
            st.write(chat)
    st.session_state.history.assistant(chat)
