#!/usr/bin/env python3
"""Render the approved Transformer clues board to its preview path."""

import render_understand_ai_retrofit_review as r


def render_preview():
    assets = r.OUT / "assets/card-illustrations"
    out = r.OUT / "previews/transformer-context-clues-v1.jpg"
    r.render_context_resolutions(assets / "context-light-pair.png", assets / "context-pronoun-pair-ragdoll-v1.png", out)
    return out


if __name__ == "__main__":
    render_preview()
