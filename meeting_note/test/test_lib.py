import threading
import time
import os
import functools
from meeting_note.lib.record import MicrophoneRecorder
from meeting_note.lib.whisper import WhisperModel
from meeting_note.lib.summarize import SummarizeModel
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
    result = whisper.transcribe(load_path_1)
    assert (result["language"] == "chinese")
    assert (wer(result['text'], "走到路上腳步多 我也習慣了") < 0.2)
    result = whisper.transcribe(load_path_2)
    assert (result["language"].lower() == "english")
    assert (wer(result['text'], "In Germany, over 100,000 tons of diapers are discarded each year.") < 0.2)


def test_whisper_split():
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    load_path_1 = os.path.join(data_folder, "1720168273.wav")
    whisper = WhisperModel()
    result = whisper.transcribe(load_path_1)
    # with open("data.txt", 'w') as f:
    #     f.write(result['text'])


def test_summary():
    paragraph = """The main input is the messages parameter. Messages must be an array of message objects, where each object has a role (either "system", "user", or "assistant") and content. Conversations can be as short as one message or many back and forth turns.
Typically, a conversation is formatted with a system message first, followed by alternating user and assistant messages.
The system message helps set the behavior of the assistant. For example, you can modify the personality of the assistant or provide specific instructions about how it should behave throughout the conversation. However note that the system message is optional and the model’s behavior without a system message is likely to be similar to using a generic message such as "You are a helpful assistant."
The user messages provide requests or comments for the assistant to respond to. Assistant messages store previous assistant responses, but can also be written by you to give examples of desired behavior.
Including conversation history is important when user instructions refer to prior messages. In the example above, the user’s final question of "Where was it played?" only makes sense in the context of the prior messages about the World Series of 2020. Because the models have no memory of past requests, all relevant information must be supplied as part of the conversation history in each request. If a conversation cannot fit within the model’s token limit, it will need to be shortened in some way."""
    model = SummarizeModel()
    result = model.infer(paragraph)
    print(result)
