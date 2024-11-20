from transformers import pipeline
from googletrans import Translator
import os
import pygame
import to_speech

source_lang = "en"
target_lang = "es"

# Initialize ASR pipeline with Whisper
asr_pipeline = pipeline("automatic-speech-recognition", 
                            model="openai/whisper-base")

# Initialize translator
translator = Translator()

# Initialize pygame for audio playback
pygame.mixer.init()


def transcribe_audio(audio_file):
    # Transcribe
    result = asr_pipeline(audio_file)
    os.remove(audio_file)
    return result["text"]



def translate_text(text, source_lang, target_lang):
    """Translate text to target language"""
    translation = translator.translate(text, 
                                            src=source_lang,
                                            dest=target_lang)
    return translation.text



def speak_text(text):
    """Convert text to speech and play it"""
    to_speech.speech_to_file(text)
    
speak_text("helooooo")


def translate_audio(from_language, to_language, audio_file):
    transcibed_text = transcribe_audio(audio_file)
    translated_text = translate_text(from_language, to_language, transcibed_text)
    speak_text(transcibed_text)




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
