#!/usr/bin/env python3
"""Validate and render the skill-area research base and activity library.

Offline and deterministic. Reads data/research.json and data/skill-activities.json,
checks them, and renders the two generated reference pages:

    python scripts/skill_library.py validate
    python scripts/skill_library.py render          # rewrite the generated pages
    python scripts/skill_library.py render --check  # fail if the pages are stale
"""
import argparse
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
AREAS = [
    ('reading', 'Reading'), ('writing', 'Writing'), ('math', 'Math'), ('science', 'Science'),
    ('art', 'Art'), ('music', 'Music'), ('movement', 'Movement and sports'),
    ('social-emotional', 'Social-emotional skills'), ('practical-life', 'Practical life and independence'),
    ('cooking', 'Cooking'), ('nature', 'Nature and outdoors'), ('building', 'Building and engineering'),
    ('second-language', 'Second language (optional)'),
]
AREA_IDS = [a for a, _ in AREAS]
CROSS = 'cross-cutting'
# Designs that test or formally rate a practice. A 'tested' activity must cite at least one.
TESTING_DESIGNS = {'meta-analysis', 'systematic-review', 'rct', 'experiment', 'quasi-experiment',
                   'case-control', 'evidence-guide', 'guideline'}
SOURCE_ID = re.compile(r'`([a-z0-9]+(?:-[a-z0-9]+)*-(?:19|20)\d{2})`')
# What the stored finding was compared with on the check date.
CHECKED = {
    'paper': "the paper's own abstract or text",
    'secondary': 'a secondary summary (press release, database entry or review page)',
    'none': 'nothing; summarised from prior knowledge',
}
GENERATED = {
    'references/research-sources.md': 'sources',
    'references/activity-catalog.md': 'catalog',
}


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


def validate_schema(name, value):
    schema = load(f'schemas/{name}.schema.json')
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value),
                    key=lambda e: list(e.path))
    if errors:
        where = '/'.join(str(p) for p in errors[0].path)
        raise ValueError(f'{name}: {errors[0].message} at {where}')


def check():
    """Return (sources by id, activities) after schema and semantic checks."""
    research = load('data/research.json')
    library = load('data/skill-activities.json')
    validate_schema('research', research)
    validate_schema('skill-activities', library)

    sources = {}
    for s in research['sources']:
        if s['id'] in sources:
            raise ValueError(f"Duplicate source id: {s['id']}")
        if s['studied_min_months'] > s['studied_max_months']:
            raise ValueError(f"Source age range is reversed: {s['id']}")
        for area in s['areas']:
            if area not in AREA_IDS and area != CROSS:
                raise ValueError(f"Unknown area on source {s['id']}: {area}")
        sources[s['id']] = s

    bands = {b['id']: b for b in library['bands']}
    seen = set()
    for a in library['activities']:
        if a['id'] in seen:
            raise ValueError(f"Duplicate activity id: {a['id']}")
        seen.add(a['id'])
        if a['area'] not in AREA_IDS:
            raise ValueError(f"Unknown area on activity {a['id']}: {a['area']}")
        if a['band'] not in bands:
            raise ValueError(f"Unknown band on activity {a['id']}: {a['band']}")
        if a['grade'] not in library['grades']:
            raise ValueError(f"Unknown grade on activity {a['id']}: {a['grade']}")
        cited = []
        for sid in a['evidence']:
            if sid not in sources:
                raise ValueError(f"Activity {a['id']} cites an unknown source: {sid}")
            cited.append(sources[sid])
        if a['grade'] == 'tested' and not any(s['design'] in TESTING_DESIGNS and s['weight'] != 'weak' for s in cited):
            raise ValueError(f"Activity {a['id']} is graded 'tested' without a source that tests or rates a practice")

    for area in AREA_IDS:
        if not any(a['area'] == area for a in library['activities']):
            raise ValueError(f'No activity for area: {area}')
        if not any(area in s['areas'] for s in sources.values()):
            raise ValueError(f'No research source for area: {area}')

    summary = ROOT / 'references/research-base.md'
    if summary.exists():
        for sid in set(SOURCE_ID.findall(summary.read_text(encoding='utf-8'))):
            if sid not in sources:
                raise ValueError(f'references/research-base.md cites an unknown source: {sid}')
    return research, library, sources


def months(lo, hi):
    def one(m):
        return f'{m} mo' if m < 24 else (f'{m // 12} y' if m % 12 == 0 else f'{m // 12} y {m % 12} mo')
    return one(lo) if lo == hi else f'{one(lo)} to {one(hi)}'


