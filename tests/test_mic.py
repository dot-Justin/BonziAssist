from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from helpers import mic


class MicrophoneConfigTests(unittest.TestCase):
    def test_missing_config_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "mic.json"
            with patch.dict(os.environ, {"BONZI_MIC_CONFIG": str(path)}):
                self.assertIsNone(mic.load_config())

    def test_invalid_config_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mic.json"
            path.write_text("not-json", encoding="utf-8")
            with patch.dict(os.environ, {"BONZI_MIC_CONFIG": str(path)}):
                self.assertIsNone(mic.load_config())

    def test_save_creates_parent_and_round_trips(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "mic.json"
            expected = {"device_index": 2, "prompt_every_time": False}
            with patch.dict(os.environ, {"BONZI_MIC_CONFIG": str(path)}):
                mic.save_config(expected)
                self.assertEqual(mic.load_config(), expected)
                self.assertEqual(json.loads(path.read_text(encoding="utf-8")), expected)


if __name__ == "__main__":
    unittest.main()
