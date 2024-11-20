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


class RealtimeTranslator:
    def __init__(self, source_lang="en", target_lang="es"):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.audio_queue = Queue()
        self.is_running = False
        
        # Initialize ASR pipeline with Whisper
        self.asr_pipeline = pipeline("automatic-speech-recognition", 
                                   model="openai/whisper-base")
        
        # Initialize translator
        self.translator = Translator()
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
    def record_audio(self, duration=5, sample_rate=16000):
        """Record audio from microphone"""
        recording = sd.rec(int(duration * sample_rate),
                         samplerate=sample_rate,
                         channels=1,
                         dtype=np.float32)
        sd.wait()
        return recording
    
    def transcribe_audio(self, audio):
        """Convert speech to text using Whisper"""
        # Save audio temporarily
        write("temp.wav", 16000, audio)
        
        # Transcribe
        result = self.asr_pipeline("temp.wav")
        os.remove("temp.wav")
        return result["text"]
    
    def translate_text(self, text):
        """Translate text to target language"""
        translation = self.translator.translate(text, 
                                             src=self.source_lang,
                                             dest=self.target_lang)
        return translation.text
    
    def speak_text(self, text):
        """Convert text to speech and play it"""
        tts = gTTS(text=text, lang=self.target_lang)
        tts.save("output.mp3")
        
        # Play the audio
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        os.remove("output.mp3")
    
    def process_audio(self):
        """Process audio from queue"""
        while self.is_running:
            if not self.audio_queue.empty():
                audio = self.audio_queue.get()
                
                # Process the audio
                text = self.transcribe_audio(audio)
                translated = self.translate_text(text)
                self.speak_text(translated)
    
    def start(self):
        """Start the real-time translation"""
        self.is_running = True
        
        # Start processing thread
        process_thread = threading.Thread(target=self.process_audio)
        process_thread.start()
        
        print("Started real-time translation. Press Ctrl+C to stop.")
        
        try:
            while self.is_running:
                # Record audio in chunks
                audio = self.record_audio()
                self.audio_queue.put(audio)
                
        except KeyboardInterrupt:
            self.stop()
     
    def stop(self):
        """Stop the translation"""
        self.is_running = False
        pygame.mixer.quit()

if __name__ == "__main__":
    # Create translator instance (English to Spanish)
    translator = RealtimeTranslator(source_lang="en", target_lang="es")
    
    # Start translation
    translator.start()


# import tkinter as tk
# from tkinter import messagebox
# import threading
# import speech_recognition as sr
# from googletrans import Translator
# from googletrans import LANGUAGES
# from gtts import gTTS
# import os

# print(LANGUAGES)

# class SpeechTranslatorApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Speech Translator")
#         self.root.geometry("400x400")

#         self.label = tk.Label(root, text="Press 'Start' to speak")
#         self.label.pack(pady=20)

#         self.start_button = tk.Button(root, text="Start", command=self.start_speech_recognition)
#         self.start_button.pack(pady=10)

#         self.stop_button = tk.Button(root, text="Stop", command=self.stop_speech_recognition, state=tk.DISABLED)
#         self.stop_button.pack(pady=10)

#         self.translation_label = tk.Label(root, text="")
#         self.translation_label.pack(pady=10)

#         self.target_language_entry = tk.Entry(root, width=20)
#         self.target_language_entry.pack(pady=5)

#         self.translate_button = tk.Button(root, text="Translate", command=self.translate_text)
#         self.translate_button.pack(pady=5)

#         self.abbreviations_button = tk.Button(root, text="Abbreviations", command=self.show_abbreviations)
#         self.abbreviations_button.pack(pady=5)

#         self.translator = Translator()
#         self.recognizer = sr.Recognizer()

#     def start_speech_recognition(self):
#         self.start_button.config(state=tk.DISABLED)
#         self.stop_button.config(state=tk.NORMAL)
#         threading.Thread(target=self.recognize_speech).start()

#     def stop_speech_recognition(self):
#         self.start_button.config(state=tk.NORMAL)
#         self.stop_button.config(state=tk.DISABLED)

#     def recognize_speech(self):
#         with sr.Microphone() as source:
#             self.label.config(text="Listening...")
#             self.recognizer.adjust_for_ambient_noise(source)
#             audio = self.recognizer.listen(source, timeout=10)  # Listen for up to 10 seconds

#         try:
#             self.label.config(text="Recognizing...")
#             original_text = self.recognizer.recognize_google(audio)
#             self.translation_label.config(text=f"Original text: {original_text}")
#         except sr.UnknownValueError:
#             messagebox.showwarning("Warning", "Sorry, could not understand audio.")
#         except sr.RequestError as e:
#             messagebox.showerror("Error", f"Could not request results from Google Web Speech API; {e}")

#     def translate_text(self):
#         original_text = self.translation_label.cget("text")[14:]  # Extract the original text
#         target_language = self.target_language_entry.get()

#         if len(target_language) != 2:
#             messagebox.showerror("Error", "Invalid language code. Please enter a valid two-letter language code.")
#             return

