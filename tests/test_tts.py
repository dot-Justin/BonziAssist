from __future__ import annotations

import importlib.util
import io
import struct
import sys
import types
import unittest
import wave
from pathlib import Path
from unittest.mock import Mock, patch


def wav_bytes() -> bytes:
    output = io.BytesIO()
    with wave.open(output, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(8000)
        audio.writeframes(struct.pack("<4h", 0, 100, -100, 0))
    return output.getvalue()


class FakeStream:
    def __init__(self) -> None:
        self.writes: list[bytes] = []
        self.stopped = False
        self.closed = False

    def write(self, data: bytes) -> None:
        self.writes.append(data)

    def stop_stream(self) -> None:
        self.stopped = True

    def close(self) -> None:
        self.closed = True


class FakePyAudio:
    instances: list["FakePyAudio"] = []

    def __init__(self) -> None:
        self.stream = FakeStream()
        self.terminated = False
        self.open_kwargs = None
        self.__class__.instances.append(self)

    def get_format_from_width(self, width: int) -> int:
        return width

    def open(self, **kwargs):
        self.open_kwargs = kwargs
        return self.stream

    def terminate(self) -> None:
        self.terminated = True


class TtsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fake_pyaudio = types.SimpleNamespace(PyAudio=FakePyAudio)
        sys.modules["pyaudio"] = fake_pyaudio
        path = Path(__file__).parents[1] / "helpers" / "tts.py"
        spec = importlib.util.spec_from_file_location("bonzi_tts", path)
        assert spec and spec.loader
        cls.tts = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.tts)

    def setUp(self) -> None:
        FakePyAudio.instances.clear()

    def test_say_downloads_and_plays_wav(self) -> None:
        response = Mock(content=wav_bytes())
        response.raise_for_status = Mock()
        with patch.object(self.tts.requests, "get", return_value=response) as get:
            self.tts.say("hello world")

        get.assert_called_once()
        self.assertEqual(get.call_args.kwargs["timeout"], 30)
        response.raise_for_status.assert_called_once_with()
        player = FakePyAudio.instances[0]
        self.assertTrue(player.stream.writes)
        self.assertTrue(player.stream.stopped)
        self.assertTrue(player.stream.closed)
        self.assertTrue(player.terminated)

    def test_http_failure_is_propagated_before_playback(self) -> None:
        response = Mock()
        response.raise_for_status.side_effect = RuntimeError("download failed")
        with patch.object(self.tts.requests, "get", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "download failed"):
                self.tts.say("hello")
        self.assertEqual(FakePyAudio.instances, [])


if __name__ == "__main__":
    unittest.main()
