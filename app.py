
"""
Streamlit
documentation: https://docs.streamlit.io/

app.py = wiring + UI

"""

import streamlit as st

from config.settings import Settings
from assistant.memory import Memory
from assistant.prompt_controller import PromptController
from assistant.llm_engine import LLMEngine
from assistant.assistant import FridayAssistant

st.set_page_config(
    page_title="Friday AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Friday – Personal AI Assistant")

settings = Settings()
memory = Memory()
prompt_controller = PromptController()
llm_engine = LLMEngine(settings)

assistant = FridayAssistant(
    llm_engine=llm_engine,
    prompt_controller=prompt_controller,
    memory=memory
)

role = st.sidebar.selectbox(
    "Select Assistant Role",
    ["Tutor", "Coder", "Mentor"]
)

if st.sidebar.button("🗑️ Clear Memory"):
    memory.history = []
    with open(memory.file_path, "w") as f:
        f.write("[]")
    st.sidebar.success("Memory cleared!")

user_input = st.chat_input("Ask Friday...")

if user_input:
    response = assistant.respond(user_input, role)
    st.chat_message("assistant").write(response)