#         try:
#             translated_text = self.translator.translate(original_text, dest=target_language)
#             self.translation_label.config(text=f"Translated text ({target_language}): {translated_text.text}")
#             self.speak_text(translated_text.text, target_language)
#         except Exception as e:
#             messagebox.showerror("Error", f"Translation failed: {e}")

#     def speak_text(self, text, language='en'):
#         tts = gTTS(text=text, lang=language, slow=False)
#         tts.save("translated_audio.mp3")
#         os.system("start translated_audio.mp3")

#     def show_abbreviations(self):
#         # Create a new window
#         abbrev_window = tk.Toplevel(self.root)
#         abbrev_window.title("Language Abbreviations")
#         abbrev_window.geometry("400x600")  # Adjust the size of the window

#         # Create a text widget to display the table
#         text_widget = tk.Text(abbrev_window, wrap=tk.NONE, height=30, width=50)
#         text_widget.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
#         text_widget.insert(tk.END, "Language Abbreviations:\n\n")

#         # Define abbreviations in a table format
#         abbreviations = [
#             ("af", "Afrikaans"), ("sq", "Albanian"),
#             ("am", "Amharic"), ("ar", "Arabic"),
#             ("hy", "Armenian"), ("az", "Azerbaijani"),
#             ("eu", "Basque"), ("be", "Belarusian"),
#             ("bn", "Bengali"), ("bs", "Bosnian"),
#             ("bg", "Bulgarian"), ("ca", "Catalan"),
#             ("ceb", "Cebuano"), ("zh", "Chinese"),
#             ("zh-TW", "Chinese (Traditional)"), ("co", "Corsican"),
#             ("hr", "Croatian"), ("cs", "Czech"),
#             ("da", "Danish"), ("nl", "Dutch"),
#             ("en", "English"), ("eo", "Esperanto"),
#             ("et", "Estonian"), ("fi", "Finnish"),
#             ("fr", "French"), ("fy", "Frisian"),
#             ("gl", "Galician"), ("ka", "Georgian"),
#             ("de", "German"), ("el", "Greek"),
#             ("gu", "Gujarati"), ("ht", "Haitian Creole"),
#             ("ha", "Hausa"), ("haw", "Hawaiian"),
#             ("he", "Hebrew"), ("hi", "Hindi"),
#             ("hmn", "Hmong"), ("hu", "Hungarian"),
#             ("is", "Icelandic"), ("ig", "Igbo"),
#             ("id", "Indonesian"), ("ga", "Irish"),
#             ("it", "Italian"), ("ja", "Japanese"),
#             ("jw", "Javanese"), ("kn", "Kannada"),
#             ("kk", "Kazakh"), ("km", "Khmer"),
#             ("rw", "Kinyarwanda"), ("ko", "Korean"),
#             ("ku", "Kurdish"), ("ky", "Kyrgyz"),
#             ("lo", "Lao"), ("la", "Latin"),
#             ("lv", "Latvian"), ("lt", "Lithuanian"),
#             ("lb", "Luxembourgish"), ("mk", "Macedonian"),
#             ("mg", "Malagasy"), ("ms", "Malay"),
#             ("ml", "Malayalam"), ("mt", "Maltese"),
#             ("mi", "Maori"), ("mr", "Marathi"),
#             ("mn", "Mongolian"), ("my", "Burmese"),
#             ("ne", "Nepali"), ("no", "Norwegian"),
#             ("ny", "Nyanja (Chichewa)"), ("or", "Odia (Oriya)"),
#             ("ps", "Pashto"), ("fa", "Persian"),
#             ("pl", "Polish"), ("pt", "Portuguese"),
#             ("pa", "Punjabi"), ("ro", "Romanian"),
#             ("ru", "Russian"), ("sm", "Samoan"),
#             ("gd", "Scots Gaelic"), ("sr", "Serbian"),
#             ("st", "Sesotho"), ("sn", "Shona"),
#             ("sd", "Sindhi"), ("si", "Sinhala"),
#             ("sk", "Slovak"), ("sl", "Slovenian"),
#             ("so", "Somali"), ("es", "Spanish"),
#             ("su", "Sundanese"), ("sw", "Swahili"),
#             ("sv", "Swedish"), ("tl", "Tagalog"),
#             ("tg", "Tajik"), ("ta", "Tamil"),
#             ("tt", "Tatar"), ("te", "Telugu"),
#             ("th", "Thai"), ("tr", "Turkish"),
#             ("tk", "Turkmen"), ("uk", "Ukrainian"),
#             ("ur", "Urdu"), ("ug", "Uyghur"),
#             ("uz", "Uzbek"), ("vi", "Vietnamese"),
#             ("cy", "Welsh"), ("xh", "Xhosa"),
#             ("yi", "Yiddish"), ("yo", "Yoruba"),
#             ("zu", "Zulu")
#         ]

#         # Format the table and insert into the text widget
#         for i, (code, language) in enumerate(abbreviations):
#             if i % 2 == 0:
#                 text_widget.insert(tk.END, f"{code:5} {language:25}")
#             else:
#                 text_widget.insert(tk.END, f"{code:5} {language:25}\n")

#         text_widget.config(state=tk.DISABLED)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SpeechTranslatorApp(root)
#     root.mainloop()
