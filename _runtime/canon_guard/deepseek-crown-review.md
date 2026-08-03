# Crown Canon Semantic Review — Triage Report

## 1. Executive Verdict

**Verdict: TRUE DRIFT CONFIRMED — HIGH PRIORITY ACTION REQUIRED**

The guard has identified **105 critical findings** that represent genuine Crown canon drift, not view-layer noise. The most serious cluster is the **C-as-tenth-factor pattern** (101 critical findings in `CROWN_OLD_MASTER_PRODUCT_WITH_C`), which directly violates the no-drift rule that `C` is the coherence operator wrapper, not a tenth product factor.

The current Crown rule is unambiguous:

```
chi(W) = C_W[ triple_integral (G*M*E*S*T*K*R*Q*F) dx dy dt ]
```

Nine factors inside the integral, `C_W` as the wrapper. Any file treating `C` as a tenth factor in the product is **true drift**, not acceptable variation.

**Priority: CRITICAL — Do not auto-fix. Requires David ratification and manual correction.**

---

## 2. Top True-Drift Findings (Ordered by Priority)

### Priority 1: C-as-Tenth-Factor (CRITICAL — 101 findings)

**Files requiring immediate attention:**

| File | Lines | Issue |
|------|-------|-------|
| `_INBOX_HARVEST_TRUTH_CARDS/03_Master-Equation-Sheets.md` | 189 | `G*M*E*S*T*K*R*Q*F*C` — C as tenth factor |
| `_INBOX_HARVEST_TRUTH_CARDS/FORMAL_SPEC.md` | 31, 87, 98 | Multiple instances of C in product |
| `_INBOX_HARVEST_TRUTH_CARDS/PROOF_PACKET.md` | 149 | C in product |
| `_runtime/canon_guard/mtl_probe/WALKTHROUGH_20260729_025004.mtl.md` | 117 | C treated as ordinary factor |
| `_runtime/framework_graph.json` | 1630 | C in factor list |
| `_vocab/master_equation_registry.json` | 75 | C as factor |
| `master-equation/01_canonical/ME-01-029-c-total-integration-measure.jsonld` | 11 | C as factor |

**Why this is true drift:** The Crown rule explicitly states `C is not a tenth factor. C is chi / coherence operator output.` These files violate this directly.

### Priority 2: Factor Count Still Ten (ERROR — 2 findings)

**File:** `_vocab/master_equation_registry.json` (lines 10, 159)

The registry declares factor count as ten with C as a factor. This contradicts the nine-factor-plus-C_W-wrapper rule. **This is a canonical registry file** — it defines the vocabulary for the entire system. If this is wrong, downstream files inherit the error.

### Priority 3: Master Equation Drift (ERROR — 134 findings)

**Files include:**
- `_INBOX_HARVEST_TRUTH_CARDS/03_Master-Equation-Sheets.md` (lines 189, 192, 233)
- `_INBOX_HARVEST_TRUTH_CARDS/PROOF_PACKET.md` (line 149)
- `_INBOX_HARVEST_TRUTH_CARDS/WALKTHROUGH.md` (line 39)

These are equations involving `chi` that differ from the Crown no-drift equation. **Semantic adjudication required** — never auto-fix. The guard is correct to flag these as errors requiring human review.

### Priority 4: Unregistered Canon (ERROR — 382 findings)

**Files include:**
- `LANE4_ATOM_LEDGER_BUILD_REPORT.md`
- `_INBOX_HARVEST_TRUTH_CARDS/00_READ_ME_FIRST.md`
- `_INBOX_HARVEST_TRUTH_CARDS/01_FORMAL_LAYER_Definition10.md`
- `_INBOX_HARVEST_TRUTH_CARDS/7Q_DOMAIN_VOCABULARY.md`
- `_INBOX_HARVEST_TRUTH_CARDS/7Q_EVIDENCE_PROTOCOL.md`

These documents claim canonical authority but are not registered in the authority manifest. **This is a governance gap** — either register them or demote their authority claims.

---

## 3. Likely False Positives or View-Layer Exceptions

### 3.1 `ATOM_STATUS_PARTIAL` (36 findings)

