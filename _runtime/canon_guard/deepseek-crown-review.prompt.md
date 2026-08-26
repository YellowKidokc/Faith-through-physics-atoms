# Crown Canon Semantic Review Request

Review this deterministic Canon Guard report.

The guard is intentionally conservative. Your job is to triage, not to rewrite.

## Canon Reference

```text
# Crown Knowledge Atom No-Drift Rules

version: 0.1.0
effective_date: 2026-07-29
status: canonical reference

This is the local Canon Guard reference for the current Crown / Master Equation
drift rules.

## Current Crown Posture

The framework should speak clearly at the top and audit honestly at the bottom.

Preferred cross-domain language:

- formal cross-domain consilience
- consilient support
- structural convergence
- theological interpretation
- identity-grade structure where warranted
- not merely metaphor when the edge is structural
- not laboratory proof

## Master Equation Rule

Current Crown rule:

```text
chi(W) = C_W[ triple_integral (G*M*E*S*T*K*R*Q*F) dx dy dt ]
```

Variables:

- G = Grace
- M = Moral Alignment
- E = Truth Signal
- S = Entropy / Sin
- T = Judgment / Time
- K = Logos / Knowledge
- R = Redemption / Repair
- Q = Quantum / Faith
- F = Strong Force / Love
- W = free will gate
- C_W = coherence operator gated by W

Important no-drift rule:

```text
C is not a tenth factor. C is chi / coherence operator output.
```

If an atom, registry, article, or topbar packet treats C as an ordinary tenth
factor in the product, flag it for review.

## Status Vocabulary Rule

Atom status should map to one of:

```text
draft | proposed | active | verified | kernel_verified | weakened | falsified | deprecated | superseded
```

View-layer statuses such as `partial` must either be mapped to atom status or
documented as page/audience status, not mixed into atom status.

## Legacy Verification Fields

The newer model should prefer:

```text
status + verifiedBy
```

Legacy fields that need migration review:

- verificationStatus
- kernelChecked
- challengeStatus

```

## Deterministic Guard Summary

