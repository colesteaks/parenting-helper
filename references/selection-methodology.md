# Selection methodology

The renderer is a transparent offline baseline, not an assessment model. It proposes seven optional family cards, each with a compatible variant for every child, and never books time on the calendar.

Eligibility requires a reviewed activity, an explicit variant matching each child's age on that date, and no `avoid` feedback within 28 days. Dated reported ages project by completed calendar months; approximate means approximate. A supplied DOB is optional. Unsupported ages receive an explicit coverage gap, not a substituted variant.

Selection maximizes this tuple in order:

1. Fewest already-selected cards in this domain, to spread exposure across the week.
2. `2 × explicit interest-tag matches + 1 if household-priority domain + up to 2 enjoyed observations − 1 if in previous briefing`.
3. A deterministic SHA-256 tie break seeded by ISO week, date and card ID, giving reproducible weekly variation.

The script never assigns a child a developmental score. Preferences come only from explicit caregiver inputs. `avoid` feedback currently suppresses a family card for all siblings; an editorial host can offer another compatible card or ask about a child-specific alternative. The profile is not rewritten by this process. History penalizes unnecessary repetition but does not prohibit welcome practice.

Calendar information is deliberately separate from card ranking: the renderer lacks reliable childcare, sleep and caregiver availability. It suggests routines and flags busy dates with three or more active commitment entries, without using transparent holidays to block the day. A human/agent editorial pass should simplify or skip ideas as needed and preserve the entire agenda.