**Verdict: LIKELY VIEW-LAYER EXCEPTION — NOT TRUE DRIFT**

The files flagged are in `_runtime/ATOM_BLUE_SHEET_ATTACK_BATCH_2026-08-01/abc-compilation/abc-map.json`. This is a **runtime compilation artifact**, not an atom-canon file. The `partial` status here likely reflects a **view-layer or processing state**, not atom status.

**Recommendation:** Document this as view-layer status in the file header or move to a separate view-status field. Do not change atom status vocabulary for this file.

### 3.2 `LEGACY_VERIFICATION_FIELDS` (689 findings)

**Verdict: MIGRATION WARNINGS — NOT TRUE DRIFT (unless contradiction)**

These are warnings, not errors. The guard correctly identifies legacy fields (`verificationStatus`, `kernelChecked`, `challengeStatus`) that should migrate to `status + verifiedBy`. However:

- **README.md** (lines 100-102): Likely documenting legacy history — acceptable as-is
- **_vocab/context.jsonld** (lines 137, 141): This is a vocabulary definition file — may be defining the legacy fields for backward compatibility

**Recommendation:** Treat as migration backlog, not drift. Only escalate if a file uses legacy fields in a way that contradicts the current `status + verifiedBy` model.

### 3.3 `OLD_STAGE_MODEL_V11` (377 findings)

**Verdict: MIXED — MOSTLY LEGACY DOCUMENTATION**

The samples show:
- `README_AI_START_HERE.md` (line 38): **Potential true drift** — this is a current entry-point document
- `_archive/phys_network_domain_sprawl_20260729/...` files: **Clearly legacy** — these are in the archive directory

**Recommendation:** Archive files are acceptable. `README_AI_START_HERE.md` needs review — if it's a current entry point, it should reference v12 stage contracts.

### 3.4 `VERSION_MISSING` (1 finding)

**File:** `_vocab/stage_contracts.json`

**Verdict: MINOR — ADD VERSION FIELD**

The manifest says version 1.0.0 but the file declares no machine-readable version. This is a simple metadata fix, not drift.

---

## 4. Exact Files/Rules David Should Ratify Before Fixes

### 4.1 Critical Ratification Required

| File | Rule/Decision Needed |
|------|---------------------|
| `_vocab/master_equation_registry.json` | **Ratify the nine-factor + C_W wrapper rule.** Confirm factor count should be 9, not 10. This is the vocabulary source — fixing this cascades to all downstream files. |
| `master-equation/01_canonical/ME-01-029-c-total-integration-measure.jsonld` | **Ratify whether this canonical atom should be rewritten** to use `C_W[...]` wrapper form, or deprecated if it's a legacy artifact. |
| `_INBOX_HARVEST_TRUTH_CARDS/03_Master-Equation-Sheets.md` | **Ratify the corrected equation form** — should be `C_W[triple_integral(G*M*E*S*T*K*R*Q*F) dx dy dt]` |
| `_INBOX_HARVEST_TRUTH_CARDS/FORMAL_SPEC.md` | **Ratify all three instances** (lines 31, 87, 98) — confirm each should use wrapper form |
| `_INBOX_HARVEST_TRUTH_CARDS/PROOF_PACKET.md` | **Ratify line 149** — confirm wrapper form |
| `_runtime/framework_graph.json` | **Ratify line 1630** — confirm C is operator, not factor |
| `_runtime/canon_guard/mtl_probe/WALKTHROUGH_20260729_025004.mtl.md` | **Ratify line 117** — confirm wrapper form |

### 4.2 Governance Ratification

| File | Rule/Decision Needed |
|------|---------------------|
| `LANE4_ATOM_LEDGER_BUILD_REPORT.md` | **Ratify whether this is canonical** — if yes, register it; if no, remove authority claims |
| `_INBOX_HARVEST_TRUTH_CARDS/00_READ_ME_FIRST.md` | **Ratify whether inbox files can claim canonical authority** — likely should be demoted to "proposed" status |
| `_INBOX_HARVEST_TRUTH_CARDS/7Q_DOMAIN_VOCABULARY.md` | **Ratify whether this is canonical vocabulary** — if yes, register it |
| `_INBOX_HARVEST_TRUTH_CARDS/7Q_EVIDENCE_PROTOCOL.md` | **Ratify whether this is canonical protocol** — if yes, register it |

