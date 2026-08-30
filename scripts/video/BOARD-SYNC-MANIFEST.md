# Video Board Sync Manifest

Use this manifest before repairing a section's videos. It connects the current lesson
board to its exact video span, camera treatment, narration, and highlight states. The
manifest is the review document; do not choose framing or colors while editing.

## One row per board span

| Field | Required value |
| --- | --- |
| `lesson_id` | Canonical lesson ID from `index.html`. |
| `video_file` | Current unsuffixed lesson video. |
| `board_order` | Board's order in the current lesson. |
| `board_asset` | Exact current lesson asset used in the video. |
| `board_sha256` | SHA-256 of that asset at audit time. |
| `video_start` / `video_end` | Frame-exact or timecode span. |
| `mismatch_class` | `current`, `design_only`, `copy_changed`, or `teaching_changed`. |
| `density` | `compact` or `dense`. |
| `camera_treatment` | `full_board`, `restrained_push`, or `zoom_pan_complete_areas`. |
| `audio_action` | `preserve`, `selective_edit`, or `reroll`. |
| `qa_status` | `pending`, `review_ready`, `approved`, or `shipped`. |

Each board row also owns an ordered list of spoken highlight states. Record these fields
for every state:

| Field | Required value |
| --- | --- |
| `spoken_onset` | Frame or timecode when the target becomes active. |
| `highlight_target` | Exact card, step, title, row, or element being discussed. |
| `highlight_mode` | `none`, `ring`, `chip`, or `ring_and_chip`. |
| `highlight_color` | Exact hex token, or `none`. |
| `highlight_source` | `card_locked_accent`, `neutral_video_purple`, or `none`. |
| `camera_state` | Full board or the complete active card/section. Never crop inside it. |

## Color inheritance

For all Editorial Explainer formats, color belongs to the inner card or flow step. Its
highlight must inherit the same locked token used by that component's title, pill, art
border, and illustration wash:

- green `#0f7a4a`
- teal `#0e8f86`
- blue `#1652f0`
- editorial purple `#4f2fc4`
- amber `#a9760c`
- red `#c41f28`

Do not sample a render, assign colors by column, or replace a component's token with
generic purple. Standard video purple `#6e51ff` is reserved for neutral board titles
and board-wide targets with no stronger local accent. An unmarked orientation or
summary state records `highlight_color: none` and `highlight_source: none`.

If narration explicitly joins multiple differently colored components, each ring keeps
its own inherited token. If narration summarizes the board without distinguishing its
components, return to the complete unmarked board.

## Example

```json
{
  "lesson_id": "example",
  "video_file": "videos/example.mp4",
  "board_order": 2,
  "board_asset": "lessons/example-2-board.jpg",
  "board_sha256": "<sha256>",
  "video_start": "01:12.400",
  "video_end": "01:38.900",
  "mismatch_class": "design_only",
  "density": "dense",
  "camera_treatment": "zoom_pan_complete_areas",
  "audio_action": "preserve",
  "qa_status": "pending",
  "states": [
    {
      "spoken_onset": "01:12.400",
      "highlight_target": "complete board",
      "highlight_mode": "none",
      "highlight_color": "none",
      "highlight_source": "none",
      "camera_state": "full board"
    },
    {
      "spoken_onset": "01:16.100",
      "highlight_target": "Blue card",
      "highlight_mode": "ring_and_chip",
      "highlight_color": "#1652f0",
      "highlight_source": "card_locked_accent",
      "camera_state": "complete Blue card"
    }
  ]
}
```

## Ship gates

Before approval, verify:

1. The lesson asset and video board are pixel-identical before highlights.
2. Every state begins when its target is spoken and ends when narration moves.
3. Every accented component uses its stored token.
4. Dense boards establish the full board, then show complete areas while panning.
5. Compact boards remain fully visible.
6. No Gemini Notebook highlighting, stale-board flashes, cropped borders, cut words,
   or audio blips remain.
7. The standard closing board uses the standard closing movement and size.
