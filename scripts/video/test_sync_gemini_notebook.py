"""Verify sync boundaries and drift detection without touching course materials."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import sync_gemini_notebook as sync

CURRENT_PROMPT = ('REQUIRED VERBATIM AUDIO\nExact lines.\nTEACH THE COMPLETE LESSON\n'
                  'Teaching.\nVOICE\nPlain words.\nBOARDS AND VISUALS\nDrawn scenes.\n')


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.out = self.root / 'gemini-notebook'
        self.registry = self.out / 'upload-sets.json'
        self.patch = patch.multiple(sync, ROOT=self.root, OUT=self.out, REGISTRY=self.registry)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.lessons = []
        for slug in ('first', 'second'):
            lesson = dict(slug=slug, title=slug.title(), markdown=f'lessons/{slug}.md',
                          prompt=f'gemini-notebook/{slug}/PROMPT.txt',
                          uploads=[f'gemini-notebook/{slug}/assets/board.jpg'],
                          post_only=[], notes='Current prep', save_as=f'Prompts/{slug}-reroll.mp4')
            for name, content in [(lesson['markdown'], 'Teaching'), (lesson['prompt'], CURRENT_PROMPT),
                                  (lesson['uploads'][0], 'Board bytes'),
                                  (f'gemini-notebook/{slug}/NOTES.md', 'Handwritten directions'),
                                  (f'gemini-notebook/{slug}/donor/PROMPT.txt', 'Alternate prompt')]:
                p = self.root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content)
            self.lessons.append(lesson)
        self.write_registry()

    def write_registry(self):
        self.registry.write_text(json.dumps({'lessons': self.lessons}))

    def run_sync(self, *args):
        with patch('sys.argv', ['sync_gemini_notebook.py', *args]), contextlib.redirect_stdout(io.StringIO()):
            sync.main()

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return sync.check(self.lessons)

    def test_full_and_single_lesson_sync_preserve_all_owned_materials(self):
        originals = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.run_sync()
        stale = self.out / 'first/upload/old-board.jpg'
        stale.write_text('Superseded upload')
        second = self.out / 'second/README.txt'
        before = second.stat().st_mtime_ns
        self.run_sync('--lesson', 'first')
        self.assertFalse(stale.exists())
        self.assertEqual(second.stat().st_mtime_ns, before)
        for p, expected in originals.items():
            self.assertEqual(p.read_bytes(), expected, str(p))
        self.assertFalse((self.root / 'Prompts').exists())
        self.assertEqual(self.check(), 0)

    def test_check_detects_prompt_upload_and_instruction_drift(self):
        self.run_sync()
        for rel in ('first/PROMPT.txt', 'first/upload/board.jpg', 'first/README.txt'):
            with self.subTest(path=rel):
                p = self.out / rel
                original = p.read_bytes()
                p.write_text('Changed')
                self.assertEqual(self.check(), 1)
                p.write_bytes(original)
        extra = self.out / 'first/upload/accidental-notes.txt'
        extra.write_text('Do not upload me')
        self.assertEqual(self.check(), 1)
        extra.unlink()
        (self.out / 'first/upload/board.jpg').unlink()
        self.assertEqual(self.check(), 1)

    def test_check_detects_registry_metadata_changes(self):
        self.run_sync()
        for key in ('title', 'notes', 'save_as'):
            with self.subTest(field=key):
                old = self.lessons[0][key]
                self.lessons[0][key] = 'Changed'
                self.assertEqual(self.check(), 1)
                self.lessons[0][key] = old
        self.assertEqual(self.check(), 0)

    def test_bad_source_prevents_partial_full_sync(self):
        self.run_sync()
        readme = self.out / 'first/README.txt'
        before = readme.read_bytes()
        self.lessons[0]['notes'] = 'New notes'
        self.lessons[1]['uploads'] = ['missing.jpg']
        self.write_registry()
        with self.assertRaisesRegex(SystemExit, 'missing source'):
            self.run_sync()
        self.assertEqual(readme.read_bytes(), before)

    def test_generated_copies_cannot_become_sources(self):
        self.run_sync()
        lesson = copy.deepcopy(self.lessons[0])
        lesson['uploads'] = ['gemini-notebook/first/upload/board.jpg']
        with self.assertRaisesRegex(SystemExit, 'generated upload copies'):
            sync.sources(lesson)

    def test_unsafe_or_duplicate_slugs_and_wrong_prompt_are_rejected(self):
        for field, value, message in [('slug', '../escape', 'invalid lesson slug'),
                                      ('prompt', 'Prompts/old.txt', 'prompt must be owned')]:
            with self.subTest(field=field):
                old = self.lessons[0][field]
                self.lessons[0][field] = value
                self.write_registry()
                with self.assertRaisesRegex(SystemExit, message):
                    sync.load()
                self.lessons[0][field] = old
        self.lessons.append(copy.deepcopy(self.lessons[0]))
        self.write_registry()
        with self.assertRaisesRegex(SystemExit, 'duplicate slugs'):
            sync.load()

    def test_legacy_prompt_cannot_be_registered_or_synced(self):
        (self.root / self.lessons[0]['prompt']).write_text('Create a video overview. Old rules.')
        with self.assertRaisesRegex(SystemExit, 'legacy or incomplete prompt'):
            self.run_sync()
        self.assertFalse((self.out / 'first/upload').exists())

    def test_retired_kit_cannot_be_synced(self):
        self.registry.write_text(json.dumps({'lessons': self.lessons,
            'needs_preparation': [{'slug': 'old-lesson', 'reason': 'Rebuild under current preparation rules.'}]}))
        with self.assertRaisesRegex(SystemExit, 'no usable prep kit'):
            self.run_sync('--lesson', 'old-lesson')
        self.assertFalse((self.out / 'old-lesson').exists())


if __name__ == '__main__':
    unittest.main()
