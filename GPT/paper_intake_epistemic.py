"""Three-call epistemic paper intake reference implementation.

Purpose
-------
Turn an incoming paper into a structured epistemic record without letting the
LLM become an automatic partisan reviewer. The system deliberately separates:

    CALL 1: lossless reconstruction
    CALL 2: rigorous evaluation
    CALL 3: adversarial synthesis + scoring

Core rule:
    Understand before classifying.
    Reconstruct before criticizing.
    Test before concluding.
    Never claim more or less than the evidence warrants.

This file is provider-agnostic. Plug `run_three_call_intake()` into whatever
API client the surrounding pipeline already uses.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Callable, Dict, List, Any
import json


EVALUATION_CATEGORIES: Dict[str, List[str]] = {
    "logical_validity": [
        "conclusion follows from stated premises",
        "no equivocation",
        "no illicit converse",
        "no circular dependency",
        "no suppressed premise",
        "quantifiers preserved",
        "necessity not upgraded from possibility",
        "sufficient is not confused with necessary",
        "correlation is not confused with causation",
        "analogy is not confused with identity",
        "existence is not inferred from notation",
        "scope is preserved",
        "modal operators are preserved",
        "no contradictory premises",
        "inference rule is identifiable",
        "countermodel attempted where applicable",
        "premise ablation attempted where applicable",
        "conclusion survives strongest charitable reconstruction",
    ],
    "internal_coherence": [
        "definitions remain stable across the paper",
        "claims do not mutually contradict",
        "local conclusions fit the global thesis",
        "dependencies do not form hidden cycles",
        "terminology is used consistently",
        "examples instantiate rather than replace the argument",
        "later sections do not silently revise earlier premises",
        "exceptions are acknowledged rather than ignored",
        "the same object keeps the same identity conditions",
        "cross-section assumptions are compatible",
        "causal direction is stable",
        "temporal ordering is stable",
        "levels of explanation are not collapsed",
        "formal and prose statements agree",
        "summary claims match body claims",
        "conclusion strength matches argument strength",
        "apparent tensions are resolved explicitly",
        "the reconstructed model has a consistent interpretation",
    ],
    "definition_precision": [
        "central terms are explicitly defined",
        "definitions are non-circular",
        "definitions are operational where measurement is claimed",
        "necessary and sufficient conditions are distinguished",
        "identity conditions are stated where relevant",
        "boundary conditions are stated",
        "terms do not shift between technical and ordinary meanings",
        "mathematical symbols have declared semantics",
        "domain-specific terms follow their domain usage or declare deviations",
        "loaded terms are decomposed before inference",
        "comparative terms have a reference standard",
        "categories are mutually distinguishable where required",
        "definitions permit counterexamples",
        "definitions preserve author intent without strengthening it",
        "bridge terms are defined on both sides of the bridge",
        "abstract terms have concrete test implications where claimed",
        "scope of each definition is explicit",
        "undefined primitives are identified as primitives",
    ],
    "evidence_adequacy": [
        "central claims have identified support",
        "source quality matches claim strength",
        "primary evidence is distinguished from interpretation",
        "formal proof is distinguished from empirical evidence",
        "sample size is adequate where statistical claims are made",
        "measurements are reproducible in principle",
        "citations actually support the attached proposition",
        "evidence is not cherry-picked against an obvious base rate",
        "negative evidence is considered",
        "uncertainty is reported",
        "causal claims have causal evidence",
        "historical claims have historical sources",
        "empirical claims have empirical support",
        "formal claims have formal receipts where claimed",
        "evidence chain has no missing critical link",
        "alternative interpretations of the same evidence are considered",
        "extraordinary claim strength is matched by support strength",
        "unsupported assertions are clearly labeled",
    ],
    "explanatory_compression": [
        "explains multiple observations with shared structure",
        "uses few independent primitive commitments",
        "requires few special exceptions",
        "requires few ad hoc parameters",
        "does not duplicate explanatory entities unnecessarily",
        "compresses without deleting relevant distinctions",
        "simpler account is preferred when explanatory coverage is equal",
        "extra complexity earns credit only for extra explanatory work",
        "model generalizes beyond the motivating example",
        "same mechanism explains multiple cases",
        "explanatory vocabulary is smaller than the phenomenon list",
        "hidden complexity is counted rather than ignored",
        "bridge assumptions are included in complexity cost",
        "unexplained primitives are counted",
        "rival model complexity is compared symmetrically",
        "compression does not rely on ambiguous words doing multiple jobs",
        "exceptions do not dominate the rule",
        "minimum sufficient account is identified",
    ],
    "rival_discrimination": [
        "serious nearby alternatives are named",
        "rivals receive charitable formulations",
        "same evidential standard is applied to rivals",
        "paper identifies observations that distinguish models",
        "rival can win if it explains the data better",
        "straw-man alternatives are rejected",
        "null model is considered",
        "chance/coincidence explanation is tested where relevant",
        "reverse-causal explanation is tested where relevant",
        "semantic relabeling is tested as a false positive",
        "alternative parameterizations are tested",
        "alternative ontologies are distinguished from alternative notation",
        "model-selection criteria are explicit",
        "rivals are compared on total explanatory debt",
        "disconfirming rival evidence is acknowledged",
        "underdetermination is reported when present",
        "unique predictions are identified",
        "winning conclusion is no stronger than discrimination achieved",
    ],
    "testability_falsifiability": [
        "central thesis exposes a possible failure condition",
        "kill condition is specific",
        "test result could in principle change the conclusion",
        "observables are operationalized",
        "predictions are temporally or logically prior to the test where possible",
        "negative controls are specified",
        "positive controls are specified where applicable",
        "edge cases are testable",
        "replication path is available",
        "formal claims can be rerun",
        "empirical claims can be independently checked",
        "failure is not redefined as confirmation",
        "test is capable of distinguishing the principal rival",
        "thresholds are specified where quantitative",
        "unknown outcomes are allowed",
        "unfalsifiable theological or metaphysical claims are labeled as such",
        "proxy measurements are distinguished from target constructs",
        "test coverage reaches the load-bearing claim",
    ],
    "cross_domain_integrity": [
        "formal proof does not masquerade as empirical confirmation",
        "empirical observation does not masquerade as deductive proof",
        "theological premise is labeled theological",
        "philosophical inference is labeled philosophical",
        "historical claim is kept in historical register",
        "analogy is not silently upgraded to isomorphism",
        "structural isomorphism is not silently upgraded to ontological identity",
        "mathematical model fidelity is separately audited",
        "domain-specific meanings are preserved",
        "bridge claims explicitly name source and target domains",
        "bridge strength is stated",
        "interpretation boundary is stated",
        "cross-domain mappings preserve relevant relations",
        "lost structure is recorded",
        "extra structure is recorded",
        "rival mappings are tested",
        "domain experts could inspect each side independently",
        "conclusion remains valid when rhetoric is removed",
    ],
    "adversarial_robustness": [
        "strongest objection is attempted",
        "counterexample search is attempted",
        "countermodel search is attempted",
        "premise ablation is attempted",
        "guard removal is attempted",
        "role permutation is attempted where structural roles matter",
        "relabel-only false positive is attempted",
        "weaker implementation is distinguished from stronger implementation",
        "duplicate theorem names do not substitute for source identity",
        "alternative definitions are stress-tested",
        "edge cases are stress-tested",
        "hostile but logically fair reading is attempted",
        "best rival is allowed full strength",
        "failure points are preserved in output",
        "model does not repair itself by adding ad hoc premises mid-test",
        "adversarial result is independently traceable",
        "load-bearing assumptions are identified",
        "surviving claim is restated after attack without inflation",
    ],
    "epistemic_calibration": [
        "proved is distinguished from supported",
        "supported is distinguished from plausible",
        "plausible is distinguished from speculative",
        "unknown is allowed",
        "confidence tracks available evidence",
        "coverage is reported separately from score",
        "interpretive judgments are labeled",
        "premises are not treated as conclusions",
        "machine verification scope is stated exactly",
        "absence of evidence is not automatically evidence of absence",
        "positive evidence is not treated as exclusivity without rival tests",
        "probability language is numerically justified where used",
        "certainty language is reserved for warranted cases",
        "author claims are not strengthened by the evaluator",
        "author claims are not weakened before reconstruction",
        "open questions remain open",
        "known source limitations propagate into the verdict",
        "final recommendation states what would change it",
    ],
}


GLOBAL_GATES = [
    "unresolved contradiction",
    "unknown or mismatched source",
    "critical hidden premise",
    "failed formal receipt",
    "untested central empirical claim",
    "unresolved category error",
    "fatal counterexample",
    "source/version collision",
]


SYSTEM_PRINCIPLE = """
You are an epistemic instrument, not an automatic reviewer and not an advocate.
Your task is not to agree or disagree with the author. Preserve the argument
exactly, separate its epistemic modes, determine what follows from what, and
locate the minimum structure sufficient to explain the source. Never strengthen
or weaken a claim before reconstructing it. Prefer simpler sufficient
explanations over additional invented machinery, but never sacrifice explanatory
adequacy merely for simplicity. A claim should score highly because it survives
many different ways of being wrong, not because one evaluator found many ways to
describe why it seems right.
""".strip()


CALL_1_PROMPT = SYSTEM_PRINCIPLE + """

