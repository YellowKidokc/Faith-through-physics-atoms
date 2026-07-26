# Markdown Intake Pipeline — Design Document

tags: #pipeline #markdown #intake #automation

**Claude (Opus) | July 25, 2026 | POF 2828**

---

## The Problem

Markdown is scattered across 5+ drives in hundreds of folders.
The atoms repo has 24 domains with the 14-stage arc ready to receive.
We need a repeatable process: markdown goes in, classified and named
files come out in the right domain and stage folder.

## The Pipeline (3 steps)

### Step 1: GATHER — Pull all markdown into one staging area

**Input:** Markdown files from everywhere
**Output:** All files in `D:\GitHub\Faith-through-physics-atoms\_intake\raw\`

```
Source locations:
- D:\md\                           (massive — thousands of files)
- D:\SubStack\Convergence\         (4 articles)
- D:\GTQ-BUILD\articles\MD\        (1 file)
- D:\GTQ-BUILD\articles\[01-26]\   (empty markdown/ folders)
- Z:\ root                         (mixed .md files)
- E:\Faith Through Physics MD\     (needs MCP fix)
- H:\00_Canonical_PRODUCTION_v1.0\ (canonical markdown)
- H:\Desktop 2\Master HTMl\markdown (root)\
- C:\theophysics\CANONICAL\        (new canonical root)
- C:\theophysics\_MD_ARCHIVE\      (archive)
```

**Script: `_scripts\gather_markdown.py`**
- Walk all source paths
- Copy (never move) every .md file into _intake\raw\
- Preserve source path in filename or sidecar .json
- Deduplicate by content hash (SHA-256)
- Output: manifest.csv (filename, source_path, hash, size, first_line)
### Step 2: CLASSIFY — Route each file to domain + stage

**Input:** Files in `_intake\raw\`
**Output:** Files in `_intake\classified\{domain}\{stage}\`

**Script: `_scripts\classify_markdown.py`**

Classification rules (in priority order):

1. **Filename match** — if filename contains a series slug:
   - `gtq-*` or `genesis-to-quantum*` → domain depends on content
   - `convergence-*` → theology or physics (check content)
   - `logos-*` → theology
   - `dt-*` or `death-test*` → theology
   - `drv-*` or `revolution*` → theology

2. **Frontmatter match** — if file has YAML frontmatter:
   - `entry_layer:` → use directly as stage
   - `domain:` → use directly
   - `series:` → map to domain
   - `tags:` → keyword match to domain list

3. **Content keyword match** — scan first 500 chars:
   - Physics terms (equation, force, field, energy) → physics
   - Theology terms (grace, sin, faith, God) → theology
   - Both → check for bridge language → synthesis stage
   - Law N reference → ten-laws domain
   - Master equation reference → master-equation domain
   - Trinity reference → trinity domain
   - Consciousness terms → consciousness domain

4. **Stage inference from content:**
   - Has equations + formal language → 07_paper or 01_canonical
   - Has "in plain language" or everyday tone → 09_everyday
   - Has narrative/story structure → 11_articles
   - Has objection/rebuttal structure → 08_objections
   - Has evidence citations → 05_evidence
   - Has kill conditions → 06_falsification
   - Has hypothesis/prediction → 04_hypothesis
   - Raw/unstructured → 00_inbox_working

5. **Fallback** — anything unclassified → `_intake\unclassified\`
   with a note explaining what the classifier couldn't determine.

**The classifier should be CONSERVATIVE.** Better to land in
00_inbox_working than to misclassify. A human or AI can promote
later. Demotion is harder than promotion.
### Step 3: PLACE — Move classified files into the atoms repo

**Input:** Files in `_intake\classified\{domain}\{stage}\`
**Output:** Files in the actual domain folders with proper naming

**Script: `_scripts\place_markdown.py`**

Placement rules:

1. **Rename to convention:** `{domain}-{stage_num}-{auto_increment}.md`
   Example: `theology-11-001.md`, `physics-01-003.md`

2. **Add frontmatter if missing:**
   ```yaml
   ---
   nodeID: {domain}-{stage_num}-{auto_increment}
   entry_layer: {stage}
   max_layer: (inferred or 00_inbox_working)
   next_action: "needs review"
   source_file: {original filename}
   source_path: {original full path}
   intake_date: {today}
   intake_hash: {SHA-256}
   ---
   ```

3. **Check for duplicates** in destination before placing:
   - Same hash already exists → skip, log as duplicate
   - Similar title exists → flag for manual review
   - No match → place

4. **Generate intake report:**
   - Total files processed
   - Per domain count
   - Per stage count
   - Duplicates skipped
   - Unclassified count
   - Files needing manual review

---

## Series → Domain Mapping

When 30 series are ready, this is how they map:

| Series | Primary Domain | Also Touches |
|--------|---------------|-------------|
| GTQ (Genesis to Quantum) | physics | theology, consciousness |
| Convergence | theology | physics, master-equation |
| Logos Papers | theology | axioms, ten-laws |
| Death Test (DT) | theology | physics, falsification |
| Revolution of Truth (DRV) | theology | history, axioms |
| Proof Architecture (PA) | axioms | physics, theology |
| Cross-Domain | master-equation | all domains |
| One-Page Stories | christian-life | theology |
| Consciousness | consciousness | physics, theology |
| Master Equation | master-equation | physics, ten-laws |
| Duality Project | physics | theology |
| Three Truths / Three Gates | axioms | theology |
| Spiritual Warfare | theology | psychology |
| Isomorphism | master-equation | physics, theology |
| Moral Decline | history | economics, theology |

Files that touch multiple domains: primary copy goes in the primary
domain. Bridge reference (a .json sidecar with edge data) goes in
the secondary domain's 03_synthesis folder.

---

## The 30-Series Transfer Process

When David says "these 30 are ready":

```
1. Run:  python _scripts\gather_markdown.py --sources series_list.txt
2. Run:  python _scripts\classify_markdown.py
3. Review: _intake\unclassified\ (manual sort)
4. Run:  python _scripts\place_markdown.py --dry-run (preview)
5. Run:  python _scripts\place_markdown.py (commit)
6. Run:  python _scripts\status_scan.py (update folder icons)
7. Check: _intake\intake_report.csv
```

Total time for 30 series: under an hour if the scripts work.
Under a day if they need debugging.

---

## What Needs Building

| Script | Status | Complexity |
|--------|--------|-----------|
| gather_markdown.py | Not built | Low — file walk + hash + copy |
| classify_markdown.py | Not built | Medium — keyword matching + frontmatter parse |
| place_markdown.py | Not built | Low — rename + frontmatter inject + copy |
| series_list.txt | Not built | Manual — David lists the 30 series paths |

The classifier is the only non-trivial piece. Everything else is
file operations. If we want to go fast, build gather and place
first (they're mechanical), then iterate on the classifier.

---

## Folder Structure After Intake

```
D:\GitHub\Faith-through-physics-atoms\
├── _intake\
│   ├── raw\              ← gathered, deduped
│   ├── classified\       ← routed to domain/stage
│   ├── unclassified\     ← needs manual sort
│   └── intake_report.csv
├── theology\
│   ├── 01_canonical\
│   │   ├── theology-01-001.md
│   │   └── theology-01-002.md
│   ├── 11_articles\
│   │   ├── theology-11-001.md  ← was convergence-01.md
│   │   ├── theology-11-002.md  ← was convergence-02.md
│   │   └── ...
│   └── ...
├── physics\
│   ├── 11_articles\
│   │   ├── physics-11-001.md   ← was gtq-01.md
│   │   └── ...
│   └── ...
└── ...
```

---

*"Transfer them, build their files, name their folders, get
everything set up so we can start walking the parallel line."*
*— David, July 25, 2026*