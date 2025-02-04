import streamlit as st
from utils import generate_quiz
import time
from datetime import datetime, timedelta

def quiz_page():
    if "topic" not in st.session_state or not st.session_state.topic:
        st.error("Please select a topic first!")
        st.stop()
    
    st.title(f"Quiz: {st.session_state.topic}")
    
    # Generate questions if needed
    if not st.session_state.questions:
        with st.spinner("Generating quiz questions..."):
            st.session_state.questions = generate_quiz(
                st.session_state.topic,
                st.session_state.level,
                st.session_state.api_key
            )
    
    # Display current question
    if st.session_state.current_index < len(st.session_state.questions):
        display_question()
    else:
        show_results()

def display_question():
    question = st.session_state.questions[st.session_state.current_index]
    
    st.subheader(f"Question {st.session_state.current_index + 1}")
    st.write(question["question"])
    
    # Handle answer selection
    answer = st.radio("Select your answer:", question["options"], key=f"q_{st.session_state.current_index}")
    
    if st.button("Submit Answer"):
        if answer == question["answer"]:
            st.session_state.score += 1
            st.success("Correct! ✅")
        else:
            st.error("Incorrect ❌")
        
        st.session_state.current_index += 1
        time.sleep(1)
        st.experimental_rerun()

def show_results():
    st.subheader("Quiz Complete! 🎉")
    
    score_percentage = (st.session_state.score / len(st.session_state.questions)) * 100
    st.write(f"Your Score: {st.session_state.score}/{len(st.session_state.questions)} ({score_percentage:.1f}%)")
    
    if score_percentage >= 80 and st.session_state.level < 3:
        st.success(f"Congratulations! You've advanced to Level {st.session_state.level + 1}!")
        if st.button("Start Next Level"):
            st.session_state.level += 1
            st.session_state.questions = None
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.experimental_rerun()
    else:
        if st.button("Try Again"):
            st.session_state.questions = None
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.experimental_rerun()

if __name__ == "__main__":
    quiz_page()
