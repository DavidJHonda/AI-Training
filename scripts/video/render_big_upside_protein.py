#!/usr/bin/env python3
"""Render Big Upside's protein board with the shared four-benefit layout.

The implementation and copy live in render_big_upside_benefits.py. Retain this
entry point for existing build commands; --art overrides only its source artwork.
"""
from pathlib import Path
import argparse
from render_big_upside_benefits import BOARDS, render as render_board
from editorial_typography import ROOT

OUTPUT = ROOT / 'course-assets/big-upside/big-upside-protein.jpg'

def render(art=None, output=OUTPUT):
    board = next(board for board in BOARDS if board[0] == 'protein')
    return render_board(*board, art_path=art, output=output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--art', type=Path)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    render(args.art, args.output)
