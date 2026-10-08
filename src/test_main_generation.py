import tempfile
import unittest
from pathlib import Path

from main import generate_pages


class TestMainGeneration(unittest.TestCase):
    def test_generate_pages_creates_nested_output(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            content_dir = root / "content"
            public_dir = root / "public"
            template_path = root / "template.html"

            (content_dir / "blog" / "glorfindel").mkdir(parents=True)
            (content_dir / "blog" / "glorfindel" / "index.md").write_text(
                "# Glorfindel\n\nHello from the blog.", encoding="utf-8"
            )
            template_path.write_text(
                "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>",
                encoding="utf-8",
            )

            generate_pages(str(content_dir), str(template_path), str(public_dir))

            output_path = public_dir / "blog" / "glorfindel" / "index.html"
            self.assertTrue(output_path.exists())
            self.assertIn("Glorfindel", output_path.read_text(encoding="utf-8"))
            self.assertIn(
                "Hello from the blog.", output_path.read_text(encoding="utf-8")
            )


if __name__ == "__main__":
    unittest.main()
