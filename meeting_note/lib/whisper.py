from openai import OpenAI
import wave
import traceback
import os
import shutil


class WhisperModel:
    def __init__(self, model_name="whisper-1", prefer_language=None, tmp_path="./tmp/", segment_time=240):
        self.client = OpenAI()
        self.model = model_name
        self.prefer_language = prefer_language
        self.tmp_path = tmp_path
        self.segment_time = segment_time
        os.makedirs(tmp_path, exist_ok=True)

    def transcribe(self, f):
        try:
            params = {}
            if self.prefer_language is not None:
                params['language'] = self.prefer_language
            text = ""
            for f_item in self._split(f):
                with open(f_item, 'rb') as f_in:
                    transcription = self.client.audio.transcriptions.create(
                        model=self.model, file=f_in, response_format="verbose_json", **params)
                    text += transcription.text
            return {"text": text, "language": transcription.language}
        except Exception:
            raise WhisperModelError(traceback.format_exc())

    def _split(self, file_path):
        with wave.open(file_path, 'rb') as wav_in:
            frames = wav_in.getnframes()
            frame_rate = wav_in.getframerate()

            file_name = os.path.splitext(os.path.basename(file_path))[0]
            if frames / frame_rate < self.segment_time:
                return [file_path]
            else:
                result = []
                for i in range(int(frames / frame_rate / self.segment_time) + 1):
                    start_frame = i * self.segment_time * frame_rate
                    end_frame = (i + 1) * self.segment_time * frame_rate
                    if frames / frame_rate - i * self.segment_time < 0.5:
                        # whisper cannot process data less than 0.1 seconds
                        continue
                    wav_in.setpos(start_frame)
                    data_frames = wav_in.readframes(end_frame - start_frame)
                    current_path = os.path.join(self.tmp_path, "{}_{}.wav".format(file_name, i))
                    with wave.open(current_path, 'wb') as f:
                        f.setparams(wav_in.getparams())
                        f.writeframes(data_frames)
                    result.append(current_path)
                return result

    def __del__(self):
        shutil.rmtree(self.tmp_path)


class WhisperModelError(Exception):
    pass
