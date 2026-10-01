#!/usr/bin/env python3
"""Run the existing assembly checks against the new board-edge candidate."""
import build_wheres_the_line_v4  # Configures the shared assembly's v4 paths.
import qa_wheres_the_line_v3 as qa

if __name__ == '__main__':
    qa.main()
