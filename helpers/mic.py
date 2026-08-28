import pyaudio
import os
import json

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(_ROOT, "mic_config.json")
LEGACY_WIN_PATH = os.path.join(_ROOT, "config", "mic_config.json")
LEGACY_LITERAL_PATH = os.path.join(_ROOT, "config\\mic_config.json")


def _existing_config_path():
    for path in (CONFIG_FILE, LEGACY_WIN_PATH, LEGACY_LITERAL_PATH):
        if os.path.isfile(path):
            return path
    return CONFIG_FILE


def _normalize(config):
    if not isinstance(config, dict):
        return config
    if "device_index" not in config and "mic_index" in config:
        config = dict(config)
        config["device_index"] = config["mic_index"]
    return config


def list_microphones():
    p = pyaudio.PyAudio()
    try:
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get("deviceCount")
        default_device_index = p.get_default_input_device_info().get("index")
        default_device_name = p.get_device_info_by_index(default_device_index).get("name")
        for i in range(num_devices):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            if device_info.get("maxInputChannels") > 0:
                suffix = " (default)" if i == default_device_index else ""
                print(f"{i}: - {device_info.get('name')}{suffix}")
        return default_device_name
    finally:
        p.terminate()


def get_device_index(num_devices, default_device_index, default_device_name):
    while True:
        user_input = input(
            f"Enter the Input Device id you want to use (enter = '{default_device_name}'): "
        ).strip()
        if user_input == "":
            return default_device_index
        if user_input.isdigit():
            device_index = int(user_input)
            if 0 <= device_index < num_devices:
                return device_index
        print("Invalid input. Please enter a valid number.")


def load_config():
    path = _existing_config_path()
    if os.path.isfile(path):
        with open(path, "r") as f:
            return _normalize(json.load(f))
    return None


def save_config(config):
    os.makedirs(_ROOT, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def configure_microphone():
    print("Available microphones:")
    default_device_name = list_microphones()
    p = pyaudio.PyAudio()
    try:
        num_devices = p.get_host_api_info_by_index(0).get("deviceCount")
        default_device_index = p.get_default_input_device_info().get("index")
    finally:
        p.terminate()
    device_index = get_device_index(num_devices, default_device_index, default_device_name)
    prompt_every_time = input(
        "Do you want to be prompted to select a microphone every time? (y/n): "
    ).strip().lower()
    config = {
        "device_index": device_index,
        "prompt_every_time": prompt_every_time == "y",
    }
    save_config(config)
    return config
