#!/usr/bin/env python3
"""Render the approved embedding illustration to its review preview path."""

import render_understand_ai_retrofit_review as r


def render_preview():
    source = r.OUT / "assets/teaching-illustrations/embedding-lookup-compact-cards.png"
    out = r.OUT / "previews/embeddings-integrated-definitions-v2.jpg"
    r.render_inside_real_model(source, out)
    return out


if __name__ == "__main__":
    render_preview()
