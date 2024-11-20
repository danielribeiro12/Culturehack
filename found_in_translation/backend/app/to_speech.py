import os
from google.cloud import texttospeech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'culture-hack.json'


def speech_to_file(text_block):


    client = texttospeech.TextToSpeechClient()


    synthesis_input = texttospeech.SynthesisInput(text= text_block)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB", 
        name= 'en-GB-Journey-D'
        # name= 'en-GB-News-K'
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=['handset-class-device'],
        # speaking_rate=1.0,
        # pitch=1
    )

    response = client.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )

    with open("output.mp3", "wb") as output:
        output.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
