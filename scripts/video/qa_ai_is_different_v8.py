#!/usr/bin/env python3
"""Versioned entry point for the AI Is Different v8 verification pass."""

from pathlib import Path
import runpy


runpy.run_path(
    str(Path(__file__).with_name("qa_ai_is_different_v7.py")),
    run_name="__main__",
)
