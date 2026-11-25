# Skill-area framing

Caregivers often want children to have repeated, low-pressure chances to cook, read, write, play with numbers, notice the world, make art and music, move, get along with other people, help at home, be outside, build things, and sometimes hear another language. This note names those areas and the questions this project still has to answer before it adds guidance.

It is a research agenda for the public skill. It is not a curriculum, a milestone checklist, a screening tool, or a list of activities to assign. Monitoring stays separate from play guidance, as in [evidence policy](evidence-policy.md). CDC milestone sources explain communication with a clinician. They do not set targets, rank children, or decide which card is selected.

The offline library today has nine activity domains and twelve cards, each with variants from 6 through 95 months. These skill areas are wider than that library. An area with no card is a gap to investigate, not permission to invent a game or an evidence rating. New detailed claims need a reviewed source leaf, a recorded age scope, and an original caregiver adaptation. See [maintenance](maintenance.md).

## How to investigate an area

Work one area at a time. Read the exact source. Record organization, URL, role, age scope, review date, and limitations in `data/source-graph.json` before any new card depends on it. Link to book lists and articles. Do not copy them.

Use these age bands so answers line up with the library:

| Band | Approximate ages | Months | Current variant |
| --- | --- | --- | --- |
| Infancy | First year and a half | 0–17 | `infant` is 6–17 months. Birth through 5 months has no card. |
| Toddler | About 1½–3 years | 18–35 | `toddler` |
| Preschool | About 3–5 years | 36–71 | `preschool`. A 5-year monitoring list falls in this band. |
| Early elementary | About 6–7 years | 72–95 | `early-school`. This is the top of the current library. |
| Later elementary | About 8–11 years | 96–143 | Outside the library. Needs an explicit reviewed adaptation. |

For every area, answer four kinds of questions:

1. **Milestones.** What do monitoring sources say that is relevant in each band, and what are their limits? Keep the result as context for caregivers and clinicians.
2. **Activities.** Which practices have an evidence guide or a practice guide for that age and setting? Preserve the source rating with the source. Do not attach it to an untested home game, or move a preschool rating onto infants or later elementary ages.
3. **Materials.** Which age-rated books, tools, or household materials do first-party sources suggest, and which need extra supervision (heat, sharp tools, small parts, allergens, outdoor hazards)?
4. **Progress.** What can a caregiver notice and record with `observe`? Observations influence preferences only. They do not mark mastery, rewrite the profile, or produce a score.

Also describe a progression across the five bands that the sources actually support. Prefer a few low-prep ideas over a new domain for its own sake. Have an adult review sibling safety. Keep stable activity IDs; do not reuse an ID for a different idea.

## Where this sits beside current data

Activity cards use `domain` values. Household `priorities` are those domain strings and change selection by one point. Skill-area ids below are not domains and not priorities. Putting `reading` or `cooking` in `priorities` or `interests` does not create a focus field. The household schema has no skill-focus field. Selection remains domain spread, explicit interests, enjoyed or avoided cards, and recent history, as in [selection methodology](selection-methodology.md).

| Skill area | Id | Nearest current domain | Cards already in the library | Open gap |
| --- | --- | --- | --- | --- |
| Cooking | `cooking` | `independence` (adjacent) | None. `laundry-sort` is a chore, not food. | No food-preparation card. |
| Reading | `reading` | `language-literacy` | `book-conversation`, `story-voices`, `sound-hunt` | Shared language and sound play, not a reading progression. |
| Writing | `writing` | `language-literacy` (adjacent) | None. One early-school line says writing is optional. | No mark-making or composing card. |
| Math | `math` | `early-math` | `table-math`, `find-a-pattern` | Later number, measurement, and elementary topics. |
| Science | `science` | `nature-science` | `nature-notice` | Science practices are not separated from nature. |
| Art | `art` | None | None. `music-creativity` is rhythm only. | No visual-art card. |
| Music | `music` | `music-creativity` | `rhythm-turns` | Singing and instruments. |
| Movement and sports | `movement` | `motor` | `movement-mirror` | Coordination sequences and team play. |
| Social-emotional skills | `social-emotional` | `social-emotional`, `executive-function` | `feelings-story`, `choice-and-plan` | Losing, turn-taking, and feeling words are only partly covered. |
| Practical life and independence | `practical-life` | `independence` | `laundry-sort` | Dressing, tidying, and helping beyond one chore. |
| Nature and outdoors | `nature` | `nature-science` | `nature-notice` | Animals, plants, and seasons are not distinct prompts. |
| Building and engineering | `building` | `spatial-reasoning` | `building-together` | Ramps, tinkering, and changing a design. |
| Second language (optional) | `second-language` | None | None | No language-exposure card. Optional for a household. |

