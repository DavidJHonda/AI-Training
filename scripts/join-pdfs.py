"""Merge PDF page objects without redrawing text; validate before replacing output."""
import argparse
import os
from pathlib import Path
import tempfile

from pypdf import PdfReader, PdfWriter


def merge(output, inputs, min_text_chars=0):
    output = Path(output)
    writer = PdfWriter()
    expected = []
    # Copy the original page objects, including font programs and Unicode maps.
    for source in inputs:
        reader = PdfReader(source)
        if not reader.pages:
            raise ValueError(f"No pages in {source}")
        for number, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            if len(text.strip()) < min_text_chars:
                raise ValueError(f"{source}, page {number}: insufficient searchable text ({len(text.strip())} characters)")
            expected.append((text, tuple(page.mediabox)))
            writer.add_page(page)
    if not expected:
        raise ValueError("No input pages")
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=output.stem + "-", suffix=".pdf", dir=output.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            writer.write(stream)
        merged = PdfReader(name)
        if len(merged.pages) != len(expected):
            raise ValueError("Page count changed during merge")
        for number, (page, (text, box)) in enumerate(zip(merged.pages, expected), 1):
            if (page.extract_text() or "") != text or tuple(page.mediabox) != box:
                raise ValueError(f"Page {number}: searchable text or page dimensions changed during merge")
        os.replace(name, output)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return len(expected)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-text-chars", type=int, default=0)
    parser.add_argument("output")
    parser.add_argument("inputs", nargs="+")
    args = parser.parse_args()
    count = merge(args.output, args.inputs, args.min_text_chars)
    print(f"{count} pages; searchable text and page dimensions preserved")
