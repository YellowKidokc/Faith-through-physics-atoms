"""Validate every atom against the controlled vocabulary.
Any value not declared in _vocab/ is illegal. Run before commit.
Usage: python _scripts/validate_atoms.py
"""
import os, json, glob, sys
sys.stdout.reconfigure(encoding="utf-8")

REPO  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB = os.path.join(REPO, "_vocab")

V  = json.load(open(os.path.join(VOCAB, "vocab.json"), encoding="utf-8"))
DT = json.load(open(os.path.join(VOCAB, "domains_and_tags.json"), encoding="utf-8"))
CP = json.load(open(os.path.join(VOCAB, "compressions.json"), encoding="utf-8"))

# A glyph shared by several tags is legal ONLY if those tags are declared
# members of the same compression class. Otherwise it is an accidental
# collision and the signature cannot be decoded back to a single term.
def check_glyph_collisions():
    errs = []
    declared = {}
    for cid, c in CP["classes"].items():
        for m in c["members"]:
            declared[m] = (cid, c["glyph"])
    byglyph = {}
    for tag, g in DT["tags"].items():
        byglyph.setdefault(g, []).append(tag)
    for g, tags in byglyph.items():
        if len(tags) < 2:
            continue
        classes = {declared.get(t, (None,))[0] for t in tags}
        if None in classes or len(classes) > 1:
            errs.append(f"VOCAB: glyph '{g}' shared by {tags} but not all "
                        f"declared in one compression class")
    return errs


# Visually confusable glyph pairs. Not illegal across axes (slots are
# positional) but flagged so no two live in the SAME enum.
CONFUSABLE = [("⧖","⧗"), ("⊙","⊚"), ("◌","○"), ("⟲","⟳"), ("⊘","⊗"),
              ("◆","◈"), ("⊢","⊦"), ("∴","∵"), ("≅","≈"), ("⇧","⇑"),
              ("□","▢"), ("◇","◊"), ("⊡","⊟"), ("✺","✣")]

def check_enum_uniqueness():
    """Within a single enum, one glyph must mean exactly one value."""
    errs = []
    enums = {
        "status": V["status"], "nodeType": V["nodeType"],
        "evidenceType": V["evidenceType"], "verifiedBy": V["verifiedBy"],
        "audienceLevel": V["audienceLevel"],
        "paradigmRelation": V["paradigmRelation"], "edgeType": V["edgeType"],
        "domainType": DT["domainType"], "root_layer": DT["root_layer"],
    }
    for name, table in enums.items():
        seen = {}
        for val, g in table.items():
            seen.setdefault(g, []).append(val)
        for g, vals in seen.items():
            if len(vals) > 1:
                errs.append(f"VOCAB: enum '{name}' glyph '{g}' maps to "
                            f"{vals} - must be unique within an enum")
        # slot 3 mixes root_layer + domainType, so they must not collide
    both = set(DT["domainType"].values()) & set(DT["root_layer"].values())
    if both:
        errs.append(f"VOCAB: slot-3 collision between root_layer and "
                    f"domainType on {sorted(both)}")
    for name, table in enums.items():
        gl = set(table.values())
        for a, b in CONFUSABLE:
            if a in gl and b in gl:
                errs.append(f"VOCAB: enum '{name}' contains confusable pair "
                            f"'{a}' / '{b}'")
    return errs


DOMAINS = set(DT["domainType"]) | set(DT["root_layer"])
TAGS    = set(DT["tags"])
GLYPHS  = (set(V["nodeType"].values()) | set(V["status"].values())
           | set(V["evidenceType"].values()) | set(V["verifiedBy"].values())
           | set(DT["domainType"].values()) | set(DT["root_layer"].values())
           | set(DT["tags"].values())
           | set(V["edgeType"].values()) | set(V["paradigmRelation"].values())
           | set(V["audienceLevel"].values())
           | {g["glyph"] for g in V["bridgeGrade"].values()})

def check(atom, path, errs):
    def bad(field, val, allowed):
        errs.append(f"{os.path.basename(path)}: {field}='{val}' not in vocabulary")

    for field, table in (("nodeType", V["nodeType"]), ("status", V["status"]),
                         ("evidenceType", V["evidenceType"]),
                         ("audienceLevel", V["audienceLevel"]),
                         ("paradigmRelation", V["paradigmRelation"])):
        val = atom.get(field)
        if val and val not in table:
            bad(field, val, table)

    dom = atom.get("domainType")
    if dom and dom not in DOMAINS:
        bad("domainType", dom, DOMAINS)

    cc = atom.get("claimClass")
    if cc and cc not in V["claimClass"]:
        bad("claimClass", cc, V["claimClass"])

    for t in atom.get("tags", []):
        if t not in TAGS:
            bad("tags", t, TAGS)

    gl = atom.get("glyphs", [])
    if len(gl) > 5:
        errs.append(f"{os.path.basename(path)}: {len(gl)} glyphs (max 5)")
    for g in gl:
        if g not in GLYPHS:
            bad("glyphs", g, "glyph set")

    for e in atom.get("edges", []):
        et = e.get("type")
        if et and et not in V["edgeType"]:
            bad("edge.type", et, V["edgeType"])
        gr = e.get("grade")
        if gr:
            if gr not in V["bridgeGrade"]:
                bad("edge.grade", gr, V["bridgeGrade"])
            elif e.get("propagates") and not V["bridgeGrade"][gr]["propagates"]:
                errs.append(f"{os.path.basename(path)}: grade '{gr}' cannot "
                            f"propagate but propagates=true")

    if atom.get("nodeType") == "claim" and not atom.get("claimID"):
        errs.append(f"{os.path.basename(path)}: claim node missing claimID")
    if atom.get("claimID") and atom.get("nodeType") not in (None, "claim"):
        errs.append(f"{os.path.basename(path)}: non-claim node has claimID")

    # --- SELF-CONSISTENCY (added 2026-07-26) -------------------------------
    # A status claim must agree with the atom's own verification fields.
    # This needs no graph resolution - it is visible inside the single file,
    # which makes it the cheapest check in the system and the one that fires
    # even when an atom's dependencies have not been written yet.
    st = atom.get("status")
    if st == "kernel_verified" and atom.get("kernelChecked") is not True:
        errs.append(f"{os.path.basename(path)}: status='kernel_verified' but "
                    f"kernelChecked={atom.get('kernelChecked')} - the kernel "
                    f"either checked it or it did not")
    if st == "verified" and atom.get("verificationStatus") in (None, "", "informal", "none", "unverified"):
        errs.append(f"{os.path.basename(path)}: status='verified' but "
                    f"verificationStatus='{atom.get('verificationStatus')}' - "
                    f"name the verification or lower the status")

