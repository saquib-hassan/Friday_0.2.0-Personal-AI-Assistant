import streamlit as st
import speech_recognition as sr

from config.settings import Settings
from assistant.memory import Memory
from assistant.prompt_controller import PromptController
from assistant.llm_engine import LLMEngine
from assistant.assistant import FridayAssistant
from auth.auth_service import AuthService

# Page config
st.set_page_config(page_title="Friday AI", page_icon="🤖")
st.title("🤖 Friday - Personal AI Assistant")


# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "confirm_logout" not in st.session_state:
    st.session_state.confirm_logout = False

auth_service = AuthService()

# Login/Register screen
if not st.session_state.authenticated:
    st.subheader("🔐 Login to Friday")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            result = auth_service.login_user(email, password)
            if result:
                user_id, user_email = result
                st.session_state.authenticated = True
                st.session_state.user_id = user_id
                st.session_state.user_email = user_email
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("Invalid email or password")

    with col2:
        if st.button("Sign Up"):
            if auth_service.register_user(email, password):
                st.success("Account created. Now login.")
            else:
                st.error("User already exists")

    st.stop()


# ===== AUTHENTICATED USER AREA =====

settings = Settings()
memory = Memory(user_id=st.session_state.user_id)
prompt_controller = PromptController()
llm_engine = LLMEngine(settings)

assistant = FridayAssistant(
    llm_engine=llm_engine,
    prompt_controller=prompt_controller,
    memory=memory
)

# Sidebar - User info
st.sidebar.markdown(f"### 👤 {st.session_state.user_email}")
st.sidebar.markdown("---")

# Sidebar - Role selection
role = st.sidebar.selectbox(
    "Assistant Role",
    ["Tutor", "Coder", "Mentor"]
)

# Sidebar - Clear memory (user-only)
if st.sidebar.button("🗑 Clear Memory"):
    memory.clear()
    st.sidebar.success("Memory cleared")
    st.rerun()

# Sidebar - Logout with confirmation
if not st.session_state.confirm_logout:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.confirm_logout = True
        st.rerun()
else:
    st.sidebar.warning("Are you sure you want to logout?")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Yes", key="logout_yes"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.confirm_logout = False
            st.rerun()
    with col2:
        if st.button("No", key="logout_no"):
            st.session_state.confirm_logout = False
            st.rerun()


# Display existing conversation history
for item in memory.history:
    st.chat_message(item["role"]).write(item["message"])


# STT - Speech to text
def listen_from_mic():
    recognizer = sr.Recognizer()
    status = st.empty()

    with sr.Microphone() as source:
        status.info("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    status.empty()

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        st.warning("Sorry, I couldn't understand.")
        return ""


# Voice input button
if st.button("🎤 Speak"):
    user_input = listen_from_mic()

    if user_input:
        st.chat_message("user").write(user_input)
        response = assistant.respond(user_input, role)
        st.chat_message("assistant").write(response)


# Text input
text_input = st.chat_input("Or type your message...")

if text_input:
    st.chat_message("user").write(text_input)
    response = assistant.respond(text_input, role)
    st.chat_message("assistant").write(response)


# Export chat
def export_chat_as_text(memory):
    text = ""
    for item in memory.history:
        role_name = item["role"].capitalize()
        message = item["message"]
        text += f"{role_name}: {message}\n\n"
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
