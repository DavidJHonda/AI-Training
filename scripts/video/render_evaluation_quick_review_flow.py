"""Purple EE-FLOW for Read / Understand / Validate; exact existing wording."""
from pathlib import Path
from render_evaluation_flow import render, PURPLE
from render_evaluate_results_quick_pass import CARD_COPY
ROOT=Path(__file__).resolve().parents[2]
STEPS=tuple((heading,body,asset,PURPLE) for heading,body,asset in zip(
    ('Read','Understand','Validate'), CARD_COPY,
    ('read.png','understand.png','validate.png')))

def main():
    render('Do a Quick Review', STEPS,
           ROOT/'scripts/video/assets/evaluation-quick-review',
           ROOT/'course-assets/evaluation-matters/evaluation-matters-quick-pass.jpg',
           ROOT/'tmp/evaluation-quick-review-flow', step_number=1)

if __name__=='__main__': main()
