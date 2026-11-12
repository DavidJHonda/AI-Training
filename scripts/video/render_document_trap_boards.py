#!/usr/bin/env python3
"""Canonical titled Document Trap page/prep boards; does not render video.

Owns the v3 assets. The older Avoid Traps batch retains legacy v2 exports
for existing video edit recipes. Use this renderer for current lesson boards.
"""

from course_credit import ROOT, save_course_image
from render_avoid_traps_editorial import Pair, render_feature, save_pair
from render_navigate_editorial_batch import (
    AMBER, BLUE, PURPLE, TEAL, Card, CardBoard, FlowBoard,
    render_card_board, render_flow_board,
)


def main():
    save_pair(
        render_feature(
            "An Incomplete Answer", "course-assets/document-trap/document-trap.jpg",
            "Uploading a file doesn’t mean AI has read it all.", BLUE,
        ),
        Pair("course-assets/document-trap/document-trap-uploaded-v3.jpg", "course-assets/document-trap/document-trap-uploaded.jpg"),
    )
    save_pair(
        render_flow_board(FlowBoard(
            "document-flow", "Split, Search, Load", (
                Card("Split", "Break the long document into smaller pieces."),
                Card("Search", "Look for pieces that match the question by keywords and meaning."),
                Card("Load", "Put the selected pieces into the context window for AI to use."),
            ), "scripts/video/assets/editorial-avoid-traps/document-flow/art-sheet.png",
            "", "", (PURPLE, BLUE, TEAL),
            takeaway="Search decides which parts reach the answer.",
        )),
        Pair("course-assets/document-trap/document-trap-flow.jpg", "course-assets/document-trap/document-trap-flow.jpg"),
    )
    render_document_tips()


def render_document_tips():
    output = "course-assets/document-trap/document-trap-moves.jpg"
    board = CardBoard(
        "document-moves", "Four Tips for Working with Long Documents", (
            Card("Name the Section", "Use the document’s own headings and keywords."),
            Card("Ask One Thing", "Give retrieval one clear target at a time."),
            Card("Share What Matters", "Paste the exact passage or upload only the relevant section."),
            Card("Ask for the Quote", "Ask AI to quote the exact passage, then compare it with the original."),
        ), "scripts/video/assets/editorial-avoid-traps/document-moves/art-sheet.png",
        output, output, "Make the right passages easier to find.", (PURPLE, BLUE, TEAL, AMBER),
    )
    save_course_image(render_card_board(board), ROOT / output, quality=95, subsampling=0, optimize=True)


if __name__ == "__main__":
    main()
