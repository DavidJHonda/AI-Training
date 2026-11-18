#!/usr/bin/env python3
"""Turn raw whisper JSON into readable, timestamped Markdown transcripts."""
import json
import sys
from pathlib import Path

LESSONS = [
    ("navigate-the-future-opener", "Opener"),
    ("loudest-voices", "Loudest Voices"),
    ("pace-of-change", "Pace of Change"),
    ("big-downside", "Big Downside"),
    ("big-upside", "Big Upside"),
    ("where-will-ai-land", "Where Will AI Land? (was Unexpected Results)"),
    ("ai-agents", "Rise of Agents"),
    ("work-changes", "Work Changes"),
    ("where-ai-lives", "Data Centers"),
]
PAUSE = 0.9      # seconds of silence that starts a new paragraph
MAX_PARA = 45.0  # seconds; split long paragraphs at the next sentence end


def stamp(t):
    return f"{int(t) // 60}:{int(t) % 60:02d}"


def paragraphs(words):
    paras, cur = [], []
    for i, w in enumerate(words):
        if cur:
            gap = w["start"] - words[i - 1]["end"]
            ended = cur[-1]["word"].rstrip('"”').endswith((".", "?", "!"))
            long = w["start"] - cur[0]["start"] > MAX_PARA
            if ended and (gap >= PAUSE or long):
                paras.append(cur)
                cur = []
        cur.append(w)
    if cur:
        paras.append(cur)
    return paras


def main():
    out = Path(sys.argv[1])
    raw = out / "raw"
    combined = ["# Navigate the Future: video transcripts", "",
                "Machine transcripts of the nine live section videos, made 2026-11-16 "
                "with faster-whisper medium.en, silence filter off. Timestamps mark where each paragraph "
                "starts. Spellings of names and numbers are the model's best guess.", ""]
    summary = []
    for n, (slug, title) in enumerate(LESSONS, 1):
        data = json.loads((raw / f"{slug}.json").read_text())
        words = []
        for w in data["words"]:
            if not w["word"]:
                continue
            if w["word"].startswith("-") and words:  # "GPT" + "-2" -> "GPT-2"
                words[-1] = {**words[-1], "word": words[-1]["word"] + w["word"], "end": w["end"]}
            else:
                words.append(dict(w))
        # Drop phantom words whisper invents in the silent closing frames.
        for i in range(len(words) - 1, max(len(words) - 6, 0), -1):
            if words[i]["start"] - words[i - 1]["end"] > 2.5:
                words = words[:i]
                break
        body = [f"**[{stamp(p[0]['start'])}]** " + " ".join(w["word"] for w in p)
                for p in paragraphs(words)]
        head = f"{n}. {title}"
        meta = f"`course-assets/{slug}/{slug}.mp4` · {stamp(data['duration'])} · {len(words)} words"
        (out / f"{n:02d}-{slug}.md").write_text(
            "\n\n".join([f"# {head}", meta] + body) + "\n")
        combined += [f"## {head}", "", meta, ""]
        for b in body:
            combined += [b, ""]
        summary.append((head, stamp(data["duration"]), len(words)))
    (out / "navigate-the-future-transcripts.md").write_text("\n".join(combined))
    for row in summary:
        print(*row, sep=" | ")


if __name__ == "__main__":
    main()
