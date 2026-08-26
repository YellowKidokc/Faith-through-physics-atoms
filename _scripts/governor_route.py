#!/usr/bin/env python3
"""GOVERNOR ROUTER v0.1 — POF 2828
Reference implementation of the meta-layer routing rule:
  resolve governors -> traverse atoms -> admit by status/grade -> stamp answer.
Proven by the manual META_LAYER_PASS_2026-07-30 (C:\\theophysics\\UNIFICATION\\00_GOVERNANCE);
this encodes that sequence. Self-tested: admitted/conditional/blocked/malformed
all fire correctly on governor_test_manifest.json.
Usage: python governor_route.py --manifest atoms.json --query "..." [--governors gov.json]
Exit 0 = routed; nonzero = configuration error. Rejections are OUTPUT, not errors.
Integration targets (existing organs, per META_LAYER_PASS routing finding #1):
  canon_guard (34) supplies drift checks -> feed as extra G02 entries
  OVERCLAIM_WARNINGS.csv (27) -> merge into G02
  coherence scorer (35) -> post-admission ranking, never admission itself
  quarantine policy (99) -> terminal status, never traversed
"""
import json, sys, argparse, datetime

DEFAULT_GOVERNORS = {
  "G01_labels": ["D","C","E","P","H","T","A","O"],
  "G02_blocked_overclaims": [
    "divine attraction is literally gravity",
    "love is gluon exchange", "logos is tachyonic",
    "repentance is beta decay", "sin literally equals heat",
    "hell is maximum entropy", "landauer proves judgment",
    "shannon entropy proves", "information theory alone proves god",
    "faith collapses the wavefunction", "prayer is quantum measurement",
    "consciousness-caused collapse", "master equation replaces",
    "absolute frame", "second law defines morality",
    "physics predicts eschatology", "landauer proves grace",
    "entanglement sends", "every law order proves",
    "complete basis", "fredholm alternative proves",
    "derived from the eigenvalue spectrum",
    "derived from a single hamiltonian", "generally covariant and replaces",
    "exit code 0 proves", "nobel prize-level verified"
  ],
  "G03_grades": {
    "structural_identity": {"propagates": True,  "admit": True},
    "structural_isomorphism": {"propagates": True,  "admit": True},
    "structural_analogy": {"propagates": False, "admit": True},
    "metaphorical": {"propagates": False, "admit": True}
  },
  "G04_trusted_statuses": ["active","verified"],
  "G04_conditional_statuses": ["conditional","open"],
  "G06_required_fields_claim": ["nodeID","claimID","label","status","kill"]
}

def load(path, default=None):
    if not path: return default
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def gate_overclaim(text, gov):
    t = (text or "").lower()
    return [b for b in gov["G02_blocked_overclaims"] if b in t]

def route(atoms, gov, query=""):
    admitted, conditional, blocked, malformed = [], [], [], []
    for a in atoms:
        body = " ".join(str(a.get(k,"")) for k in ("name","summary","body"))
        hits = gate_overclaim(body, gov)
        if hits:
            blocked.append({"nodeID": a.get("nodeID","?"), "overclaims": hits}); continue
        if a.get("nodeType") == "claim":
            missing = [f for f in gov["G06_required_fields_claim"] if not a.get(f)]
            if missing:
                malformed.append({"nodeID": a.get("nodeID","?"), "missing": missing}); continue
        lab = a.get("label")
        if lab and lab not in gov["G01_labels"]:
            malformed.append({"nodeID": a.get("nodeID","?"), "missing": [f"bad label {lab}"]}); continue
        st = a.get("status","open")
        bad_edges = [e for e in a.get("edges",[])
                     if e.get("grade") not in gov["G03_grades"]]
        if bad_edges:
            malformed.append({"nodeID": a.get("nodeID","?"),
                              "missing": ["ungraded edge(s)"]}); continue
        if st in gov["G04_trusted_statuses"]: admitted.append(a)
        elif st in gov["G04_conditional_statuses"]: conditional.append(a)
        else: blocked.append({"nodeID": a.get("nodeID","?"),
                              "overclaims": [f"status {st} not admissible"]})
    return {
        "meta": {"router": "governor_route v0.1", "query": query,
                 "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 "rule": "resolved governors before traversal; admitted != endorsed"},
        "admitted":   [a["nodeID"] for a in admitted],
        "conditional":[a["nodeID"] for a in conditional],
        "blocked": blocked, "malformed": malformed,
        "labels_present": sorted({a.get("label","?") for a in admitted}),
        "stamp": "Answers may cite ADMITTED atoms only; CONDITIONAL atoms may be "
                 "named as open work; BLOCKED content may not be reproduced."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--governors", default=None)
    p.add_argument("--query", default="")
    a = p.parse_args()
    gov = load(a.governors, DEFAULT_GOVERNORS)
    atoms = load(a.manifest)
    print(json.dumps(route(atoms, gov, a.query), indent=2))

if __name__ == "__main__":
    main()
