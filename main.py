from helpers import mic, llm
import argparse
import importlib.util
from pathlib import Path
import wave
import random
import os
import sys
import time
import json

PROJECT_DIR = Path(__file__).resolve().parent


def load_vosk_classes():
    original_path = list(sys.path)
    old_vosk_module = sys.modules.pop("vosk", None)
    try:
        sys.path = [
            path for path in sys.path
            if Path(path or ".").resolve() != PROJECT_DIR
        ]
        import vosk
        return vosk.Model, vosk.KaldiRecognizer
    finally:
        sys.path = original_path
        if old_vosk_module is not None:
            sys.modules["vosk"] = old_vosk_module

class BonziResponse:
    def __init__(self, canned_directory="canned_responses/"):
        self.canned_directory = canned_directory
        self.canned_responses = [os.path.join(canned_directory, f) for f in os.listdir(canned_directory) if f.endswith('.wav')]
        self.preloaded_audio = self.preload_audio_files()

    def preload_audio_files(self):
        audio_files = {}
        for file_path in self.canned_responses:
            wf = wave.open(file_path, 'rb')
            audio_files[file_path] = wf.readframes(wf.getnframes())
        return audio_files

    def play_audio(self, file_path):
        audio_data = self.preloaded_audio[file_path]
        p = pyaudio.PyAudio()
        wf = wave.open(file_path, 'rb')
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        stream.write(audio_data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def play_random_response(self):
        response = random.choice(self.canned_responses)
        self.play_audio(response)

def listen_for_bonzi(device_index=None):
    from helpers import tts

    audio = mic.require_pyaudio()
    try:
        Model, KaldiRecognizer = load_vosk_classes()
    except (ModuleNotFoundError, ImportError, AttributeError):
        raise ModuleNotFoundError("Missing Python package: vosk. Run `pip install -r requirements.txt` first.")

    model_path = "vosk/vosk-model-small-en-us-0.15"
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    bonzi_response = BonziResponse()
    p = audio.PyAudio()
    stream = p.open(format=audio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000, input_device_index=device_index)
    stream.start_stream()

    keywords = ["bonzi", "bones you", "bones", "ponzi", "bondi", "banking", "bouncy", "monsey", "bonds it", "bons it", "juan the", "bungie", "bons the", "bonds the", "monte", "pansy", "bonds a", "bonds a", "bundy", "bonnie", "money", "bunny"]
    command_active = False

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            print(f"Heard: {text}")

            if command_active:
                # Directly use the first captured text as the command
                if text:
                    llm_response = llm.request(text.strip())
                    print(f"LLM response: {llm_response}")
                    tts.say(llm_response)
                command_active = False  # Reset after processing

            words = text.split()
            if any(keyword in text for keyword in keywords) and len(words) < 4 and not command_active:
                bonzi_response.play_random_response()
                time.sleep(.45)
                command_active = True  # Enable command capture

def run_setup_check():
    missing_dependencies = llm.get_missing_dependencies()
    if mic.pyaudio is None:
        missing_dependencies.append("pyaudio")
    for package_name in ("requests", "simpleaudio"):
        if importlib.util.find_spec(package_name) is None:
            missing_dependencies.append(package_name)
    try:
        load_vosk_classes()
    except (ModuleNotFoundError, ImportError, AttributeError):
        missing_dependencies.append("vosk")

    checks = {
        "Python dependencies": not missing_dependencies,
        "Vosk model": os.path.isdir("vosk/vosk-model-small-en-us-0.15"),
        "Canned responses": os.path.isdir("canned_responses") and any(
            f.endswith(".wav") for f in os.listdir("canned_responses")
        ),
        "LLM environment": not llm.get_missing_environment(),
        "Microphone config": mic.load_config() is not None,
    }

    for name, ok in checks.items():
        print(f"{'OK' if ok else 'MISSING'} - {name}")

    if missing_dependencies:
        print(
            "Run `pip install -r requirements.txt` to install: "
            + ", ".join(missing_dependencies)
        )

    missing_env = llm.get_missing_environment()
    if missing_env:
        print(
            "Copy helpers/.env.example to helpers/.env and set: "
            + ", ".join(missing_env)
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run BonziAssist.")
    parser.add_argument("--check", action="store_true", help="Check setup without starting the microphone loop.")
    args = parser.parse_args()

    if args.check:
        run_setup_check()
        raise SystemExit(0)

    config = mic.load_config()
    if config is None or config.get("prompt_every_time", False):
        config = mic.configure_microphone()
    device_index = config['device_index']
    listen_for_bonzi(device_index)
