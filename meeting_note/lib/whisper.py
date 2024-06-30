from openai import OpenAI


class WhisperModel:
    def __init__(self, model_name="whisper-1", prefer_language=None):
        self.client = OpenAI()
        self.model = model_name
        self.prefer_language = prefer_language

    def transcribe(self, f):
        params = {}
        if self.prefer_language is not None:
            params['language'] = self.prefer_language
        transcription = self.client.audio.transcriptions.create(
            model=self.model, file=f, response_format="verbose_json", **params)
        return {"text": transcription.text, "language": transcription.language}
