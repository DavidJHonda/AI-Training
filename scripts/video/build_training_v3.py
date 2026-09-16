#!/usr/bin/env python3
"""Training v3: the live 2026-09-09 video retrofitted onto the current course boards.

Visual-only retrofit under RETROFIT-PLAYBOOK.md. The only surviving source is the
finished live video (the raw rolls training-1/2.mp4 were removed in the 2026-09-15
cleanup), so every Notebook span is re-encoded from that file (disclosed in REVIEW.md).
Audio: the live track is carried untouched for all 8249 source frames; the only
change is 78 frames of matched room tone appended so the canonical close settles
for four seconds after the closing audio.

Changes on the output timeline:
  * five course boards re-rendered from the current canonical JPGs (they now carry the
    website credit) on the house stage, constant 5px rings, current framework
  * the 2026-09-09 video-only "Three Phases of Training" graphic replaced by the new page board
    training-three-phases.jpg (David, 2026-09-16)
  * the "Gemini Notebook" corner mark cleaned on every kept Notebook frame
  * Notebook's garbled-title morph at 3:59.8-4:00.4 covered by a hold of the last
    clean "Three Training Phases" frame (source 7193) until the packaged-model scene
  * the current canonical close (white background) with the standard motion
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, GREEN, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'course-assets/training/training.mp4'          # live video, sole surviving source
OUT = ROOT / 'video-audit/training-repair-2026-09-16'
DEST = ROOT / 'Prompts/training-v3.mp4'
A = ROOT / 'course-assets/training'
BOARDS = {
    'before': A / 'training-before-starts.jpg',
    'loop': A / 'training-guess-check-adjust.jpg',
    'overview': A / 'training-three-phases.jpg',   # new page board (2026-09-16) replacing the 09-09 video-only graphic
    'pre': A / 'training-pretraining.jpg',
    'inst': A / 'training-instruction-tuning.jpg',
    'pref': A / 'training-preference-tuning.jpg',
}

# Source visual cuts (scenes.py, sequential decode) — half-open [in, out) source frames.
BEFORE = (1112, 1694)     # 0:37.07 -> 0:56.47
LOOP = (1694, 2572)       # 0:56.47 -> 1:25.73
OVERVIEW = (2572, 2986)   # 1:25.73 -> 1:39.53
PRE = (2986, 4264)        # 1:39.53 -> 2:22.13
INST = (4264, 5507)       # 2:22.13 -> 3:03.57
PREF = (5507, 7059)       # 3:03.57 -> 3:55.30
GIB = (7194, 7212)        # Notebook's garbled-title morph; hold source 7193 instead
CLOSE_IN, END = 8009, 8249   # 4:26.97 Notebook close cut; file end
CLOSE_TAIL = 78           # -> 120 settled frames after the audio ends

# Spoken onsets (seconds, source timeline; medium.en word timestamps, see REVIEW.md)
ON = dict(
    before_setup=43.62, before_gather=48.18,                       # "First, they design…" / "Then, they gather…"
    loop_example=59.54, loop_guess=62.34, loop_check=66.92, loop_adjust=72.46, loop_banner=80.72,   # "Using the phrase…" / "given the prompt…" / "It moves to the check step" / "Because it's wrong…" / "Repeating this loop…"
    ov_question=92.06,                                             # "To see how they work, we'll run the exact same prompt…"
    pre_1=102.82, pre_2=115.10, pre_3=129.86,                      # "The model ingests…" / "If we ask our basketball question…" / "but there is a core limitation…"
    inst_1=146.96, inst_2=158.00, inst_3=172.66,                   # "Now, humans provide…" / "Now, when we ask…" / "However, while the model…"
    pref_1=187.80, pref_2=205.96, pref_3=222.36,                   # "In this stage…" / "Look at the final answer…" / "But there is still a vulnerability."
)




def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'index.html', ROOT / 'lessons/training.md', *BOARDS.values(), A / 'training-close.jpg'])
    # speech-free windows measured with pauses.sh on the live track
    b.load_audio([(182.10, 183.55), (234.20, 235.35), (242.75, 244.25), (265.65, 267.00)])

    b.keep(0, BEFORE[0], 'Notebook opening: chemistry/code, basketball analogy, guess-check-adjust drawings')
    b.keep(*BEFORE, 'Before Training Starts', 'before')
    b.keep(*LOOP, 'The Training Loop', 'loop')
    b.keep(*OVERVIEW, 'Three Phases of Training', 'overview')
    b.keep(*PRE, '1 · Pretraining', 'pre')
    b.keep(*INST, '2 · Instruction Tuning', 'inst')
    b.keep(*PREF, '3 · Preference Tuning', 'pref')
    b.keep(PREF[1], GIB[0], 'Notebook: Three Training Phases drawing (fade-in kept)')
    b.keep(*GIB, 'Hold last clean Three Training Phases frame over the garbled-title morph', video_from=GIB[0] - 1, video_end=GIB[0])
    b.keep(GIB[1], CLOSE_IN, 'Notebook: packaged model, chat window, frozen weights')
    b.mark_close_start()
    b.close(CLOSE_IN, END, tail=CLOSE_TAIL)
    b.finish_audio()

    # Ring rectangles in source-image pixels (xyxy), verified against the current JPGs (rects-sheet in REVIEW.md).
    b.board('before', BOARDS['before'], *BEFORE, 'compact', [
        dict(label='Set Up the System', at=ON['before_setup'], rects=[[40, 127, 783, 717]], color=PURPLE),
        dict(label='Gather the Data', at=ON['before_gather'], rects=[[817, 127, 1559, 717]], color=BLUE)])
    b.board('loop', BOARDS['loop'], *LOOP, 'compact', [
        dict(label='Training example line', at=ON['loop_example'], rects=[[66, 151, 1532, 218]], color=NEUTRAL),
        dict(label='1 Guess', at=ON['loop_guess'], rects=[[76, 247, 540, 781]], color=PURPLE),
        dict(label='2 Check', at=ON['loop_check'], rects=[[568, 247, 1031, 781]], color=BLUE),
        dict(label='3 Adjust', at=ON['loop_adjust'], rects=[[1059, 247, 1523, 781]], color=TEAL)],
        banner_at=ON['loop_banner'], banner=[40, 967, 1560, 1055])
    b.board('overview', BOARDS['overview'], *OVERVIEW, 'compact', [
        dict(label='The same question', at=ON['ov_question'], rects=[[40, 112, 1560, 244]], color=NEUTRAL)])
    for key, col, ys in [('pre', PURPLE, [(165, 467), (500, 664), (697, 861)]),
                         ('inst', BLUE, [(165, 412), (444, 650), (683, 847)]),
                         ('pref', GREEN, [(165, 412), (444, 691), (724, 888)])]:
        span = dict(pre=PRE, inst=INST, pref=PREF)[key]
        labels = ['Learn card', 'What an Answer Might Look Like', 'What Still Needs Work']
        b.board(key, BOARDS[key], *span, 'compact', [
            dict(label=labels[i], at=ON[f'{key}_{i + 1}'], rects=[[74, y0, 1526, y1]], color=col) for i, (y0, y1) in enumerate(ys)])
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('training')
    b.manifest(dict(retrofit_scope='Visual-only retrofit of the live 2026-09-09 video onto current boards; audio untouched except a 78-frame room-tone tail',
                    source_limitation='Raw rolls removed 2026-09-15; the finished live video is the only source, so kept Notebook spans are re-encoded from it'))
    print('prepared', b.total, 'frames', round(b.total / 30, 2), 's')
    if args.prepare_only: return
    m = b.render(clean_corner=True)
    print('rendered', DEST, 'corner:', m['corner_mark']['cloned_frames'], m['corner_mark']['inpainted_frames'], 'declined', len(m['corner_mark']['declined']))


if __name__ == '__main__': main()
