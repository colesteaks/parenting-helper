import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import skill_library as lib  # noqa: E402


class SkillLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.research, cls.library, cls.sources = lib.check()

    def test_every_area_has_sources_and_activities(self):
        for area in lib.AREA_IDS:
            self.assertTrue([a for a in self.library['activities'] if a['area'] == area], area)
            self.assertTrue([s for s in self.sources.values() if area in s['areas']], area)

    def test_area_ids_match_the_skill_area_framing(self):
        framing = (ROOT / 'references/skill-areas.md').read_text(encoding='utf-8')
        for area in lib.AREA_IDS:
            self.assertIn(f'`{area}`', framing)

    def test_tested_grade_needs_a_source_that_tests_a_practice(self):
        for a in self.library['activities']:
            if a['grade'] == 'tested':
                cited = [self.sources[s] for s in a['evidence']]
                self.assertTrue(any(s['design'] in lib.TESTING_DESIGNS and s['weight'] != 'weak' for s in cited), a['id'])

    def test_no_activity_rests_only_on_weak_sources_unless_marked_down(self):
        for a in self.library['activities']:
            if all(self.sources[s]['weight'] == 'weak' for s in a['evidence']):
                self.assertNotEqual(a['grade'], 'tested', a['id'])

    def test_every_activity_has_an_easier_and_harder_version_and_safety(self):
        for a in self.library['activities']:
            for field in ('easier', 'harder', 'safety', 'notice', 'why'):
                self.assertTrue(a[field].strip(), f"{a['id']}:{field}")

    def test_sources_are_https_checked_and_do_not_claim_unread_full_text(self):
        for s in self.sources.values():
            self.assertTrue(s['url'].startswith('https://'), s['id'])
            self.assertEqual(s['citation_checked_on'], self.research['checked_on'])
            self.assertFalse(s['full_text_read'], s['id'])
            self.assertNotRegex(s['citation'], r'\d+\(\d+\), \d+', s['id'])  # no unconfirmed volume/pages

    def test_summary_cites_only_known_sources_and_activities(self):
        text = (ROOT / 'references/research-base.md').read_text(encoding='utf-8')
        for sid in lib.SOURCE_ID.findall(text):
            self.assertIn(sid, self.sources)
        ids = {a['id'] for a in self.library['activities']}
        prefixes = {i.split('-')[0] for i in ids}
        cited = {t for t in re.findall(r'`([a-z0-9]+(?:-[a-z0-9]+)+)`', text) if t.split('-')[0] in prefixes and t not in lib.AREA_IDS}
        self.assertEqual(cited - ids - set(self.sources), set())
        self.assertEqual(ids - cited, set(), 'every activity is listed in the summary')

    def test_unknown_source_and_overclaimed_grade_are_rejected(self):
        bad = json.loads(json.dumps(self.library))
        bad['activities'][0]['evidence'] = ['no-such-source-2020']
        with self.assertRaises(ValueError):
            self._check_with(bad)
        over = json.loads(json.dumps(self.library))
        target = next(a for a in over['activities'] if a['grade'] == 'plausible' and
                      not any(self.sources[s]['design'] in lib.TESTING_DESIGNS and self.sources[s]['weight'] != 'weak' for s in a['evidence']))
        target['grade'] = 'tested'
        with self.assertRaises(ValueError):
            self._check_with(over)

    def _check_with(self, library):
        original = lib.load
        lib.load = lambda rel: library if rel == 'data/skill-activities.json' else original(rel)
        try:
            return lib.check()
        finally:
            lib.load = original

    def test_generated_pages_are_current(self):
        done = subprocess.run([sys.executable, str(ROOT / 'scripts/skill_library.py'), 'render', '--check'],
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_library_is_public_safe(self):
        blob = json.dumps(self.library) + json.dumps(self.research)
        self.assertNotRegex(blob, r'[\w.+-]+@[\w-]+\.[\w.]+')  # no email addresses


if __name__ == '__main__':
    unittest.main()
