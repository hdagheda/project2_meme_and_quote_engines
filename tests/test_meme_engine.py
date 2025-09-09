# tests/test_meme_engine.py
import os
import shutil
import tempfile
import unittest
from PIL import Image

from MemeEngine import MemeEngine


class TestMemeEngine(unittest.TestCase):
    def setUp(self):
        # Temporary output directory for memes
        self.tmp_dir = tempfile.mkdtemp(prefix="memeengine-tests-")
        # Create a temporary input image
        self.input_dir = tempfile.mkdtemp(prefix="memeengine-input-")
        self.input_image_path = os.path.join(self.input_dir, "input.jpg")

        # Generate a simple image (white background)
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))
        img.save(self.input_image_path, "JPEG")

        self.engine = MemeEngine(self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        shutil.rmtree(self.input_dir, ignore_errors=True)

    def test_output_dir_created(self):
        # The output directory should exist after initialization
        self.assertTrue(os.path.isdir(self.tmp_dir))

    def test_make_meme_creates_file(self):
        quote_body = "Stay pawsitive."
        quote_author = "Doggo"

        out_path = self.engine.make_meme(self.input_image_path, quote_body, quote_author)

        # The method should return a valid path
        self.assertIsInstance(out_path, str)
        self.assertTrue(os.path.isabs(out_path) or os.path.exists(out_path))

        # The file should exist and be a readable image
        self.assertTrue(os.path.isfile(out_path))
        with Image.open(out_path) as out_img:
            out_img.verify()  # verifies it's an image

        # Ensure the output is placed under the configured tmp dir (or within it)
        self.assertTrue(os.path.dirname(out_path).startswith(self.tmp_dir))

    def test_make_meme_with_empty_text(self):
        # Even with empty text, a meme image should be produced (no overlay)
        out_path = self.engine.make_meme(self.input_image_path, "", "")
        self.assertTrue(os.path.isfile(out_path))
        with Image.open(out_path) as out_img:
            out_img.verify()

    def test_make_meme_invalid_image_raises(self):
        with self.assertRaises(Exception):
            self.engine.make_meme("nonexistent_image.jpg", "Hello", "Author")


if __name__ == "__main__":
    unittest.main()