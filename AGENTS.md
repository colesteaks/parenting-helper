# Repository instructions

This is a PUBLIC reusable skill repository. Never store real child profiles, calendar identifiers, event titles/locations, household observations, private briefing output or credentials here, including in fixtures, logs, issues or PRs. Use the separate private household instance. Keep examples explicitly fictional.

Read SKILL.md, references/evidence-policy.md and references/maintenance.md before changing guidance. Preserve stable activity IDs, source scopes, private/public boundaries and the optional activity-finder dependency. Monitoring is not curriculum. The renderer remains deterministic, offline and free of model/API calls.

Run the library validator, `python scripts/skill_library.py validate` and `render --check`, the unittest suite and the fictional README demo before a push. Research summaries in data/research.json must not claim more than their `full_text_read` and `limits` fields allow. Do not write calendar events, change repository access, or publish private artifacts. Add meaningful regression coverage for parser/schema changes. Keep VERSION, SKILL metadata and CHANGELOG consistent for releases.
