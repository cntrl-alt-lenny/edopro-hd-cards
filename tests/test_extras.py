import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import extras


class OptionalExtrasTests(unittest.TestCase):
    def test_replaces_files_and_preserves_each_previous_version(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artwork = root / "assets" / "textures" / "bg.png"
            artwork.parent.mkdir(parents=True)
            artwork.write_bytes(b"new background")
            game = root / "game"
            background = game / "textures" / "bg.png"
            background.parent.mkdir(parents=True)
            background.write_bytes(b"stock background")
            config = root / "state" / "config.json"

            with patch.object(extras, "ASSETS", root / "assets"):
                extras.install(str(game), str(config), "textures")
                extras.install(str(game), str(config), "textures")
                background.write_bytes(b"user background")
                extras.install(str(game), str(config), "textures")

            self.assertEqual(background.read_bytes(), b"new background")
            backups = (config.parent / "extras-backups").rglob("bg.png")
            self.assertCountEqual(
                (file.read_bytes() for file in backups), [b"stock background", b"user background"]
            )
