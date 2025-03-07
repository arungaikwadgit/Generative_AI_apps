import os

import google.generativeai as genai
from elevenlabs import play,save
from elevenlabs.client import ElevenLabs

UPLOAD_FOLDER = "audio_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the Load Google Gemini model and provide the sql query
def gen_gemini_response(text,gemini_api_key):
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(text)
    
    return response.text

def generate_audio(text, language, duration, voice, gemini_api_key, elevenlabs_api_key):
    if not text:
        return dict({"error": "Text is required","status_code":400})

    try:
        response_text = gen_gemini_response(text+"in "+language+" for "+str(duration)+" secs",gemini_api_key)
        client = ElevenLabs(api_key=elevenlabs_api_key)
        # Generate audio file
        audio = client.generate(
            text=response_text,
            voice="Sam",# - Soothing Hindi Voice",#voice
            model="eleven_flash_v2_5"
        )
    except Exception as e:
        return dict({"error": e.__str__(),"status_code":400})
    # Save the file
    audio_path = os.path.join(UPLOAD_FOLDER, "podcast.mp3")
    save(audio, audio_path)
    
    # Return response with explicit Content-Type
    response = dict({"audio_url":audio_path,"status_code":200})
    return response
    
    