CALL 1 — LOSSLESS RECONSTRUCTION
Do not score or adjudicate the paper. Extract what is actually present.
Return strict JSON with:
- source_integrity
- definitions
- atomic_claims
- premises
- conclusions
- equations
- observations
- cited_evidence
- formal_results
- empirical_claims
- historical_claims
- philosophical_claims
- theological_claims
- bridge_claims
- analogies
- predictions
- falsifiers
- explicit_uncertainties
- dependencies
- argument_edges
- interpretation_boundaries
Assign stable local IDs (D001, P001, C001, E001, F001, B001, K001...).
Use the strongest charitable formulation that does NOT strengthen the author.
If the source is empty, truncated, corrupted, or ambiguous, stop semantic
inference at that boundary and report it.
"""


CALL_2_PROMPT = SYSTEM_PRINCIPLE + """

CALL 2 — STRUCTURAL EVALUATION
Use ONLY the reconstructed record from Call 1 as the object of evaluation.
Do not replace it with your preferred version of the argument.
For each load-bearing conclusion:
1. list its required premises and definitions;
2. identify the inference type;
3. test hidden premises;
4. test modal validity and scope preservation;
5. distinguish formal, mathematical, empirical, historical, philosophical,
   theological, bridge, analogy, and conjectural content;
6. test internal coherence and evidence adequacy;
7. search for a simpler sufficient account;
8. compare serious rival explanations symmetrically;
9. identify explicit counterexamples, countermodels, falsifiers, or ablations;
10. return VALID, CONDITIONAL, GAP, CONTRADICTED, or UNRESOLVED per claim.
Return strict JSON. Do NOT produce the final overall score yet.
"""


CALL_3_PROMPT_TEMPLATE = SYSTEM_PRINCIPLE + """

