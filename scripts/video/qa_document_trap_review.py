"""Final-output frame and audio-splice checks for Document Trap."""
import qa_hallucination_review as qa
import build_document_trap_review as build

if __name__ == '__main__':
    qa.build=build
    qa.main()
