# ARCHITECTURE DECISION LOG
## What we rejected and why — for cross-session continuity
## July 23, 2026

---

## v1: Filing cabinet by type (articles, proofs, templates)
REJECTED: Categories fragment the framework. A file about 
psychology that touches physics has no home.

## v2: Dual trunk (math side / word side / bridge)
REJECTED: Better than v1 but still categories. "Be Glad 
You're a Loser" doesn't fit either trunk cleanly.

## v3: Domain-first with native/bridge/synthesis per domain
ACCEPTED AS BASE: David's insight. Organize by knowledge 
domain, not by type. Infinite domains, same internal structure.

## v4: Added _SYNTHESIS (meta-level) and _THESIS (formal papers)
REJECTED AS TOP-LEVEL: These became stages INSIDE domains 
instead of sitting above them.

## v5: Parity mirror — proof side / audience side
PARTIALLY KEPT: The mirror concept survived as the descent 
rule. The explicit mirror structure was too rigid.

## v6: Scientific method AS the top level
REJECTED: David said "no, the domain is the skeleton, the 
arc is the heartbeat inside every domain." Arc moved inside.

## v7: Domain-first, arc inside, 8 stages
ACCEPTED: Core architecture locked. Master equation is a 
domain, not a god-folder.

## v8: Added paradigm stage
ACCEPTED: Goes right after canonical. Reframing thinking 
before you predict from it.

## v9: Added hypothesis + fulfilled as bookends, 62 rigor items
ACCEPTED: Rigor falls out of the structure. 62 requirements,
zero checklists.

## v10: Merged GPT's three-field tags, route classification
ACCEPTED: entry_layer + max_layer + next_action per file.
Route classes for different content types.

## v11: Final synthesis — added GPT website requirements,
## Codex route classification, Kimi cathedral shell
ACCEPTED AS CANONICAL: 14 stages, 62 rigor requirements,
31 website requirements, descent rule, route classes.

---

## KEY DECISIONS (the ones that changed everything)

1. **Domains are infinite, arc is fixed.**
   The thing that grows (domains) is the top level.
   The thing that's constant (stages) is inside.

2. **Down is never optional.**
   David: "God didn't say the high end class. He said the 
   prostitutes, the beggars, the thieves." Truth flows down.

3. **The paper is the MIDPOINT, not the endpoint.**
   PhD paper enters at 07, must descend through everyday, 
   worldcheck, articles, audience. The paper serves the people,
   not the other way around.

4. **The structure IS the rigor.**
   We don't need checklists. Populated folders = requirements met.
   Empty folders = visible gaps. The architecture does the auditing.

5. **Not every file runs the full arc.**
   The full arc is the POSSIBLE route. Most content enters in 
   the middle and only descends. Upward is optional. The pieces 
   that complete the full route are the strongest pieces.

6. **Paradigm goes right after canonical.**
   You lock the truth, THEN reframe how people think about it.
   The paradigm shift is what generates the hypothesis.

7. **Everyday before articles.**
   Plain truth first. Story version second. The simple version 
   comes before the longer treatment because the simple version 
   IS the truth. The article is the packaging.

---

## OPEN ITEMS FROM KIMI'S STRESS TEST

1. NLP drift-detection script needed in 91_pipelines_nlp/
   - Reads frontmatter, checks tag consistency, flags drift
   - NOT BUILT YET

2. Descent enforcement mechanism
   - Website labels empty lower stages as "unfinished descent"
   - Public accountability, not private tracking
   - SPECIFIED BUT NOT BUILT

3. Cathedral shell ↔ content stage integration
   - Cathedral renders content; stages produce content
   - One-pager stories = 12_audience content
   - Reading levels = cathedral toggle, not separate files
   - DESIGNED BUT NOT BUILT

4. Compressed carry-forward state
   - THIS FILE is the decision log
   - v11 canonical spec is the current state
   - Together they give any AI full reconstruction
