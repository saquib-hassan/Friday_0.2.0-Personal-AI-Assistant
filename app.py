
"""
Streamlit
documentation: https://docs.streamlit.io/

app.py = wiring + UI
"""

import time
import speech_recognition as sr
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

def stream_text(text, delay=0.03):
    for word in text.split():
        yield word + " "
        time.sleep(delay)

#Text Input
user_input = st.chat_input("Ask Friday...")

if user_input:
    st.chat_message("user").write(user_input)

    response = assistant.respond(user_input, role)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed_text = ""

        for chunk in stream_text(response):
            streamed_text += chunk
            placeholder.markdown(streamed_text)

#STT
def listen_from_mic():
    recognizer = sr.Recognizer()
    status = st.empty()

    with sr.Microphone() as source:
        status.info("🎤 Friday is listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    status.empty()

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""



if st.button("🎤 Speak"):
    user_input = listen_from_mic()

    if user_input:
        st.chat_message("user").write(user_input)

        response = assistant.respond(user_input, role)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            streamed_text = ""

            for chunk in stream_text(response):
                streamed_text += chunk
                placeholder.markdown(streamed_text)
