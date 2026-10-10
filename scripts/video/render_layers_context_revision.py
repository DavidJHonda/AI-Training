#!/usr/bin/env python3
"""Canonical Layers CAT/IT board and pronunciation variant, 2026-10-10.

Render the editable native board source without changing other lesson boards.
"""
from pathlib import Path
from render_understand_ai_retrofit_review import render_layers_resolve_it_flow
ROOT = Path(__file__).resolve().parents[2]

if __name__ == '__main__':
    render_layers_resolve_it_flow(ROOT / 'course-assets/layers/layers-resolves-it.jpg')
    render_layers_resolve_it_flow(ROOT / 'gemini-notebook/layers/assets/layers-resolves-it-lowercase.jpg', lowercase=True)
