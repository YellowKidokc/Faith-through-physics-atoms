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
    errs, warns, n = [], [], 0
    for path in glob.glob(os.path.join(REPO, "**", "*.jsonld"), recursive=True):
        if "_vocab" in path or "_protocol" in path: continue
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
