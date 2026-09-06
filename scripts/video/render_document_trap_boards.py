#!/usr/bin/env python3
"""Canonical titled Document Trap page/prep boards; does not render video.

Owns the v3 assets. The older Avoid Traps batch retains legacy v2 exports
for existing video edit recipes. Use this renderer for current lesson boards.
"""

from render_avoid_traps_editorial import Pair, render_feature, save_pair
from render_embrace_editorial_batch import (
    AMBER, BLUE, PURPLE, TEAL, Card, CardBoard, FlowBoard,
    render_card_board, render_flow_board,
)


def main():
    save_pair(
        render_feature(
            "An Incomplete Answer", "illustrations/document-trap.jpg",
            "Uploading a file doesn’t mean AI has read it all.", BLUE,
        ),
        Pair("illustrations/document-trap-uploaded-v3.jpg", "lessons/document-trap-1-uploaded.jpg"),
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
        Pair("illustrations/document-trap-flow-v3.jpg", "lessons/document-trap-2-flow.jpg"),
    )
    save_pair(
        render_card_board(CardBoard(
            "document-moves", "Four Moves for Better Retrieval", (
                Card("Name the Section", "Use the document’s own headings and keywords."),
                Card("Ask One Thing", "Give retrieval one clear target at a time."),
                Card("Share What Matters", "Paste the exact passage or upload only the relevant section."),
                Card("Ask for the Quote", "Ask AI to quote the exact passage, then compare it with the original."),
            ), "scripts/video/assets/editorial-avoid-traps/document-moves/art-sheet.png",
            "", "", "Make the right passages easier to find.", (PURPLE, BLUE, TEAL, AMBER),
        )),
        Pair("illustrations/document-trap-moves-v3.jpg", "lessons/document-trap-3-moves.jpg"),
    )


if __name__ == "__main__":
    main()
