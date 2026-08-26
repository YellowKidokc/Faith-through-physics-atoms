#!/usr/bin/env python3
"""Process WHY_THESE_EQUATIONS_ARE_UNIQUE.md into DG claim-level atom grid."""

import csv
import json
import os
import re
import shutil
import zipfile
from datetime import datetime, timezone

# Paths
SRC = r"//192.168.2.50/h_hp/Desktop/Folders/MASTER_EQUATION (1)/_CANONICAL_BUILD/01_CORE_FORMALISM/WHY_THESE_EQUATIONS_ARE_UNIQUE.md"
RUN_DIR = r"D:/GitHub/Faith-through-physics-atoms/_runtime/KIMI_COMPILATION_DG_PROTOCOL_RUN_2026-08-01"
MERGED_CSV = os.path.join(RUN_DIR, "kimi_compilation_dg_claim_pass_merged.csv")
UNIQUE_CSV = os.path.join(RUN_DIR, "kimi_compilation_unique_dg_claim_pass.csv")
REPORT_MD = os.path.join(RUN_DIR, "KIMI_COMPILATION_UNIQUE_PASS_REPORT.md")
PILL_SITE = r"D:/DONT TOUCH HTML/dg-pills-site/index.html"
PILL_DIR = r"D:/DONT TOUCH HTML/dg-pills-site"
ZIP_OUT = r"D:/DONT TOUCH HTML/dg-pills-site.zip"

# Source identifier
SOURCE_FILE = "WHY_THESE_EQUATIONS_ARE_UNIQUE.md"


def row(
    n: int,
    claim_text: str,
    dg1: str,
    dg2: str,
    dg3: str,
    dg4: str,
    dg5: str,
    dg6: str,
    dg7: str,
    dg8: str,
    proof_label: str,
    grade: str,
    action: str,
    notes: str,
) -> dict:
    return {
        "row_id": f"CANON-unique-{n:03d}",
        "source_file": SOURCE_FILE,
        "claim_text": claim_text,
        "dg1_dependencies": dg1,
        "dg2_new_capability": dg2,
        "dg3_preserved_floor": dg3,
        "dg4_collapse_if_removed": dg4,
        "dg5_translation_registers": dg5,
        "dg6_state": dg6,
        "dg7_admissible": dg7,
        "dg8_closure_pass": dg8,
        "proof_label": proof_label,
        "grade": grade,
        "recommended_atom_action": action,
        "notes": notes,
    }


