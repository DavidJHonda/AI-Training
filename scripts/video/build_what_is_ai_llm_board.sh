#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
standardized="$repo_root/board-review-first-four/standardized/start-smarter/what-is-ai-llm.jpg"
output="$repo_root/board-review-first-four/alternatives/start-smarter/what-is-ai-3-llm-alternative.jpg"

# The LLM board is part of the shared Start Smarter component set. Rebuild the
# complete set first so this one-off entry point cannot restore the legacy white
# footer or pre-standardization canvas.
bash "$repo_root/scripts/video/standardize_start_smarter_boards.sh" >/dev/null
mkdir -p "$(dirname "$output")"
cp "$standardized" "$output"

echo "Built $output"
