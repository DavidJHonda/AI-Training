"""Regression checks for searchable packet assembly. Run with .video-venv/bin/python."""
from pathlib import Path
import runpy
import tempfile
import unittest

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

merge = runpy.run_path(str(Path(__file__).with_name("join-pdfs.py")))["merge"]


class PacketMergeTests(unittest.TestCase):
    def test_text_order_fonts_and_continuous_page_sizes_survive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = []
            for i, (font, size) in enumerate((("Helvetica", (720, 2500)), ("Times-Roman", (720, 1800)))):
                path = root / f"lesson-{i}.pdf"
                pdf = canvas.Canvas(str(path), pagesize=size)
                pdf.setFont(font, 14)
                for line in range(12):
                    pdf.drawString(40, size[1] - 50 - line * 22, f"Lesson {i}: AI can help you learn. Don’t skip the thinking. Line {line}.")
                pdf.showPage()
                pdf.save()
                sources.append(path)
            expected = [(page.extract_text(), tuple(page.mediabox))
                        for path in sources for page in PdfReader(path).pages]
            destination = root / "packet.pdf"
            self.assertEqual(merge(destination, sources, min_text_chars=200), 2)
            actual = [(page.extract_text(), tuple(page.mediabox)) for page in PdfReader(destination).pages]
            self.assertEqual(actual, expected)
            self.assertIn("Don’t skip the thinking", actual[0][0])

    def test_unsearchable_input_does_not_replace_the_previous_packet(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "outlined.pdf"
            writer = PdfWriter()
            writer.add_blank_page(width=720, height=2500)
            writer.write(source)
            destination = root / "packet.pdf"
            destination.write_bytes(b"previous packet")
            with self.assertRaisesRegex(ValueError, "insufficient searchable text"):
                merge(destination, [source], min_text_chars=200)
            self.assertEqual(destination.read_bytes(), b"previous packet")


if __name__ == "__main__":
    unittest.main()
