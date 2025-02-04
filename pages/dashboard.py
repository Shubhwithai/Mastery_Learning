import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import streamlit as st

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def initialize_session_state():
    """Initialize session state variables"""
    if "level" not in st.session_state:
        st.session_state.level = 1
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "questions" not in st.session_state:
        st.session_state.questions = None
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "topic" not in st.session_state:
        st.session_state.topic = None

def generate_quiz(topic, level, api_key):
    """Generate quiz questions using OpenAI API"""
    question_types = {
        1: "MCQ (Single Correct), True/False",
        2: "MCQ (Single/Multiple Correct), Matching",
        3: "Passage-Based, Multiple Response, Matching (Complex), Sequence Ordering"
    }
    
    prompt = f"""
        Generate {level}-level quiz questions for {topic}.
        Question types should be: {question_types[level]}.
        Ensure at least 8 questions for Level 1 & 2, and 6 for Level 3.
        Format output as JSON:
        [
          {{"question": "What is 2+2?", "options": ["2", "3", "4", "5"], "answer": "4", "type": "MCQ (Single Correct)"}},
          {{"question": "...", "options": ["..."], "answer": "...", "type": "..."}}
        ]
    """
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error generating quiz: {e}")
        return []
