import sys
import threading
import functools
import os
import shutil
import shlex
import yaml
import time
from meeting_note import MicrophoneRecorder
from meeting_note import SummarizeModel
from meeting_note import WhisperModel

class App:
    def __init__(self, config):
        self.fn = [
            "start", "stop", "start_continuous", "summarize"
        ]
        self.config = config
        self.recorder = MicrophoneRecorder(config["record"]["rate"], config["record"]["chunk"], config["record"]["channels"])
        self.whisper = WhisperModel(config["transcribe"]["model"], config["transcribe"].get("language"))
        self.summary = SummarizeModel(config["summary"]["model"], config["summary"].get("prompt"))
        self.recorder.set_default_device_id(config["record"]["device_id"])
        self.text_file = open(os.path.join(config["save_path"], "transcribe.txt"), 'w')
        self.thread = None
        self.files = []
        self.text = []
        self.summary_result = ""
    def __del__(self):
        self.text_file.close()
    def help(self):
        return "Please use the following supported commands: {}".format(", ".join(self.fn))
    def __call__(self, command, args):
        if command not in self.fn:
            raise Exception("No command: {}, all_commands: {}".format(command, ', '.join(self.fn)))
        self.__getattribute__(command)(*args)
    def start(self):
        if self.thread is not None:
            raise Exception("start: Please stop recording first.")
        data_folder = self.config["save_path"]
        file_name = str(int(time.time()))
        save_path = os.path.join(data_folder, "{}.wav".format(file_name))
        self.files.append(save_path)
        self.recorder.start_stream()
        self.thread = threading.Thread(target=functools.partial(self.recorder.record_flow, file_name=save_path))
        self.thread.start()
    def stop(self):
        if self.thread is None:
            raise Exception("stop: Please start recording first.")
        self.recorder.close_stream()
        self.thread.join()
        self.thread = None
        text = self.whisper.transcribe(self.files[-1])["text"]
        self.text.append(text)
        path_name = os.path.basename(self.files[-1])
        print("{}: {}".format(path_name, text), flush=True)
        self.text_file.write("\n{}\n".format(text))
        self.text_file.flush()
    def summarize(self):
        self.summary_result = self.summary.infer('\n'.join(self.text))["text"]
        with open(os.path.join(self.config["save_path"], "summary.txt"), 'w') as f:
            f.write("{}\n".format(self.summary_result))
        print("summary: {}".format(self.summary_result))


def main():
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    recorder = MicrophoneRecorder()
    if config["record"].get("device_id", -1) < 0:
        prompt = "Please choose your device_id:\n"
        for k, item in recorder.get_all_devices().items():
            prompt += "{}) {}\n".format(k, item['name'])
        while True:
            print(prompt, flush=True)
            line = sys.stdin.readline()
            try:
                if int(line.strip()) in recorder.get_all_devices():
                    config["record"]["device_id"] = int(line.strip())
                    break
                print("no such device_id: {}".format(line.strip()), flush=True)
            except Exception:
                print("no such device_id: {}".format(line.strip()), flush=True)
    print("Please set a directory to save your files:", flush=True)
    config["save_path"] = sys.stdin.readline().strip()
    if os.path.exists(config["save_path"]):
        shutil.rmtree(config["save_path"])
    os.mkdir(config["save_path"])
    app = App(config)
    print(app.help(), flush=True)
    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        line = line.strip()
        try:
            command, *args = shlex.split(line)
            app(command, args)
        except Exception as e:
            print(e, file=sys.stderr, flush=True)

if __name__ == "__main__":
    main()
