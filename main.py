from __future__ import annotations

import json
import os
import random
import time
import wave
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = PROJECT_ROOT / "vosk" / "vosk-model-small-en-us-0.15"


def resolve_model_path() -> Path:
    override = os.environ.get("BONZI_VOSK_MODEL")
    path = Path(override).expanduser() if override else DEFAULT_MODEL_PATH
    if not path.is_dir():
        raise FileNotFoundError(
            "Vosk model not found. Download 'vosk-model-small-en-us-0.15', place it at "
            f"'{DEFAULT_MODEL_PATH}', or set BONZI_VOSK_MODEL to its directory."
        )
    return path


class BonziResponse:
    def __init__(self, canned_directory: Path | None = None) -> None:
        self.canned_directory = canned_directory or PROJECT_ROOT / "canned_responses"
        self.canned_responses = sorted(self.canned_directory.glob("*.wav"))
        if not self.canned_responses:
            raise FileNotFoundError(f"No canned response WAV files found in '{self.canned_directory}'.")
        self.preloaded_audio = self.preload_audio_files()

    def preload_audio_files(self) -> dict[Path, bytes]:
        audio_files: dict[Path, bytes] = {}
        for file_path in self.canned_responses:
            with wave.open(str(file_path), "rb") as audio_file:
                audio_files[file_path] = audio_file.readframes(audio_file.getnframes())
        return audio_files

    def play_audio(self, file_path: Path) -> None:
        import pyaudio

        audio_data = self.preloaded_audio[file_path]
        audio = pyaudio.PyAudio()
        with wave.open(str(file_path), "rb") as audio_file:
            stream = audio.open(
                format=audio.get_format_from_width(audio_file.getsampwidth()),
                channels=audio_file.getnchannels(),
                rate=audio_file.getframerate(),
                output=True,
            )
            try:
                stream.write(audio_data)
            finally:
                stream.stop_stream()
                stream.close()
                audio.terminate()

    def play_random_response(self) -> None:
        self.play_audio(random.choice(self.canned_responses))


def listen_for_bonzi(device_index: int | None = None) -> None:
    import pyaudio
    from vosk import KaldiRecognizer, Model

    from helpers import llm, tts

    model = Model(str(resolve_model_path()))
    recognizer = KaldiRecognizer(model, 16000)
    bonzi_response = BonziResponse()
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8000,
        input_device_index=device_index,
    )
    stream.start_stream()

    keywords = [
        "bonzi", "bones you", "bones", "ponzi", "bondi", "banking", "bouncy",
        "monsey", "bonds it", "bons it", "juan the", "bungie", "bons the",
        "bonds the", "monte", "pansy", "bonds a", "bundy", "bonnie", "money", "bunny",
    ]
    command_active = False

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            text = json.loads(recognizer.Result()).get("text", "")
            print(f"Heard: {text}")

            if command_active:
                if text:
                    llm_response = llm.request(text.strip())
                    print(f"LLM response: {llm_response}")
                    tts.say(llm_response)
                command_active = False

            words = text.split()
            if any(keyword in text for keyword in keywords) and len(words) < 4 and not command_active:
                bonzi_response.play_random_response()
                time.sleep(0.45)
                command_active = True


def main() -> int:
    from helpers import mic

    try:
        resolve_model_path()
        config = mic.load_config()
        if config is None or config.get("prompt_every_time", False):
            config = mic.configure_microphone()
        listen_for_bonzi(config["device_index"])
    except (FileNotFoundError, KeyError) as exc:
        print(f"Startup error: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
