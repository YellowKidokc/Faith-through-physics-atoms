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
