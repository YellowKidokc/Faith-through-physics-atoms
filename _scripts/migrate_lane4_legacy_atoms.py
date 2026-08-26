#!/usr/bin/env python3
"""Repair legacy Lane 4 atom records without changing claim standing upward.

The migration is intentionally conservative:
- legacy atoms get deterministic UUIDv5 identifiers derived from atom_uid;
- missing event ids are rebuilt from event content, with a legacy index only
  when needed to preserve duplicate historical entries without deleting them;
- empty assumptions get an explicit administrative placeholder;
- old Master Equation records are marked RERUN_OWED rather than promoted.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ATOMS = ROOT / "_ledger" / "atoms"
V3 = "X=(G,M,E,S,T,K,Q,R,F); chi(X)=C_W[prod_i X_i]; dX/dt = W(X,t) grad chi(X)+eta(X,t)"
ATOM_NAMESPACE = uuid.UUID("8fa0f6a5-03ea-4c97-919e-7e508aa1e2ac")
EVENT_NAMESPACE = uuid.UUID("c58b7490-35e3-4ebd-8e65-d14d6334d44e")
LEGACY_ASSUMPTION = (
    "LEGACY_IMPORT_ASSUMPTION_UNDECOMPOSED: this atom predates Lane 4 "
    "assumption decomposition; do not promote beyond its current proof_label "
    "without human review."
)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    raw = value if isinstance(value, bytes) else canonical(value).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def event_digest(event: dict[str, Any]) -> str:
    stable = {k: v for k, v in event.items() if k not in {"event_uuid", "event_id"}}
    return digest(stable)


def stable_uuid(namespace: uuid.UUID, value: str) -> str:
    return str(uuid.uuid5(namespace, value))


def migrate_atom(path: Path) -> bool:
    atom = json.loads(path.read_text(encoding="utf-8-sig"))
    changed = False

    if not atom.get("atom_uuid"):
        atom["atom_uuid"] = stable_uuid(ATOM_NAMESPACE, atom["atom_uid"])
        changed = True

    if not atom.get("assumptions"):
        atom["assumptions"] = [LEGACY_ASSUMPTION]
        changed = True

    text = (atom.get("title", "") + " " + atom.get("claim", "")).lower()
    equations = " ".join(atom.get("equations", []))
    if "master equation" in text and V3 not in equations:
        if atom.get("rerun_status") != "RERUN_OWED":
            atom["rerun_status"] = "RERUN_OWED"
            changed = True
        if atom.get("proof_label") not in {"RERUN_OWED", "QUARANTINE"}:
            atom["proof_label"] = "RERUN_OWED"
            changed = True

    seen: set[str] = set()
    for index, event in enumerate(atom.get("ledger", []), 1):
        candidate = event_digest(event)
        if candidate in seen:
            event.setdefault("legacy_event_index", index)
            candidate = event_digest(event)
            changed = True
        if event.get("event_id") != candidate:
            event["event_id"] = candidate
            changed = True
        if not event.get("event_uuid"):
            event["event_uuid"] = stable_uuid(EVENT_NAMESPACE, event["event_id"])
            changed = True
        seen.add(event["event_id"])

    if changed:
        path.write_text(json.dumps(atom, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    changed = 0
    for path in sorted(ATOMS.glob("*.json")):
        if migrate_atom(path):
            changed += 1
    print(f"migrated {changed} atom file(s)")


if __name__ == "__main__":
    main()
