# Parenting Helper

A reusable Agent Skill for private weekly family learning briefings: all calendar commitments, one small play-based learning idea per day, and a separate adaptation for each child. Profiles grow through dated caregiver observations. Local outings come from the separate [KC activity finder](https://github.com/colesteaks/kc-activity-finder).

The public repository contains guidance, code and **fictional** examples. Keep real profiles, calendar IDs, agendas and briefings in a separate private repository. This skill does not publish a website or modify calendars.

## Install and try it

Requires Python 3.11+ and `jsonschema`. Install a versioned skill copy in your agent's skills directory, or clone it and provide its `SKILL.md` to an agent that supports the Agent Skills format. Release tags pin the code; live calendar and event data must still be refreshed.

```bash
git clone --branch v0.1.0 https://github.com/colesteaks/parenting-helper.git
cd parenting-helper
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/family_briefing.py validate-library
.venv/bin/python scripts/skill_library.py validate
.venv/bin/python scripts/family_briefing.py build \
  --synthetic --household examples/fictional-household.json \
  --calendar examples/fictional-calendar.json --start 2026-11-23 \
  --out /tmp/fictional-family-briefing.md
.venv/bin/python -m unittest discover -s tests -v
```

Read [SKILL.md](SKILL.md) for the agent workflow. This is a portable skill, not a proprietary plugin or hosted service; there are no embedded credentials, API calls or paid dependencies.

## Use your private household instance

1. Create a private repository and verify its visibility. Copy the example household shape there; remove `fictional` and supply only the facts you want stored in GitHub. Aliases and approximate ages work; birth dates are optional. Never commit credentials.
2. Have the connected assistant enumerate all calendars and fetch all pages of events for the week. Save the snapshot under an ignored `.runtime/` directory. Follow the [calendar contract](references/calendar-contract.md). A local Python process does not inherit ChatGPT calendar authentication.
3. Keep `calendar-sources.json` containing a `calendars` list of expected `{id,label,role}` entries, an empty `observations.jsonl`, and optional prior private briefings.
4. Build outside the public skill checkout:

```bash
python scripts/family_briefing.py build \
  --household ../my-private-family/household.json \
  --calendar ../my-private-family/.runtime/calendar.json \
  --calendar-config ../my-private-family/calendar-sources.json \
  --observations ../my-private-family/observations.jsonl \
  --start YYYY-MM-DD \
  --out ../my-private-family/briefings/YYYY-MM-DD.md
```

Use `--history ../my-private-family/briefings/PREVIOUS.md` to prefer novel activities when other priorities are equal. Add explicit caregiver feedback with:

```bash
python scripts/family_briefing.py observe \
  --household ../my-private-family/household.json \
  --journal ../my-private-family/observations.jsonl \
  --child CHILD_ID --date YYYY-MM-DD \
  --activity book-conversation --response enjoyed \
  --text 'Asked to look at the same picture again.'
```

Observations influence preferences, never automatically mark development or rewrite profiles. `avoid` feedback suppresses the card for 28 days; an agent should review feedback and access needs before adapting. With mixed siblings, the library selects only cards that have a variant for everyone. It reports unsupported ages instead of guessing. Source applicability is validated per variant.

## Contents and boundaries

- `data/source-graph.json`: 11 reviewed first-party guidance sources, scoped by age and evidence role.
- `data/activities.json`: 12 original caregiver adaptations across 9 domains, each with four age variants covering 6–95 months. The games are not evaluated interventions.
- `data/research.json`: 71 research sources across the thirteen skill areas, each with design, ages studied, finding, limits and a weight. Citations were confirmed to exist; no full text was re-read, and the file says so per source.
- `data/skill-activities.json`: 63 original activities for ages 4–6 (48–71 months) across the thirteen areas, each with an easier and a harder version and an evidence grade of `tested`, `adapted` or `plausible`. The weekly renderer does not read this file yet.
- `scripts/skill_library.py`: validates both files and renders `references/research-sources.md` and `references/activity-catalog.md`.
- `scripts/family_briefing.py`: deterministic calendar normalization, age progression, preference-based selection, agenda rendering and caregiver feedback capture.
- `schemas/`: profile, calendar-snapshot and observation contracts; semantic validation supplements JSON Schema.
- `tests/`: calendar correctness, age/source scope, feedback, reproducibility and public-path privacy checks.
- `references/`: evidence policy, [skill-area framing](references/skill-areas.md), [research base for ages 4–6](references/research-base.md), [research sources](references/research-sources.md), [activity catalog](references/activity-catalog.md), calendar contract, selection methodology and maintenance.

## Skill areas to investigate

[Skill-area framing](references/skill-areas.md) lists thirteen areas a caregiver may want children to explore, from cooking through an optional second language. For each area it records open questions: milestones by age band, evidence-based activities, materials, and how progress can be noticed from infancy through elementary age. The 48–71 month band now has a first answer in the [research base](references/research-base.md) and [activity catalog](references/activity-catalog.md); the other bands are open. Use that list to choose the next reviewed addition. The agenda is wider than today's nine activity domains. It does not change card selection, household profiles, or the line between monitoring checklists and play.

Age bands organize options, not readiness standards. The engine does not interpret free-text access notes; the host/caregiver must adapt. Unknown interests stay unknown. Approximate ages are projected by completed calendar months from their report date and are always labeled approximate. A supplied leap-day birthday uses completed calendar months. Calendar snapshots are not continuous sync and completeness only describes what the connected account can see.

The skill is educational support, not a child assessment or medical service. [CDC explains the limits of milestone checklists](https://www.cdc.gov/act-early/milestones/key-points.html). We distinguish those tools from play guidance and from [preschool evidence recommendations](https://ies.ed.gov/ncee/wwc/practiceguide/30).

## Versioning and maintenance

MIT license. Version `0.1.0`; semantic version tags and a changelog identify reproducible skill releases. Maintain source scope, regression tests and private/public separation using [maintenance instructions](references/maintenance.md). The static skill and renderer require no daily model calls or cloud hosting. Connected calendar reads and a Sunday editorial run require a host with those capabilities.