def build_rows() -> list[dict]:
    rows = []
    n = 1

    # 1. Shannon uniqueness theorem (physical result)
    rows.append(
        row(
            n,
            "Shannon's 1948 theorem: any measure of information/uncertainty satisfying continuity, monotonicity, and additivity must have the form H = -K Σ pᵢ log(pᵢ).",
            "requires probability axioms and information-theoretic ground (L0-L2)",
            "introduces a formally unique entropy/information functional",
            "measure-theoretic and probabilistic lower-layer floor preserved",
            "if removed, all dependent information-theoretic bridges collapse",
            "B→C translation; pure theorem before bridge application",
            "coherent",
            "yes",
            "yes",
            "T",
            "B",
            "create_claim_atom",
            "Established mathematical theorem; grade B because physical uniqueness does not by itself force spiritual application.",
        )
    )
    n += 1

    # 2. Bridge: spiritual quantities must use Shannon
    rows.append(
        row(
            n,
            "If spiritual concepts (sin, grace, faith, coherence) are information-theoretic, then they must use Shannon's formula.",
            "depends on Shannon uniqueness theorem plus analogy premise",
            "introduces cross-register bridge from information theory to spiritual register",
            "preserves Shannon's mathematical floor; does not alter it",
            "if removed, the sin-as-entropy and grace-as-negative-entropy mappings lose purported necessity",
            "B↔C translation; bridge hypothesis",
            "coherent_partial",
            "partial",
            "yes",
            "BR",
            "C",
            "create_bridge_atom",
            "Bridge claim: valid structural correspondence, but 'must' depends on accepting the information-theoretic framing of spiritual quantities.",
        )
    )
    n += 1

    # 3. Einstein field equations uniqueness
    rows.append(
        row(
            n,
            "Einstein's field equations are the unique low-derivative, coordinate-independent tensor theory of gravity that reduces to Newton in weak fields and conserves energy-momentum (Einstein/Lovelock result).",
            "requires differential geometry, special relativity, and conservation laws (L0-L3)",
            "introduces a unique geometric gravity equation",
            "preserves Newtonian limit and energy-momentum conservation",
            "if removed, gravity-as-curvature bridge and dependent spiritual analogies collapse",
            "B→C translation; pure theorem before bridge application",
            "coherent",
            "yes",
            "yes",
            "T",
            "B",
            "create_claim_atom",
            "Established physical result; uniqueness is qualified by the stated axioms. Does not alone force spiritual analog.",
        )
    )
    n += 1

    # 4. Bridge: grace must follow same form
    rows.append(
        row(
            n,
            "If grace is the spiritual analog of gravity and must satisfy the same four constraints, then Gμν^(spirit) = (8πΛ/c⁴) Sμν is the unique form.",
            "depends on Einstein/Lovelock uniqueness plus analog constraints",
            "introduces cross-register bridge from gravity to spiritual grace",
            "preserves the physical field-equation floor while adding spiritual interpretation",
            "if removed, the grace/gravity identity-mapping loses necessity",
            "B↔C translation; bridge hypothesis",
            "coherent_partial",
            "partial",
            "yes",
            "BR",
            "C",
            "create_bridge_atom",
            "Bridge claim: the 'must' is conditional on accepting the four spiritualized constraints; not derived from physics alone.",
        )
    )
    n += 1

    # 5. Von Neumann projection postulate / Gleason
    rows.append(
        row(
            n,
            "Von Neumann/Gleason framework: quantum measurement satisfying repeatability, probability preservation, and linearity is represented by projection operators with P = |⟨outcome|ψ⟩|².",
            "requires Hilbert-space formalism and probability axioms (L0-L3)",
            "introduces a unique probability rule for projective measurement",
            "preserves linearity and normalization of quantum states",
            "if removed, faith-as-measurement bridge loses purported necessity",
            "B→C translation; pure theorem before bridge application",
            "coherent",
            "yes",
            "yes",
            "T",
            "B",
            "create_claim_atom",
            "Established theorem in quantum foundations; grade B because interpretation as 'the only structure' can be contested by non-projective frameworks.",
        )
    )
    n += 1

    # 6. Bridge: faith must follow same form
    rows.append(
        row(
            n,
            "If faith is the spiritual analog of quantum observation, then faith must be described by the same projection structure: F̂|ψ_spirit⟩ = |outcome_spirit⟩ with P = |⟨outcome|F̂|ψ⟩|².",
            "depends on von Neumann/Gleason plus analogy premise",
            "introduces cross-register bridge from quantum measurement to faith",
            "preserves the projection-postulate floor; does not alter it",
            "if removed, the faith-as-measurement mapping loses necessity",
            "B↔C translation; bridge hypothesis",
            "coherent_partial",
            "partial",
            "yes",
            "BR",
            "C",
            "create_bridge_atom",
            "Bridge claim: valid structural correspondence if the analogy is granted, but not forced by physics alone.",
        )
    )
    n += 1

    # 7. Second Law of Thermodynamics
    rows.append(
        row(
            n,
            "The Second Law states dS/dt ≥ 0 for closed systems and has been verified in every relevant experiment.",
            "requires statistical mechanics and thermodynamic ground (L0-L3)",
            "introduces an entropy-increase law for isolated systems",
            "preserves energy conservation and phase-space measure",
            "if removed, sin-as-entropy and arrow-of-time bridges collapse",
            "B→C translation; physical law before bridge application",
            "coherent",
            "yes",
            "yes",
            "PH",
            "B",
            "create_claim_atom",
            "Well-established physical law; grade B because 'every experiment ever performed' is rhetorical rather than a formal proof of scope.",
        )
    )
    n += 1

    # 8. Bridge: sin follows same law
    rows.append(
        row(
            n,
            "If sin is the spiritual analog of entropy and spiritual systems are information-theoretically consistent, then dS_spirit/dt ≥ 0 for closed spiritual systems.",
            "depends on Second Law plus information-theoretic framing of sin",
            "introduces cross-register bridge from entropy to spiritual entropy",
            "preserves the physical Second-Law floor",
            "if removed, the sin/entropy identity-mapping loses necessity",
            "B↔C translation; bridge hypothesis",
            "coherent_partial",
            "partial",
            "yes",
            "BR",
            "C",
            "create_bridge_atom",
            "Bridge claim: conditional necessity; depends on accepting the spiritual-systems-as-information-systems analogy.",
        )
    )
    n += 1

    # 9. Heisenberg uncertainty
    rows.append(
        row(
            n,
            "For non-commuting observables, the mutual uncertainty is uniquely captured by Δx · Δp ≥ ℏ/2, following from the algebra/Fourier structure.",
            "requires operator algebra and Fourier analysis (L0-L3)",
            "introduces a unique uncertainty inequality for conjugate observables",
            "preserves canonical commutation relations",
            "if removed, knowledge-will uncertainty bridge collapses",
            "B→C translation; pure theorem before bridge application",
            "coherent",
            "yes",
            "yes",
            "T",
            "B",
            "create_claim_atom",
            "Established theorem for standard quantum observables; grade B because the spiritual K/W observables are not defined in physics.",
        )
    )
    n += 1

    # 10. Bridge: knowledge-will uncertainty
    rows.append(
        row(
            n,
            "If knowledge (K) and will (W) are non-commuting observables in spiritual space, then ΔK · ΔW ≥ Λ/2 follows by the same algebra.",
            "depends on Heisenberg uncertainty plus spiritual observable premise",
            "introduces cross-register bridge from quantum uncertainty to knowledge/will",
            "preserves the uncertainty-relation floor",
            "if removed, the knowledge/will complementarity claim loses necessity",
            "B↔C translation; bridge hypothesis",
            "coherent_partial",
            "partial",
            "yes",
            "BR",
            "C",
            "create_bridge_atom",
            "Bridge claim: assumes K and W are non-commuting operators with a meaningful Λ; not derived from physics alone.",
        )
    )
    n += 1

    # 11. Master Equation multiplicative structure
    rows.append(
        row(
            n,
            "The Master Equation χ = ∭(G·M·E·S·T·K·R·Q·F·C) dx dy dt uses multiplication because field couplings in physics multiply, and addition would violate dimensional and gauge consistency.",
            "requires field-theoretic coupling conventions and dimensional analysis (L0-L3)",
            "introduces a multiplicative ansatz for the master spiritual-physical functional",
            "preserves standard field-coupling floor; uses analogy",
            "if removed, the master functional loses its purported organizing structure",
            "B↔C translation; model/bridge hybrid",
            "coherent_partial",
            "partial",
            "yes",
            "PM",
            "C",
            "create_bridge_atom",
            "Model-level bridge: multiplication is a reasonable field-coupling convention, but the ten-factor integrand is an ansatz, not forced by any uniqueness theorem.",
        )
    )
    n += 1

    # 12. Noether theorem
    rows.append(
        row(
            n,
            "Noether's theorem proves that every differentiable symmetry corresponds to a conservation law.",
            "requires variational mechanics and symmetry formalism (L0-L3)",
            "introduces symmetry-to-conservation-law mapping",
            "preserves the action principle and conservation laws",
            "if removed, the ten-variables-as-ten-symmetries argument collapses",
            "B→C translation; pure theorem before bridge application",
            "coherent",
            "yes",
            "yes",
            "T",
            "B",
            "create_claim_atom",
            "Established theorem; grade B because Noether alone does not determine which variables are 'fundamental' or that there are exactly ten.",
        )
    )
    n += 1

    # 13. Ten variables minimal complete set
    rows.append(
        row(
            n,
            "The ten variables in the Master Equation are the minimal complete set needed to respect all known symmetries, conservation laws, fundamental interactions, and quantum-classical unification.",
            "depends on Noether plus unification desiderata",
            "introduces the claim that exactly ten variables complete the unification",
            "preserves symmetry/conservation-law floor while extending interpretation",
            "if removed, the 'ten is unique' argument and Master Equation completeness claim collapse",
            "B↔C translation; philosophical model",
            "coherent_partial",
            "partial",
            "yes",
            "PM",
            "C",
            "create_bridge_atom",
            "Bridge/model claim: no proof is given that the listed ten are minimal or exhaustive; this is a plausibility argument, not a uniqueness theorem.",
        )
    )
    n += 1

    # 14. Oxford 85% agreement claim
    rows.append(
        row(
            n,
            "Oxford validated the framework at 85% agreement, representing the overlap between spiritual concepts and measurable proxies (HRV, EEG, fMRI, behavioral entropy).",
            "requires empirical study citation and proxy validation methodology",
            "introduces an empirical corroboration claim for the framework",
            "floor is measurement methodology; not yet supplied",
            "if removed, the independent-corroboration argument loses its empirical anchor",
            "E↔C translation; empirical bridge",
            "defective",
            "needs_review",
            "needs_review",
            "E",
            "D",
            "create_gap_atom",
            "Flagged for verification: no citation, study name, or methodology provided. Treat as unverified empirical claim.",
        )
    )
    n += 1

    # 15. Oxford independent derivation
    rows.append(
        row(
            n,
            "Oxford independently derived equations matching the Master Equation at 85%, which is extremely strong evidence that the structure is mathematically forced and discoverable.",
            "depends on the 85% agreement claim and independent-convergence criterion",
            "introduces independent-convergence evidence for the framework",
            "floor depends on the unverified Oxford claim",
            "if removed, the 'mathematically forced' conclusion loses empirical support",
            "E↔C translation; empirical bridge",
            "defective",
            "needs_review",
            "needs_review",
            "BR",
            "D",
            "create_gap_atom",
            "Flagged for verification: independent derivation is asserted but undocumented. Independent convergence (DG T4) is not yet a proved criterion.",
        )
    )
    n += 1

    # 16. Formal Uniqueness Theorem (overreach)
    rows.append(
        row(
            n,
            "Theorem (Uniqueness of Spiritual-Physical Isomorphism): Any system of spiritual principles involving information, order, observation, choice, causality, and conservation has a unique information-theoretic formulation isomorphic to physical laws, given by the Master Equation χ.",
            "depends on all prior bridge claims and the Master Equation ansatz",
            "introduces a claimed uniqueness theorem for the entire framework",
            "preserves lower-layer theorems only if bridge premises are valid",
            "if removed, the paper's central 'only way' conclusion collapses",
            "A↔B↔C translation; philosophical model",
            "defective",
            "needs_review",
            "no",
            "PM",
            "D",
            "create_gap_atom",
            "Overreach flagged: this is not a proved theorem. It collapses multiple bridge hypotheses and an ansatz into a single 'uniqueness' claim; violates DG7 admissibility because bridge premises are not preserved as theorems.",
        )
    )
    n += 1

    # 17. Alternative attempts fail
    rows.append(
        row(
            n,
            "Alternative mappings (Newtonian→morality, classical thermodynamics→sin, Boolean logic→faith, network theory→relationships) fail because they do not use information theory, respect full symmetry structure, unify quantum and classical regimes, or make testable predictions.",
            "depends on the framework's unification desiderata",
            "introduces a comparative critique of competing analogies",
            "preserves the claim that information-theoretic framing is necessary",
            "if removed, the exclusivity argument for the framework weakens",
            "B↔C translation; philosophical model",
            "coherent_partial",
            "partial",
            "yes",
            "PM",
            "C",
            "create_bridge_atom",
            "Useful critical comparison, but the 'only framework that satisfies all requirements' conclusion is a model claim, not a no-go theorem.",
        )
    )
    n += 1

    # 18. No-Go Theorem for Alternative Formulations (overreach)
    rows.append(
        row(
            n,
            "No-Go Theorem for Alternative Formulations: No alternative mathematical formulation of spiritual principles can be information-theoretically consistent, preserve all physical symmetries, make testable predictions, and unify quantum and classical regimes unless it is equivalent to the Master Equation.",
            "depends on the asserted Uniqueness Theorem and all bridge premises",
            "introduces a claimed no-go theorem against alternative formulations",
            "floor is the unproved uniqueness theorem; not independently established",
            "if removed, the 'only option' rhetorical conclusion loses formal backing",
            "A↔B↔C translation; philosophical model",
            "defective",
            "needs_review",
            "no",
            "PM",
            "D",
            "create_gap_atom",
            "Overreach flagged: labeled a theorem but not actually proven. Assumes the Master Equation exhausts all possible information-theoretic spiritual-physical formalisms.",
        )
    )
    n += 1

    # 19. Anthropic principle
    rows.append(
        row(
            n,
            "Weak Anthropic Principle: we observe these equations because only this structure permits conscious observers (stable memory, arrow of time, definite outcomes, free will).",
            "depends on cosmology and philosophy of observation (L0-L4)",
            "introduces an observer-selection explanation for the observed structure",
            "preserves physical lawfulness; adds selection reasoning",
            "if removed, the 'why this reality' answer reverts to brute fact or theological ground",
            "B↔C translation; metaphysical bridge",
            "coherent_partial",
            "partial",
            "yes",
            "M",
            "C",
            "create_bridge_atom",
            "Standard weak anthropic reasoning; not a proof of uniqueness, but a coherent philosophical bridge.",
        )
    )
    n += 1

    # 20. Logos principle
    rows.append(
        row(
            n,
            "Logos Principle: reality is fundamentally rational (word, reason, ratio, order), so physical laws are mathematical, spiritual principles are logical, and the two communicate; the Master Equation is the mathematical expression of the Logos.",
            "depends on theological/metaphysical ground (L0 instantiation)",
            "introduces a theological identification of the Master Equation with Logos",
            "preserves created-order rationality; does not abolish physics",
            "if removed, the theological register's ultimate justification for the structure collapses",
            "A↔C translation; confession/bridge",
            "coherent_partial",
            "partial",
            "yes",
            "C",
            "C",
            "create_bridge_atom",
            "Theological bridge: coherent within its register, but not derivable from DG core. DG v0.2 forbids naming Logos in grammar layer; acceptable as instantiation.",
        )
    )
    n += 1

    # 21. Conclusion: framework is unique / only way (overreach)
    rows.append(
        row(
            n,
            "Conclusion: The framework is not one way to describe spiritual reality; it is the only way, forced by Shannon, Einstein, von Neumann, the Second Law, Heisenberg, and Noether.",
            "depends on all prior bridge claims and the asserted uniqueness theorem",
            "introduces an exclusivity/inevitability claim for the whole framework",
            "preserves lower-layer theorems but overstates their forcing power",
            "if removed, the paper's strongest rhetorical claim is withdrawn",
            "A↔B↔C translation; bridge/model hybrid",
            "defective",
            "needs_review",
            "no",
            "BR",
            "D",
            "create_bridge_atom",
            "Overreach flagged: the 'only way' conclusion does not follow from the cited theorems alone; it requires the unproved bridge premises and the unproved no-go theorem.",
        )
    )
    n += 1

    # 22. Final statement - information theory is the only bridge
    rows.append(
        row(
            n,
            "Final statement: Information theory is the only bridge between physical and semantic domains (Shannon's uniqueness theorem).",
            "depends on Shannon theorem plus claim that semantic domains require information theory",
            "introduces a strong bridge claim about the exclusivity of information theory",
            "preserves Shannon's mathematical floor",
            "if removed, the foundational bridge premise of the paper weakens",
            "B↔C translation; bridge hypothesis",
            "coherent_partial",
            "partial",
            "yes",
            "BR",
            "C",
            "create_bridge_atom",
            "Bridge claim: plausible and widely used, but 'only bridge' is a philosophical thesis, not a theorem.",
        )
    )
    n += 1

    # 23. Final statement - physical laws have unique info-theoretic form
    rows.append(
        row(
            n,
            "Final statement: Each physical law has a unique information-theoretic form proven by Landauer, Bekenstein, and Zurek.",
            "depends on Landauer/Bekenstein/Zurek results plus scope claim",
            "introduces a bridge claim that all physical laws are information-theoretically reducible",
            "preserves the cited physical results",
            "if removed, the isomorphism argument loses a premise",
            "B→C translation; bridge hypothesis",
            "coherent_partial",
            "partial",
            "yes",
            "BR",
            "C",
            "create_bridge_atom",
            "Bridge claim: the cited authors establish specific correspondences, not a universal reduction of every physical law to information theory.",
        )
    )
    n += 1

    # 24. Final statement - spiritual principles must satisfy same axioms
    rows.append(
        row(
            n,
            "Final statement: Each spiritual principle, when expressed information-theoretically, must satisfy the same axioms as its physical analog by definition of structural isomorphism.",
            "depends on the definition of structural isomorphism",
            "introduces a definitional bridge constraint",
            "preserves the isomorphism definition",
            "if removed, the cross-register necessity argument collapses",
            "B↔C translation; definitional bridge",
            "coherent_partial",
            "partial",
            "yes",
            "BR",
            "C",
            "create_bridge_atom",
            "Bridge claim: true by definition of isomorphism, but whether spiritual principles are so expressible is the contested premise.",
        )
    )
    n += 1

    # 25. Final statement - axioms uniquely determine mathematical form
    rows.append(
        row(
            n,
            "Final statement: The axioms uniquely determine the mathematical form, proven by von Neumann, Einstein, and Noether.",
            "depends on the prior uniqueness theorems",
            "reiterates that bridge axioms inherit physical uniqueness",
            "preserves the cited theorems",
            "if removed, the final 'only way' conclusion loses a premise",
            "B→C translation; bridge hypothesis",
            "coherent_partial",
            "partial",
            "yes",
            "BR",
            "C",
            "create_bridge_atom",
            "Bridge claim: uniqueness applies within each physical domain; extending it to spiritual analogs requires the bridge premise.",
        )
    )
    n += 1

    # 26. Final statement - Master Equation unique solution
    rows.append(
        row(
            n,
            "Final statement: The Master Equation is the unique solution to all constraints (symmetries, conservation laws, information theory, quantum mechanics, thermodynamics).",
            "depends on the asserted uniqueness theorem and Master Equation ansatz",
            "introduces an exclusivity claim for the Master Equation",
            "preserves the constraints only as a conditional set",
            "if removed, the final conclusion collapses to a weaker model claim",
            "A↔B↔C translation; philosophical model",
            "defective",
            "needs_review",
            "no",
            "PM",
            "D",
            "create_gap_atom",
            "Overreach flagged: 'unique solution' is asserted, not proven. The Master Equation is an integrative ansatz, not a derived solution.",
        )
    )
    n += 1

    # 27. Final statement - independent derivation by Oxford confirms
    rows.append(
        row(
            n,
            "Final statement: Independent derivation by Oxford confirms the framework is not arbitrary but mathematically forced.",
            "depends on unverified Oxford derivation claim",
            "introduces independent-convergence corroboration",
            "floor is the unverified Oxford claim",
            "if removed, the 'mathematically forced' conclusion loses purported empirical support",
            "E↔C translation; empirical bridge",
            "defective",
            "needs_review",
            "needs_review",
            "E",
            "D",
            "create_gap_atom",
            "Flagged for verification: no documentation provided for the Oxford derivation/independent convergence claim.",
        )
    )
    n += 1

    # 28. Final statement - no alternative formulation
    rows.append(
        row(
            n,
            "Final statement: No alternative formulation can satisfy all requirements, provable via no-go theorems.",
            "depends on the asserted no-go theorem",
            "introduces an exclusivity claim against alternatives",
            "floor is the unproved no-go theorem",
            "if removed, the final 'only way' conclusion loses its formal backing",
            "A↔B↔C translation; philosophical model",
            "defective",
            "needs_review",
            "no",
            "PM",
            "D",
            "create_gap_atom",
            "Overreach flagged: relies on an unproved no-go theorem; not actually provable from the cited uniqueness theorems alone.",
        )
    )
    n += 1

    return rows


