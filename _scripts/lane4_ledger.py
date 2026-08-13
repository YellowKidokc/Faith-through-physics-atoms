#!/usr/bin/env python3
"""Deterministic, append-only Lane 4 claim ledger (standard library only)."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "_ledger"
ATOMS = LEDGER / "atoms"
FIELDS = ("atom_id atom_uid atom_uuid event_uuid claim_title claim_class lane event_type result proof_label "
          "current_status rerun_status artifact_path source_path new_path reviewer "
          "timestamp meaning limits").split()
LABELS = {
    "LEAN_FORMAL_PROOF", "LEAN_CONDITIONAL_PROOF", "LEAN_GUARDRAIL_SUPPORTED",
    "PYTHON_RUNTIME_SUPPORTED", "COLAB_REPRODUCIBLE", "SYMBOLIC_SUPPORTED",
    "HISTORICALLY_SUPPORTED", "ABDUCTIVELY_FAVORED", "BRIDGE_DECLARED",
    "ISOMORPHIC_EVENT_CANDIDATE", "COUNTERMODEL_FOUND", "NOT_ESTABLISHED",
    "RERUN_OWED", "QUARANTINE", "NARRATIVE_ANCHOR",
}
V3 = "X=(G,M,E,S,T,K,Q,R,F); chi(X)=C_W[prod_i X_i]; dX/dt = W(X,t) grad chi(X)+eta(X,t)"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    raw = value if isinstance(value, bytes) else canonical(value).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def event_digest(event):
    stable = {k: v for k, v in event.items() if k not in {"event_uuid", "event_id"}}
    return digest(stable)


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "untitled"


def atom_identity(atom):
    title = atom["title"]
    source_id = atom.get("source_claim_id")
    stem = slug(source_id or title)
    atom_id = f"tp:lane4/{slug(atom['domain'])}/{stem}"
    identity = {k: atom.get(k) for k in ("domain", "lane", "source_claim_id", "title", "claim")}
    return atom_id, digest(identity)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atom_path(atom_id):
    return ATOMS / (slug(atom_id) + ".json")


def load_atoms():
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(ATOMS.glob("*.json"))]


def get_atom(atom_id):
    matches = [a for a in load_atoms() if a["atom_id"] == atom_id or a["atom_uid"] == atom_id]
    if len(matches) != 1:
        raise SystemExit(f"atom not found or ambiguous: {atom_id}")
    return matches[0]


def save(atom):
    ATOMS.mkdir(parents=True, exist_ok=True)
    atom_path(atom["atom_id"]).write_text(json.dumps(atom, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(atom, event):
    event = {k: v for k, v in event.items() if v not in (None, "")}
    event.setdefault("timestamp", now())
    event.setdefault("lane", atom["lane"])
    event.setdefault("event_uuid", str(uuid.uuid4()))
    event["event_id"] = event_digest(event)
    if any(e["event_id"] == event["event_id"] for e in atom["ledger"]):
        raise SystemExit("duplicate event refused")
    atom["ledger"].append(event)
    save(atom)


def normalize_atom(data, source=None):
    title = data.get("title") or data.get("name") or (source.stem.replace("_", " ") if source else "Untitled")
    claim = data.get("claim") or data.get("statementTechnical") or data.get("statementPlain")
    if not claim:
        raise SystemExit("ingest requires a claim (claim, statementTechnical, or statementPlain)")
    atom = {
        "atom_id": "", "atom_uid": "", "atom_uuid": data.get("atom_uuid") or str(uuid.uuid4()),
        "title": title, "claim": claim,
        "domain": data.get("domain") or data.get("domainType") or "unclassified",
        "lane": data.get("lane", "Lane4"), "claim_class": data.get("claim_class") or data.get("claimKind", "unclassified"),
        "mode_classification": data.get("mode_classification", "candidate"),
        "assumptions": data.get("assumptions", []), "definitions": data.get("definitions", []),
        "equations": data.get("equations", []), "bridges": data.get("bridges", []),
        "dependencies": data.get("dependencies", []), "negative_guards": data.get("negative_guards", []),
        "kill_conditions": data.get("kill_conditions", []), "proof_label": data.get("proof_label", "NOT_ESTABLISHED"),
        "current_status": data.get("current_status", "active_candidate"),
        "rerun_status": data.get("rerun_status", "not_applicable"),
        "source_artifacts": data.get("source_artifacts", [str(source)] if source else []), "ledger": [],
    }
    if data.get("glyphs"):
        atom["glyphs"] = data["glyphs"]
    if data.get("glyph_paths"):
        atom["glyph_paths"] = data["glyph_paths"]
    if data.get("classification_bundle"):
        atom["classification_bundle"] = data["classification_bundle"]
    if data.get("source_claim_id") or data.get("claimID"):
        atom["source_claim_id"] = data.get("source_claim_id") or data["claimID"]
    old_master = "master equation" in (title + " " + claim).lower() and V3 not in " ".join(atom["equations"])
    if old_master:
        atom["rerun_status"] = "RERUN_OWED"
        atom["proof_label"] = "RERUN_OWED"
    atom["atom_id"], atom["atom_uid"] = atom_identity(atom)
    return atom


def ingest(path):
    source = Path(path).resolve()
    if not source.is_file():
        raise SystemExit(f"not a file: {source}")
    if source.suffix.lower() in {".json", ".jsonld"}:
        data = json.loads(source.read_text(encoding="utf-8"))
    else:
        text = source.read_text(encoding="utf-8")
        title = next((x.lstrip("# ").strip() for x in text.splitlines() if x.strip()), source.stem)
        data = {"title": title, "claim": text.strip(), "source_artifacts": [str(source)]}
    atom = normalize_atom(data, source)
    if atom_path(atom["atom_id"]).exists():
        raise SystemExit(f"atom already exists: {atom['atom_id']}")
    append_event(atom, {"event_type": "claim_ingested", "result": "recorded", "artifact_path": str(source),
                        "meaning": "Source claim ingested into Lane 4 ledger.", "limits": "Ingestion is not proof."})
    rebuild(); print(atom["atom_id"])


def rows():
    for atom in load_atoms():
        for event in atom["ledger"]:
            row = {"atom_id": atom["atom_id"], "atom_uid": atom["atom_uid"], "claim_title": atom["title"],
                   "atom_uuid": atom.get("atom_uuid", ""),
                   "claim_class": atom["claim_class"], "proof_label": atom["proof_label"],
                   "current_status": atom["current_status"], "rerun_status": atom["rerun_status"]}
            row.update(event)
            if "old_path" in event: row["source_path"] = event["old_path"]
            yield {k: row.get(k, "") for k in FIELDS}


def rebuild():
    LEDGER.mkdir(exist_ok=True)
    all_rows = list(rows())
    (LEDGER / "LANE4_GLOBAL_CLAIM_LEDGER.jsonl").write_text("".join(canonical(r) + "\n" for r in all_rows), encoding="utf-8")
    with (LEDGER / "LANE4_GLOBAL_CLAIM_LEDGER.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS); writer.writeheader(); writer.writerows(all_rows)
    make_report()


def make_report():
    atoms = load_atoms(); counts = {}
    for atom in atoms: counts[atom["proof_label"]] = counts.get(atom["proof_label"], 0) + 1
    lines = ["# Lane 4 Latest Status", "", f"Generated: {now()}", "", f"Atoms: **{len(atoms)}**", "", "## Proof labels", ""]
    lines += [f"- `{key}`: {counts[key]}" for key in sorted(counts)]
    lines += ["", "## Atoms", "", "| Atom | Status | Proof label | Rerun |", "|---|---|---|---|"]
    lines += [f"| `{a['atom_id']}` | {a['current_status']} | {a['proof_label']} | {a['rerun_status']} |" for a in atoms]
    (LEDGER / "LANE4_LATEST_STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate():
    errors = []
    for a in load_atoms():
        pfx = a.get("atom_id", "unknown")
        for key in ("atom_uuid", "assumptions", "source_artifacts", "current_status"):
            if not a.get(key): errors.append(f"{pfx}: missing {key}")
        label, cls, lane = a.get("proof_label"), a.get("claim_class", "").lower(), a.get("lane", "").lower()
        if label not in LABELS: errors.append(f"{pfx}: unknown proof_label {label}")
        if "histor" in cls and label and label.startswith("LEAN_"): errors.append(f"{pfx}: historical claim cannot be Lean-proved")
        if ("python" in lane or "colab" in lane) and label in {"LEAN_FORMAL_PROOF", "LEAN_CONDITIONAL_PROOF"}: errors.append(f"{pfx}: runtime lane cannot be formal proof")
        if "bridge" in cls and label == "LEAN_FORMAL_PROOF" and not a.get("bridges"): errors.append(f"{pfx}: bridge theorem lacks bridge proof")
        if "isomorph" in cls and a.get("mode_classification") not in {"C5", "formal_isomorphism"} and label == "LEAN_FORMAL_PROOF": errors.append(f"{pfx}: below-C5 event cannot be formal isomorphism")
        text = (a.get("title", "") + a.get("claim", "")).lower()
        if "master equation" in text and V3 not in " ".join(a.get("equations", [])) and a.get("rerun_status") != "RERUN_OWED": errors.append(f"{pfx}: old Master Equation requires RERUN_OWED")
        for index, event in enumerate(a.get("ledger", []), 1):
            if not event.get("event_id"): errors.append(f"{pfx}: ledger event {index} missing event_id")
            if not event.get("event_uuid"): errors.append(f"{pfx}: ledger event {index} missing event_uuid")
        ids = [e.get("event_id") for e in a.get("ledger", [])]
        if len(ids) != len(set(ids)): errors.append(f"{pfx}: duplicate ledger event")
    for error in errors: print("ERROR", error)
    print(f"validated {len(load_atoms())} atoms: {len(errors)} error(s)")
    return bool(errors)


def main():
    parser = argparse.ArgumentParser(prog="lane4-ledger")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("ingest"); p.add_argument("path")
    p = sub.add_parser("attach-run"); p.add_argument("--atom", required=True); p.add_argument("--lane", required=True); p.add_argument("--result", required=True); p.add_argument("--artifact", required=True); p.add_argument("--meaning", default="Runtime or proof receipt attached."); p.add_argument("--limits", default="The receipt establishes only what its lane can test."); p.add_argument("--reviewer", default="")
    p = sub.add_parser("move-file"); p.add_argument("--old", required=True); p.add_argument("--new", required=True)
    for name in ("validate", "status", "export-csv", "make-report"): sub.add_parser(name)
    args = parser.parse_args()
    if args.command == "ingest": ingest(args.path); return
    if args.command == "attach-run":
        a = get_atom(args.atom); append_event(a, {"event_type":"test_run", "lane":args.lane, "result":args.result, "artifact_path":args.artifact, "meaning":args.meaning, "limits":args.limits, "reviewer":args.reviewer}); rebuild(); return
    if args.command == "move-file":
        old, new = Path(args.old), Path(args.new); before = digest(old.read_bytes()) if old.is_file() else "unavailable"; after = digest(new.read_bytes()) if new.is_file() else "unavailable"; found = 0
        for a in load_atoms():
            if args.old in a["source_artifacts"] or any(e.get("artifact_path") == args.old for e in a["ledger"]):
                append_event(a, {"event_type":"file_moved", "old_path":args.old, "new_path":args.new, "content_hash_before":before, "content_hash_after":after, "same_content":before == after and before != "unavailable", "result":"recorded"}); found += 1
        if not found: raise SystemExit("old path is not attached to an atom")
        rebuild(); return
    if args.command == "validate": sys.exit(validate())
    rebuild(); print((LEDGER / "LANE4_LATEST_STATUS.md").read_text(encoding="utf-8"))

if __name__ == "__main__": main()
