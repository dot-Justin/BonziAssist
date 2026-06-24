import importlib
import json
import os
import tempfile
import unittest
from pathlib import Path


class MicConfigTests(unittest.TestCase):
    def setUp(self):
        self.previous_config = os.environ.get("BONZI_MIC_CONFIG")
        self.tempdir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.tempdir.name) / "nested" / "mic_config.json"
        os.environ["BONZI_MIC_CONFIG"] = str(self.config_path)

        import helpers.mic as mic

        self.mic = importlib.reload(mic)

    def tearDown(self):
        self.tempdir.cleanup()
        if self.previous_config is None:
            os.environ.pop("BONZI_MIC_CONFIG", None)
        else:
            os.environ["BONZI_MIC_CONFIG"] = self.previous_config

    def test_missing_config_returns_none(self):
        self.assertIsNone(self.mic.load_config())

    def test_legacy_mic_index_is_accepted(self):
        self.config_path.parent.mkdir(parents=True)
        self.config_path.write_text(json.dumps({"mic_index": 53}), encoding="utf-8")

        config = self.mic.load_config()

        self.assertEqual(config["device_index"], 53)
        self.assertFalse(config["prompt_every_time"])

    def test_save_config_creates_parent_directory(self):
        self.mic.save_config({"device_index": 7, "prompt_every_time": True})

        config = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["device_index"], 7)
        self.assertTrue(config["prompt_every_time"])


if __name__ == "__main__":
    unittest.main()
