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

WARN = ["tags", "keywords", "glyphs", "mathFormNormal", "audienceLevel"]

if __name__ == "__main__":
    errs, warns, n = check_glyph_collisions() + check_enum_uniqueness(), [], 0
    for cid, c in CP["classes"].items():
        if c.get("grade") == "ungraded":
            warns.append(f"VOCAB: compression class '{cid}' is ungraded "
                         f"({', '.join(c['members'])}) - grade it or it cannot propagate")
    for path in glob.glob(os.path.join(REPO, "**", "*.jsonld"), recursive=True):
        if "_vocab" in path: continue
        n += 1
        try:
            atom = json.load(open(path, encoding="utf-8"))
        except Exception as ex:
            errs.append(f"{os.path.basename(path)}: unreadable ({ex})"); continue
        check(atom, path, errs)
        missing = [f for f in WARN if not atom.get(f)]
        if missing:
            warns.append(f"{os.path.basename(path)}: missing {', '.join(missing)}")

    print(f"validated {n} atoms")
    for e in errs:  print("  ERROR  ", e)
    for w in warns: print("  warn   ", w)
    print(f"\n{len(errs)} errors, {len(warns)} warnings")
