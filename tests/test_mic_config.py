import importlib
import json
import os
import tempfile
import unittest
from pathlib import Path


class MicConfigTests(unittest.TestCase):
    def reload_mic_with_config(self, config_path):
        os.environ["BONZI_MIC_CONFIG"] = str(config_path)
        import helpers.mic as mic
        return importlib.reload(mic)

    def tearDown(self):
        os.environ.pop("BONZI_MIC_CONFIG", None)

    def test_load_config_returns_none_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            mic = self.reload_mic_with_config(Path(tmp) / "missing" / "mic_config.json")
            self.assertIsNone(mic.load_config())

    def test_save_config_creates_parent_directory_and_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "config" / "mic_config.json"
            mic = self.reload_mic_with_config(config_path)

            mic.save_config({"device_index": 3, "prompt_every_time": False})

            self.assertTrue(config_path.exists())
            self.assertEqual(
                json.loads(config_path.read_text()),
                {"device_index": 3, "prompt_every_time": False},
            )
            self.assertEqual(
                mic.load_config(),
                {"device_index": 3, "prompt_every_time": False},
            )


if __name__ == "__main__":
    unittest.main()
