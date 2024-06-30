import threading
import time
import os
import functools
from meeting_note.lib.record import MicrophoneRecorder

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

# def test_whisper():
#     transcript()