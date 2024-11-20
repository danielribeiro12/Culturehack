import whisper
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


# Load the Whisper model
model = whisper.load_model("small")

# Specify the audio file
audio_path = "output.mp3"

# Transcribe in the original language
result = model.transcribe(audio_path, language="ne")  # Specify the source language, e.g., French
transcription = result["text"]

print("Transcribed Text:", transcription)
