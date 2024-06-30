import threading
import time
import os
import functools
from meeting_note.lib.record import MicrophoneRecorder
from meeting_note.lib.whisper import WhisperModel
from meeting_note.helper.helper import wer

def test_record():
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    save_path = os.path.join(data_folder, "test_1.wav")
    recorder = MicrophoneRecorder()
    devices = recorder.get_all_devices()
    assert len(devices) > 0, "No recording devices in the computer!"
    device_id = 1 if 1 in devices else list(devices.keys())[0]
    # 1. set device_id first
    recorder.set_default_device_id(device_id)
    # 2. start_stream
    recorder.start_stream()
    # 3. record for some seconds
    # with open(save_path, 'wb') as f:
    #     recorder.record_flow(file_name=f, duration=5)
    recorder.record_flow(file_name=save_path, duration=5)
    # 4. close the stream
    recorder.close_stream()
    assert os.path.exists(save_path)

def test_record_async():
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    save_path = os.path.join(data_folder, "test_2.wav")
    recorder = MicrophoneRecorder()
    devices = recorder.get_all_devices()
    assert len(devices) > 0, "No recording devices in the computer!"
    device_id = 1 if 1 in devices else list(devices.keys())[0]
    # 1. set device_id first
    recorder.set_default_device_id(device_id)
    # 2. start_stream
    recorder.start_stream()
    # 3. start a thread and run this function record
    thread = threading.Thread(target=functools.partial(recorder.record_flow, file_name=save_path))
    thread.start()
    # 4. sleep for 5 seconds (emulate a user stop), close_stream
    time.sleep(5)
    recorder.close_stream()
    thread.join()

def test_whisper():
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    load_path_1 = os.path.join(data_folder, "test1.wav")
    load_path_2 = os.path.join(data_folder, "test2.wav")
    whisper = WhisperModel()
    with open(load_path_1, 'rb') as f:
        result = whisper.transcribe(f)
    print(result)
    with open(load_path_2, 'rb') as f:
        result = whisper.transcribe(f)
    print(result)