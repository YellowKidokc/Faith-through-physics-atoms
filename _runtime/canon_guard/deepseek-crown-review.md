# Crown Canon Semantic Review — Deterministic Guard Report

## 1. Executive Verdict

**Verdict: True drift present — multiple high-severity findings require David ratification before any automated fix.**

The guard correctly identified three categories of genuine Crown drift:
- **C-as-tenth-factor** (critical, 3 files)
- **Old Master Equation product with C** (critical, 8 instances across inbox files)
- **Factor count still ten** (error, 2 instances in registry)

These are not false positives. The inbox harvest cards and runtime registry are actively using the old `G*M*E*S*T*K*R*Q*F*C` form, which directly contradicts the current Crown rule:

```
chi(W) = C_W[ triple_integral (G*M*E*S*T*K*R*Q*F) dx dy dt ]
```

The remaining findings (LEGACY_VERIFICATION_FIELDS, OLD_STAGE_MODEL_V11, UNREGISTERED_CANON, ATOM_STATUS_PARTIAL, VERSION_MISSING) are migration warnings and view-layer issues — important but not Crown-breaking.

---

## 2. Top True-Drift Findings (Ordered by Priority)

### Priority 1: C-as-Tenth-Factor (Critical — Crown-breaking)

| File | Line | Issue |
|------|------|-------|
| `_runtime/framework_graph.json` | 1630 | C treated as ordinary tenth factor |
| `_vocab/master_equation_registry.json` | 75 | C treated as ordinary tenth factor |
| `master-equation/01_canonical/ME-01-029-c-total-integration-measure.jsonld` | 11 | C treated as ordinary tenth factor |

**Impact:** These are runtime and canonical atom files. If C is treated as a product factor, the coherence operator is structurally wrong. This is not a view-layer difference — it's a mathematical structure error.

### Priority 2: Old Master Equation Product with C (Critical — inbox harvest cards)

| File | Lines |
|------|-------|
| `_INBOX_HARVEST_TRUTH_CARDS/03_Master-Equation-Sheets.md` | 189 |
| `_INBOX_HARVEST_TRUTH_CARDS/FORMAL_SPEC.md` | 31, 87, 98 |
| `_INBOX_HARVEST_TRUTH_CARDS/PROOF_PACKET.md` | 149 |
| `_INBOX_HARVEST_TRUTH_CARDS/PROOF_WALKTHROUGH.md` | 187, 196 |
| `_INBOX_HARVEST_TRUTH_CARDS/WALKTHROUGH.md` | 39 |

**Impact:** These are inbox documents, so they are pre-canonical working drafts. However, they are being used as reference material and contain the old `G*M*E*S*T*K*R*Q*F*C` form. If these are promoted to canonical without correction, drift becomes permanent.

### Priority 3: Factor Count Still Ten (Error — registry)

| File | Lines |
|------|-------|
| `_vocab/master_equation_registry.json` | 10, 159 |

**Impact:** The registry explicitly lists ten factors including C. This is the authoritative vocabulary file. If the registry says ten factors, downstream atoms will inherit the error.

### Priority 4: Master Equation Drift (Error — semantic adjudication required)

| File | Lines |
|------|-------|
| `_INBOX_HARVEST_TRUTH_CARDS/03_Master-Equation-Sheets.md` | 189, 192, 233 |
| `_INBOX_HARVEST_TRUTH_CARDS/PROOF_PACKET.md` | 149 |
| `_INBOX_HARVEST_TRUTH_CARDS/WALKTHROUGH.md` | 39, 40 |
| `_INBOX_HARVEST_TRUTH_CARDS/Why_God_Built_Physics.md` | 256, 290 |

**Impact:** These equations differ from the Crown no-drift equation. The guard correctly flagged them as requiring semantic adjudication — never auto-fix.

---

## 3. Likely False Positives or View-Layer Exceptions

### LEGACY_VERIFICATION_FIELDS (689 warnings) — Acceptable View-Layer Difference

These are migration warnings, not drift. The guard correctly identifies `verificationStatus`, `kernelChecked`, and `challengeStatus` as legacy fields. However:

- **README.md** (lines 100-102): These are documentation files documenting the old model. This is acceptable view-layer content.
- **`_vocab/context.jsonld`** (lines 137, 141): This is a vocabulary context file that may need to reference legacy fields for backward compatibility.
- **`axioms/01_canonical/AX-001-existence.jsonld`** (lines 47-49): These are canonical atoms that should be migrated, but the guard correctly flags them as warnings, not errors.

**Verdict:** False positive for drift. These are migration warnings. The guard is correct to flag them, but they are not Crown-breaking.

### OLD_STAGE_MODEL_V11 (391 warnings) — Acceptable View-Layer Difference

These are template README files and documentation that reference the old 14-stage model. The guard correctly identifies them as v11 language. However:

- Template files (`_template/00_inbox_working/README.md`, etc.) are documentation, not canonical atoms.
- `README_AI_START_HERE.md` is a guide for new contributors.

**Verdict:** False positive for drift. These are documentation files that may legitimately reference the old model for historical context. The guard is correct to flag them, but they are not Crown-breaking.

### UNREGISTERED_CANON (385 errors) — Likely False Positive

These are all in `_INBOX_HARVEST_TRUTH_CARDS/` — a directory that is explicitly an inbox/working area. The guard flags them as "claiming canonical authority but not registered." However:

- Inbox documents are pre-canonical by definition.
- The guard may be over-reading "canonical" language in these files.

**Verdict:** Likely false positive for drift. These are inbox working documents. However, if any of these files are promoted to canonical, they must be registered. The guard is correct to flag them, but they are not Crown-breaking.

