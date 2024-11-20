# from gtts import gTTS
# import os

# # Text to convert to speech
# text = "how are you?"

# # Generate speech
# tts = gTTS(text, lang="en")  # Set the language code (e.g., 'fr' for French)
# tts.save("output.mp3")

# # Play the output (optional)
# # os.system("start output.mp3")


import speech_recognition as sr
from gtts import gTTS
from deep_translator import GoogleTranslator
import os
import pygame


languages = GoogleTranslator().get_supported_languages()
print("Available languages:")
for lang in sorted(languages):
    print(lang)


class SpeechTranslator:
    def __init__(self, target_lang='es'):
        self.recognizer = sr.Recognizer()
        self.translator = GoogleTranslator(source='auto', target=target_lang)
        self.target_lang = target_lang
        pygame.mixer.init()
        
    def record_and_translate(self):
        with sr.Microphone() as source:
            print(f"Listening... (translating to {self.target_lang})")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
        try:
            # Speech to text
            text = self.recognizer.recognize_google(audio)
            print(f"Original text: {text}")
            
            # Translate
            translation = self.translator.translate(text)
            print(f"Translated text: {translation}")
            
            # Text to speech
            tts = gTTS(text=translation, lang=self.target_lang)
            tts.save("translated_output.mp3")
            
            # Play audio
            pygame.mixer.music.load("translated_output.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            os.remove("translated_output.mp3")
            return translation
            
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
        except Exception as e:
            print(f"Translation error: {e}")
        
        return None

if __name__ == "__main__":
    # Initialize with target language
    translator = SpeechTranslator(target_lang='es')
    
    while True:
        translator.record_and_translate()