def render_sources(research, sources):
    out = ['# Research sources', '',
           '<!-- Generated by scripts/skill_library.py from data/research.json. Do not edit by hand. -->', '',
           research['note'], '']
    counts = {k: sum(s['finding_checked_against'] == k for s in research['sources']) for k in CHECKED}
    out += [f"Of {len(research['sources'])} sources, the finding was checked against {CHECKED['paper']} for {counts['paper']}, "
            f"against {CHECKED['secondary']} for {counts['secondary']}, and against nothing for {counts['none']}. "
            'Each entry says which.', '',
           'Weight says how much a source can bear when deciding what a caregiver does at home with a child of 4-6: '
           '`strong`, `moderate` or `weak`. It is this project\'s judgement, not a rating taken from the source. '
           'For the synthesis by area, read [research-base.md](research-base.md).', '']
    groups = [(CROSS, 'Cross-cutting')] + AREAS
    for area, label in groups:
        rows = [s for s in research['sources'] if s['areas'][0] == area]
        if not rows:
            continue
        out += [f'## {label}', '']
        for s in rows:
            also = [a for a in s['areas'][1:]]
            out += [f"### `{s['id']}`", '',
                    f"{s['citation']} [Link]({s['url']})", '',
                    f"- Design: {s['design']}. Ages studied: {months(s['studied_min_months'], s['studied_max_months'])}. Weight: {s['weight']}.",
                    f"- Finding: {s['finding']}",
                    f"- Limits: {s['limits']}",
                    f"- Finding checked against: {CHECKED[s['finding_checked_against']]}."]
            if also:
                out.append(f"- Also informs: {', '.join(also)}.")
            out.append('')
    return '\n'.join(out).rstrip() + '\n'


def render_catalog(library, sources):
    band = library['bands'][0]
    out = ['# Activity catalog', '',
           '<!-- Generated by scripts/skill_library.py from data/skill-activities.json. Do not edit by hand. -->', '',
           f"Band `{band['id']}`: {band['label']} ({band['min_months']}-{band['max_months']} months). "
           'Every activity has an easier and a harder version so it can be pitched at the edge of what a child can do. '
           'These are original caregiver adaptations. The grade says how close the research comes to the activity itself:', '']
    for grade, text in library['grades'].items():
        out.append(f'- `{grade}`: {text}')
    out += ['', 'Source ids link to [research-sources.md](research-sources.md). For what the research does and does not '
            'support in each area, read [research-base.md](research-base.md).', '',
            '| Area | Activities | Tested | Adapted | Plausible |', '| --- | --- | --- | --- | --- |']
    for area, label in AREAS:
        rows = [a for a in library['activities'] if a['area'] == area]
        counts = [sum(a['grade'] == g for a in rows) for g in ('tested', 'adapted', 'plausible')]
        out.append(f"| [{label}](#{area}) | {len(rows)} | {counts[0]} | {counts[1]} | {counts[2]} |")
    out.append('')
    for area, label in AREAS:
        out += [f'<a id="{area}"></a>', '', f'## {label}', '']
        for a in [a for a in library['activities'] if a['area'] == area]:
            cites = ', '.join(f"[`{s}`](research-sources.md#{s})" for s in a['evidence'])
            out += [f"### {a['title']}", '',
                    f"`{a['id']}` · {a['grade']} · about {a['minutes']} min · {a['cadence']}", '',
                    f"- **Goal:** {a['goal']}",
                    f"- **Do:** {a['do']}",
                    f"- **Easier:** {a['easier']}",
                    f"- **Harder:** {a['harder']}",
                    f"- **Materials:** {a['materials']}",
                    f"- **Why:** {a['why']} Sources: {cites}.",
                    f"- **Notice:** {a['notice']}",
                    f"- **Safety:** {a['safety']}", '']
    return '\n'.join(out).rstrip() + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('validate')
    render = sub.add_parser('render')
    render.add_argument('--check', action='store_true', help='fail if a generated page is stale')
    args = parser.parse_args()
    try:
        research, library, sources = check()
        if args.command == 'validate':
            print(f"Skill library is valid: {len(sources)} sources, {len(library['activities'])} activities, {len(AREA_IDS)} areas.")
            return 0
        pages = {'sources': render_sources(research, sources), 'catalog': render_catalog(library, sources)}
        stale = []
        for rel, key in GENERATED.items():
            path = ROOT / rel
            if args.check:
                if not path.exists() or path.read_text(encoding='utf-8') != pages[key]:
                    stale.append(rel)
            else:
                path.write_text(pages[key], encoding='utf-8')
        if stale:
            print('Stale generated pages: ' + ', '.join(stale) + '. Run: python scripts/skill_library.py render', file=sys.stderr)
            return 1
        print('Generated pages are current.' if args.check else 'Rendered ' + ', '.join(GENERATED) + '.')
        return 0
    except (ValueError, KeyError, json.JSONDecodeError, OSError) as exc:
        print(f'Skill library check failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
