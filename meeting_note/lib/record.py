import pyaudio
import wave
from collections import namedtuple
import threading

MicrophoneRecorderConfiguration = namedtuple("MicrophoneRecorderConfiguration", ["rate", "chunk", "channels"])


class MicrophoneRecorder:
    def __init__(self, rate=44100, chunk=1024, channels=1):
        """Microphone Recorder developed by python

        Args:
            rate (int, optional): Bit rate of Microphone Recorder. Defaults to 44100.
            chunk (int, optional): number of bytes for one chunk of wav. Defaults to 1024.
            channels (int, optional): channel number. Defaults to 1.
        """
        self.audio, self.stream = None, None
        self._lock = threading.Lock()
        self.config = MicrophoneRecorderConfiguration(rate=rate, chunk=chunk, channels=channels)
        self.reset()

    def reset(self):
        if self.audio is not None:
            self.audio.terminate()
        self.audio = pyaudio.PyAudio()
        self._device_dict = self._get_all_devices()
        self._device_id = None
        self.open = False
        if self.stream is not None:
            self.close_stream()

    def _get_all_devices(self):
        result = {}
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                result[i] = device_info
        return result

    def set_default_device_id(self, current_id):
        if current_id in self._device_dict:
            self._device_id = current_id
        else:
            raise MicrophoneIdNonExist("Non-existed device_id: {}, DeviceDict: {}",
                                       current_id, self._device_dict)

    def get_all_devices(self):
        return self._device_dict

    def start_stream(self):
        if self._device_id is None:
            raise MicrophoneIdUnselected("Please select the device_id by `set_default_device_id` first!")
        if self.stream is not None or self.open:
            raise MicrophoneStreamStarted("The stream has been started")
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=self.config.channels, rate=self.config.rate,
                                      input=True, input_device_index=self._device_id, frames_per_buffer=self.config.chunk)
        self.open = True

    def record_flow(self, file_name, duration=-1):
        if self.stream is None or not self.open:
            raise MicrophoneNotStarted("Please start the stream by `start_stream` first!")
        wf = wave.open(file_name, 'wb')
        try:
            current_duration = 0
            wf.setnchannels(self.config.channels)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.config.rate)
            while self.stream is not None and self.open:
                if duration > 0 and current_duration >= duration:
                    break
                try:
                    self._lock.acquire()
                    if self.stream is not None:
                        data = self.stream.read(self.config.chunk)
                        wf.writeframes(data)
                        current_duration += self.config.chunk * 1.0 / self.config.rate
                finally:
                    self._lock.release()
        except OSError:
            # closed
            pass
        finally:
            wf.close()

    def close_stream(self):
        try:
            self._lock.acquire()
            if self.stream is not None:
                self.open = False
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
        finally:
            self._lock.release()

    def __del__(self):
        self.close_stream()
        self.audio.terminate()


class MicrophoneIdUnselected(Exception):
    pass


class MicrophoneIdNonExist(Exception):
    pass


class MicrophoneNotStarted(Exception):
    pass


class MicrophoneStreamStarted(Exception):
    pass
