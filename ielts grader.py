import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Define the safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Streamlit app
st.title('IELTS Writing Grader')
st.write('Paste your IELTS essay below and get feedback.')

# User input for essay title
title = st.text_input('Title of Your Writing')

# User input for the essay
essay = st.text_area('Your IELTS Essay', height=300)

def check_essay(task):
    if essay:
        try:
            # Start a chat session
            chat_session = model.start_chat(history=[])
            # Construct the message to be sent
            message = f"{task} the following essay:\n\n{essay}"
            # Send the message to the chat session
            response = chat_session.send_message(message)
            # Display the generated text
            st.write(f'### {task.capitalize()} Check Result:')
            st.write(response.text.strip())
        except genai.APIException as e:
            st.write('An error occurred:', e)
    else:
        st.write(f'Please enter an essay to {task.lower()}.')

if st.button('Check Spelling'):
    check_essay('Check spelling in')

if st.button('Check Grammar'):
    check_essay('Check grammar in')

if st.button('Grade My Essay'):
    if essay and title:
        try:
            # Start a chat session
            chat_session = model.start_chat(history=[])
            # Construct the message to be sent
            message = f"Title: {title}\n\n{essay}\n\nPlease provide a grade band (0.0 - 9.0) for this IELTS essay and detailed feedback."
            # Send the essay to the chat session
            response = chat_session.send_message(message)
            # Extract the response
            feedback = response.text.strip()
            # Display the feedback
            st.write('### Feedback:')
            st.write(feedback)
            # Extract and display the grade band (assuming the grade is in the response text)
            import re
            grade_match = re.search(r'grade band: (\d+(\.\d+)?)', feedback, re.IGNORECASE)
            if grade_match:
                grade_band = grade_match.group(1)
                st.write(f'### Grade Band: {grade_band}')
            else:
                st.write('### Grade Band not found in the feedback.')
        except genai.APIException as e:
            st.write('An error occurred:', e)
    else:
        st.write('Please enter both a title and an essay to grade.')
