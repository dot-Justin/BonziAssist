import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from helpers import mic


class MicConfigTests(unittest.TestCase):
    def load_config_quietly(self, config_path):
        with redirect_stdout(io.StringIO()):
            return mic.load_config(config_path)

    def test_default_config_path_is_project_root(self):
        self.assertEqual(
            mic.DEFAULT_CONFIG_FILE,
            Path(mic.__file__).resolve().parents[1] / "mic_config.json",
        )

    def test_load_config_returns_none_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(mic.load_config(Path(tmp) / "missing" / "mic_config.json"))

    def test_save_config_creates_parent_directory_and_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "nested" / "mic_config.json"

            mic.save_config(
                {"device_index": "3", "prompt_every_time": "yes"},
                config_path,
            )

            self.assertEqual(
                json.loads(config_path.read_text(encoding="utf-8")),
                {"device_index": 3, "prompt_every_time": True},
            )
            self.assertEqual(
                mic.load_config(config_path),
                {"device_index": 3, "prompt_every_time": True},
            )

    def test_load_config_rejects_legacy_mic_index_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "mic_config.json"
            config_path.write_text('{"mic_index": 53}', encoding="utf-8")

            self.assertIsNone(self.load_config_quietly(config_path))

    def test_load_config_rejects_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "mic_config.json"
            config_path.write_text("{not json", encoding="utf-8")

            self.assertIsNone(self.load_config_quietly(config_path))


if __name__ == "__main__":
    unittest.main()
