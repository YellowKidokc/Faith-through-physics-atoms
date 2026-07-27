# Cowork Brief — Phase 2
**Date:** April 16, 2026 | **Continues from:** Phase 1 (sidebar, prev/next, PI links — DONE)
**Repo:** `D:\GitHub\genesis-to-quantum`
**TTS Pipeline:** 69 files processing in `O:\999_IGNORE\TTS_Engines\TTS_Pipeline\`

---

## WHAT'S DONE

- ✅ Task 1: GTQ sidebar links fixed (21 files, 3 template variants)
- ✅ Task 2: Prev/next nav fixed (3 repaired, 17 already correct)
- ✅ Task 3: PI links injected (22 articles → PI reports)
- ✅ TTS: 69 files in pipeline (Edge TTS, Brian voice)
- ✅ PI reports: 36 deployed at `/paper-intelligence/`
- ⏳ NOT YET DEPLOYED — nothing pushed to Cloudflare yet

---

## TASK 4: ADD SIDEBARS TO OTHER SERIES

**Only GTQ has a sidebar. Five other series have zero in-series navigation.**

### 4A: Convergence Sidebar (5 articles in `convergence/`)

Reading order (by Master Narrative act number):
```
1. the-turtles-and-the-floor.html          (Act 1)
2. convergence-02-six-theorems-proved-grace.html  (Act 2)
3. convergence-01-why-god-drown-everybody.html    (Act 9)
4. convergence-04-same-trick-different-costume.html (Act 10)
5. convergence-03-day-map-became-territory.html   (Act 11)
```

Each file needs: sidebar toggle button, overlay div, sidebar nav with all 5 links, `class="current"` on own entry, link to `../index.html` (main hub). Copy the CSS/JS pattern from any GTQ main article.

### 4B: Consciousness Sidebar (10 articles in `consciousness/`)

Reading order:
```
1. consciousness-constraint-argument.html     (The Wall)
2. consciousness-coherence-bridge.html        (The Bridge)
3. consciousness-chi-field-action.html        (The Action)
4. consciousness-grace-source-term.html       (The Source)
5. consciousness-reality-assessment.html      (The Verdict)
6. consciousness-scientific-convergence.html  (The Convergence)
7. consciousness-evidence-predictions.html    (The Evidence)
8. consciousness-free-will-evil.html          (The Problem)
9. consciousness-parallel-laws.html           (The Mirror)
10. consciousness-ontological-taxonomy.html   (The Map)
```

### 4C: Cross-Domain Sidebar (12 articles in `cross-domain/`)

Files are numbered 01-12. Reading order = file number order.

### 4D: Moral Decline Sidebar (14+ articles in `moral-decline/`)

Reading order:
```
1. moral-decline-01-introduction.html
2. moral-decline-02-phase-transition.html
3. moral-decline-03-semantic-collapse.html
4. moral-decline-04-cognitive-decline.html
5. moral-decline-05-spiritual-collapse.html
6. moral-decline-06-signal-went-dark.html
7. moral-decline-07-phantom-money.html
8. moral-decline-08-observer-collapsed.html
9. moral-decline-09-amish-proof.html
10. moral-decline-10-way-back.html
```
Plus hub pages (moral-decline-america.html, moral-decline-of-america.html) and extras (facts-paper, technology-entropy, timeline) — these go at the bottom of the sidebar as supplementary links.

### 4E: Blue / Research Papers Sidebar (10 articles in `blue/`)

No strict reading order. List alphabetically or by category.

### Sidebar CSS/JS to inject (if file doesn't already have it)

Check each file first — if it already has `.sidebar` CSS rules, just inject the HTML. If not, add the full block. The CSS and JS are identical to what GTQ uses:

```css
.sidebar{position:fixed;top:0;left:0;width:280px;height:100vh;background:#0a0a0a;border-right:1px solid #333;z-index:100;overflow-y:auto;transform:translateX(-100%);transition:transform .3s ease;padding:1.5rem 1rem;}
.sidebar.open{transform:translateX(0);}
.sidebar-toggle{position:fixed;top:1rem;left:1rem;z-index:101;background:#1a1a1a;border:1px solid #333;color:#d4af37;width:40px;height:40px;border-radius:.375rem;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1rem;}
.sidebar-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.6);z-index:99;}
.sidebar-overlay.show{display:block;}
.sidebar .series-title{font-family:'Oswald',sans-serif;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:#d4af37;margin-bottom:1rem;padding-bottom:.5rem;border-bottom:1px solid #333;}
.sidebar a{display:block;padding:.45rem .75rem;color:#a0a0a0;text-decoration:none;font-size:.8rem;border-radius:.3rem;transition:all .15s ease;line-height:1.4;}
.sidebar a:hover{color:#e0e0e0;background:#2a2a2a;}
.sidebar a.current{color:#d4af37;background:rgba(212,175,55,.1);font-weight:600;}
```

```javascript
function toggleSidebar(){
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('sidebarOverlay').classList.toggle('show');
}
```

---

## TASK 5: UN-ORPHAN MORAL DECLINE CHAPTERS

**12 chapters (01-10 + SAMPLE) are deployed but unreachable.**

The series hub page `moral-decline/moral-decline-america.html` exists and IS linked from the main index. But it doesn't link to the individual chapters.

**Fix:** Open `moral-decline/moral-decline-america.html` and add links to all 10 chapters. These should be in a card grid or list matching the hub's existing style.

Also add prev/next nav to each chapter file (same pattern as GTQ).

---

## TASK 6: STICKY NAV ON NON-GTQ ARTICLES

**Problem:** Most articles outside GTQ have no sticky nav bar at all.

**Check each article.** If it has no `<nav style="position:sticky...">` at the top of `<body>`, add one:

```html
<nav style="position:sticky;top:0;z-index:1000;background:#0a0a0a;border-bottom:1px solid #222;padding:.5rem 1.5rem;display:flex;align-items:center;justify-content:space-between;font-family:'Inter',sans-serif;font-size:.8rem;">
  <div style="display:flex;gap:1rem;align-items:center;">
    <a href="[PATH_TO_ROOT]index.html" style="color:#999;text-decoration:none;">← Hub</a>
    <span style="color:#333;">|</span>
    <a href="[SERIES_INDEX]" style="color:[COLOR];text-decoration:none;font-weight:500;">[Series Name]</a>
  </div>
  <div style="display:flex;gap:1rem;align-items:center;">
    <a href="[PREV]" style="color:#999;text-decoration:none;">← Prev</a>
    <a href="[NEXT]" style="color:#999;text-decoration:none;">Next →</a>
  </div>
</nav>
```

Path rules:
- Root articles: `index.html` for hub, no `../`
- Subfolder articles: `../index.html` for hub

Series colors: GTQ = `#c94040`, Convergence = `#d4af37`, Consciousness = `#2dd4bf`, Cross-domain = `#a855f7`, Moral Decline = `#ef4444`, Blue = `#4a9eff`

---

## TASK 7: WIRE TTS OUTPUT TO ARTICLES

**Do this AFTER the TTS pipeline finishes.**

### Step 1: Check OUTBOX
```
O:\999_IGNORE\TTS_Engines\TTS_Pipeline\OUTBOX\
```
Should contain MP3 files for all 69 processed articles plus the earlier GTQ/consciousness batches.

### Step 2: Upload to R2
Use Wrangler CLI or Cloudflare dashboard to upload all MP3s to the R2 bucket. Naming convention should match the article slug.

R2 bucket URL pattern: `https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio/FILENAME.mp3`

### Step 3: Add player HTML to each article
For each article that now has an MP3, inject the player dock. Place it right after the opening `<body>` tag (or after the sticky nav if present):

```html
<div style="position:fixed;bottom:0;left:0;right:0;z-index:90;background:#0a0a0a;border-top:1px solid #222;padding:.5rem 1.5rem;display:flex;align-items:center;gap:.75rem;">
  <i class="fas fa-volume-up" style="color:#d4af37;font-size:.8rem"></i>
  <span style="font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.15em;text-transform:uppercase;color:#999;">Listen</span>
  <audio controls preload="metadata" style="flex:1;height:32px;max-width:500px;">
    <source src="https://pub-5b15c954dc1642f18573a365cf6dc2c5.r2.dev/audio/SLUG.mp3" type="audio/mpeg">
  </audio>
</div>
```

---

## TASK 8: DEPLOY

After completing any batch of changes:

```bash
cd D:\GitHub\genesis-to-quantum
npx wrangler pages deploy .
```

Site: https://genesis-to-quantum.pages.dev/

---

## PRIORITY FOR THIS SESSION

```
4. Sidebars for other series    — 5 series, biggest structural win
5. Un-orphan moral decline      — 12 files, quick
6. Sticky nav on all articles   — systematic pass
7. Wire TTS (after pipeline)    — upload R2 + inject players
8. Deploy                       — push everything live
```

---

*Phase 2 of 3 | Tasks 1-3 complete | TTS processing | 5 series need sidebars | 12 orphans to rescue*