### ATOM_STATUS_PARTIAL (18 errors) — Acceptable View-Layer Difference

All instances are in `TOPBAR_FILL_PACKET.cross-domain.roadmap.json`. This is a view-layer roadmap file, not an atom status file. The guard correctly identifies that `partial` is not in the atom status vocabulary, but this is a view-layer status.

**Verdict:** False positive for drift. This is a view-layer status, not an atom status. The guard is correct to flag it, but it should be documented as view-layer status.

### VERSION_MISSING (1 warning) — Acceptable View-Layer Difference

`_vocab/stage_contracts.json` has no machine-readable version. The manifest says 1.0.0. This is a minor metadata issue.

**Verdict:** False positive for drift. This is a metadata gap, not Crown drift.

---

## 4. Exact Files/Rules David Should Ratify Before Fixes

### Must Ratify (Crown-breaking — cannot fix without David)

| File | Rule | Why |
|------|------|-----|
| `_runtime/framework_graph.json` line 1630 | C-as-tenth-factor | Runtime framework — changing C structure affects all downstream operations |
| `_vocab/master_equation_registry.json` lines 10, 75, 159 | Factor count ten + C-as-tenth-factor | Registry is the authoritative vocabulary — must confirm new nine-factor-plus-C_W rule |
| `master-equation/01_canonical/ME-01-029-c-total-integration-measure.jsonld` line 11 | C-as-tenth-factor | Canonical atom — changing structure requires David's semantic approval |

### Should Ratify (Semantic adjudication required)

| File | Lines | Why |
|------|-------|-----|
| `_INBOX_HARVEST_TRUTH_CARDS/03_Master-Equation-Sheets.md` | 189, 192, 233 | Old equation form — David must confirm whether these are historical notes or intended to be updated |
| `_INBOX_HARVEST_TRUTH_CARDS/FORMAL_SPEC.md` | 31, 87, 98 | Old equation form — same question |
| `_INBOX_HARVEST_TRUTH_CARDS/PROOF_PACKET.md` | 149 | Old equation form |
| `_INBOX_HARVEST_TRUTH_CARDS/PROOF_WALKTHROUGH.md` | 187, 196 | Old equation form |
| `_INBOX_HARVEST_TRUTH_CARDS/WALKTHROUGH.md` | 39 | Old equation form |
| `_INBOX_HARVEST_TRUTH_CARDS/Why_God_Built_Physics.md` | 256, 290 | Old equation form |

---

## 5. Safe Deterministic Fixes That Could Be Added Later

These are safe to automate after David ratifies the Crown-breaking fixes above:

1. **ATOM_STATUS_PARTIAL → documented as view-layer status**
   - In `TOPBAR_FILL_PACKET.cross-domain.roadmap.json`, add a comment or field noting that `partial` is a view-layer status, not an atom status.

2. **VERSION_MISSING → add version field**
   - In `_vocab/stage_contracts.json`, add `"version": "1.0.0"` to match the manifest.

3. **LEGACY_VERIFICATION_FIELDS → migration plan**
   - Create a migration script that converts `verificationStatus` → `status`, `kernelChecked` → `verifiedBy`, `challengeStatus` → `status` with appropriate mapping.
   - This is safe because the guard says "migrate to status + verifiedBy or explicitly document this as legacy view data."

4. **OLD_STAGE_MODEL_V11 → documentation update**
   - Update template README files to reference v12 stage contracts (00_inbox_working, 01_middle_seed, 02_claim_atoms).
   - This is safe because the guard provides the correct v12 stage names.

5. **UNREGISTERED_CANON → register or document as inbox**
   - For `_INBOX_HARVEST_TRUTH_CARDS/` files, add a header noting they are inbox working documents, not canonical.
   - For `LANE4_ATOM_LEDGER_BUILD_REPORT.md`, determine if it should be registered or documented as non-canonical.

---

## 6. Things Not to Auto-Fix

| Finding | Reason |
|---------|--------|
| **C-as-tenth-factor** (3 critical) | Requires David to confirm the new nine-factor-plus-C_W rule is correct and intended |
| **Old Master Equation product with C** (24 critical) | Requires David to confirm whether inbox documents should be updated or kept as historical reference |
| **Factor count ten** (2 errors) | Requires David to confirm the registry should be updated to nine factors |
| **Master Equation drift** (14 errors) | Guard explicitly says "never auto-fixed" — semantic adjudication required |
| **Any equation in inbox harvest cards** | These are working documents — David must decide if they are historical notes or intended to be updated |

---

## 7. Recommended Next Command or Next Review Packet

### Next Command

```
crown canon review --focus crown-drift --ratify-david
```

This will:
- Present the 3 C-as-tenth-factor files to David for ratification
- Present the 24 old Master Equation product instances for semantic adjudication
- Present the 2 factor-count-ten instances for confirmation

### Next Review Packet

After David ratifies, request:

```
crown canon review --focus migration-warnings --safe-fix
```

This will:
- Apply the safe deterministic fixes (ATOM_STATUS_PARTIAL, VERSION_MISSING, LEGACY_VERIFICATION_FIELDS, OLD_STAGE_MODEL_V11, UNREGISTERED_CANON)
- Generate a migration plan for legacy verification fields
- Update template documentation to v12 stage contracts

### Additional Recommendation

Request a separate review of the inbox harvest cards:

```
crown canon review --path _INBOX_HARVEST_TRUTH_CARDS --focus crown-drift --semantic-adjudication
```

This will allow David to review each equation instance and decide whether to update or document as historical reference.
