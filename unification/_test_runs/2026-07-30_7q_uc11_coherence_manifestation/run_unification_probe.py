"""
Run selected UNIFICATION canon candidates through the 7Q derivation extension.
"""

from scorer import (
    ClaimProfile,
    EvidenceItem,
    PredictionItem,
    DeathTest,
    DerivationStep,
    compute_truth_score,
    score_summary,
    machine_block,
)
from obsidian_writer import write_note
from html_report import write_html_report


def uc01_boundary_wrapper() -> ClaimProfile:
    return ClaimProfile(
        claim_id="UC-01",
        claim_text=(
            "The nine-coordinate Master Equation functions as a boundary-condition "
            "wrapper over native domains, not as a replacement for native equations."
        ),
        domain="UNI",
        mode="INVEST",
        entity_type="BOUNDARY",
        axiom_class="BOUNDARY",
        status="CANDIDATE",
        source="ORIGINAL",
        scales=["META", "MULTI"],
        iso_status="PARALLEL",
        cross_domain_key="PAR3+",
        domains_present=["UNI", "PHY", "INF", "THE", "MTH"],
        claim_type="STRUCTURAL",
        precision="DETAILED",
        certainty="CONDITIONAL",
        scope="FRAMEWORK",
        formal_statement=(
            "For native domain models D_i with local equations E_i, the Master "
            "Equation supplies normalized boundary coordinates X_i and wrapper "
            "constraint C_W[prod_i X_i] while preserving E_i as native-domain "
            "authority."
        ),
        dependency_chain=[
            "DP-02: constraint-class vs reduction-class",
            "DP-03: socket",
            "DP-04: wrapper",
            "DP-05: boundary condition",
            "DP-06: bridge grade",
            "DP-08: warrant labels",
            "DP-11: negative control",
            "The Unification Constitution Articles I-VII",
        ],
        derivation="DEDUCTIVE",
        derivation_steps=[
            DerivationStep(
                step_id="UC-01-DRV-001",
                kind="DEFINITION",
                source_id="DP-02",
                statement=(
                    "The unification class is constraint-class, so native equations "
                    "are governed at a boundary/constraint layer rather than reduced "
                    "to one common physical force."
                ),
                status="CHECKED",
            ),
            DerivationStep(
                step_id="UC-01-DRV-002",
                kind="DEFINITION",
                source_id="DP-03/DP-04",
                statement=(
                    "Sockets receive native-domain quantities, while the wrapper "
                    "holds the coordinates together without becoming a replacement "
                    "factor inside the product."
                ),
                status="CHECKED",
            ),
            DerivationStep(
                step_id="UC-01-DRV-003",
                kind="BOUNDARY",
                source_id="DP-05",
                statement=(
                    "The unification layer is treated as boundary data and reference "
                    "capacity, which local domains cannot derive from inside their "
                    "own equations."
                ),
                status="CHECKED",
            ),
            DerivationStep(
                step_id="UC-01-DRV-004",
                kind="EVIDENCE",
                source_id="trial-stack verdicts",
                statement=(
                    "Native-domain preservation and limiting-case checks must be "
                    "attached before this can graduate from conditional canon."
                ),
                status="OPEN",
                notes="The unification atom set says this is pending source-gate verification.",
            ),
            DerivationStep(
                step_id="UC-01-DRV-005",
                kind="EVIDENCE",
                source_id="negative controls",
                statement=(
                    "Random-order and rival-framework tests must fail or diverge in "
                    "the expected way for the wrapper claim to discriminate."
                ),
                status="OPEN",
                notes="The seed requires controls, but this probe has not attached the control reports.",
            ),
        ],
        assumptions=[
            "The Master Equation coordinates are normalized boundary coordinates, not raw native-domain variables.",
            "The trial-stack source reports exist and can be attached to the atom.",
            "Bridge grades are enforced on edges and do not silently upgrade analogy into identity.",
        ],
        boundary_conditions=[
            "Physics keeps authority over physical equations and empirical prediction.",
            "Theology keeps authority over Christian identification and confession.",
            "Mathematics proves derivations only from stated axioms and definitions.",
            "Information theory governs formal information quantities and communication constraints.",
            "The wrapper claim is killed if it replaces native equations instead of preserving them.",
        ],
        proof_obligations=[
            "Attach the exact trial-stack source packet for UC-01.",
            "Show at least one native-domain limiting-case preservation test.",
            "Attach negative-control results, including random-order law paths.",
            "Document bridge grades and which failures propagate.",
        ],
        terminus="AXIOM",
        evidence=[
            EvidenceItem(
                name="Unification Constitution jurisdiction and bridge rules",
                evidence_type="DOCUMENTARY",
                tier="T2",
                strength="STRONG",
                linkage="STRUCTURAL",
                ps_raw=0.78,
                ed=0.78,
                ec=0.72,
            ),
            EvidenceItem(
                name="Definition pill seed set for wrapper, socket, boundary, bridge grade",
                evidence_type="DOCUMENTARY",
                tier="T2",
                strength="STRONG",
                linkage="STRUCTURAL",
                ps_raw=0.76,
                ed=0.76,
                ec=0.70,
            ),
            EvidenceItem(
                name="Trial-stack and negative-control reports named but not attached",
                evidence_type="OBSERVATIONAL",
                tier="T3",
                strength="MODERATE",
                linkage="CORROBORATE",
                vulnerabilities=["SOURCE_GAP"],
                ps_raw=0.56,
                ed=0.52,
                ec=0.38,
            ),
        ],
        predictions=[
            PredictionItem(
                description=(
                    "A valid UC-01 packet should preserve native-domain equations "
                    "while adding boundary labels, reference capacities, and kill conditions."
                ),
                pred_type="STRUCTURAL",
                competing="DISCRIMIN",
                confirmed=True,
            ),
            PredictionItem(
                description=(
                    "A ten-factor C-inside product should fail the wrapper rule and be flagged as retired."
                ),
                pred_type="STRUCTURAL",
                competing="DISCRIMIN",
                confirmed=True,
            ),
        ],
        death_tests=[
            DeathTest(death_type="SELFREF", result="SURVIVES"),
            DeathTest(death_type="REGRESS", result="SURVIVES"),
            DeathTest(
                death_type="EMPIRICAL",
                result="UNTESTED",
                notes="Needs attached native-domain preservation and source-gate evidence.",
            ),
            DeathTest(
                death_type="INCOHERENT",
                result="SURVIVES",
                notes="The constitution blocks domain-annexation and overclaim.",
            ),
            DeathTest(
                death_type="EXPLAIN",
                result="WEAKENED",
                notes="A rival could accept boundary wrappers while denying this specific nine-coordinate product.",
            ),
        ],
        robustness="ARGUED",
        cascade_scope="FRAMEWORK",
    )