Reviewed sources that already touch some of these areas include CDC monitoring pages, the Harvard executive-function and serve-and-return guides, the IES/WWC preschool practice guide, AAP play guidance, ZERO TO THREE Math4Littles, and the Reach Out and Read and NAEYC family hubs. Hub pages are starting points. Read the leaf before attributing a recommendation. `ztt-math` is scoped to about 24–47 months. `ies-prek` is scoped to about 36–71 months. Do not treat either as coverage for infants or for later elementary age.

## Cooking

Food preparation with a caregiver: watching, touching safe foods, stirring, pouring, measuring, following a simple recipe, and helping serve. Includes kitchen safety, heat, sharp tools, allergens, and choking hazards. Touches math (how much), reading (a recipe), and practical life (helping).

- Which monitoring sources mention feeding, cups, utensils, or helping with food in each band, and what do they say those lists are for?
- Which evidence guides or practice guides describe caregiver-child cooking or food play, for which ages and settings? What must stay unclaimed when the source did not study a home recipe?
- Which tools and foods are recommended at each band, and which are out (heat, knives, small hard foods, allergens) until a source and a safety review say otherwise?
- What can a caregiver write down about joining in ("stirred", "asked to pour") without treating that note as permission to use heat or a sharp tool?
- What progression do sources support from watching and tasting, to stirring and pouring, to measuring, to preparing a simple snack in the elementary years?
- How should a future cooking card stay distinct from `table-math` and `laundry-sort`?

## Reading

Shared looking and reading, talk about pictures and stories, letters and sounds, and the later move toward reading print. Listening and storytelling stay in this area because they support reading. Current cards are conversation, story-making, and sound play in `language-literacy`.

- Which monitoring items in each band concern joint attention, pictures, words, letters, and reading, and how should the project quote their limits?
- Which shared-reading practices are backed for which ages? The preschool evidence guide includes vocabulary, letters and sounds, and shared reading. Which of those recommendations stop at preschool?
- Which first-party book lists (including the Reach Out and Read hub) should be linked for each band, and how do we point at them without copying the lists into this repository?
- Which signs of interest are worth an observation, and which must stay out of any reading level or rank?
- What progression do sources support from noticing a picture, to choosing and talking, to predicting a story, to retelling, to reading words in elementary age?
- How should sound play (`sound-hunt`) stay a language card rather than be relabeled as reading instruction?

## Writing

Marks on a page, drawings, letter-like forms, writing a name, invented spelling, and short messages a child wants to send. Includes grasp and posture, and the difference between forming letters and composing an idea. No current card is about writing.

- Which monitoring items in each band mention scribbling, drawing, or writing, and what age limits come with them?
- What do evidence and practice guides say about composing meaning versus copying letters, and for which ages?
- Which materials are suggested at each band, and which fine-motor tools are a poor fit for infants and toddlers?
- How can a caregiver note "made marks" or "asked an adult to write a word" without a handwriting score?
- What progression do sources support from watching an adult mark, to scribbling, to drawing and dictating, to letter play, to short messages in elementary age?
- Should a future idea be a new card with a new id, and should its domain stay `language-literacy` or wait until writing has its own reviewed scope?

## Math

Everyday number, comparison, pattern, shape, space, and measurement in play and routines. Current cards set a pretend table and make a large pattern. ZERO TO THREE’s math guide covers two- and three-year-olds. The preschool evidence guide includes math only for its preschool population.

