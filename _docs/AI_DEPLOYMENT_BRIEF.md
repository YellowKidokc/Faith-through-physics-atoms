# FAITH THROUGH PHYSICS — AI DEPLOYMENT BRIEF
## For GPT to distribute to all workers (Codex CLI + Claude CLI)
## July 23, 2026

---

## SITUATION

David is spinning up 2-3 Codex CLI instances and 1-2 Claude CLI 
instances as workers. GPT and Claude Opus are managers. Workers 
need to know where everything is, what to do, and how to do it.

The master equation domain is RESERVED — David and the managers 
handle that one. Workers take the other domains.

---

## STEP 1: READ FIRST (every worker, before anything else)

```
C:\theophysics\CANONICAL\README_AI_START_HERE.md
```

This file explains:
- The 14-stage folder arc
- The descent rule (down is never optional)
- How nodes/atoms work
- How to create new domains
- Where everything lives

---

## STEP 2: READ THE SPECS (if you need detail)

```
C:\theophysics\CANONICAL\_docs\THEOPHYSICS_ARCHITECTURE_v11_CANONICAL.md
C:\theophysics\CANONICAL\_docs\CLAIM_ATOM_NODE_TYPES.md
C:\theophysics\CANONICAL\_docs\ROOT_LAYER_SPEC.md
C:\theophysics\CANONICAL\_docs\ATOM_BUILD_PACK.md
```

---

## STEP 3: FIND YOUR EXISTING CONTENT

Content is scattered across these locations. Gather what you 
need for your assigned domain(s):

### Primary sources:
```
D:\GitHub\faiththruphysics-site-data\           ← site repo (HTML + MD)
O:\_Theophysics_v5\                              ← Obsidian vault
\\192.168.2.50\h_hp\00_Canonical_PRODUCTION_v1.0\ ← NAS canonical
\\192.168.2.50\h_hp\Desktop\Files\               ← claim atom standard 1.0
```

### Series locations in site repo:
```
D:\GitHub\faiththruphysics-site-data\genesis-to-quantum\    ← GTQ (26 articles)
D:\GitHub\faiththruphysics-site-data\convergence-series\    ← CNS (7 articles)
D:\GitHub\faiththruphysics-site-data\convergence-deep\      ← CDT (6 articles)
D:\GitHub\faiththruphysics-site-data\revolution-of-truth\   ← DRV (6 articles)
D:\GitHub\faiththruphysics-site-data\logos-papers\           ← LP (14 articles)
D:\GitHub\faiththruphysics-site-data\isomorphism\            ← ISO (38 articles)
```

### Key NAS content:
```
\\192.168.2.50\h_hp\00_Canonical_PRODUCTION_v1.0\Crown\                    ← Crown docs
\\192.168.2.50\h_hp\00_Canonical_PRODUCTION_v1.0\01_MASTER_EQUATION_CORE\  ← ME core
\\192.168.2.50\h_hp\Desktop\TEN_LAWS_CANONICAL\                            ← Ten Laws
```

---

## STEP 4: YOUR WORKFLOW

For each domain you're assigned:

### A. Gather
1. Find existing content for this domain across all source locations
2. Copy relevant files into the domain's `00_inbox_working/` folder
3. Don't reorganize yet — just get everything in one place

### B. Classify  
4. Read each file and determine its entry_layer (which stage it belongs in)
5. Move it to the correct stage folder
6. Add frontmatter tags: entry_layer, max_layer, next_action

### C. Populate downward
7. For every file, check: are the stages BELOW it populated?
8. If not, that's your TODO — write the missing descent stages
9. Priority: every canonical claim (01) needs an everyday version (09)
10. Every article (11) needs an audience version (12)

### D. Create atoms (when ready)
11. For canonical claims, create .jsonld atoms
12. Use the schema from CLAIM_ATOM_NODE_TYPES.md
13. Set edges to connect to other atoms (dependsOn, bridgesTo)
14. Atoms should trace upward: claim → law → master equation

---

## STEP 5: WHAT TO BUILD IN EACH FOLDER

Each stage folder has a README with a checklist. Follow it.
But here's the quick version:

| Stage | What you produce | Format |
|-------|-----------------|--------|
| 00 | dump raw content here | anything |
| 01 | formal claim statement + plain version | .md with frontmatter |
| 02 | old paradigm → break → new paradigm | .md |
| 03 | cross-domain bridge with bridgeGrade | .md or .jsonld |
| 04 | testable prediction + methodology | .md |
| 05 | external evidence + citations | .md with sources |
| 06 | kill attempts + outcomes | .md |
| 07 | doctoral template paper (13 sections) | .md |
| 08 | steelmanned objections + responses | .md |
| 09 | plain language, no jargon, Monday morning | .md |
| 10 | pressure test against real world | .md |
| 11 | narrative story form article | .md |
| 12 | SEO/social/toolkit version | .md or .html |
| 13 | results: confirmed/partial/failed | .md |

---

## DOMAIN ASSIGNMENTS

GPT: assign these based on who's available. Suggested split:

### Codex CLI #1: Physics-heavy domains
- physics
- cosmology
- information-theory
- consciousness

### Codex CLI #2: Cross-domain / life sciences  
- biology
- pharmacology
- epidemiology
- ecology
- addiction-science

### Codex CLI #3: Social / applied domains
- economics
- education
- history
- network-science

### Claude CLI #1: Theology / scripture
- theology
- scripture
- christian-life

### Claude CLI #2: Framework core
- ten-laws
- axioms
- trinity

### RESERVED (David + managers):
- master-equation (the root — handled separately)

---

## RULES

1. **READ the README in every folder before writing anything.**

2. **Down is never optional.** If you populate 01_canonical, you OWE 
   09_everyday at minimum. If you write 07_paper, you OWE everything 
   below it.

3. **Don't touch other workers' domains** unless coordinating through 
   GPT or Claude Opus.

4. **Atoms (.jsonld) only for 01_canonical claims.** Everything else 
   is .md files with frontmatter for now.

5. **The master-equation domain is OFF LIMITS** to workers. 
   Managers handle the root layer.

6. **When in doubt, ask.** Post your question to your domain's 
   00_inbox_working/ as a note. A manager will see it.

7. **Track your work.** After each session, run:
   ```
   python C:\theophysics\CANONICAL\_scripts\status_scan.py
   ```
   This updates folder icons and generates the status report.

---

## THE HIERARCHY (for context)

```
GOD
  ↓
[Two classifications — being defined]
  ↓
MASTER EQUATION (χ)
  ↓
TEN LAWS (10 expressions)
  ↓
DOMAINS (infinite, each with 14-stage arc)
  ↓
ATOMS (self-describing, self-connecting nodes)
```

Every claim traces upward: claim → law → master equation.
The graph builds itself from the edges in the atoms.

---

## API / NLP HOOKS (future — not wired yet)

Each folder README lists what NLP and API calls should eventually 
run against its content. For now, do the work manually. When we 
wire the automation, it'll run against what you've already produced.

Key future hooks:
- 01_canonical: Lean 4 verification
- 05_evidence: web search for competing frameworks  
- 09_everyday: Flesch-Kincaid readability scoring
- 10_worldcheck: LLM consensus check
- 11_articles: cross-reference validation

---

_Faith Through Physics | POF 2828_
_Truth always flows down._
