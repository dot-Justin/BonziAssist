import os
import json
from pathlib import Path

DEFAULT_CONFIG_FILE = Path(__file__).resolve().parents[1] / "mic_config.json"


def get_config_file():
    override = os.getenv("BONZI_MIC_CONFIG")
    if override:
        return Path(override).expanduser()
    return DEFAULT_CONFIG_FILE


def get_pyaudio():
    import pyaudio

    return pyaudio

def list_microphones():
    pyaudio = get_pyaudio()
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    default_device_index = p.get_default_input_device_info().get('index')
    default_device_name = p.get_device_info_by_index(default_device_index).get('name')

    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            if i == default_device_index:
                print(f"{i}: - {device_info.get('name')} (default)")
            else:
                print(f"{i}: - {device_info.get('name')}")
    p.terminate()
    return default_device_name

def get_device_index(num_devices, default_device_index, default_device_name):
    while True:
        user_input = input(f"Enter the Input Device id you want to use (enter = '{default_device_name}'): ").strip()
        if user_input == "":
            return default_device_index  # Default to the default device if no input is given
        if user_input.isdigit():
            device_index = int(user_input)
            if 0 <= device_index < num_devices:
                return device_index
        print("Invalid input. Please enter a valid number.")

def load_config():
    config_file = get_config_file()
    if config_file.exists():
        with config_file.open("r", encoding="utf-8") as f:
            config = json.load(f)
        if "device_index" not in config and "mic_index" in config:
            config["device_index"] = config["mic_index"]
        config.setdefault("prompt_every_time", False)
        return config
    return None

def save_config(config):
    config_file = get_config_file()
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with config_file.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def configure_microphone():
    print("Available microphones:")
    default_device_name = list_microphones()
    pyaudio = get_pyaudio()
    p = pyaudio.PyAudio()
    num_devices = p.get_host_api_info_by_index(0).get('deviceCount')
    default_device_index = p.get_default_input_device_info().get('index')
    p.terminate()
    device_index = get_device_index(num_devices, default_device_index, default_device_name)
    prompt_every_time = input("Do you want to be prompted to select a microphone every time? (y/n): ").strip().lower()
    config = {
        "device_index": device_index,
        "prompt_every_time": prompt_every_time == 'y'
    }
    save_config(config)
    return config