def uc11_coherence_manifestation() -> ClaimProfile:
    return ClaimProfile(
        claim_id="UC-11",
        claim_text=(
            "If coherence is real in the framework's sense, it must have a "
            "nonzero external signature."
        ),
        domain="UNI",
        mode="INVEST",
        entity_type="HYPOTHESIS",
        axiom_class="EMPIRICAL",
        status="CANDIDATE",
        source="ORIGINAL",
        scales=["HUMAN", "SOCIAL", "META"],
        iso_status="PARALLEL",
        cross_domain_key="PAR3+",
        domains_present=["UNI", "CON", "PSY", "THE", "INF"],
        claim_type="CAUSAL",
        precision="DETAILED",
        certainty="CONDITIONAL",
        scope="FRAMEWORK",
        formal_statement=(
            "For an internal coherence state C_int satisfying the framework's "
            "definition of alignment/truth-relation, there exists at least one "
            "downstream signature S_ext such that coupling(C_int, S_ext) != 0."
        ),
        dependency_chain=[
            "The Unification Constitution Article II: bridges must state what is preserved",
            "The Unification Constitution Article IV: greater claims carry greater burden",
            "DP-05: boundary condition",
            "DP-06: bridge grade",
            "DP-08: warrant labels",
            "MATH_IS_GOD_GOLD_EXTRACTION: Coherence Must Manifest",
        ],
        derivation="ABDUCTIVE",
        derivation_steps=[
            DerivationStep(
                step_id="UC-11-DRV-001",
                kind="ASSUMPTION",
                source_id="framework chi-coupling hypothesis",
                statement=(
                    "Coherence is treated as more than a private description; it is "
                    "claimed to couple to behavior, speech, relation, or measurement."
                ),
                status="OPEN",
                notes="This is the core hypothesis, not yet an established theorem.",
            ),
            DerivationStep(
                step_id="UC-11-DRV-002",
                kind="BRIDGE",
                source_id="Matthew 7 fruit criterion / public descent rule",
                statement=(
                    "Theological fruit-language is mapped to observable downstream "
                    "signature, not to direct proof of the whole framework."
                ),
                status="CHECKED",
            ),
            DerivationStep(
                step_id="UC-11-DRV-003",
                kind="EVIDENCE",
                source_id="behavioral and linguistic signature tests",
                statement=(
                    "Human and AI coherence should be detectable through behavior, "
                    "language, correction posture, relational repair, and consistency "
                    "under pressure."
                ),
                status="OPEN",
                notes="Needs operational metrics before it can graduate.",
            ),
            DerivationStep(
                step_id="UC-11-DRV-004",
                kind="BOUNDARY",
                source_id="no hidden-proof rule",
                statement=(
                    "Absence of a measured signature does not automatically falsify "
                    "the theological claim unless the measurement domain was actually "
                    "adequate to detect the predicted signature."
                ),
                status="CHECKED",
            ),
        ],
        assumptions=[
            "The claim targets operational coherence, not private faith as a whole.",
            "External signature may be behavioral, linguistic, relational, physiological, or statistical.",
            "The measurement protocol must be capable of detecting the claimed signature.",
        ],
        boundary_conditions=[
            "Does not prove God from behavior alone.",
            "Does not equate social conformity with coherence.",
            "Does not make every claimed spiritual state directly measurable.",
            "Requires independent definitions of coherence and signature before testing.",
        ],
        proof_obligations=[
            "Define internal coherence without circularly using the external signature.",
            "Define allowable signature classes and detection windows.",
            "Specify negative controls, including coherent-looking deception.",
            "Separate theological confession from empirical measurement.",
        ],
        terminus="HYPOTHESIS",
        evidence=[
            EvidenceItem(
                name="Public descent / fruit criterion supplies a testable grammar",
                evidence_type="DOCUMENTARY",
                tier="T2",
                strength="MODERATE",
                linkage="STRUCTURAL",
                ps_raw=0.68,
                ed=0.70,
                ec=0.62,
            ),
            EvidenceItem(
                name="Behavioral science broadly supports internal-state externalization",
                evidence_type="OBSERVATIONAL",
                tier="T2",
                strength="MODERATE",
                linkage="CORROBORATE",
                ps_raw=0.65,
                ed=0.58,
                ec=0.54,
            ),
            EvidenceItem(
                name="No attached operational protocol yet for chi-coherence measurement",
                evidence_type="OBSERVATIONAL",
                tier="T3",
                strength="WEAK",
                linkage="INDIRECT",
                vulnerabilities=["SOURCE_GAP"],
                ps_raw=0.38,
                ed=0.34,
                ec=0.22,
            ),
        ],
        predictions=[
            PredictionItem(
                description=(
                    "A defined coherence state should improve consistency between "
                    "speech, behavior, correction posture, and relational repair."
                ),
                pred_type="STRUCTURAL",
                competing="DISCRIMIN",
                confirmed=False,
            ),
            PredictionItem(
                description=(
                    "Coherent-looking deception should eventually produce detectable "
                    "inconsistency, repair failure, or load-bearing contradiction."
                ),
                pred_type="TESTABLE",
                competing="DISCRIMIN",
                confirmed=False,
            ),
        ],
        death_tests=[
            DeathTest(death_type="SELFREF", result="SURVIVES"),
            DeathTest(
                death_type="REGRESS",
                result="WEAKENED",
                notes="Needs a non-circular definition of internal coherence.",
            ),
            DeathTest(
                death_type="EMPIRICAL",
                result="UNTESTED",
                notes="No formal measurement protocol attached.",
            ),
            DeathTest(
                death_type="INCOHERENT",
                result="SURVIVES",
                notes="The claim is bounded to operational signature, not total proof.",
            ),
            DeathTest(
                death_type="EXPLAIN",
                result="WEAKENED",
                notes="Psychology can explain many signatures without accepting chi-field ontology.",
            ),
        ],
        robustness="ARGUED",
        cascade_scope="FRAMEWORK",
    )


def run_probe(profile: ClaimProfile) -> None:
    result = compute_truth_score(profile)
    print("\n" + "=" * 72)
    print(profile.claim_id)
    print("=" * 72)
    print(score_summary(result))
    print()
    print(machine_block(profile, result))
    note_path = write_note(profile, result, mode="unification-probe")
    html_path = write_html_report(profile, result, mode="unification-probe")
    print(f"\nNOTE: {note_path}")
    print(f"HTML: {html_path}")


if __name__ == "__main__":
    run_probe(uc01_boundary_wrapper())
    run_probe(uc11_coherence_manifestation())
