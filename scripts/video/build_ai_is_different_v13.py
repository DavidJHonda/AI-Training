#!/usr/bin/env python3
"""October 9 approved roll-5 assembly. Produces a review candidate, never installs it."""
from pathlib import Path
import argparse
import json
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, GREEN, RED, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/ai-is-different-build-2026-10-09-v13'
DEST = ROOT / 'Prompts/ai-is-different-v13.mp4'
R4, R5, R6 = [ROOT / f'Prompts/ai-is-different-{n}.mp4' for n in (4, 5, 6)]
A = ROOT / 'course-assets/ai-is-different'
LIVE = A / 'ai-is-different.mp4'
ASSETS = {k: A / f'ai-is-different-{s}.jpg' for k, s in
          [('rules', 'rules'), ('cooking', 'cooking-analogy')]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare-only', action='store_true')
    ap.add_argument('--reuse-legs', action='store_true')
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    b = Build(ROOT, R5, OUT, DEST, protected=[R4, R6, LIVE,
        ROOT / 'lessons/ai-is-different.md', *ASSETS.values(), A / 'ai-is-different-close.jpg'])
    b.kb = Path(__file__).resolve()
    # Avoid duplicating the extraction used for waveform inspection.
    if not (OUT / 'source.wav').exists() and (OUT / 'roll5.wav').exists():
        os.link(OUT / 'roll5.wav', OUT / 'source.wav')
    b.load_audio([(56.2, 56.7), (164.3, 164.9), (172.3, 172.7), (199.3, 199.7)])
    segments, marks = [], {}

    def keep(s, e, label, board=None, **kw):
        s, e = fr(s), fr(e)
        segments.append(('r5', s, e, b.cursor))
        b.keep(s, e, label, board or 'source',
               **({'video_from': b.cursor} if board else kw))

    def graft(src, key, s, e, label, gain, board):
        s, e = fr(s), fr(e)
        segments.append((key, s, e, b.cursor))
        b.graft(src, s, e, label, key, picture_from=b.cursor,
                gain_db=gain, visual=board)

    def output(t, key='r5'):
        f = fr(t)
        for k, s, e, o in segments:
            if k == key and s <= f < e:
                return (o + f - s) / 30
        raise ValueError((key, t))

    keep(0, 37.5, 'Password hook; calculator and spreadsheet drawings')
    marks['rules'] = b.cursor
    keep(37.5, 51, 'Canonical Rules Look Like This; both branches', 'rules')
    graft(R4, 'r4-consistency', 50.5, 53.6,
          'Exact consistency line; removes guarantees certainty', .44, 'rules')
    keep(56.6, 1718 / 30, 'Rules board through natural transition', 'rules')
    marks['rules_end'] = b.cursor
    keep(1718 / 30, 3598 / 30, 'Playlist, learned patterns, and AI is still software')
    marks['cooking'] = b.cursor
    keep(3598 / 30, 130.5, 'Cooking introduction and robot card', 'cooking')
    keep(130.5, 138.5, 'Supporting robot recipe and repeated cupcakes drawings',
         video_src=LIVE, video_from=fr(80), video_end=fr(88))
    keep(138.5, 151, 'Same-result takeaway, then chef card', 'cooking')
    keep(151, 151 + 163 / 30, 'Relocated kitchen drawing under ingredient and heat explanation',
         video_src=R5, video_from=3598, video_end=3761)
    keep(151 + 163 / 30, 160 + 11 / 30, 'Chef does not need a recipe', 'cooking')
    graft(R6, 'r6-substitutions', 112.9, 120 + 1 / 30,
          'Chef recognizes pairings and substitutions; different dishes', .23, 'cooking')
    # The replacement also removes the false exclusive-raw-materials bridge.
    keep(172.5, 5198 / 30, 'Natural handoff into the GPA example', 'cooking')
    marks['cooking_end'] = b.cursor
    keep(5198 / 30, 191.7, 'Structured GPA table; illustrated campus photo')
    keep(191.7, 196 + 19 / 30, 'Drawn campus replaces photo-style wood/table insert',
         video_src=R6, video_from=fr(132), video_end=fr(137))
    keep(199 + 19 / 30, 228 + 8 / 30,
         'Campus clues animation, tradeoff, and mistaken identification; false spreadsheet claim cut')
    keep(232 + 28 / 30, 236.1, 'It might look great, but still have mistakes; oversight detour cut')
    b.mark_close_start()
    keep(236.1, 245.7, 'Canonical closing message; exact final two lines', 'close')
    # Original post-speech gap is preserved. No extra pause or logo outro.
    b.finish_audio()

    def target(label, at, rect, color):
        return dict(label=label, at=at, rects=[rect], color=color, radius=18)

    b.board('rules', ASSETS['rules'], marks['rules'], marks['rules_end'], 'compact', [
        target('User enters password', output(42.22), [585,170,1016,259], NEUTRAL),
        target('IF password matches', output(44.86), [555,346,1046,437], BLUE),
        target('THEN open app', output(47.5), [125,592,706,700], GREEN),
        target('ELSE error message', output(48.62), [805,565,1516,726], RED),
    ], banner_at=output(50.84, 'r4-consistency'))
    b.board('cooking', ASSETS['cooking'], marks['cooking'], marks['cooking_end'], 'compact', [
        target('Rule-Based Software whole card', output(127.22), [40,118,784,880], PURPLE),
        target('Same recipe. Same result every time.', output(139.64), [58,787,766,862], PURPLE),
        target('AI whole card', output(143.34), [816,118,1560,880], BLUE),
        target('Learned patterns. Different dishes.', output(117.94, 'r6-substitutions'), [834,787,1542,862], BLUE),
    ], push=False)
    if not args.reuse_legs:
        b.render_legs()
        for key in b.boards:
            b.state_sheet(key)
    b.make_close('aivscode')
    b.manifest({
        'approval': 'User: build it please, October 9, 2026; candidate only',
        'plan': 'video-audit/ai-is-different-comparison-2026-10-09/REVIEW.md',
        'production_scope': 'Approved full production pass; live video unchanged',
        'board_output_spans': {k:[marks[k],marks[k+'_end']] for k in ASSETS},
        'narration_removed_r5_seconds': [[51,56.6],[160+11/30,172.5],
                                       [196+19/30,199+19/30],[228+8/30,232+28/30]],
        'graft_loudness': {'r4_input_lufs':-20.40,'r5_input_lufs':-19.96,
                          'r6_input_lufs':-20.19,'r4_gain_db':.44,'r6_gain_db':.23},
        'framing_decision': 'Full cooking cards readable at 720p; tall complete-card zoom offers little gain. Full view retained.',
        'supporting_visuals': [
            {'base_seconds':[130.5,138.5], 'source':str(LIVE), 'source_seconds':[80,88]},
            {'base_seconds':[151,151+163/30], 'source':str(R5), 'source_frames':[3598,3761]},
            {'base_seconds':[191.7,196+19/30], 'source':str(R6), 'source_seconds':[132,136+28/30],
             'reason':'Replace realistic wooden tabletop/photo treatment with drawn campus/field illustration'},
        ],
        'selective_pauses': [],
        'closing_tail': 'Original gap only; standard 48-frame hold and 150-frame push, then settled through ending',
        'listening': 'Not performed. ASR and waveform checks do not verify voice/cadence match.',
    })
    print(f'Prepared {b.total} frames, {b.total/30:.3f} seconds', flush=True)
    if not args.prepare_only:
        b.render()
        print(DEST, flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].endswith('.json'):
        import ken_burns_path as kb
        from build_understand_ai_opener_v12 import draw_ring
        kb.draw_ring = draw_ring
        kb.main()
    else:
        main()
