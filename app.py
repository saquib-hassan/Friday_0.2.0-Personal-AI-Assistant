import streamlit as st
import speech_recognition as sr

from config.settings import Settings
from assistant.memory import Memory
from assistant.prompt_controller import PromptController
from assistant.llm_engine import LLMEngine
from assistant.assistant import FridayAssistant
from auth.auth_service import AuthService

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


def export_chat_as_text(memory):
    text = ""
    for item in memory.history:
        role = item["role"].capitalize()
        message = item["message"]
        text += f"{role}: {message}\n\n"
    return text


st.sidebar.markdown("---")

if st.sidebar.button("📤 Export Chat"):
    chat_text = export_chat_as_text(memory)

    st.sidebar.download_button(
        label="⬇️ Download chat.txt",
        data=chat_text,
        file_name="friday_chat.txt",
        mime="text/plain"
    )


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 Login to Friday")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            if AuthService.login(email, password):
                st.session_state.authenticated = True
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("Sign Up"):
            if AuthService.register(email, password):
                st.success("Account created. Please login.")
            else:
                st.error("User already exists")

    st.stop()






st.sidebar.subheader("🔐 Register")

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Register"):
    user_service = UserService()
    success = user_service.register_user(email, password)

    if success:
        st.sidebar.success("Account created successfully!")
    else:
        st.sidebar.error("Email already exists or error occurred")
