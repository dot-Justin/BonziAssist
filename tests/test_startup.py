from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class StartupTests(unittest.TestCase):
    def test_missing_model_has_actionable_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing-model"
            with patch.dict(os.environ, {"BONZI_VOSK_MODEL": str(missing)}):
                with self.assertRaisesRegex(FileNotFoundError, "BONZI_VOSK_MODEL"):
                    main.resolve_model_path()

    def test_model_override_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            model = Path(directory) / "model"
            model.mkdir()
            with patch.dict(os.environ, {"BONZI_VOSK_MODEL": str(model)}):
                self.assertEqual(main.resolve_model_path(), model)


if __name__ == "__main__":
    unittest.main()
