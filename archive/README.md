# Video production archive

The exact NotebookLM sources each shipped video was generated from: the per-lesson
video prompt, the lesson `.md` export, and every board/illustration jpg, organized
as `archive/<lesson-slug>/`. Reconstructed 2026-07-08 from git history (each file is
the version at its retirement commit's parent — i.e., what the shipped run actually
used). `master-prompt/` holds the retired Gemini-era guidelines PDF; the evolving
`Prompts/Master Prompt.md` stays live, and its per-ship versions are in
`git log -p -- "Prompts/Master Prompt.md"`.

Going forward, the retirement step MOVES a shipped lesson's sources here instead of
deleting them. These files are frozen history — never edit them, and never upload
from here for a re-roll without first checking the live lesson hasn't changed
(regenerate the `.md` and recapture boards from the live app instead).
