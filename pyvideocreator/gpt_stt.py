import openai

class OpenAISTT:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def transcribe_audio(self, audio_path: str, response_format: str = "json"):
        with open(audio_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format=response_format
            )
        return transcript

    def translate_audio(self, audio_path: str):
        with open(audio_path, "rb") as audio_file:
            transcript = self.client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript

# Example Usage
# api_key = "your_openai_key"
# stt_api = OpenAISTT(api_key)

# # Transcribing an audio file
# transcription = stt_api.transcribe_audio("C:/Users/Erick/trabajo/_ trabajo alcala/ML/python/ai_channel/audios/haunted cities/haunted cities_audio.mp3")
# print(transcription)

# Translating an audio file
# translation = stt_api.translate_audio("C:/Users/Erick/trabajo/_ trabajo alcala/ML/python/ai_channel/audios/haunted cities/haunted cities_audio.mp3")
# print(translation)
