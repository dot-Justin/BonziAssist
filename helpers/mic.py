import json
import os
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_FILE = APP_ROOT / "mic_config.json"
CONFIG_FILE = DEFAULT_CONFIG_FILE
CONFIG_ENV_VAR = "BONZI_MIC_CONFIG"


def _pyaudio():
    import pyaudio
    return pyaudio


def _config_path(config_path=None):
    if config_path is not None:
        return Path(config_path)

    override = os.getenv(CONFIG_ENV_VAR)
    if override:
        return Path(override).expanduser()

    return DEFAULT_CONFIG_FILE


def _bool_from_config(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def _normalize_config(config, config_path):
    if not isinstance(config, dict):
        print(f"Microphone config at {config_path} is not a JSON object. Reconfiguring.")
        return None

    if "device_index" not in config:
        legacy_note = " The old mic_index key is no longer used." if "mic_index" in config else ""
        print(f"Microphone config at {config_path} is missing device_index.{legacy_note} Reconfiguring.")
        return None

    try:
        device_index = int(config["device_index"])
    except (TypeError, ValueError):
        print(f"Microphone config at {config_path} has an invalid device_index. Reconfiguring.")
        return None

    if device_index < 0:
        print(f"Microphone config at {config_path} has a negative device_index. Reconfiguring.")
        return None

    return {
        "device_index": device_index,
        "prompt_every_time": _bool_from_config(config.get("prompt_every_time", False)),
    }


def list_microphones():
    p = _pyaudio().PyAudio()
    try:
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
        return default_device_name
    finally:
        p.terminate()

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


def load_config(config_path=None):
    path = _config_path(config_path)
    if not path.exists():
        return None

    try:
        with path.open("r", encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read microphone config at {path}: {exc}. Reconfiguring.")
        return None

    return _normalize_config(config, path)


def save_config(config, config_path=None):
    path = _config_path(config_path)
    normalized_config = _normalize_config(config, path)
    if normalized_config is None:
        raise ValueError("Microphone config must include a non-negative device_index.")

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(normalized_config, f, indent=4)
        f.write("\n")


def configure_microphone():
    print("Available microphones:")
    default_device_name = list_microphones()
    p = _pyaudio().PyAudio()
    try:
        num_devices = p.get_host_api_info_by_index(0).get('deviceCount')
        default_device_index = p.get_default_input_device_info().get('index')
    finally:
        p.terminate()
    device_index = get_device_index(num_devices, default_device_index, default_device_name)
    prompt_every_time = input("Do you want to be prompted to select a microphone every time? (y/n): ").strip().lower()
    config = {
        "device_index": device_index,
        "prompt_every_time": prompt_every_time == 'y',
    }
    save_config(config)
    return config