- Which monitoring items touch quantity, comparison, or problem solving in each band, and how do we keep them out of card selection?
- Which math recommendations are evidence-rated, for which ages, and which playful number games are practice guidance with no effect size?
- Which household materials and linked activity lists are enough for each band, without commercial curricula copied into the repo?
- What observations show that a math moment was welcome, and how do we avoid turning a correct count into a mastery flag?
- What progression do sources support from noticing "more" and "in/out", to one-to-one matching and patterns, to comparing amounts, to elementary problem solving?
- Which elementary topics (place value, operations, measurement) have home guidance we can review, given the library ends at 95 months?

## Science

Practices of noticing, guessing, trying, and talking about what happened. Questions, changes, and simple comparisons. Distinct from nature content below, even though the library currently folds both into `nature-science` and a single "notice one thing" card.

- Do any monitoring sources describe curiosity or cause-and-effect play in a way we may cite, and at which ages?
- Which guides distinguish science practices from science facts for infants through elementary age, and which of those were studied outside the home?
- Which safe, low-prep materials support trying one variable (sink/float, ramp, shadow) at each band, and which experiments are inappropriate without adult control of heat, chemicals, or small parts?
- How can a caregiver record a question or a try ("asked what would happen") without grading the explanation?
- What progression do sources support from watching a cause the adult repeats, to trying one change, to comparing two tries, to a short elementary investigation?
- Should science stay inside `nature-science` until there are two reviewed cards, rather than adding a domain name first?

## Art

Making marks, color, collage, sculpture, and other visual play for its own sake. Process and choice matter more than a finished display. No current card. Rhythm lives under music, not here.

- Which monitoring items, if any, mention drawing or making, and what must we avoid inferring from them?
- Which practice guides describe open-ended art with a caregiver, for which ages, and do any evidence guides study art as an outcome?
- Which materials are age-rated (large crayons, dough, paper) and which fail a sibling small-part or toxicity check?
- What observations capture engagement without judging the product or comparing siblings?
- What progression do sources support from sensory mark-making, to choosing colors and tools, to planning a picture, to revisiting an idea in elementary age?
- How should art materials and instructions stay separate from the writing area when both use marks on paper?

## Music

Rhythm, singing, and instruments: copying a beat, songs, pitch play, and simple sound-makers. The current card trades a clapped or tapped rhythm. Singing and instruments are not separate ideas yet. Hearing, volume, and shared-instrument hygiene belong in the safety review.

- Which monitoring items mention sounds, songs, or response to music in each band?
- Which guides recommend singing, beat play, or instruments, at which ages, and which claims are general play guidance rather than a studied music program?
- Which household sound-makers are appropriate at each band, and which instruments or small parts are unsafe for infants and toddlers?
- How can a caregiver note enjoyment or a request to repeat a song without rating musical ability?
- What progression do sources support from responding to a voice, to taking a turn with a sound, to singing a short phrase, to keeping a beat or exploring an instrument in elementary age?
- What would a singing card and an instrument card add that `rhythm-turns` does not already cover?

## Movement and sports

Coordination, balance, locomotor play, throwing and catching with a caregiver, and later cooperative games. Team play includes waiting, roles, and handling winning and losing, which also belongs to social-emotional skills. The current card mirrors one movement. It is not a sport and not a motor assessment.

- Which monitoring items describe movement in each band, and how do their authors say to use them?
- Which guides support active play, and which organized-sport recommendations exist for preschool versus elementary age? Keep injury, concussion, and specialization claims attached to those sources.
- Which spaces and equipment are suggested at each band, and which need supervision, helmets, or a decision to skip?
- What observations describe energy and willingness to play without a fitness or coordination score?
- What progression do sources support from floor play and cruising, to running and climbing, to simple games with rules, to team play in elementary age?
- How should a movement card leave losing and turn-taking to the social-emotional area instead of duplicating them?

## Social-emotional skills

Getting along during play: waiting a turn, losing a game, naming a feeling, and repairing a small conflict with adult help. Current cards give a toy a feeling and choose a tiny project. Those are adaptations informed by executive-function and play guidance, not a social-emotional curriculum. For worry or loss of skills, help the caregiver form questions for a clinician. Do not screen.

