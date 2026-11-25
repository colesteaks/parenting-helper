# Maintenance and releases

Keep household facts out of this repository and all public CI output. Use fictional profiles and calendars in regression fixtures. The activity finder remains a separate dependency; do not duplicate its event inventory or calendar collectors here.

Quarterly, or before introducing materially new guidance:

1. Check existing source URLs, organization ownership, age applicability and the exact supporting recommendation. Read leaves rather than treating hub search snippets as evidence. Record review dates and limitations. Deprecate unsupported cards without reusing their stable IDs for different ideas.
2. Review gaps by age and domain, starting from the open questions in `references/skill-areas.md`. Weigh home feasibility, language/access representation and caregiver feedback. Add a few useful, low-prep ideas rather than expanding domain count for its own sake. Have an adult review sibling safety and age-rated materials. Skill-area ids are a research agenda. Activity `domain` values stay the selection categories until a reviewed card says otherwise.
3. Update source graph and cards together. Preserve monitoring versus curriculum boundaries and source population scope. New detailed claims require source review; do not silently change research evidence ratings.
4. Run `python scripts/family_briefing.py validate-library`, `python scripts/skill_library.py validate`, `python scripts/skill_library.py render --check`, `python -m unittest discover -s tests -v`, and the README fictional demo. Check rendered all-day dates, overlaps, completeness warnings and age variants. Scan every staged file for real profiles, calendar IDs, emails, private locations and credentials.
5. Update `VERSION`, SKILL metadata and CHANGELOG together. Use patch for fixes, minor for compatible features, major for breaking schema/CLI changes. Create and push a semantic version tag after CI passes. Record the immutable commit in private instance dependencies. Never overwrite a released tag.

Private household upkeep: read all visible calendars fresh for each briefing; keep raw snapshots ignored; preserve dated caregiver facts and aliases. Profile growth is not automatic developmental inference. Verify the remote is private immediately before every push. An accidental secret commit requires removing it and rotating the secret; Git history is persistent, so avoid unnecessary sensitive detail.

Automation: a connected scheduled assistant may run the host workflow for an authorized private household. GitHub Actions runs only synthetic CI here. The renderer has zero network/model calls and no daily token spend. A Sunday run must report incomplete access and cannot claim it fetched data or pushed files without evidence. Calendar reads, code execution, GitHub access and private visibility must all work before scheduling the complete publishing workflow.

## Skill-area library

Edit `data/research.json` and `data/skill-activities.json`, then run `python scripts/skill_library.py render` and commit the regenerated pages with the data. Do not edit `references/research-sources.md` or `references/activity-catalog.md` by hand. `references/research-base.md` is written by hand and must cite only source ids that exist.

- Before adding a source, confirm the citation exists and record the date. Set `full_text_read` to true only after reading it, and then correct the finding and limits against the text. Leave out volume and page numbers unless confirmed.
- Reading the 71 current sources in full and correcting their summaries is the main outstanding work. Start with the ones whose `limits` say a figure was recalled from memory.
- Keep activity ids stable. Change a grade when the evidence changes, and say why in the changelog.
- A new band needs its own research pass. Do not widen an existing band's months to cover it.