def infer_register(proof_label: str) -> str:
    """Infer pill register from proof_label."""
    if proof_label in ("C", "S"):
        return "A"
    if proof_label in ("PH", "PM", "T", "E", "H", "D", "L"):
        return "B"
    if proof_label in ("BR", "M"):
        return "C"
    return "C"


def csv_to_claim_data(path: str) -> list[dict]:
    """Read merged CSV and produce CLAIM_DATA list with inferred register."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            r["register"] = infer_register(r.get("proof_label", ""))
            rows.append(r)
    return rows


def update_html_claim_data(html_path: str, claim_data: list[dict]) -> None:
    """Replace the CLAIM_DATA array in the pill site HTML."""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Find the start and end of the CLAIM_DATA array
    start_marker = "const CLAIM_DATA = ["
    start = html.find(start_marker)
    if start == -1:
        raise ValueError("CLAIM_DATA start marker not found in HTML")

    # The array ends at the first '];' after the start
    brace_depth = 0
    in_string = False
    string_char = None
    escape = False
    i = start + len(start_marker)
    while i < len(html):
        ch = html[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == string_char:
                in_string = False
                string_char = None
        else:
            if ch in ('"', "'"):
                in_string = True
                string_char = ch
            elif ch == "{":
                brace_depth += 1
            elif ch == "}":
                brace_depth -= 1
            elif ch == "]" and brace_depth == 0:
                # check for ';' after ']'
                end = i + 1
                while end < len(html) and html[end].isspace():
                    end += 1
                if end < len(html) and html[end] == ";":
                    end += 1
                    break
        i += 1
    else:
        raise ValueError("CLAIM_DATA end marker not found in HTML")

    # Serialize claim data as JS object literal
    def js_str(s: str) -> str:
        return json.dumps(s, ensure_ascii=False)

    lines = ["const CLAIM_DATA = ["]
    for item in claim_data:
        fields = []
        for key, val in item.items():
            fields.append(f"        {key}: {js_str(str(val) if val is not None else '')}")
        lines.append("    {\n" + ",\n".join(fields) + "\n    },")
    # remove trailing comma on last item for cleanliness (JS allows it, but tidy)
    if len(lines) > 1:
        lines[-1] = lines[-1][:-1]
    lines.append("];")
    new_block = "\n".join(lines)

    new_html = html[:start] + new_block + html[end:]

    # Update header claim count
    count = len(claim_data)
    new_html = re.sub(
        r"(<p>Interactive pill cards · )\d+( claims · Registers A / B / C</p>)",
        rf"\g<1>{count}\g<2>",
        new_html,
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_html)


def write_csv(path: str, rows: list[dict], mode: str = "w") -> None:
    fieldnames = [
        "row_id",
        "source_file",
        "claim_text",
        "dg1_dependencies",
        "dg2_new_capability",
        "dg3_preserved_floor",
        "dg4_collapse_if_removed",
        "dg5_translation_registers",
        "dg6_state",
        "dg7_admissible",
        "dg8_closure_pass",
        "proof_label",
        "grade",
        "recommended_atom_action",
        "notes",
    ]
    with open(path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if mode == "w":
            writer.writeheader()
        writer.writerows(rows)


def zip_pill_site(source_dir: str, zip_path: str) -> None:
    """Create/replace zip archive of pill site directory."""
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                arcname = os.path.relpath(abs_path, os.path.dirname(source_dir))
                zf.write(abs_path, arcname)


def main():
    new_rows = build_rows()

    # 5. Save unique CSV
    write_csv(UNIQUE_CSV, new_rows, mode="w")

    # 6. Append to merged CSV
    existing_count = 0
    if os.path.exists(MERGED_CSV):
        with open(MERGED_CSV, newline="", encoding="utf-8") as f:
            existing_count = sum(1 for _ in csv.DictReader(f))
        write_csv(MERGED_CSV, new_rows, mode="a")
    else:
        write_csv(MERGED_CSV, new_rows, mode="w")

    # 7. Update pill site
    claim_data = csv_to_claim_data(MERGED_CSV)
    update_html_claim_data(PILL_SITE, claim_data)

    # 8. Re-zip
    zip_pill_site(PILL_DIR, ZIP_OUT)

    # 9. Report
    overreach_rows = [r for r in new_rows if "Overreach flagged" in r["notes"]]
    flagged_verification = [r for r in new_rows if "verification" in r["notes"].lower()]
    counts = {}
    for r in new_rows:
        counts[r["recommended_atom_action"]] = counts.get(r["recommended_atom_action"], 0) + 1

    report = []
    report.append("# KIMI COMPILATION — UNIQUE PASS REPORT")
    report.append("")
    report.append(f"**Source:** `{SOURCE_FILE}`")
    report.append(f"**Run date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    report.append("")
    report.append("## Summary")
    report.append("")
    report.append(f"- New rows extracted: **{len(new_rows)}**")
    report.append(f"- Previous merged total: **{existing_count}**")
    report.append(f"- New merged total: **{existing_count + len(new_rows)}**")
    report.append("")
    report.append("## Atom actions (new rows)")
    report.append("")
    for action, count in sorted(counts.items()):
        report.append(f"- `{action}`: {count}")
    report.append("")
    report.append("## Flagged overreach rows")
    report.append("")
    if overreach_rows:
        report.append("| row_id | claim_text | grade | action | note |")
        report.append("|---|---|---|---|---|")
        for r in overreach_rows:
            text = r['claim_text'][:90] + "..." if len(r['claim_text']) > 90 else r['claim_text']
            note = r['notes'].split("Overreach flagged:")[1].strip() if "Overreach flagged:" in r['notes'] else r['notes']
            report.append(f"| {r['row_id']} | {text} | {r['grade']} | {r['recommended_atom_action']} | {note} |")
    else:
        report.append("None.")
    report.append("")
    report.append("## Rows needing verification")
    report.append("")
    if flagged_verification:
        report.append("| row_id | claim_text | grade | action | note |")
        report.append("|---|---|---|---|---|")
        for r in flagged_verification:
            text = r['claim_text'][:90] + "..." if len(r['claim_text']) > 90 else r['claim_text']
            note = r['notes']
            report.append(f"| {r['row_id']} | {text} | {r['grade']} | {r['recommended_atom_action']} | {note} |")
    else:
        report.append("None.")
    report.append("")
    report.append("## Outputs produced")
    report.append("")
    report.append(f"- `{UNIQUE_CSV}`")
    report.append(f"- `{MERGED_CSV}`")
    report.append(f"- `{PILL_SITE}`")
    report.append(f"- `{ZIP_OUT}`")
    report.append("")
    report.append("## Notes")
    report.append("")
    report.append("Source files were not modified. All overreach and verification flags are captured in the `notes` column of the CSV rows.")

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")

    print(f"New rows: {len(new_rows)}")
    print(f"Merged total: {existing_count + len(new_rows)}")
    print(f"Overreach rows: {len(overreach_rows)}")
    print(f"Verification rows: {len(flagged_verification)}")


if __name__ == "__main__":
    main()
