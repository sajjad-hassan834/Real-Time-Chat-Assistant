from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import streamlit as st
import os
import google.generativeai as genai
import time  # For adding a delay between words

# Debug: Print the API key to verify it's loaded
api_key = os.getenv("api_key")
print(f"API Key: {api_key}")  # Check the console for this output

if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

try:
    # Configure Gemini
    genai.configure(api_key=api_key)  # Use the API key from the environment variable
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
except Exception as e:
    st.error(f"Failed to configure Gemini: {e}")
    st.stop()

# Function to get Gemini response
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Failed to get response from Gemini: {e}")
        return None

# Function to display text word by word (like ChatGPT)
def display_word_by_word(text):
    placeholder = st.empty()  # Create a placeholder to update the text dynamically
    displayed_text = ""
    for char in text:  # Iterate over each character in the text
        displayed_text += char  # Add the character to the displayed text
        placeholder.markdown(displayed_text)  # Update the placeholder
        time.sleep(0.05)  # Add a small delay (adjust as needed for typing effect)

# Streamlit app setup
st.set_page_config(page_title="Q&A Demo")
st.header("Real Time Chatting Assistant")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input and button
input = st.text_input("Promt:", key="input")
submit = st.button("Ask")

# Handle user input and display response
if submit and input:
    response = get_gemini_response(input)
    if response:
        st.session_state["chat_history"].append(("You", input))
        st.subheader("Response :")
        
        # Accumulate the response text
        full_response = ""
        for chunk in response:
            full_response += chunk.text
        
        # Display the response word by word (like ChatGPT)
        display_word_by_word(full_response)
        st.session_state["chat_history"].append(("Bot", full_response))

# Display chat history
st.subheader("History:")
for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")