```json
{
  "summary": {
    "files_scanned": 1952,
    "findings": 1726,
    "critical": 105,
    "errors": 554,
    "warnings": 1067,
    "changed": 0
  },
  "counts_by_code": {
    "ATOM_STATUS_PARTIAL": 36,
    "CROWN_C_TENTH_FACTOR_LANGUAGE": 4,
    "CROWN_FACTOR_COUNT_TEN": 2,
    "CROWN_OLD_MASTER_PRODUCT_WITH_C": 101,
    "LEGACY_VERIFICATION_FIELDS": 689,
    "MASTER_EQUATION_DRIFT": 134,
    "OLD_STAGE_MODEL_V11": 377,
    "UNREGISTERED_CANON": 382,
    "VERSION_MISSING": 1
  },
  "counts_by_severity": {
    "critical": 105,
    "error": 554,
    "warning": 1067
  },
  "samples_by_code": {
    "UNREGISTERED_CANON": [
      {
        "severity": "error",
        "path": "LANE4_ATOM_LEDGER_BUILD_REPORT.md",
        "line": null,
        "message": "Document claims canonical authority but is not registered in the authority manifest.",
        "canonical_id": null
      },
      {
        "severity": "error",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/00_READ_ME_FIRST.md",
        "line": null,
        "message": "Document claims canonical authority but is not registered in the authority manifest.",
        "canonical_id": null
      },
      {
        "severity": "error",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/01_FORMAL_LAYER_Definition10.md",
        "line": null,
        "message": "Document claims canonical authority but is not registered in the authority manifest.",
        "canonical_id": null
      },
      {
        "severity": "error",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/7Q_DOMAIN_VOCABULARY.md",
        "line": null,
        "message": "Document claims canonical authority but is not registered in the authority manifest.",
        "canonical_id": null
      },
      {
        "severity": "error",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/7Q_EVIDENCE_PROTOCOL.md",
        "line": null,
        "message": "Document claims canonical authority but is not registered in the authority manifest.",
        "canonical_id": null
      }
    ],
    "LEGACY_VERIFICATION_FIELDS": [
      {
        "severity": "warning",
        "path": "README.md",
        "line": 100,
        "message": "Legacy verification field detected. Newer atom model should migrate to status + verifiedBy or explicitly document this as legacy view data.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "warning",
        "path": "README.md",
        "line": 101,
        "message": "Legacy verification field detected. Newer atom model should migrate to status + verifiedBy or explicitly document this as legacy view data.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "warning",
        "path": "README.md",
        "line": 102,
        "message": "Legacy verification field detected. Newer atom model should migrate to status + verifiedBy or explicitly document this as legacy view data.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "warning",
        "path": "_vocab/context.jsonld",
        "line": 137,
        "message": "Legacy verification field detected. Newer atom model should migrate to status + verifiedBy or explicitly document this as legacy view data.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "warning",
        "path": "_vocab/context.jsonld",
        "line": 141,
        "message": "Legacy verification field detected. Newer atom model should migrate to status + verifiedBy or explicitly document this as legacy view data.",
        "canonical_id": "stage-contracts-v12"
      }
    ],
    "OLD_STAGE_MODEL_V11": [
      {
        "severity": "warning",
        "path": "README_AI_START_HERE.md",
        "line": 38,
        "message": "Old v11/14-stage language detected. v12 stage_contracts currently defines 00_inbox_working, 01_middle_seed, and 02_claim_atoms.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "warning",
        "path": "_archive/phys_network_domain_sprawl_20260729/addiction-science/00_inbox_working/README.md",
        "line": 30,
        "message": "Old v11/14-stage language detected. v12 stage_contracts currently defines 00_inbox_working, 01_middle_seed, and 02_claim_atoms.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "warning",
        "path": "_archive/phys_network_domain_sprawl_20260729/addiction-science/01_canonical/README.md",
        "line": 37,
        "message": "Old v11/14-stage language detected. v12 stage_contracts currently defines 00_inbox_working, 01_middle_seed, and 02_claim_atoms.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "warning",
        "path": "_archive/phys_network_domain_sprawl_20260729/addiction-science/02_paradigm/README.md",
        "line": 32,
        "message": "Old v11/14-stage language detected. v12 stage_contracts currently defines 00_inbox_working, 01_middle_seed, and 02_claim_atoms.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "warning",
        "path": "_archive/phys_network_domain_sprawl_20260729/addiction-science/03_synthesis/README.md",
        "line": 35,
        "message": "Old v11/14-stage language detected. v12 stage_contracts currently defines 00_inbox_working, 01_middle_seed, and 02_claim_atoms.",
        "canonical_id": "stage-contracts-v12"
      }
    ],
    "CROWN_OLD_MASTER_PRODUCT_WITH_C": [
      {
        "severity": "critical",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/03_Master-Equation-Sheets.md",
        "line": 189,
        "message": "Possible old Master Equation product: G*M*E*S*T*K*R*Q*F*C. Current Crown rule expects G*M*E*S*T*K*R*Q*F inside C_W[...], with C not a tenth factor.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "critical",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/FORMAL_SPEC.md",
        "line": 31,
        "message": "Possible old Master Equation product: G*M*E*S*T*K*R*Q*F*C. Current Crown rule expects G*M*E*S*T*K*R*Q*F inside C_W[...], with C not a tenth factor.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "critical",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/FORMAL_SPEC.md",
        "line": 87,
        "message": "Possible old Master Equation product: G*M*E*S*T*K*R*Q*F*C. Current Crown rule expects G*M*E*S*T*K*R*Q*F inside C_W[...], with C not a tenth factor.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "critical",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/FORMAL_SPEC.md",
        "line": 98,
        "message": "Possible old Master Equation product: G*M*E*S*T*K*R*Q*F*C. Current Crown rule expects G*M*E*S*T*K*R*Q*F inside C_W[...], with C not a tenth factor.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "critical",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/PROOF_PACKET.md",
        "line": 149,
        "message": "Possible old Master Equation product: G*M*E*S*T*K*R*Q*F*C. Current Crown rule expects G*M*E*S*T*K*R*Q*F inside C_W[...], with C not a tenth factor.",
        "canonical_id": "crown-knowledge-atom"
      }
    ],
    "MASTER_EQUATION_DRIFT": [
      {
        "severity": "error",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/03_Master-Equation-Sheets.md",
        "line": 189,
        "message": "Equation involving chi differs from the Crown no-drift equation. Semantic adjudication required; never auto-fixed.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "error",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/03_Master-Equation-Sheets.md",
        "line": 192,
        "message": "Equation involving chi differs from the Crown no-drift equation. Semantic adjudication required; never auto-fixed.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "error",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/03_Master-Equation-Sheets.md",
        "line": 233,
        "message": "Equation involving chi differs from the Crown no-drift equation. Semantic adjudication required; never auto-fixed.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "error",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/PROOF_PACKET.md",
        "line": 149,
        "message": "Equation involving chi differs from the Crown no-drift equation. Semantic adjudication required; never auto-fixed.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "error",
        "path": "_INBOX_HARVEST_TRUTH_CARDS/WALKTHROUGH.md",
        "line": 39,
        "message": "Equation involving chi differs from the Crown no-drift equation. Semantic adjudication required; never auto-fixed.",
        "canonical_id": "crown-knowledge-atom"
      }
    ],
    "ATOM_STATUS_PARTIAL": [
      {
        "severity": "error",
        "path": "_runtime/ATOM_BLUE_SHEET_ATTACK_BATCH_2026-08-01/abc-compilation/abc-map.json",
        "line": 19,
        "message": "Status vocabulary drift: atom status uses 'partial'. Map it to draft/proposed/active/verified/kernel_verified/weakened/falsified/deprecated/superseded, or document it as view-layer status.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "error",
        "path": "_runtime/ATOM_BLUE_SHEET_ATTACK_BATCH_2026-08-01/abc-compilation/abc-map.json",
        "line": 34,
        "message": "Status vocabulary drift: atom status uses 'partial'. Map it to draft/proposed/active/verified/kernel_verified/weakened/falsified/deprecated/superseded, or document it as view-layer status.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "error",
        "path": "_runtime/ATOM_BLUE_SHEET_ATTACK_BATCH_2026-08-01/abc-compilation/abc-map.json",
        "line": 51,
        "message": "Status vocabulary drift: atom status uses 'partial'. Map it to draft/proposed/active/verified/kernel_verified/weakened/falsified/deprecated/superseded, or document it as view-layer status.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "error",
        "path": "_runtime/ATOM_BLUE_SHEET_ATTACK_BATCH_2026-08-01/abc-compilation/abc-map.json",
        "line": 52,
        "message": "Status vocabulary drift: atom status uses 'partial'. Map it to draft/proposed/active/verified/kernel_verified/weakened/falsified/deprecated/superseded, or document it as view-layer status.",
        "canonical_id": "stage-contracts-v12"
      },
      {
        "severity": "error",
        "path": "_runtime/ATOM_BLUE_SHEET_ATTACK_BATCH_2026-08-01/abc-compilation/abc-map.json",
        "line": 60,
        "message": "Status vocabulary drift: atom status uses 'partial'. Map it to draft/proposed/active/verified/kernel_verified/weakened/falsified/deprecated/superseded, or document it as view-layer status.",
        "canonical_id": "stage-contracts-v12"
      }
    ],
    "CROWN_C_TENTH_FACTOR_LANGUAGE": [
      {
        "severity": "critical",
        "path": "_runtime/canon_guard/mtl_probe/WALKTHROUGH_20260729_025004.mtl.md",
        "line": 117,
        "message": "Possible Crown drift: C is being treated as an ordinary tenth factor. Current Crown rule says C_W is the wrapper/operator and C is not a tenth product factor.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "critical",
        "path": "_runtime/framework_graph.json",
        "line": 1630,
        "message": "Possible Crown drift: C is being treated as an ordinary tenth factor. Current Crown rule says C_W is the wrapper/operator and C is not a tenth product factor.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "critical",
        "path": "_vocab/master_equation_registry.json",
        "line": 75,
        "message": "Possible Crown drift: C is being treated as an ordinary tenth factor. Current Crown rule says C_W is the wrapper/operator and C is not a tenth product factor.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "critical",
        "path": "master-equation/01_canonical/ME-01-029-c-total-integration-measure.jsonld",
        "line": 11,
        "message": "Possible Crown drift: C is being treated as an ordinary tenth factor. Current Crown rule says C_W is the wrapper/operator and C is not a tenth product factor.",
        "canonical_id": "crown-knowledge-atom"
      }
    ],
    "CROWN_FACTOR_COUNT_TEN": [
      {
        "severity": "error",
        "path": "_vocab/master_equation_registry.json",
        "line": 10,
        "message": "Possible Crown drift: factor count is still ten with C as a factor. Review against current nine-factor-plus-C_W-wrapper rule.",
        "canonical_id": "crown-knowledge-atom"
      },
      {
        "severity": "error",
        "path": "_vocab/master_equation_registry.json",
        "line": 159,
        "message": "Possible Crown drift: factor count is still ten with C as a factor. Review against current nine-factor-plus-C_W-wrapper rule.",
        "canonical_id": "crown-knowledge-atom"
      }
    ],
    "VERSION_MISSING": [
      {
        "severity": "warning",
        "path": "_vocab/stage_contracts.json",
        "line": null,
        "message": "Canonical document declares no machine-readable version; manifest says 1.0.0.",
        "canonical_id": "stage-contracts-v12"
      }
    ]
  }
}
```

## Required Output

Return Markdown with these sections:

1. Executive verdict
2. Top true-drift findings, ordered by priority
3. Likely false positives or view-layer exceptions
4. Exact files/rules David should ratify before fixes
5. Safe deterministic fixes that could be added later
6. Things not to auto-fix
7. Recommended next command or next review packet

Rules:

- Do not say the old equation is fixed unless the report proves it.
- Distinguish atom-canon status from page/view status.
- Treat C-as-tenth-factor drift as high priority unless the file is clearly documenting legacy history.
- Treat legacy verification fields as migration warnings unless they create contradiction.
- Keep the current Crown rule visible: chi(W) = C_W[triple_integral(G*M*E*S*T*K*R*Q*F) dx dy dt].
