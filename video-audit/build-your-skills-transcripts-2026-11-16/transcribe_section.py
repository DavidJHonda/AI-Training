#!/usr/bin/env python3
"""Transcribe a course section's live videos and write readable Markdown.

Usage: transcribe_section.py OUT_DIR "Section Name" slug=Title [slug=Title ...]
Run from the repo root. Videos are course-assets/<slug>/<slug>.mp4.
The silence (VAD) filter stays OFF: it dropped spoken quotes in Loudest Voices.
"""
import json
import sys
from pathlib import Path

PAUSE = 0.9      # seconds of silence that starts a new paragraph
MAX_PARA = 45.0  # seconds; split long paragraphs at the next sentence end


def stamp(t):
    return f"{int(t) // 60}:{int(t) % 60:02d}"


def transcribe(lessons, raw):
    from faster_whisper import WhisperModel
    model = None
    for slug, _ in lessons:
        if (raw / f"{slug}.json").exists():
            continue
        model = model or WhisperModel("medium.en", device="cpu", compute_type="int8")
        src = f"course-assets/{slug}/{slug}.mp4"
        segs, info = model.transcribe(src, beam_size=5, word_timestamps=True,
                                      vad_filter=False, condition_on_previous_text=False)
        rows, words = [], []
        for g in segs:
            rows.append({"start": g.start, "end": g.end, "text": g.text.strip()})
            words += [{"start": w.start, "end": w.end, "word": w.word.strip()}
                      for w in g.words or []]
        (raw / f"{slug}.json").write_text(json.dumps(
            {"source": src, "duration": info.duration, "segments": rows, "words": words},
            indent=2) + "\n")
        (raw / f"{slug}.txt").write_text("\n".join(
            f"{r['start']:7.2f}-{r['end']:7.2f}  {r['text']}" for r in rows) + "\n")
        print("transcribed", slug, len(words), flush=True)


def clean(raw_words):
    words = []
    for w in raw_words:
        if not w["word"]:
            continue
        if w["word"].startswith("-") and words:  # "GPT" + "-2" -> "GPT-2"
            words[-1] = {**words[-1], "word": words[-1]["word"] + w["word"], "end": w["end"]}
        else:
            words.append(dict(w))
    # Drop phantom words whisper invents in the silent closing frames.
    for i in range(len(words) - 1, max(len(words) - 6, 0), -1):
        if words[i]["start"] - words[i - 1]["end"] > 2.5:
            print("  dropped tail:", " ".join(w["word"] for w in words[i:]))
            words = words[:i]
            break
    return words


def paragraphs(words):
    paras, cur = [], []
    for i, w in enumerate(words):
        if cur:
            gap = w["start"] - words[i - 1]["end"]
            ended = cur[-1]["word"].rstrip('"”').endswith((".", "?", "!"))
            if ended and (gap >= PAUSE or w["start"] - cur[0]["start"] > MAX_PARA):
                paras.append(cur)
                cur = []
        cur.append(w)
    if cur:
        paras.append(cur)
    return paras


def main():
    out, section = Path(sys.argv[1]), sys.argv[2]
    lessons = [tuple(a.split("=", 1)) for a in sys.argv[3:]]
    raw = out / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    transcribe(lessons, raw)
    slugname = section.lower().replace(" ", "-")
    combined = [f"# {section}: video transcripts", "",
                f"Machine transcripts of the {len(lessons)} live section videos, made with "
                "faster-whisper medium.en, silence filter off. Timestamps mark where each "
                "paragraph starts. Spellings of names and numbers are the model's best guess.", ""]
    for n, (slug, title) in enumerate(lessons, 1):
        data = json.loads((raw / f"{slug}.json").read_text())
        words = clean(data["words"])
        gaps = [(stamp(words[i]["end"]), round(words[i + 1]["start"] - words[i]["end"], 1))
                for i in range(len(words) - 1) if words[i + 1]["start"] - words[i]["end"] > 2.5]
        body = [f"**[{stamp(p[0]['start'])}]** " + " ".join(w["word"] for w in p)
                for p in paragraphs(words)]
        head = f"{n}. {title}"
        meta = f"`course-assets/{slug}/{slug}.mp4` · {stamp(data['duration'])} · {len(words)} words"
        (out / f"{n:02d}-{slug}.md").write_text("\n\n".join([f"# {head}", meta] + body) + "\n")
        combined += [f"## {head}", "", meta, ""]
        for b in body:
            combined += [b, ""]
        print(head, stamp(data["duration"]), len(words), "last word",
              stamp(words[-1]["end"]), "gaps", gaps, sep=" | ")
    (out / f"{slugname}-transcripts.md").write_text("\n".join(combined))


if __name__ == "__main__":
    main()
