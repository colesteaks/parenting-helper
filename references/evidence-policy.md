# Evidence and guidance policy

Prefer relevant first-party sources over newsletter listicles or affiliate recommendations. Authority alone does not establish that an individual game was studied. The source graph records organization, exact leaf, role, age scope, review date and limitations.

| Role | Examples | Appropriate use |
| --- | --- | --- |
| Evidence guide | IES What Works Clearinghouse Pre-K guide | Match the population, setting and actual recommendation. Preserve source-specific evidence ratings when discussed; never attach them to an untested adaptation. |
| Practice guide | Harvard executive function, AAP play, ZERO TO THREE Math4Littles | Practical context for playful caregiver adaptations, with stated age limits. No precise effect or guaranteed result. |
| Monitoring | CDC milestones | Explain monitoring and caregiver-clinician communication. Never select curriculum targets, screen, diagnose, rank children or infer deficits. |
| Resource hub | NAEYC families, Reach Out and Read resources | Discover relevant leaves and books. Review those leaves before attributing specific detailed guidance. |

Core coverage: responsive relationships; language/shared reading; early math and spatial ideas; self-regulation and executive function; social-emotional learning; movement; independence; creativity; nature/science exploration. These are opportunities for exposure rather than a performance checklist. Broader subjects or ages require new reviewed cards, not ungrounded claims of complete coverage.

The 12 initial cards are original caregiver adaptations. Their source IDs refer to compatible underlying guidance, not exact protocols. Cards include full-range applicable practice guidance; narrower toddler math / preschool evidence links are included only when their scope covers the variant. Hub and monitoring sources cannot substantiate card selection. The source validator enforces these constraints.

For additional advice, read the exact source and record a short original summary of its applicability and limits. Respect copyright: link instead of reproducing articles or proprietary materials. Record unavailable sources as unavailable and withhold claims. Separate caregiver observations from professional guidance and from assistant suggestions. Do not use anecdotes as diagnostic evidence.

For worries, loss of skills or requests to assess a child, encourage an appropriate clinician conversation; do not turn the briefing into screening or provide medical interpretation. Do not access child health records. Offer accessible adaptations with the caregiver; age alone does not establish mobility, sensory preferences, language or readiness.

## Primary research and the skill-area library

`data/research.json` holds research papers, reviews and guidelines alongside the first-party guidance in the source graph. The two are kept apart: the source graph substantiates the weekly cards, and the research file substantiates the skill-area library. Each research source records:

- **Design**, from meta-analysis and randomized trial down to theory. Correlational designs (longitudinal, cross-sectional, observational) are never described as showing that a practice works.
- **Ages studied**, so a finding is not silently moved to another age.
- **Weight** (`strong`, `moderate`, `weak`): this project's judgement of how much the source can bear for a home decision at ages 4–6. It is not a rating taken from the source.
- **Verification**: `citation_checked_on` is the date the citation was confirmed to exist. `finding_checked_against` records what the stored finding was compared with: `paper` (the paper's own abstract or text), `secondary` (a press release, database entry or clearinghouse page), or `none` (prior knowledge only). `full_text_read` is true only when the full text was read end to end. Specific numbers from a `none` source are treated as unverified, and volume and page numbers are omitted.

Each activity in `data/skill-activities.json` carries a grade:

| Grade | Meaning | How to present it |
| --- | --- | --- |
| `tested` | A close practice was tested or rated for children near this age. Requires at least one cited source that tests or rates a practice and is not weak. | "A practice like this has been studied." Never a promised result. |
| `adapted` | Research on another age or setting, or correlational evidence. The home routine is untested. | "Based on research with ..., adapted for home." |
| `plausible` | Reasonable and low risk, with no reviewed study behind it. | "No direct evidence. Included because ..." |

The validator enforces the `tested` rule. When evidence is contested, say so in the source's `limits` and in the summary. When a source that might change a conclusion was seen but not reviewed, record that in `limits` and do not characterise its findings. Record negative findings (no transfer, no advantage, fade-out) with the same care as positive ones.
