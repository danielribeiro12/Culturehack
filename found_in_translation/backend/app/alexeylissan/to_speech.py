import os
from google.cloud import texttospeech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'culture-hack.json'


def speech_to_file(text_block, target_lang = 'en-GB'):


    client = texttospeech.TextToSpeechClient()

    lang_mapping = {
        'es': 'es-ES',
        'fr': 'fr-FR',
        'de': 'de-DE',
        'it': 'it-IT',
        'ja': 'ja-JP',
        'ko': 'ko-KR',
        'ru': 'ru-RU',
        'zh': 'zh-CN',
        'hi': 'hi-IN',
        'ar': 'ar-XA'
    }

    language_code = lang_mapping.get(target_lang, 'en-GB')
    voice_name = 'en-GB-Journey-D' if language_code == 'en-GB' else f'{language_code}-Standard-A'


    synthesis_input = texttospeech.SynthesisInput(text= text_block)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
        # language_code="en-GB", 
        # name= 'en-GB-Journey-D'
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


