import streamlit as st
import requests
import json
import audio_file as audio 
import sys

# Set page configuration with dark theme
st.set_page_config(page_title="Podcast Generator", layout="wide", page_icon="🎙️")

# Custom CSS for Dark Mode
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #e0e0e0;
    }
    .stTextInput>div>input, .stSelectbox>div>div {
        background-color: #1e1e1e;
        color: #e0e0e0;
        border: 1px solid #4caf50;
        border-radius: 5px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4caf50, #2e7d32);
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
    }
    .stAudio {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
    }
    div[data-testid="column"]:nth-child(1) {
        border-right: 2px solid #4caf50;
        padding-right: 20px;
    }
    div[data-testid="column"]:nth-child(2) {
        padding-left: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎙️ Create Your Professional Podcast")

# # API Key Inputs
# st.sidebar.header("🔑 API Key Configuration")
# gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password")
# elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")

# API Key Inputs with Instructions
st.sidebar.header("🔑 API Key Configuration")

gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password")
# st.sidebar.markdown("<small style='color: #c0c0c0;'>🔹 Required for text generation. Get it from Google AI.</small>", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <small style='color: #c0c0c0;'>
    <strong>How to get a Gemini API Key?</strong><br>  
    Visit the <a href='https://aistudio.google.com/app/apikey' target='_blank' style='color: #4caf50; text-decoration: none;'>AI Studio Google</a>  
    to create a project, enable the Gemini API, and generate an API key.  
    </small>
    """, 
    unsafe_allow_html=True
)

elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
st.sidebar.markdown(
    """
    <small style='color: #c0c0c0;'>
    <strong>How to get an ElevenLabs API Key?</strong><br>   
    Sign up on the <a href='https://elevenlabs.io/' target='_blank' style='color: #4caf50; text-decoration: none;'>ElevenLabs website</a>,  
    go to your account settings, and generate an API key.  
    For more details, check the <a href='https://docs.elevenlabs.io/' target='_blank' style='color: #4caf50; text-decoration: none;'>ElevenLabs API documentation</a>.
    </small>
    """, 
    unsafe_allow_html=True
)


# Podcast Details
st.subheader("Podcast Details")
main_topic = st.text_input("Main Topic", placeholder="e.g., AI in Healthcare")
subtopic = st.text_input("Subtopic (Optional)", placeholder="e.g., Impact on Diagnosis")

# Language and Voice Selection
language_voice_map = {
    "English": ["Sam", "Chris", "Rachel"], 
    "Hindi": ["Sam", "Chris", "Rachel"]
}
language = st.selectbox("Language", options=list(language_voice_map.keys()))
voice_style = st.selectbox("Voice Style", options=language_voice_map[language])

# Duration
duration_map = {
    "5 minutes": 300,
    "10 minutes": 500,
    "15 minutes": 900
}
duration = st.selectbox("Duration", list(duration_map.keys()))

# Generate Button
if st.button("Generate Podcast"):
    if not main_topic:
        st.error("Main Topic is required to generate Podcast!")
    elif not gemini_api_key :
        st.error("Gemini API key is required to generate Podcast!")
    elif not elevenlabs_api_key:
        st.error("ElevenLabs API key is required to generate Podcast!")
    else:
       
        text = f"{main_topic} {subtopic}"
        duration =  duration_map[duration]

        print(text, language, duration, voice_style,gemini_api_key,elevenlabs_api_key)
        
        response = audio.generate_audio(text, language, duration, voice_style,gemini_api_key,elevenlabs_api_key)
        print(response)
        print(type(response))
        if response.get("status_code") == 200:
            st.success("✅ Podcast generated successfully!")
            st.audio(response.get("audio_url"), format="audio/mp3")
        else:
            st.error("❌ Error generating podcast. "+response.get("error"))
