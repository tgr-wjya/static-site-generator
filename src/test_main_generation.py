import tempfile
import unittest
from pathlib import Path

from main import generate_pages_recursive


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
                '<html><head><link href="/index.css"></head><body>{{ Content }}</body></html>',
                encoding="utf-8",
            )

            generate_pages_recursive(
                str(content_dir), str(template_path), str(public_dir), "/blog/"
            )

            output_path = public_dir / "blog" / "glorfindel" / "index.html"
            self.assertTrue(output_path.exists())
            self.assertIn("Glorfindel", output_path.read_text(encoding="utf-8"))
            self.assertIn(
                "Hello from the blog.", output_path.read_text(encoding="utf-8")
            )
            self.assertIn('href="/blog/index.css"', output_path.read_text(encoding="utf-8"))

    def test_generate_pages_rewrites_root_relative_assets(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            content_dir = root / "content"
            destination_dir = root / "docs"
            template_path = root / "template.html"

            content_dir.mkdir()
            (content_dir / "index.md").write_text(
                "# Home\n\n![Tolkien](/images/tolkien.png)", encoding="utf-8"
            )
            template_path.write_text(
                '<link href="/index.css"><body>{{ Content }}</body>',
                encoding="utf-8",
            )

            generate_pages_recursive(
                str(content_dir), str(template_path), str(destination_dir), "/site/"
            )

            output = (destination_dir / "index.html").read_text(encoding="utf-8")
            self.assertIn('href="/site/index.css"', output)
            self.assertIn('src="/site/images/tolkien.png"', output)


if __name__ == "__main__":
    unittest.main()
