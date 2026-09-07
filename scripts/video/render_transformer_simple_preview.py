#!/usr/bin/env python3
"""Render the approved simple attention/transformation board to its preview path."""

import render_understand_ai_retrofit_review as r


def render_preview():
    out = r.OUT / "previews/transformer-attention-transformation-simple-v1.jpg"
    r.render_attention_transformation(out)
    return out


if __name__ == "__main__":
    render_preview()
