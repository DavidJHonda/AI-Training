#!/usr/bin/env python3
"""Apply shared frame/audio preservation QA to the second board refresh."""
import argparse
import cv2
import build_board_font_sync_round2 as build
build.configure()
import qa_board_font_sync as check

if __name__=='__main__':
    cv2.setNumThreads(1)
    parser=argparse.ArgumentParser();parser.add_argument('slug',choices=build.CONFIG)
    args=parser.parse_args();check.qa(args.slug)