# ---------------------------------------------------------------------------
# STATUS MONOTONICITY  (added 2026-07-26)
#
# A claim's status may never exceed the weakest status it depends on.
# Restating, citing, or summarising NEVER strengthens a claim. Status rises
# only through a re-derivation event that names its own artifact.
#
# Basis: the data processing inequality. truth -> source -> restatement is a
# Markov chain, and post-processing cannot increase information about the
# source. Re-derivation is the one case that breaks the chain -- the agent
# went and looked at the thing itself -- which is why it is the only legal
# exception.
#
# The existing propagationScope table covers FAILURE travelling outward and
# descentInvariant covers CONFIDENCE travelling down to a public audience.
# This covers the third direction: STATUS travelling up from dependencies.
# ---------------------------------------------------------------------------

STATUS_RANK = {
    "captured": 0, "classified": 1, "weakened": 1, "proposed": 2,
    "active": 3, "verified": 4, "kernel_verified": 5,
}
DEAD_STATUS = {"falsified", "deprecated", "superseded"}
CEILING_EDGE = "dependsOn"


def atom_keys(atom):
    """Every identifier an edge target may legally use to reach this atom."""
    return [k for k in (atom.get("nodeID"), atom.get("@id"),
                        atom.get("claimID")) if k]


def check_status_monotonicity(atoms):
    """Second pass. atoms: list of (path, atom). Needs the whole graph."""
    errs, warns = [], []
    index = {}
    for path, atom in atoms:
        for k in atom_keys(atom):
            index[k] = (path, atom)

    for path, atom in atoms:
        name = os.path.basename(path)
        st = atom.get("status")
        if st is None or st in DEAD_STATUS:
            continue                    # dead nodes impose a ceiling, don't inherit
        my_rank = STATUS_RANK.get(st)
        if my_rank is None:
            continue                    # unknown status already reported by check()

        rd = atom.get("rederivation") or {}
        rederived = rd.get("artifact") if isinstance(rd, dict) else None

        for e in atom.get("edges", []):
            et, tgt = e.get("type"), e.get("target")
            if not tgt:
                continue
            # bridges transmit status only if the grade is allowed to propagate
            if et == "bridgesTo":
                gr = e.get("grade")
                if not (gr and V["bridgeGrade"].get(gr, {}).get("propagates")):
                    continue
            elif et != CEILING_EDGE:
                continue

            if tgt not in index:
                warns.append(f"{name}: edge target '{tgt}' not found - "
                             f"status ceiling unverifiable")
                continue

            dep = index[tgt][1]
            dep_st = dep.get("status")

            if dep_st in DEAD_STATUS:
                errs.append(f"{name}: status='{st}' but depends on '{tgt}' "
                            f"which is '{dep_st}' - dead dependency")
                continue

            dep_rank = STATUS_RANK.get(dep_st)
            if dep_rank is None:
                continue
            if my_rank > dep_rank and not rederived:
                errs.append(f"{name}: status='{st}' exceeds dependency '{tgt}' "
                            f"at '{dep_st}' - status cannot rise by citation. "
                            f"Attach rederivation.artifact or lower to '{dep_st}'")
    return errs, warns


WARN = ["tags", "keywords", "glyphs", "mathFormNormal", "audienceLevel"]

if __name__ == "__main__":
    errs, warns, n = check_glyph_collisions() + check_enum_uniqueness(), [], 0
    loaded = []
    for cid, c in CP["classes"].items():
        if c.get("grade") == "ungraded":
            warns.append(f"VOCAB: compression class '{cid}' is ungraded "
                         f"({', '.join(c['members'])}) - grade it or it cannot propagate")
    for path in glob.glob(os.path.join(REPO, "**", "*.jsonld"), recursive=True):
        if "_vocab" in path or "_protocol" in path: continue
        n += 1
        try:
            atom = json.load(open(path, encoding="utf-8"))
        except Exception as ex:
            errs.append(f"{os.path.basename(path)}: unreadable ({ex})"); continue
        check(atom, path, errs)
        loaded.append((path, atom))
        missing = [f for f in WARN if not atom.get(f)]
        if missing:
            warns.append(f"{os.path.basename(path)}: missing {', '.join(missing)}")

    mono_errs, mono_warns = check_status_monotonicity(loaded)
    errs += mono_errs
    warns += mono_warns

    print(f"validated {n} atoms")
    for e in errs:  print("  ERROR  ", e)
    for w in warns: print("  warn   ", w)
    print(f"\n{len(errs)} errors, {len(warns)} warnings")
