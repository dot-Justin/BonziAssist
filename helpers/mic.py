from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_FILE = PROJECT_ROOT / "mic_config.json"


def config_file() -> Path:
    override = os.environ.get("BONZI_MIC_CONFIG")
    return Path(override).expanduser() if override else DEFAULT_CONFIG_FILE


def _pyaudio():
    import pyaudio

    return pyaudio


def list_microphones() -> str:
    pyaudio = _pyaudio()
    audio = pyaudio.PyAudio()
    try:
        info = audio.get_host_api_info_by_index(0)
        num_devices = info.get("deviceCount")
        default_device_index = audio.get_default_input_device_info().get("index")
        default_device_name = audio.get_device_info_by_index(default_device_index).get("name")

        for index in range(num_devices):
            device_info = audio.get_device_info_by_host_api_device_index(0, index)
            if device_info.get("maxInputChannels") > 0:
                suffix = " (default)" if index == default_device_index else ""
                print(f"{index}: - {device_info.get('name')}{suffix}")
        return default_device_name
    finally:
        audio.terminate()


def get_device_index(num_devices: int, default_device_index: int, default_device_name: str) -> int:
    while True:
        user_input = input(
            f"Enter the Input Device id you want to use (enter = '{default_device_name}'): "
        ).strip()
        if not user_input:
            return default_device_index
        if user_input.isdigit():
            device_index = int(user_input)
            if 0 <= device_index < num_devices:
                return device_index
        print("Invalid input. Please enter a valid number.")


def load_config() -> dict[str, Any] | None:
    path = config_file()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("device_index"), int):
        return None
    return payload


def save_config(config: dict[str, Any]) -> None:
    path = config_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=4) + "\n", encoding="utf-8")


def configure_microphone() -> dict[str, Any]:
    print("Available microphones:")
    default_device_name = list_microphones()
    pyaudio = _pyaudio()
    audio = pyaudio.PyAudio()
    try:
        num_devices = audio.get_host_api_info_by_index(0).get("deviceCount")
        default_device_index = audio.get_default_input_device_info().get("index")
    finally:
        audio.terminate()

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
