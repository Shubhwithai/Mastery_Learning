import streamlit as st
from config import OPENAI_API_KEY
from utils import initialize_session_state

st.set_page_config(page_title="AI Learning System", layout="wide")

def main():
    initialize_session_state()
    
    st.title("AI-Powered Adaptive Learning System")
    
    # Sidebar navigation
    menu = st.sidebar.radio("Navigation", ["Home", "Take Quiz", "Dashboard"])
    
    if menu == "Home":
        st.write("Welcome to the AI-Powered Learning System!")
        st.write("This platform uses GPT-4 to generate personalized quizzes and adapt to your learning level.")
        
        if not OPENAI_API_KEY:
            api_key = st.text_input("Enter your OpenAI API Key:", type="password")
            if api_key:
                st.session_state.api_key = api_key
            else:
                st.error("Please provide an OpenAI API key to continue.")
                st.stop()
        
    elif menu == "Take Quiz":
        st.header("Start a New Quiz")
        selected_topic = st.text_input("Enter a topic:", "")
        
        if st.button("Generate Quiz") and selected_topic.strip():
            st.session_state.topic = selected_topic
            st.session_state.questions = None
            st.experimental_rerun()
            
    elif menu == "Dashboard":
        show_dashboard()

def show_dashboard():
    st.title("📊 Student Dashboard")
    
    level = st.session_state.get("level", 1)
    score = st.session_state.get("score", 0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Current Level", level)
        st.metric("Total Score", score)
    
    with col2:
        st.subheader("Progress by Skill Area")
        progress_data = {
            "Knowledge": min(level * 20, 100),
            "Application": min(level * 15, 100),
            "Analysis": min(level * 10, 100)
        }
        
        st.bar_chart(progress_data)

if __name__ == "__main__":
    main()