### 4.3 Status Vocabulary Ratification

| File | Rule/Decision Needed |
|------|---------------------|
| `_runtime/ATOM_BLUE_SHEET_ATTACK_BATCH_2026-08-01/abc-compilation/abc-map.json` | **Ratify that `partial` is view-layer status**, not atom status. Document this in the file header. |

---

## 5. Safe Deterministic Fixes That Could Be Added Later

These are fixes that do not require semantic adjudication and can be automated after David ratifies the rules:

### 5.1 Version Field Addition (1 finding)
```json
// _vocab/stage_contracts.json
// Add:
"version": "1.0.0"
```
**Safe because:** The manifest already declares 1.0.0. This is metadata completion, not semantic change.

### 5.2 Archive Directory Exemption (377 findings)
```json
// Canon Guard configuration
// Add rule: Files under _archive/ are exempt from OLD_STAGE_MODEL_V11 checks
```
**Safe because:** Archive files document history by definition. They should not be flagged for using old stage models.

### 5.3 Runtime Directory View-Status Exemption (36 findings)
```json
// Canon Guard configuration
// Add rule: Files under _runtime/ with "compilation" or "map" in path
// may use view-layer statuses like "partial"
```
**Safe because:** Runtime artifacts are processing states, not atom-canon statuses.

### 5.4 Legacy Field Documentation (689 findings)
```json
// Canon Guard configuration
// Add rule: Files that document legacy fields in README or vocabulary
// contexts are exempt from LEGACY_VERIFICATION_FIELDS warnings
```
**Safe because:** Documenting legacy history is not drift.

---

## 6. Things NOT to Auto-Fix

### 6.1 NEVER Auto-Fix Master Equation Drift (134 findings)
The guard explicitly states: "Semantic adjudication required; never auto-fixed." **This is correct.** Each equation must be reviewed by David to confirm the intended form.

### 6.2 NEVER Auto-Fix C-as-Tenth-Factor (101 findings)
While the rule is clear, each file may have context that matters:
- Some may be **documenting the old equation** for historical purposes
- Some may be **explaining the drift** in a teaching context
- Some may be **genuinely wrong** and need rewriting

**Requires manual review of each file's context.**

### 6.3 NEVER Auto-Fix Unregistered Canon (382 findings)
Registering a document as canonical is a **governance decision**, not a mechanical fix. David must decide:
- Which files are truly canonical
- Which should be demoted to "proposed" or "working"
- Which should be moved to archive

### 6.4 NEVER Auto-Fix Factor Count in Registry (2 findings)
The `_vocab/master_equation_registry.json` is the **source of truth** for the vocabulary. Changing factor count from 10 to 9 requires:
1. David ratifies the nine-factor rule
2. Registry is updated
3. All downstream files are checked for consistency

This is a **cascading change**, not a single-file fix.

---

## 7. Recommended Next Command or Next Review Packet

### Recommended Next Command

```bash
# Generate a focused review packet for the C-as-tenth-factor cluster
canon-guard review \
  --code CROWN_OLD_MASTER_PRODUCT_WITH_C \
  --severity critical \
  --output _runtime/canon_guard/review_packets/C_TENTH_FACTOR_REVIEW_20260801.md \
  --include-context 5 \
  --format markdown
```

### Recommended Next Review Packet

**Packet: `C_TENTH_FACTOR_REVIEW_20260801.md`**

This packet should include:
1. All 101 files with `CROWN_OLD_MASTER_PRODUCT_WITH_C` findings
2. For each file: the exact line, the equation text, and 5 lines of surrounding context
3. A decision template for David:
   - [ ] Rewrite to wrapper form
   - [ ] Document as legacy history
   - [ ] Deprecate file
   - [ ] Other: ______

### Secondary Recommendation

```bash
# After David ratifies the nine-factor rule
