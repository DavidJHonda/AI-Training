#!/usr/bin/env python3
"""Write word-timestamp transcripts for selected course videos."""

import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("videos", nargs="+")
    parser.add_argument("--output-dir", default="/tmp/ai-training-video-edit/transcripts")
    parser.add_argument("--model", default="base.en")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    for source_name in args.videos:
        source = Path(source_name)
        print(f"Transcribing {source}", flush=True)
        segments, info = model.transcribe(
            str(source),
            beam_size=5,
            word_timestamps=True,
            vad_filter=True,
        )
        rows = []
        words = []
        for segment in segments:
            rows.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
            })
            for word in segment.words or []:
                words.append({
                    "start": word.start,
                    "end": word.end,
                    "word": word.word.strip(),
                })
        payload = {
            "source": str(source),
            "duration": info.duration,
            "segments": rows,
            "words": words,
        }
        output = output_dir / f"{source.stem}.json"
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        text_output = output.with_suffix(".txt")
        text_output.write_text("\n".join(
            f"{row['start']:7.2f}-{row['end']:7.2f}  {row['text']}" for row in rows
        ) + "\n")
        print(f"Wrote {output} ({len(words)} words)", flush=True)


if __name__ == "__main__":
    main()
