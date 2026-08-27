"""Tests for coverage reporting to ignore corrupt artwork."""

import os
import tempfile
import types
import unittest

import main


class CoverageTests(unittest.TestCase):
    def test_corrupt_images_are_not_counted_as_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            pics = os.path.join(tmp, "pics")
            field = os.path.join(pics, "field")
            os.makedirs(field)
            valid_jpeg = main.JPEG_MAGIC + b"x" * 1024 + main.JPEG_END
            valid_png = main.PNG_MAGIC + b"x" * 1024 + b"IEND"
            files = {
                os.path.join(pics, "1.jpg"): valid_jpeg,
                os.path.join(pics, "2.jpg"): b"broken" * 200,
                os.path.join(field, "3.png"): valid_png,
                os.path.join(field, "4.png"): b"broken" * 200,
            }
            for path, content in files.items():
                with open(path, "wb") as file_obj:
                    file_obj.write(content)

            cfg = types.SimpleNamespace(
                pics_path=pics,
                config_path=os.path.join(tmp, "state", "config.json"),
            )
            data = main.collect_coverage_stats(
                cfg, {1: "One", 2: "Two", 3: "Three", 4: "Four"}, {3, 4}
            )

        self.assertEqual(data["cards_total"], 4)
        self.assertEqual(data["cards_have"], 1)
        self.assertEqual(data["fields_total"], 2)
        self.assertEqual(data["fields_have"], 1)
        self.assertEqual(data["disk_bytes"], sum(len(content) for content in files.values()))


if __name__ == "__main__":
    unittest.main()
