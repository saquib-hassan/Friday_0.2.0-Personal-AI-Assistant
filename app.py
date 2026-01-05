import streamlit as st
import speech_recognition as sr

from config.settings import Settings
from assistant.memory import Memory
from assistant.prompt_controller import PromptController
from assistant.llm_engine import LLMEngine
from assistant.assistant import FridayAssistant

st.set_page_config(page_title="Friday AI", page_icon="🤖")
st.title("🤖 Friday - Personal AI Assistant")

settings = Settings()
memory = Memory()
prompt_controller = PromptController()
llm_engine = LLMEngine(settings)

assistant = FridayAssistant(
    llm_engine=llm_engine,
    prompt_controller=prompt_controller,
    memory=memory
)

# Sidebar
role = st.sidebar.selectbox(
    "Assistant Role",
    ["Tutor", "Coder", "Mentor"]
)

if st.sidebar.button("🗑 Clear Memory"):
    memory.history = []
    with open(memory.file_path, "w") as f:
        f.write("[]")
    st.sidebar.success("Memory cleared")

# STT
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
        st.warning("Sorry, I couldn't understand.")
        return ""

# Buttons
if st.button("🎤 Speak"):
    user_input = listen_from_mic()

    if user_input:
        st.chat_message("user").write(user_input)

        response = assistant.respond(user_input, role)
        st.chat_message("assistant").write(response)

# Text Input (optional)
text_input = st.chat_input("Or type your message...")

if text_input:
    st.chat_message("user").write(text_input)

    response = assistant.respond(text_input, role)
    st.chat_message("assistant").write(response)
