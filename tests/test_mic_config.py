"""Tests for the microphone config path and schema.

The app previously crashed on startup because:
1. ``CONFIG_FILE`` used a backslash path ("config\\mic_config.json") that only
   resolves on Windows from the repo root, and pointed at a config/ directory
   that does not exist (the file lives at the repo root).
2. The checked-in ``mic_config.json`` used the key ``mic_index`` while
   ``main.py`` reads ``device_index``, raising a KeyError on first run.
"""

import json
import sys
import types
from pathlib import Path

import pytest

# pyaudio is a heavy native dependency; stub it out for these tests.
pyaudio_stub = types.ModuleType("pyaudio")
sys.modules["pyaudio"] = pyaudio_stub

from helpers import mic  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_config_file_resolves_to_repo_root():
    """The config path must be anchored to the repo root, cross-platform."""
    assert "\\" not in mic.CONFIG_FILE
    assert Path(mic.CONFIG_FILE) == REPO_ROOT / "mic_config.json"


def test_checked_in_config_uses_device_index_schema():
    """The shipped config must match the schema main.py reads."""
    with open(REPO_ROOT / "mic_config.json") as f:
        config = json.load(f)
    assert "device_index" in config
    assert "mic_index" not in config
    assert isinstance(config["device_index"], int)


def test_load_save_round_trip(tmp_path, monkeypatch):
    """load_config/save_config must round-trip through the resolved path."""
    monkeypatch.setattr(mic, "CONFIG_FILE", str(tmp_path / "mic_config.json"))
    config = {"device_index": 3, "prompt_every_time": False}
    mic.save_config(config)
    assert mic.load_config() == config


def test_load_config_returns_none_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mic, "CONFIG_FILE", str(tmp_path / "nope.json"))
    assert mic.load_config() is None