CALL 3 — ADVERSARIAL SYNTHESIS AND SATURATING SCORE
Attempt to break the strongest charitable reconstruction from Calls 1 and 2.
Do not attack a stronger claim than the author made.

Score the following ten dimensions from 0 to 10:
{categories}

Each dimension contains multiple independent probes. Award at most 1 evidence
point per satisfied probe. The reported category score SATURATES at 10 even when
more than 10 probes succeed:

    category_score = min(10, earned_probe_points)

Also return probe_coverage and confidence separately. Do not subtract points
artificially merely to avoid high scores. A score of 10 means the category has
at least ten independent positive checks; it does NOT mean omniscience.

Apply global gates. A perfect overall result cannot be reported while any of
these load-bearing conditions remains unresolved:
{gates}

Return strict JSON containing:
- adversarial_attacks
- load_bearing_assumptions
- what_survives
- what_fails
- what_remains_conditional
- what_remains_unresolved
- simplest_sufficient_account
- category_scores (score, earned_probes, total_probes, coverage, confidence,
  satisfied_probes, failed_probes, unknown_probes)
- global_gates
- raw_score_out_of_100
- final_score_out_of_100
- score_explanation
- canonical_recommendation
- what_would_change_the_verdict

The final recommendation must never claim more or less than the evidence warrants.
"""


@dataclass
class IntakeResult:
    call_1: Dict[str, Any]
    call_2: Dict[str, Any]
    call_3: Dict[str, Any]

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, ensure_ascii=False)


def _category_block() -> str:
    lines: List[str] = []
    for name, probes in EVALUATION_CATEGORIES.items():
        lines.append(f"\n{name.upper()} ({len(probes)} probes)")
        for i, probe in enumerate(probes, 1):
            lines.append(f"  {i:02d}. {probe}")
    return "\n".join(lines)


def build_call_3_prompt() -> str:
    return CALL_3_PROMPT_TEMPLATE.format(
        categories=_category_block(),
        gates="\n".join(f"- {g}" for g in GLOBAL_GATES),
    )


def _parse_json_response(text: str) -> Dict[str, Any]:
    """Parse model JSON while failing loudly instead of silently repairing it."""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model returned invalid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("Model response must be a JSON object.")
    return parsed


def run_three_call_intake(
    source_text: str,
    call_model: Callable[[str, str], str],
) -> IntakeResult:
    """Run the three-call intake.

    `call_model(system_or_instruction, payload) -> str` is deliberately generic.
    Wrap OpenAI, Anthropic, DeepSeek, Gemini, a local model, or a router behind
    that two-string interface.
    """
    if not source_text or not source_text.strip():
        raise ValueError("Source is empty; preserve it as an integrity record, do not semantically score it.")

    raw_1 = call_model(CALL_1_PROMPT, source_text)
    call_1 = _parse_json_response(raw_1)

    raw_2 = call_model(
        CALL_2_PROMPT,
        json.dumps(call_1, ensure_ascii=False),
    )
    call_2 = _parse_json_response(raw_2)

    synthesis_payload = {
        "reconstruction": call_1,
        "evaluation": call_2,
    }
    raw_3 = call_model(
        build_call_3_prompt(),
        json.dumps(synthesis_payload, ensure_ascii=False),
    )
    call_3 = _parse_json_response(raw_3)

    return IntakeResult(call_1=call_1, call_2=call_2, call_3=call_3)


def explanatory_compression_index(
    independent_phenomena_explained: float,
    primitive_commitments: float,
    special_exceptions: float,
    unsupported_bridges: float,
) -> float:
    """Structural economy metric; never interpret this as truth probability."""
    denominator = (
        1.0
        + primitive_commitments
        + special_exceptions
        + unsupported_bridges
    )
    return independent_phenomena_explained / denominator


if __name__ == "__main__":
    print("Three-call epistemic intake module loaded.")
    print("Categories:", len(EVALUATION_CATEGORIES))
    print("Total scoring probes:", sum(map(len, EVALUATION_CATEGORIES.values())))
    print("Use run_three_call_intake(source_text, call_model) from your pipeline.")
