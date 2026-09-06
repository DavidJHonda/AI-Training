#!/usr/bin/env python3
"""Current titled Mind Trap lesson/prep boards. Does not modify videos.

Owns v3 exports; the older batch keeps v2 assets for legacy video recipes.
Preserves the existing structured comparison and two-card teaching copy.
"""
from render_avoid_traps_editorial import CompareSide, Pair, render_comparison, save_pair
from render_embrace_editorial_batch import AMBER, BLUE, PURPLE, TEAL, Card, CardBoard, render_card_board


def main():
    comparison = render_comparison(
        "The Same Question. Different Answers.",
        "Should I choose Michigan or Indiana?",
        (
            CompareSide(
                "MOM", "Your Mom",
                "Indiana. You seemed more comfortable there, and when you get stuck, you tend to go quiet. Being somewhere you’ll ask for help matters more for you than another ranking.",
                (("KNOWS", "Your history."),
                 ("NOTICES", "How you act when you are stuck."),
                 ("STAKE", "Shares the outcome.")), BLUE,
            ),
            CompareSide(
                "AI", "The Chatbot",
                "Michigan. It offers world-class academics and a vibrant campus community. It could be an excellent fit for you.",
                (("SEES", "What you typed."),
                 ("MATCHES", "Common patterns."),
                 ("STAKE", "Does not share the outcome.")), AMBER,
            ),
        ),
        "scripts/video/assets/editorial-avoid-traps/comparisons/human-vs-ai.png",
        scenario_label="YOU",
    )
    save_pair(comparison, Pair(
        "illustrations/mind-trap-comparison-v3.jpg", "lessons/mind-trap-1-comparison.jpg",
    ))
    eliza = CardBoard(
        "mind-eliza", "Why AI Feels Like Somebody", (
            Card("Your Brain Looks for a Person",
                 "When something responds to you, your brain starts looking for a person behind it."),
            Card("AI Sounds Like One",
                 "Your brain hears a person when AI says “I think” and “I feel.” But those are generated words."),
        ), "scripts/video/assets/editorial-avoid-traps/mind-eliza/art-sheet.png",
        "", "", "Sounding human does not make AI human.", (TEAL, PURPLE),
    )
    save_pair(render_card_board(eliza), Pair(
        "illustrations/mind-trap-eliza-effect-v3.jpg", "lessons/mind-trap-2-eliza.jpg",
    ))


if __name__ == "__main__":
    main()
