"""Export the approved banner-free board edit at the canonical 1600 px width."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'scripts/video/assets/how-ai-answers-before-answer-no-banner.png'
OUTPUT = ROOT / 'course-assets/how-ai-answers/how-ai-answers-before-answer-begins.jpg'

def main():
    image = Image.open(SOURCE).convert('RGB')
    if image.size != (1568, 1003):
        raise ValueError('Unexpected source dimensions; review footer framing before export.')
    # Trim only surplus blank canvas beneath the existing website credit.
    image = image.crop((0, 0, 1568, 904))
    image = image.resize((1600, round(904 * 1600 / 1568)), Image.Resampling.LANCZOS)
    image.save(OUTPUT, 'JPEG', quality=95, subsampling=0, optimize=True)
    print(f'{OUTPUT}: {image.width}x{image.height}')

if __name__ == '__main__':
    main()
