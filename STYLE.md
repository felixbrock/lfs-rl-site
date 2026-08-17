# Page style guide

Checklist for any agent editing index.html. Telegraph bullets, read
top to bottom before editing, verify bottom section after editing.

## Voice and register

- StatQuest clarity, professional register. Plain words, never casual.
- One idea per sentence. Short sentences beat compound ones.
- Introduce every term plain-words first, name it after. "the model
  looks at the deciding evidence first, we call this routing" and
  never the reverse.
- Concrete over abstract. Name the file, the count, the command.
- No ambiguous nouns. "a broken thing" forbidden, "a specific problem
  to repair" correct.
- No informal phrasing. Forbidden examples, "parroted", "rubber-
  stamps", "thrown out", "leans the right way", "feeds on", "walked
  into", "tip-off", "for free", "lucky run".
- No caps for emphasis. Never "WHY", "NOT", "APPEARS". Use sentence
  structure or markup instead.
- No both-sides tautologies. "whether it produces the correct output"
  correct, "it either produces the correct output or it does not"
  forbidden. Real contrasts that exclude a weaker reading are allowed,
  "runs, not merely builds".
- One precise verb per central concept, reused everywhere. The
  incident is "reproduced", never a rotating set of synonyms.
- The haystack metaphor is the one approved metaphor. Add no others.

## Communication order

- Conclusion first, everywhere. Abstract before content, takeaway
  before mechanism, result before method, caption states the finding
  before the encoding.
- The page opens with an Abstract that summarizes the whole page,
  thesis plus the headline numbers, five sentences maximum.
- KPI row directly under the abstract carries the headline numbers.
- Every section opens with its conclusion in the first sentence.
- Supporting detail follows the conclusion, never precedes it.

## Claims discipline

- Every number scoped to its evidence. Say what was measured, how many
  episodes, under which conditions.
- Separate direction from claim. Small samples "trend", they never
  "show". State the sample size next to any trend.
- Say plainly what is verified and what is not. Unmeasured dials are
  named as unmeasured.
- Honesty caveats survive every rewrite. Never trade a caveat for
  flow.

## Visualization

- Visualize wherever possible. Any counts, comparisons, or outcome
  lists go into a figure, prose keeps only what a figure cannot carry,
  mechanism and caveat.
- Reuse the page's existing idioms before inventing one. Episode dot
  ledger for per-episode outcomes, 2x2 grid for factor contrasts,
  booktabs table for enumerable facts, inline SVG for rates and
  distributions.
- Dot vocabulary is fixed. Hollow green held or safe completion, solid
  red incident reproduced or bricked, hollow gray held but incomplete.
  Identity never rides on color alone, fill and shape differ too.
- Captions are conclusion-first and self-contained, a reader who sees
  only the figure gets the finding, the encoding, and the caveat.
- Every SVG carries a role and aria-label with the numbers in text.
- Complex figures get a table fallback in a details element.
- Render and inspect any new or changed figure before pushing, check
  label collisions, overflow, and grayscale legibility.

## Design

- Academic journal look. Existing tokens and fonts only, STIX serif
  body, Plex Sans labels, the defined palette variables.
- Page is pinned light mode, keep the color-scheme meta as is.
- No new colors, no new fonts, no decorative elements. New CSS only
  for a genuinely new figure type, and it follows the token system.
- Wide content scrolls inside its own container, the page body never
  scrolls horizontally.

## Edit process checklist

- Read the full current page before changing anything.
- Match new content to the nearest existing idiom, prose block,
  ledger, grid, table, or SVG.
- After editing, grep the page for the forbidden patterns above.
- After editing, confirm every new number has its evidence scope and
  every trend its sample size.
- Screenshot changed figures at desktop width and inspect.
- Keep figure numbering sequential and cross-references intact.
- Commit with a one-line subject describing the change, push, verify
  the push landed.
