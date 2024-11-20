from flask import Flask, request, jsonify, render_template, send_file
from transformers import pipeline
# from googletrans import Translator
from deep_translator import GoogleTranslator
import os
import pygame
import to_speech

source_lang = "en"
target_lang = "ko"

# Initialize ASR pipeline with Whisper
asr_pipeline = pipeline("automatic-speech-recognition", 
                            model="openai/whisper-base")

# Initialize translator
# translator = Translator()
translator = GoogleTranslator(source=source_lang, target=target_lang)


def transcribe_audio(audio_file):
    # Transcribe
    result = asr_pipeline(audio_file)
    # os.remove(audio_file)
    return result["text"]


def translate_text(text, source_lang, target_lang):
    """Translate text to target language"""
    translation = translator.translate(text, 
                                    src=source_lang,
                                    dest=target_lang)
    return translation


def save_text_to_sound(text):
    """Convert text to speech and play it"""
    to_speech.speech_to_file(text)
    


def translate_audio(from_language, to_language, audio_file):
    transcribed_text = transcribe_audio(audio_file)
    print(transcribed_text)
    translated_text = translate_text(transcribed_text, from_language, to_language)
    save_text_to_sound(translated_text)
    return "output.mp3"



# Initialize the Flask application
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "<h1>Hello world</h1>"



# Example route with query parameters
@app.route('/translate-text')
def translate_text_endpoint():
    from_language = request.args.get("from_lang")
    to_language = request.args.get("to_lang")
    text = request.args.get("text")

    return translate_text(text, from_language, to_language)

@app.route('/process-audio', methods=['POST'])
def process_audio():
    print("processing audio")
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'})
    
    audio_file = request.files['audio']
    from_language = request.form.get('from_lang', 'en')
    to_language = request.form.get('to_lang', 'es')
    
    # Save the uploaded file temporarily
    temp_path = f"temp_audio_{os.getpid()}.m4a"
    audio_file.save(temp_path)
    
    try:
        result = translate_audio(from_language, to_language, temp_path)
        return jsonify({'translation': result})
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route('/translate-audio', methods=['POST'])
def translate_audio_endpoint():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
        
    audio_file = request.files['audio']
    from_language = request.form.get('from_lang', 'en')
    to_language = request.form.get('to_lang', 'es')
    
    # Save the uploaded file temporarily
    temp_path = f"temp_audio_{os.getpid()}.m4a"
    audio_file.save(temp_path)
    
    try:
        result = translate_audio(from_language, to_language, temp_path)
        return jsonify({'translation': result})
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route("/hand-sign")
def hand_sign_endpoint():
    import hand_sign



# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5000)
