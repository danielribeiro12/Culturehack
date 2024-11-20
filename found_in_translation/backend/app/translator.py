from flask import Flask, request, jsonify
import sounddevice as sd
import numpy as np
from transformers import Pipeline, pipeline
from scipy.io.wavfile import write
import torch
from googletrans import Translator
from gtts import gTTS
import os
import pygame
from queue import Queue
import threading
import time
import to_speech

app = Flask(__name__)

source_lang = "en"
target_lang = "es"

# Initialize ASR pipeline with Whisper
asr_pipeline = pipeline("automatic-speech-recognition", 
                            model="openai/whisper-base")

# Initialize translator
translator = Translator()

# Initialize pygame for audio playback
pygame.mixer.init()

def transcribe_audio():
    # Transcribe
    result = asr_pipeline("temp.wav")
    os.remove("temp.wav")
    return result["text"]

def translate_text(text):
    """Translate text to target language"""
    translation = translator.translate(text, 
                                            src=source_lang,
                                            dest=target_lang)
    return translation.text

def speak_text(text):
    """Convert text to speech and play it"""
    to_speech.speech_to_file(text)
    
speak_text("helooooo")

@app.route('/translate-audio', methods=['POST'])
def handle_translation():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    target_lang = request.form.get('target_lang', 'es')  # Default to Spanish if not specified
    
    # Save the uploaded file temporarily
    file.save('temp.wav')
    
    try:
        # Chain the translation process
        text = transcribe_audio()
        translated = translate_text(text)
        speak_text(translated)
        
        return jsonify({
            'original_text': text,
            'translated_text': translated
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)