"""Create a v12 bidirectional domain: 21 folders, icons, desktop.ini.
Usage: python _scripts/new_domain_v12.py <domain-name> [--demo]
"""
import os, sys, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(REPO, "_icons")

STAGES = [
    ("00_inbox_working",      "I am thinking about this"),
    ("01_middle_seed",        "Here is what we found and why it might matter"),
    ("02_claim_atoms",        "What exactly is being claimed?"),
    ("10_technical_canon",    "Most precise defensible statement"),
    ("11_technical_paradigm", "Which existing model changes?"),
    ("12_technical_synthesis","Formal structures across domains"),
    ("13_hypothesis",         "What should happen if true?"),
    ("14_evidence",           "What bears directly on the claim?"),
    ("15_falsification",      "How can this claim lose?"),
    ("16_objections",         "Strongest opposing case"),
    # 17_doctoral_paper removed - papers are composites that span domains
    # and live in /papers/, referencing claims by claimID. See papers/README.md
    ("20_everyday_canon",     "Simplest faithful statement"),
    ("21_everyday_paradigm",  "How does this change how a person sees it?"),
    ("22_lived_synthesis",    "How it meets the world people know"),
    ("23_public_evidence",    "Receipts an ordinary person can inspect"),
    ("24_application",        "What might someone do differently?"),
    ("25_worldcheck",         "Does the plain claim survive contact?"),
    ("26_audience",           "How it reaches the person who needs it"),
    ("30_real_world_verdict", "What actually happened?"),
    ("31_revision_return",    "What changes now?"),
]

BRANCH = {"0": "capture", "1": "technical", "2": "public", "3": "verdict"}

README = """# {stage}
> {question}

**Branch:** {branch}

## What belongs here
[fill]

## Exit condition
[what must be true before this stage is considered served]

## State
This folder's icon reflects its state automatically:
- gray dot  = empty
- amber dot = has content, unfinished
- green dot = complete (drop a file named `_STATUS.done`)
- red dot   = failed (drop a file named `_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
"""

def make_domain(domain, demo=False):
    domain = domain.lower().strip()
    reserved_names = {"_template_domain", "_template", "template_domain"}
    if domain in reserved_names or domain.startswith("_"):
        raise ValueError(f"Refusing reserved/system domain name: {domain}")

    root = os.path.join(REPO, domain)
    os.makedirs(root, exist_ok=True)
    for stage, question in STAGES:
        p = os.path.join(root, stage)
        os.makedirs(p, exist_ok=True)
        rp = os.path.join(p, "README.md")
        if not os.path.exists(rp):
            with open(rp, "w", encoding="utf-8") as f:
                f.write(README.format(stage=stage, question=question,
                                      branch=BRANCH[stage[0]]))
    manifest = {
        "domain": domain,
        "architecture": "v12-bidirectional",
        "entry_point": "01_middle_seed",
        "technical_status": "empty",
        "public_status": "empty",
        "verdict_status": "pending",
        "technical_next": "",
        "public_next": "",
        "stages": [s for s, _ in STAGES],
        "rule": "Public descent mandatory. Technical ascent proportional. "
                "Neither canon folder is hand-authored - both render from the atom."
    }
    with open(os.path.join(root, "_DOMAIN.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"created {domain}: {len(STAGES)} stages")
    return root

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    try:
        make_domain(sys.argv[1], "--demo" in sys.argv)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
