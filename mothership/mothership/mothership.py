"""Mothership orchestrator: scan address maps, ingest bodies, produce reports.

The mothership is the central canonical body store.  Papers contribute only
thin address-map JSONL files; this class reads them, pulls bodies from a
bodies directory, runs the identity store and canon engine, and emits a nightly
report plus PR-ready text.  It never writes back to paper directories.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mothership.address import Address, Resolution, resolve_address
from mothership.canon_engine import CanonEngine
from mothership.identity_store import Divergence, IdentityStore


@dataclass
class NightlyReport:
    """Result of a mothership nightly run."""

    generated_at: str
    maps_dir: Path
    bodies_dir: Path
    new_identities: list[dict[str, Any]] = field(default_factory=list)
    linked_occurrences: int = 0
    divergences: list[dict[str, Any]] = field(default_factory=list)
    canon_candidates: list[dict[str, Any]] = field(default_factory=list)
    resolution_summary: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "maps_dir": str(self.maps_dir),
            "bodies_dir": str(self.bodies_dir),
            "new_identities": self.new_identities,
            "linked_occurrences": self.linked_occurrences,
            "divergences": self.divergences,
            "canon_candidates": self.canon_candidates,
            "resolution_summary": self.resolution_summary,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_pr_text(self) -> str:
        lines = [
            "## Mothership Nightly Report",
            "",
            f"Generated: {self.generated_at}",
            f"Maps: `{self.maps_dir}`",
            f"Bodies: `{self.bodies_dir}`",
            "",
            f"- New identities: {len(self.new_identities)}",
            f"- Linked occurrences: {self.linked_occurrences}",
            f"- Divergences: {len(self.divergences)}",
            f"- Canon candidates: {len(self.canon_candidates)}",
            "",
            "### Resolution summary",
            json.dumps(self.resolution_summary, indent=2),
        ]

        if self.divergences:
            lines.extend(["", "### Divergences requiring review"])
            for d in self.divergences:
                lines.append(f"- `{d['term']}`: {d['existing_sha256'][:16]}... vs {d['incoming_sha256'][:16]}...")

        if self.canon_candidates:
            lines.extend(["", "### Canon candidates"])
            for c in self.canon_candidates:
                lines.append(f"- `{c['term']}` ({c['identity_uuid']})")

        return "\n".join(lines)


class Mothership:
    """Centralized canonical body store."""

    def __init__(self, canon_engine: CanonEngine | None = None) -> None:
        self.store = IdentityStore()
        self.engine = canon_engine if canon_engine is not None else CanonEngine()
        self.resolutions: list[dict[str, Any]] = []

    def scan(
        self,
        maps_dir: str | Path,
        bodies_dir: str | Path,
        resolve: bool = True,
    ) -> NightlyReport:
        """Scan address maps, ingest bodies, and produce a nightly report.

        Args:
            maps_dir: directory containing JSONL address-map files.
            bodies_dir: directory containing body text files named by sha256.
            resolve: whether to run the address resolution waterfall against
                each body.  Defaults to True.
        """
        maps_dir = Path(maps_dir)
        bodies_dir = Path(bodies_dir)

        # Clear previous run state.
        self.store = IdentityStore()
        self.resolutions = []

        identity_uuids_seen_before: set[str] = set()
        occurrences_ingested = 0

        for map_file in sorted(maps_dir.glob("*.jsonl")):
            with map_file.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    address = Address.from_dict(data)
                    term = data.get("term", address.handle or address.uuid)
                    body_text = self._pull_body(bodies_dir, address.sha256)

                    occurrences_ingested += 1

                    # Resolution runs against the pulled body regardless of
                    # whether this occurrence creates a divergence.
                    if resolve:
                        resolution = resolve_address(address, body_text)
                        self.resolutions.append({
                            "address_uuid": address.uuid,
                            "status": resolution["status"],
                            "reason": resolution["reason"],
                        })

                    try:
                        identity_uuid = self.store.ingest(term, address, body_text)
                    except Divergence:
                        # Recorded inside the store; continue scanning.
                        continue

                    identity_uuids_seen_before.add(identity_uuid)

        report = self._build_report(
            maps_dir=maps_dir,
            bodies_dir=bodies_dir,
            occurrences_ingested=occurrences_ingested,
        )
        return report

    @staticmethod
    def _pull_body(bodies_dir: Path, sha256: str) -> str:
        """Pull a body text file named by its sha256."""
        body_path = bodies_dir / sha256
        if not body_path.exists():
            # Fall back to a file without extension if the literal sha256 exists.
            body_path = bodies_dir / (sha256 + ".txt")
        if not body_path.exists():
            raise FileNotFoundError(f"Body not found for sha256 {sha256}: {body_path}")
        return body_path.read_text(encoding="utf-8")

    def _build_report(
        self,
        maps_dir: Path,
        bodies_dir: Path,
        occurrences_ingested: int,
    ) -> NightlyReport:
        report = NightlyReport(
            generated_at=datetime.now(timezone.utc).isoformat(),
            maps_dir=maps_dir,
            bodies_dir=bodies_dir,
            linked_occurrences=occurrences_ingested,
        )

        for identity in self.store.identities.values():
            report.new_identities.append({
                "uuid": identity.uuid,
                "sha256": identity.sha256,
                "term": identity.term,
                "occurrence_count": len(identity.occurrences),
            })

            receipt = self.engine.evaluate(identity, identity.body_text)
            if receipt["overall"]:
                report.canon_candidates.append({
                    "identity_uuid": identity.uuid,
                    "sha256": identity.sha256,
                    "term": identity.term,
                    "receipt": receipt,
                })

        report.divergences = [
            {
                "term": d.term,
                "existing_identity_uuid": d.existing_identity_uuid,
                "existing_sha256": d.existing_sha256,
                "incoming_sha256": d.incoming_sha256,
                "incoming_address_uuid": d.incoming_address_uuid,
            }
            for d in self.store.divergences
        ]

        summary: dict[str, int] = {
            Resolution.RESOLVED.value: 0,
            Resolution.RE_AIMED.value: 0,
            Resolution.MOVED.value: 0,
            Resolution.LOST.value: 0,
        }
        for r in self.resolutions:
            status = r["status"]
            summary[status] = summary.get(status, 0) + 1
        report.resolution_summary = summary

        return report
