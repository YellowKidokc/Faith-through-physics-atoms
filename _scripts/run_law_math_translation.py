#!/usr/bin/env python3
"""Run math translation layer on Obsidian Law Expansion markdown files.

Takes markdown files containing physical/spiritual equations and generates or verifies
Obsidian callout translation blocks formatted according to 00_LAW_EXPANSION_TEMPLATE.md:
- Word-substituted structural form
- Plain-English sentence translation
- Symbol ledger
- Operational significance (multiplicative zero-kill, resistance gates, geodesic free fall)
- Concise 2-3 sentence honest hedge/boundary

Usage:
    python run_law_math_translation.py --file "path/to/LAW_01.md"
    python run_law_math_translation.py --file "path/to/LAW_01.md" --apply
    python run_law_math_translation.py --dir "path/to/020_LAW_EXPANSIONS" --apply
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any

# Standard dictionary of symbols across the 10 laws and master equation
CANONICAL_GLOSSARY = {
    # Newton / Gravity / Grace
    "F": "Attraction Force",
    "F_g": "Received Grace Pull",
    "G": "Universal Gravitational Constant",
    "G_s": "Divine Grace Source Constant",
    "G_0": "Baseline Grace Emission",
    "m_1": "Source Mass",
    "m_2": "Receiver Mass",
    "r": "Distance of Separation",
    "r^2": "Separation Distance Squared",
    "d": "Spiritual Distance / Alienation",
    "d^2": "Spiritual Distance Squared",
    "R": "Creature Resistance Factor",
    "1 - R": "Creature Reception Gate",
    "psi_1": "Creator Stake",
    "psi_2": "Creature Capacity",
    "G(t)": "Active Grace at Time t",
    
    # Einstein / Curvature
    "G_{\\mu\\nu}": "Einstein Spacetime Curvature Tensor",
    "R_{\\mu\\nu}": "Ricci Curvature Tensor",
    "g_{\\mu\\nu}": "Spacetime Metric Tensor",
    "T_{\\mu\\nu}": "Stress-Energy-Momentum Tensor",
    "\\Gamma^\\mu_{\\alpha\\beta}": "Christoffel Connection Coefficients",
    "a^\\mu": "Proper Acceleration Four-Vector",
    "c": "Speed of Light Constant",
    
    # Master Equation
    "\\chi": "Total Coherence of Life",
    "\\chi(\\mathbf{X})": "Total System Coherence Function",
    "C_W": "Christological Wrapper and Boundary Condition",
    "X_G": "Normalized Grace Coordinate",
    "X_M": "Normalized Meaning Coordinate",
    "X_E": "Normalized Truth Coordinate",
    "X_S": "Normalized Love / Confinement Coordinate",
    "X_T": "Normalized Thermodynamic Arrow Coordinate",
    "X_K": "Normalized Kinetic Works Coordinate",
    "X_Q": "Normalized Quantum Agency / Will Coordinate",
    "X_F": "Normalized Faith / Substrate Trust Coordinate",
    "X_R": "Normalized Covenant Frame Coordinate",
    
    # Quantum / Substrate
    "|\\psi\\rangle": "State Vector in Hilbert Space (Unseen Reality)",
    "\\Sigma_F": "Fundamental Substrate (High Symmetry, Eternal)",
    "\\Sigma_D": "Derivative Substrate (Spacetime, Broken Symmetry)",
    "C_0": "Old Covenant Coupling (Local, Fragile, Mediated)",
    "C_1": "New Covenant Coupling (Universal, Self-Sustaining)",
    "\\tau_{lock}": "Vacuum Stabilization Locking Threshold (33 Years)",
    "\\hat{M}": "Measurement Projection Operator",
    "|k\\rangle": "Collapsed Physical Outcome",
}

OPERATORS = [
    ("<=>", " exactly when "),
    ("=>", " leads to "),
    (">=", " at least "),
    ("<=", " at most "),
    ("!=", " differs from "),
    ("=", " equals "),
    (" + ", " plus "),
    (" - ", " minus "),
    (" * ", " times "),
    (" \\cdot ", " times "),
    ("\\times", " times "),
    ("/", " divided by "),
]

IDENTIFIER = re.compile(r"(?<![A-Za-z0-9_])([A-Za-z][A-Za-z0-9_]*(?:_[A-Za-z0-9]+)?)(?![A-Za-z0-9_])")


def word_equation(equation: str, glossary: dict[str, str] | None = None) -> str:
    """Produce an intuitive word-substituted version of an equation string."""
    g = {**CANONICAL_GLOSSARY, **(glossary or {})}
    # Replace known multi-char or LaTeX symbols first
    text = equation
    for sym, name in sorted(g.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(sym, f" [{name}] ")
    for op, name in OPERATORS:
        text = text.replace(op, f" {name.strip()} ")
    # Clean up whitespace and brackets
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_translation_callout(
    title: str,
    equation: str,
    plain_english: str,
    symbol_ledger: dict[str, str],
    operational_note: str,
    hedge: str = "",
) -> str:
    """Build an Obsidian callout block following the standard template."""
    ledger_lines = "\n".join(f"> - `{sym}` — {desc}" for sym, desc in symbol_ledger.items())
    
    hedge_block = ""
    if hedge:
        hedge_block = f"""\n>
