# Parenting Helper — development handoff

Status reviewed: November 24, 2026, America/Chicago (November 25 UTC).

## What to do next

Improve the quality of the actual family briefing. The current release is a functional scaffold, not evidence that the recommendations are useful. Read this file, `AGENTS.md`, `SKILL.md`, and the authorized private household instance's handoff before designing changes. Inspect a real private output there, then produce a substantially better sample before expanding infrastructure or declaring success on test counts.

The intended product combines strong developmental/educational guidance, growing individual child profiles, the real household calendar, everyday learning opportunities and optional local experiences. It should help a parent decide what matters this week and how to expose each child to it. A rotating list of generic games with an agenda attached does not meet that goal.

## Repositories and boundaries

- This PUBLIC repository owns the reusable skill, evidence/source graph, schemas, deterministic utilities, synthetic examples, tests and releases.
- A separate PRIVATE household repository owns actual child profiles, calendar identifiers, observations, private briefings and delivery configuration. Obtain its location from the authorized user/context; never copy those facts into this repository, public issues, PRs or CI artifacts.
- [KC activity finder](https://github.com/colesteaks/kc-activity-finder) is a separate dependency for local places, events, recurring programs and advance registration. Do not alter or duplicate its inventory as part of this handoff. The private instance and `dependencies.json` pin its code; current hours/availability still require verification.
- No hosted service or database was added. Keep inexpensive deterministic ingestion/rendering separate from the weekly agent's research and editorial judgment.

## Exact shipping state

| Item | State at handoff |
| --- | --- |
| Public default branch | `main`; this handoff is proposed on `docs/agent-handoff` for PR review |
| Published release | [v0.1.0](https://github.com/colesteaks/parenting-helper/releases/tag/v0.1.0), MIT; commit `8b91d9cb0188fb11a287c420455058f5e3fdf507` |
| Parser/presentation corrections | [PR #1](https://github.com/colesteaks/parenting-helper/pull/1), OPEN, branch `fix/calendar-preview-review`, code commit `a4d8ee4556ce257b15e06dda5c942520798d8ce6` |
| Checks at that release | Library validation, 19 tests and fictional demo passed; GitHub CI passed |
| Checks on PR #1 | Library validation, 23 tests and fictional demo passed; GitHub CI passed |
| Private dependency | Was still pinned to the v0.1.0 commit; a new public `main` commit or open PR does not update it |

PR #1 measures snapshot age against the time of review rather than a future planning date, excludes all-day/transparent context from the busy-day count, and narrows pickup-deadline warnings so ordinary errands do not trigger them. Review the existing PR rather than duplicating it. It is not merged or released by this handoff. Do not overwrite the existing release tag. Recheck all branch/PR state before working.

## What exists

- `SKILL.md`: portable Agent Skill instructions for a connected host.
- `data/source-graph.json`: 11 first-party source entries, age scope, evidence role, limits and review dates. This is a curated registry, not a continuously researched knowledge system.
- `data/activities.json`: 12 original caregiver activity cards in nine domains, each with four variants spanning 6–95 months. These are adaptations, not evaluated protocols.
- `scripts/family_briefing.py`: offline Python CLI for profile validation, approximate age progression, calendar normalization, selection, Markdown rendering and explicit observations.
- `schemas/`: profile, calendar, source graph, activity and observation contracts.
- `references/`: evidence policy, calendar semantics, selection formula and maintenance rules.
- `examples/`, `tests/`, `.github/workflows/ci.yml`: synthetic demonstrations and correctness checks.

Calendar collection, fresh source research, human-quality editorial synthesis, Git publication and email delivery are performed by the connected host. The Python engine does not implement those connectors. A shell checkout cannot automatically use a ChatGPT calendar/Gmail connection. There is no reusable committed email renderer/sender or full scheduled-run integration test yet.

## Main quality gaps, grounded in the implementation

1. **The selection pool is too small and static.** Twelve stock cards cannot supply an evolving developmental briefing. Source links in a footer are not weekly evidence synthesis. Add a maintained way to identify relevant parent guidance and worthwhile opportunities without uncontrolled browsing or manufactured research claims.
2. **Personalization mostly amounts to age bands.** Interests are pooled across children in `select_plan`; an `avoid` observation suppresses a card for the entire household. One child outside the supported range can prevent all siblings from receiving a card. The schema lacks useful structured goals, routines, languages, current questions and dated caregiver context. Fix these deliberately rather than inventing missing facts.
3. **Selection incentives are weak.** Domain variety outranks explicit preferences, with a hash tie break. There is no thoughtful learning sequence, reason to revisit a topic, per-child objective, or explanation of why this idea matters for this household this week. Novelty is not inherently better than repetition.
4. **Calendar data barely changes recommendations.** It appears in an agenda and a coarse busy-day note. It is not yet translated into helpful routine anchors, preparation for an existing experience, follow-through afterward, or realistic alternatives. Preserve the full calendar while making the main newsletter readable; an appendix can retain all entries. Do not infer free time, childcare or affected children from titles or blank slots.
5. **The product scope was narrowed without a user requirement.** One five-minute family game per day is an implementation choice, not a settled constraint. Consider a small number of meaningful weekly priorities, books/read-alouds, conversation, practical skills, social-emotional support, science/nature, music/art, movement, ongoing classes and opportunities within existing routines. Offer individual time as well as sibling activities. Avoid an overwhelming checklist.
6. **Presentation is mechanical.** Repeated supervision, attribution and status boilerplate crowds the output. Separate a concise parent-facing briefing from technical coverage/evidence details. Provide concrete materials, caregiver language and an easy fallback. Avoid source-count/test-count claims as a substitute for a good newsletter.
7. **Evidence tracing needs to be sharper.** Preserve which recommendation/variant is supported by which exact source and its age/population limits. Organizational authority and a hub link do not substantiate a specific claim. CDC monitoring checklists are not curriculum or screening. Do not label invented home games research-proven or transfer preschool evidence to infants.
8. **The growth loop is minimal.** The current journal influences preferences, not a useful evolving profile. Build lightweight, explicit caregiver feedback with dates and provenance; no inferred mastery, deficits or diagnoses. Ask only the few questions that would materially improve the next briefing.
9. **The integration is not yet reproducible.** A real test required manual editorial edits and an ad hoc email renderer. Passing parser tests does not demonstrate a fresh, coherent end-to-end newsletter or a successful scheduled run. Capture these seams without leaking private fixtures.

## Suggested implementation sequence

1. Inspect the private sample and its handoff. Write a better replacement briefing using available facts and clear unknowns. Show the improvement in usefulness, not just more content.
2. Settle a small output contract: week/logistics highlights, a few worthwhile priorities, clearly distinct child-specific ideas with rationale, manageable routine anchors, optional verified opportunities, exact supporting links and one easy feedback request. Include every calendar entry somewhere accessible.
3. Improve the profile/evidence/briefing data model with backwards-compatible migration and dated provenance. Make individual child needs first-class; do not let one unsupported profile disable everyone.
4. Replace arbitrary card rotation with a grounded editorial pipeline and deterministic support for evidence, freshness, history and calendar correctness. Keep model work bounded to the weekly host; retain token-free deterministic operations where they help.
5. Reuse/review PR #1, add meaningful regressions for new behavior and evaluate at least one realistic private week plus synthetic edge cases. A reviewed sample should explicitly distinguish known family facts, source-backed guidance and creative adaptations.
6. Release reviewed changes with a new version; then update the private lock file intentionally. Verify the actual scheduled host can fetch current inputs, render/review, publish privately and report access failures. Delivery authorization and schedules live with the private instance.

## Start and verify

Fetch current remote branches first; do not assume this machine or any old checkout survives. Read repo instructions and confirm private visibility before any household push. Use a separate worktree/branch for implementation. Inspect existing PRs to avoid duplicate work.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/family_briefing.py validate-library
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/family_briefing.py build \
  --synthetic --household examples/fictional-household.json \
  --calendar examples/fictional-calendar.json --start 2026-11-23 \
  --out /tmp/fictional-family-briefing.md
```

Synthetic dates are fixed examples, not current calendar data. Read README for real private invocation. Inspect semantic quality separately from schema/test success. Do not manufacture current sources, child capabilities, live availability, automation execution or email delivery.

## Completion bar

The next agent should leave a demonstrably better private briefing, reusable public code/skill improvements with synthetic regression coverage, intentional dependency/version updates, clear remaining gaps and verified GitHub publication. A plan, another source list, or a prettier version of the same generic cards is insufficient.
