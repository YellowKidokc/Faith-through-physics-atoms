# Status Update — April 18, 2026
**Updated by:** Claude Opus (David's session)

---

## WHAT CHANGED SINCE APRIL 16

### GTQ-01 is now the Gold Standard
`gtq-01-measurement-collapsed-reality.html` was rebuilt from the ground up:
- Custom audio players (not browser chrome) — play/pause/seek/mute
- Player strip at top of Paper tab (3 inline players: Deep Dive blue, Read Aloud gold, Debate purple)
- Player strip duplicated on Tangent tab
- Oversized Born Rule section — 3-column gold/teal/white grid
- Decoherence Steps 1/2/3 — large cards with Oswald headers
- Red gradient falsification criteria
- Sign-out cards side-by-side at bottom
- Canvas-based chalkboard (GTQ-01 only)
- Tab rename: "Watch & Listen" → "Media & Tools"
- ~800 lines of CSS, full JS block for audio + tabs + sidebar + progress

### New Landing Page (index.html)
Complete data-driven rewrite with:
- Master equation display, stats ribbon
- Variable heat map, argument flow (Mermaid.js), concept threading (Canvas)
- Reading order cards with CHI badges
- Fruits of the Spirit grid, Framework Integrity checks

### Pipeline Run Complete
- Paper Intelligence pipeline ran on all 25 GTQ markdown sources
- Fresh Excel + JSON in `D:\GitHub\genesis-to-quantum\THEOPHYSICS_PAPER_INTELLIGENCE\OUTPUT\`
- Knowledge graph HTML exported
- L8 (GoEmotions) failed on 7 papers (512-token limit) — known, non-critical

### New Files Created
- `articles.json` — full manifest of all 20 articles with metadata, audio paths, tangent relationships, prev/next, status
- `AGENTS.md` — complete handoff spec for template stamping
- `GTQ-01_SESSION_NOTES.md` — narrative of all changes made to GTQ-01

---

## WHAT COWORK SHOULD DO NEXT

### Priority 1: GTQ Template Stamping (THE BIG ONE)
**See `AGENTS.md` for full spec.** **See `articles.json` for the manifest.**

For each of the 20 non-GTQ-01 articles:
1. Open the existing HTML file
2. Replace the CSS block with GTQ-01's CSS (verbatim — ~800 lines)
3. Replace the JS block with GTQ-01's JS (minus chalkboard engine)
4. Add player strip to top of Paper tab (update audio URLs per article)
5. Add player strip to top of Tangent tab (if it has one)
6. Rename tab buttons (article title replaces "The Paper", tangent names)
7. **Keep all existing article body content** — DO NOT rewrite
8. Keep existing Summary and Rigor tab content
9. Verify no unclosed tags or broken CSS

### Priority 2: Build 5 Missing Tangent HTML Files
These have markdown sources but no HTML yet:
- gtq-07a-empirical-testing.html (from GTQ_07A_Empirical_Testing_Master_Equation.md)
- gtq-08b-how-god-restores.html (from GTQ_08B_How_God_Restores.md)
- gtq-08c-science-behind-restoration.html (from GTQ_08C_Science_Behind_Restoration.md)
- gtq-09a-regime-dependent-theology.html (from GTQ_09A_Regime_Dependent_Theology.md)
- gtq-09b-civilizational-decay.html (from GTQ_09B_Isomorphism_Civilizational_Decay.md)

Build these using the tangent article template from GTQ-01A as a base.

### Priority 3: Continue Phase 2-3 Tasks
Tasks 4-10 from the original briefs still apply (sidebars for other series, orphans, sticky nav, TTS wiring, podcast index).

---

## DESIGN RULES (from David, April 18)
1. **Fonts lean bold** — no thin/light weights
2. **Visual breakup every section** — rotate cards, grids, gradient blocks, pull quotes. No walls of text.
3. **Appropriate image density** — 1-2 for short articles, 4-5 for longer ones
4. **Gradients are good** — use them liberally on section backgrounds, cards, containers
5. **Vary the visual pattern** — don't repeat the same layout variable all the way down the page

---

## ANOMALIES TO FIX
- `gtq-06-the-photon-isnt-watching.html` is a duplicate of gtq-07 (same Article 07 content inside). Delete or redirect.
- `gtq-08a` bottom nav links to `gtq-08.html` (broken — should be `gtq-08-god-doesnt-need-a-clock.html`)
- Two audio CDNs in use: `r2.faiththruphysics.com` (main articles, preferred) vs `pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev` (older tangents). Standardize to `r2.faiththruphysics.com`.
- 4 tangent files have empty audio src (04b, 05a, 05b, 05c) — wire up when audio is uploaded

---

## FILE MAP
```
D:\Cowork\
├── AGENTS.md                    ← GTQ template stamping spec (NEW)
├── articles.json                ← Full article manifest with metadata (NEW)
├── STATUS_UPDATE_April18.md     ← This file (NEW)
├── REBUILD_TASKS.md             ← Master task list (April 16)
├── Theophysics_Website_Rebuild.md ← Full cowork brief (April 16)
├── Phase2_Sidebars_Orphans_Audio.md ← Phase 2 tasks
├── Phase3_Audio_Wiring_Podcasts.md  ← Phase 3 tasks
├── Audio_Mapping_OUTBOX_to_Articles.md ← 102 MP3 → article mapping

D:\GitHub\genesis-to-quantum\genesis-to-quantum\
├── gtq-01-measurement-collapsed-reality.html  ← GOLD STANDARD (do not modify)
├── articles.json                               ← Same manifest (also here)
├── AGENTS.md                                   ← Same spec (also here)
└── [20 other GTQ HTML files to upgrade]
```

---

*April 18, 2026 | GTQ-01 rebuilt | Pipeline run complete | 20 articles need template stamp | 5 tangents need HTML from scratch*
