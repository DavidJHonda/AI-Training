"""Use the shared frame/state and audio-splice QA for Training Bias."""
import qa_hallucination_review as qa
import build_training_bias_review as build

if __name__ == '__main__':
    qa.build = build
    qa.main()
