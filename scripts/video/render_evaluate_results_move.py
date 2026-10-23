#!/usr/bin/env python3
"""Render the current Make Your Move board through the canonical card renderer."""
from pathlib import Path
import subprocess

def main():
    script=Path(__file__).with_name('render_evaluation_cards.cjs')
    subprocess.run(['node', str(script), '--board', 'move'], check=True)

if __name__ == '__main__':
    main()