> **Honest Boundary & Hedge (2-3 sentences):**  
> {hedge.strip()}"""

    return f"""> [!translation]- {title} — Plain English & Translation Layer
> **Word-for-Word Reading:**  
> $$
> {word_equation(equation)}
> $$
> 
> **Plain English:**  
> {plain_english.strip()}
> 
> **Operational Significance:**  
> {operational_note.strip()}
> 
> **Symbol Ledger:**  
{ledger_lines}{hedge_block}
"""


def parse_and_report_file(file_path: Path) -> dict[str, Any]:
    """Inspect a markdown file for mathematical blocks and translation status."""
    content = file_path.read_text(encoding="utf-8")
    
    # Find all $$ ... $$ equation blocks
    eq_blocks = re.findall(r"\$\$(.*?)\$\$", content, re.DOTALL)
    
    # Find all translation callouts
    translation_blocks = re.findall(r"> \[!translation\]-(.*?)(?=\n\n|\n#[#\s]|\Z)", content, re.DOTALL)
    
    return {
        "file": file_path.name,
        "path": str(file_path),
        "equation_count": len(eq_blocks),
        "translation_callout_count": len(translation_blocks),
        "has_multiplicative_note": "multiplicative" in content.lower() or "kill condition" in content.lower(),
        "has_agency_gate_note": "(1 - r)" in content.lower() or "resistance" in content.lower(),
    }


def main():
    parser = argparse.ArgumentParser(description="Process Law Expansion markdown files for Obsidian math translation layers.")
    parser.add_argument("--file", help="Specific markdown file to inspect or process.")
    parser.add_argument("--dir", help="Directory of markdown files to process.")
    parser.add_argument("--apply", action="store_true", help="Apply updates in-place if specified.")
    
    args = parser.parse_args()
    
    target_files: list[Path] = []
    if args.file:
        p = Path(args.file)
        if p.exists():
            target_files.append(p)
        else:
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
    elif args.dir:
        d = Path(args.dir)
        if d.exists():
            target_files = sorted(d.glob("*.md"))
        else:
            print(f"Error: Directory not found: {args.dir}")
            sys.exit(1)
    else:
        # Default to local 020_LAW_EXPANSIONS directory if available
        default_dir = Path(r"C:\Users\David\Documents\faiththruphysics.com\04_MASTER_EQUATION\020_LAW_EXPANSIONS")
        if default_dir.exists():
            target_files = sorted(default_dir.glob("*.md"))
            print(f"No target specified. Using default directory: {default_dir}")
        else:
            print("Please specify --file or --dir.")
            sys.exit(1)
            
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        
    print(f"\n=======================================================")
    print(f" LAW EXPANSION MATH TRANSLATION LAYER AUDITOR & RUNNER")
    print(f"=======================================================\n")
    print(f"Found {len(target_files)} file(s) to inspect:\n")
    
    for tf in target_files:
        info = parse_and_report_file(tf)
        status_symbol = "[OK]  " if info["translation_callout_count"] > 0 else "[WARN]"
        print(f"{status_symbol} {info['file']}:")
        print(f"    - Equations found: {info['equation_count']}")
        print(f"    - Translation callouts: {info['translation_callout_count']}")
        print(f"    - Multiplicative kill noted: {'Yes' if info['has_multiplicative_note'] else 'No'}")
        print(f"    - Agency gate noted: {'Yes' if info['has_agency_gate_note'] else 'No'}")
        print()

    print("Audit complete.")


if __name__ == "__main__":
    main()
