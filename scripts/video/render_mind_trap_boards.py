#!/usr/bin/env python3
"""Current titled Mind Trap lesson/prep boards. Does not modify videos.

Owns v3 comparison and v4 ELIZA exports; older assets stay for legacy recipes.
Preserves the existing structured comparison and two-card teaching copy.
"""
from pathlib import Path
from PIL import Image
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
    # Reorder intact native artwork panels with their copy and accent colors.
    root = Path(__file__).resolve().parents[2]
    art_path = root/'scripts/video/assets/editorial-avoid-traps/mind-eliza/art-sheet.png'
    art = Image.open(art_path).convert('RGB')
    half = art.width // 2
    reordered = Image.new('RGB', art.size)
    reordered.paste(art.crop((half, 0, art.width, art.height)), (0, 0))
    reordered.paste(art.crop((0, 0, half, art.height)), (art.width-half, 0))
    reordered.save(art_path.with_name('art-sheet-ai-first.png'))
    eliza = CardBoard(
        "mind-eliza", "Why AI Feels Like Somebody", (
            Card("AI Sounds Like One",
                 "Your brain hears a person when AI says “I think” and “I feel.” But those are generated words."),
            Card("Your Brain Looks for a Person",
                 "When something responds to you, your brain starts looking for a person behind it."),
        ), "scripts/video/assets/editorial-avoid-traps/mind-eliza/art-sheet-ai-first.png",
        "", "", "Sounding human does not make AI human.", (PURPLE, TEAL),
    )
    save_pair(render_card_board(eliza), Pair(
        "illustrations/mind-trap-eliza-effect-v4.jpg", "lessons/mind-trap-2-eliza.jpg",
    ))


if __name__ == "__main__":
    main()
