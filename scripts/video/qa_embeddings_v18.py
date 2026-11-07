#!/usr/bin/env python3
"""Run the shortening checks against the corrected badge join in v18."""
import build_embeddings_v18
import qa_embeddings_v17 as qa

if __name__ == '__main__':
    qa.b = build_embeddings_v18.build
    qa.main()