- Which monitoring items mention calming, play with others, or feelings in each band, and what are they not allowed to decide?
- Which recommendations in the preschool evidence guide and the Harvard executive-function guide match turn-taking, frustration, or feeling words, and where does that evidence stop?
- Which books or picture supports do first-party hubs suggest for naming feelings, and which proprietary programs must we link rather than reproduce?
- How should observations such as "waited for a turn" or "named a feeling" be stored so they never update a profile or imply a diagnosis?
- What progression do sources support from an adult naming a feeling, to a child using a feeling word, to practicing a hard moment in a game, to elementary peer problem solving?
- Which pieces of "handling losing" are already covered by `choice-and-plan` or `feelings-story`, and which need a new reviewed card?

## Practical life and independence

Dressing, tidying, and helping at home: manageable pieces of real work a child can join. The current card sorts laundry. Cooking is framed separately even though helping in the kitchen is also practical life.

- Which monitoring items mention dressing, feeding, or helping, and at which ages?
- Which practice guides describe household participation, and which popular practical-life sequences are tradition rather than a reviewed study?
- Which clothing, storage, and tool setups make helping realistic at each band without creating a safety problem for younger siblings?
- What observations record a wanted job ("put cups on the table") without a chore chart or an independence score?
- What progression do sources support from watching and holding a piece of clothing, to simple dressing and putting things away, to a short helping job, to planning a household task in elementary age?
- Which helping ideas overlap cooking or math and should stay a single card so domains do not multiply?

## Nature and outdoors

Animals, plants, weather, and seasons, mostly by noticing what is already outside or on a windowsill. The current card asks the family to notice one outdoor thing. Science practices are listed separately; this area is the content of the living world. Include water, plants, wildlife, sun, and weather in the safety review. Indoor alternatives belong in the same investigation for days outside is not possible.

- Which monitoring or parent-tip sources mention outdoor play or animals, and what age scope do they state?
- Which guides support nature play or caregiving for a plant or animal, and which conservation or pet-care claims are outside those sources?
- Which field guides, library books, or household routines (a window, a walk, a seed) are recommended at each band, by link rather than excerpt?
- How can a caregiver note what a child returned to ("watched the same bird") without turning it into knowledge the child is supposed to have mastered?
- What progression do sources support from sensory time outside, to naming one plant or animal, to noticing a seasonal change, to a simple elementary nature journal?
- Should animals, plants, and seasons be three prompts on one card or three cards, given the preference for a few low-prep ideas?

## Building and engineering

Blocks, ramps, enclosures, and tinkering: stacking, connecting, and changing a structure to see what happens. The current card builds and changes a structure under `spatial-reasoning`. Spatial ideas also sit inside early math guidance, so this area overlaps math.

- Which monitoring items mention stacking, problem solving, or play with objects in each band?
- Which guides treat block play or spatial talk as a recommendation, for which ages, and which of those are evidence-rated only for preschool?
- Which loose parts are safe at each band, and how do infant and toddler variants keep small building pieces away from younger children?
- What observations capture persistence or a change in the build without scoring engineering skill?
- What progression do sources support from handling one object, to stacking and knocking down, to a ramp or enclosure, to planning a change in elementary age?
- How should a building card cite math or spatial sources without claiming those sources evaluated a specific block brand or ramp game?

## Second language (optional)

Hearing and using a language other than the one already strongest at home, through songs, books, talk, and play. This area is optional. A household that uses one language can ignore it. Do not assume which languages are present, and do not store a real family's languages in this public repository. Caregiver-supplied language context belongs in the private household instance.

- What do monitoring sources say, if anything, about language development when a child hears more than one language, and which myths do those sources reject?
- Which evidence guides address bilingual exposure or second-language learning in early childhood and elementary age, and which populations did they study?
- Which song, book, and conversation practices are recommended for home exposure, and which packaged curricula should only be linked?
- How can a caregiver note "asked for the same song again" without labeling fluency or mixing this up with a reading score?
- What progression do sources support from hearing a language in routines, to songs and shared books, to short exchanges, to reading or writing in that language in elementary age?
- Under what conditions would the library add a card at all, given this area is optional and no card exists today?

## What a finished answer includes

A useful answer names the skill-area id, the age bands it covers, the source leaves read, and the role of each source. It states limits in the source's own terms. It recommends at most a few new cards, with new stable ids, safety notes, and variants only where the source applies. It leaves profiles, calendars, and real household details out of this repository. If the sources do not support a claim, the answer says the claim is unavailable and withholds it.
