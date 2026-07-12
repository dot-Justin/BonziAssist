from helpers import mic, llm, tts
import pyaudio
import wave
import random
import os
import time
import json
from vosk import Model, KaldiRecognizer
import urllib.request
import zipfile

VOSK_MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
VOSK_MODEL_DIR = "vosk"
VOSK_MODEL_NAME = "vosk-model-small-en-us-0.15"

def download_vosk_model():
    """Download Vosk model if not present"""
    model_path = os.path.join(VOSK_MODEL_DIR, VOSK_MODEL_NAME)
    
    if os.path.exists(model_path):
        print(f"Vosk model found at {model_path}")
        return model_path
    
    print("Vosk model not found. Downloading...")
    os.makedirs(VOSK_MODEL_DIR, exist_ok=True)
    
    zip_path = os.path.join(VOSK_MODEL_DIR, f"{VOSK_MODEL_NAME}.zip")
    try:
        urllib.request.urlretrieve(VOSK_MODEL_URL, zip_path)
        print("Download complete. Extracting...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(VOSK_MODEL_DIR)
        
        os.remove(zip_path)
        print(f"Vosk model installed at {model_path}")
        return model_path
    except Exception as e:
        print(f"Failed to download Vosk model: {e}")
        raise

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
    model_path = download_vosk_model()
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    bonzi_response = BonziResponse()
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000, input_device_index=device_index)
    stream.start_stream()

    keywords = ["bonzi", "bones you", "bones", "ponzi", "bondi", "banking", "bouncy", "monsey", "bonds it", "bons it", "juan the", "bungie", "bons the", "bonds the", "monte", "pansy", "bonds a"]
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

if __name__ == "__main__":
    config = mic.load_config()
    if config is None or config.get("prompt_every_time", False):
        config = mic.configure_microphone()
    device_index = config['device_index']
    listen_for_bonzi(device_index)
