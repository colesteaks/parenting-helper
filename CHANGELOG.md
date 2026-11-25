# Changelog

## Unreleased

- Widen the research base to 181 sources and add `finding_checked_against` to each source (schema, renderer and tests updated). 83 findings were checked against an abstract or summary page and corrected; 98 are labelled as not yet checked.
- Rewrite the music and art sections of `references/research-base.md`, adding the arts trials the first version missed and the dispute over music and IQ. Replace the effort-tier table, which ranked music and art down, with an evidence-and-routine table, and add a section on breadth and interest development.
- Expand music and art from 8 to 20 activities, add breadth activities (`sel-try-new-activity`, `science-follow-the-interest`), and attach new evidence to existing activities. `writing-invented-spelling`, `cooking-taste-new-foods` and `building-copy-model` are now graded `tested`; `sel-brave-thing` is now `adapted`.
- Add a research base for ages 4–6 (48–71 months): `data/research.json` with 71 sources across the thirteen skill areas, and `references/research-base.md` stating what the research supports and does not support in each area, with confidence labels.
- Add `data/skill-activities.json`: 63 original activities across the thirteen areas, each with an easier and a harder version and an evidence grade of `tested`, `adapted` or `plausible`.
- Add `scripts/skill_library.py` (validate and render), two schemas, ten tests, and the generated pages `references/research-sources.md` and `references/activity-catalog.md`. CI runs the validator and a stale-page check.
- Add a "Skill-area library" workflow to `SKILL.md`. The weekly renderer, the twelve cards and card selection are unchanged.
- Add `references/skill-areas.md`, a research framing for thirteen caregiver skill areas from infancy through elementary age. Linked from the README, the skill workflow, and maintenance. No schema, activity-id, or selection change.

## 0.1.0

- Initial portable parenting-helper skill with a scoped first-party guidance graph and original age-adapted caregiver ideas.
- Deterministic seven-day briefing builder, complete calendar agenda, calendar coverage/overlap checks, explicit feedback journal and approximate age progression.
- Separate public skill and private household storage; synthetic regression fixtures and CI.
- Pinned optional activity-finder dependency for outings.
