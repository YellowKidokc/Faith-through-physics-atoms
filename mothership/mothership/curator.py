"""Curator Pass: corpus-wide proposal generator.

The curator scans pills, address maps, the identity store, and bodies and emits
a ranked `build_next` queue of proposals for human review.  It is read-only with
respect to papers, statuses, and UUID minting.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mothership.address import Address, resolve_address
from mothership.identity_store import IdentityStore

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


CURATOR_VERSION = "2026-09-22.v1"
RULE_VERSION = "2026-09-22.v1"

PRIORITY = {
    "diverge": 1,
    "test": 2,
    "extract": 3,
    "define": 4,
    "link": 5,
    "cover": 6,
    "meta": 7,
}


@dataclass
class CuratorConfig:
    """Configurable thresholds for the curator pass."""

    link_similarity_threshold: float = 0.0  # shared term/alias counts above this
    test_receipt_key: str = "testReceipts"
    falsification_keys: tuple[str, ...] = ("falsificationCondition", "kill_condition")
    meta_required_keys: tuple[str, ...] = ("curator_version", "rule_version")


class CuratorPass:
    """Generate the weekly `build_next` proposal queue."""

    def __init__(
        self,
        pills_dir: str | Path,
        address_maps_dir: str | Path,
        identity_store: IdentityStore,
        bodies_dir: str | Path,
        config: CuratorConfig | None = None,
    ) -> None:
        self.pills_dir = Path(pills_dir)
        self.address_maps_dir = Path(address_maps_dir)
        self.identity_store = identity_store
        self.bodies_dir = Path(bodies_dir)
        self.config = config if config is not None else CuratorConfig()
        self._proposal_counter = 0

    def _next_proposal_id(self) -> str:
        self._proposal_counter += 1
        return f"PROP-{self._proposal_counter:04d}"

    def _receipt(self) -> dict[str, str]:
        return {
            "curator_version": CURATOR_VERSION,
            "rule_version": RULE_VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "generator": "CuratorPass",
        }

    def _make_proposal(
        self,
        proposal_type: str,
        targets: list[str],
        reason: str,
        expected_yield: float | str,
    ) -> dict[str, Any]:
        """Build a proposal atom with status: proposed and a receipt."""
        return {
            "proposal_id": self._next_proposal_id(),
            "type": proposal_type,
            "targets": targets,
            "reason": reason,
            "expected_yield": expected_yield,
            "priority": PRIORITY[proposal_type],
            "status": "proposed",
            "receipt": self._receipt(),
        }

    def _load_pills(self) -> list[dict[str, Any]]:
        """Load all YAML pills from the pills directory."""
        if yaml is None:  # pragma: no cover
            raise RuntimeError("PyYAML is required to load pills")
        pills: list[dict[str, Any]] = []
        if not self.pills_dir.exists():
            return pills
        for pill_file in sorted(self.pills_dir.rglob("*.pill.yaml")):
            with pill_file.open("r", encoding="utf-8") as fh:
                pill = yaml.safe_load(fh)
                if pill:
                    pills.append(pill)
        return pills

    def _load_address_maps(self) -> dict[str, list[dict[str, Any]]]:
        """Load address maps keyed by doc_uuid."""
        maps: dict[str, list[dict[str, Any]]] = {}
        if not self.address_maps_dir.exists():
            return maps
        for map_file in sorted(self.address_maps_dir.rglob("*.jsonl")):
            with map_file.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    doc_uuid = data.get("source", {}).get("doc_uuid")
                    if doc_uuid:
                        maps.setdefault(doc_uuid, []).append(data)
        return maps

    def _pull_body(self, sha256: str) -> str | None:
        """Fetch a body by sha256 from the bodies directory."""
        body_path = self.bodies_dir / sha256
        if not body_path.exists():
            body_path = self.bodies_dir / (sha256 + ".txt")
        if not body_path.exists():
            return None
        return body_path.read_text(encoding="utf-8")

    @staticmethod
    def _sha256(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _detect_extract(
        self, pills: list[dict[str, Any]], address_maps: dict[str, list[dict[str, Any]]]
    ) -> list[dict[str, Any]]:
        """Pills that claim to be atoms but have no resolvable address/body."""
        proposals: list[dict[str, Any]] = []
        all_address_uuids = {
            addr["uuid"]
            for addrs in address_maps.values()
            for addr in addrs
        }
        for pill in pills:
            target_type = pill.get("target_type") or pill.get("face", {}).get("target_type")
            pill_uuid = pill.get("uuid") or pill.get("face", {}).get("uuid")
            if not target_type or not pill_uuid:
                continue
            if pill_uuid not in all_address_uuids:
                proposals.append(
                    self._make_proposal(
                        "extract",
                        [pill_uuid],
                        f"{target_type} pill {pill_uuid} has no address occurrence.",
                        0.7,
                    )
                )
                continue
            # Address exists; verify body resolves.
            for doc_addrs in address_maps.values():
                for addr_data in doc_addrs:
                    if addr_data["uuid"] == pill_uuid:
                        address = Address.from_dict(addr_data)
                        body_text = self._pull_body(address.sha256)
                        if body_text is None:
                            proposals.append(
                                self._make_proposal(
                                    "extract",
                                    [pill_uuid],
                                    f"{target_type} pill {pill_uuid} points to a missing body.",
                                    0.65,
                                )
                            )
                            break
                        resolution = resolve_address(address, body_text)
                        if resolution["status"] in ("lost",):
                            proposals.append(
                                self._make_proposal(
                                    "extract",
                                    [pill_uuid],
                                    f"{target_type} pill {pill_uuid} address is unresolvable.",
                                    0.6,
                                )
                            )
                            break
        return proposals

    def _detect_define(self, pills: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Definition targets whose term is not in the identity store."""
        proposals: list[dict[str, Any]] = []
        known_terms = {identity.term for identity in self.identity_store.identities.values() if identity.term}
        for pill in pills:
            face = pill.get("face", pill)
            if face.get("target_type") != "definition":
                continue
            term = face.get("term")
            pill_uuid = face.get("uuid")
            if term and term not in known_terms:
                proposals.append(
                    self._make_proposal(
                        "define",
                        [pill_uuid] if pill_uuid else [],
                        f"Definition term {term!r} is in use but has no registry identity.",
                        0.6,
                    )
                )
        return proposals

    def _detect_link(
        self, pills: list[dict[str, Any]], address_maps: dict[str, list[dict[str, Any]]]
    ) -> list[dict[str, Any]]:
        """Propose edges between pills that share terms/aliases/dependencies."""
        proposals: list[dict[str, Any]] = []
        index: dict[str, set[str]] = {}  # normalized term -> set of pill uuids
        existing_edges: set[tuple[str, str]] = set()  # recorded edges (symmetric)
        pill_uuids: set[str] = set()

        for pill in pills:
            face = pill.get("face", pill)
            veins = pill.get("veins", {})
            pill_uuid = face.get("uuid")
            if not pill_uuid:
                continue
            pill_uuids.add(pill_uuid)

            terms: list[str] = []
            for key in ("term", "canonical_term", "preferredTerm", "name"):
                if face.get(key):
                    terms.append(face[key])
            aliases = veins.get("aliases", []) if isinstance(veins, dict) else []
            for alias in aliases:
                if isinstance(alias, str):
                    terms.append(alias)

            for term in {t.lower().strip() for t in terms if t}:
                index.setdefault(term, set()).add(pill_uuid)

            recorded = veins.get("links", []) if isinstance(veins, dict) else []
            recorded = veins.get("edges", recorded) if isinstance(veins, dict) else recorded
            for edge in recorded:
                target = edge.get("target") if isinstance(edge, dict) else edge
                if isinstance(target, str):
                    existing_edges.add(tuple(sorted((pill_uuid, target))))

        # Shared terms / aliases.
        seen_pairs: set[tuple[str, str]] = set()
        for term, uuids in index.items():
            if len(uuids) < 2:
                continue
            pair = tuple(sorted(uuids))
            if pair not in existing_edges and pair not in seen_pairs:
                proposals.append(
                    self._make_proposal(
                        "link",
                        list(uuids),
                        f"Pills share term/alias {term!r} but have no recorded edge.",
                        0.5,
                    )
                )
                seen_pairs.add(pair)

        # Explicit dependencies that are not yet recorded as edges.
        for pill in pills:
            face = pill.get("face", pill)
            veins = pill.get("veins", {})
            pill_uuid = face.get("uuid")
            if not pill_uuid:
                continue
            deps = veins.get("dependencies", []) if isinstance(veins, dict) else []
            for dep in deps:
                if not isinstance(dep, str):
                    continue
                pair = tuple(sorted((pill_uuid, dep)))
                if dep in pill_uuids and pair not in existing_edges and pair not in seen_pairs:
                    proposals.append(
                        self._make_proposal(
                            "link",
                            [pill_uuid, dep],
                            f"Pill {pill_uuid} depends on {dep} but no edge is recorded.",
                            0.55,
                        )
                    )
                    seen_pairs.add(pair)

        # Pills whose addresses co-occur in the same document map.
        doc_uuids: dict[str, set[str]] = {}
        for doc_uuid, addrs in address_maps.items():
            doc_uuids[doc_uuid] = {a["uuid"] for a in addrs}
        for doc_uuid, uuids in doc_uuids.items():
            uuids = [u for u in uuids if u in pill_uuids]
            for i, u1 in enumerate(uuids):
                for u2 in uuids[i + 1 :]:
                    pair = tuple(sorted((u1, u2)))
                    if pair not in existing_edges and pair not in seen_pairs:
                        proposals.append(
                            self._make_proposal(
                                "link",
                                [u1, u2],
                                f"Addresses co-occur in document {doc_uuid} with no recorded edge.",
                                0.45,
                            )
                        )
                        seen_pairs.add(pair)

        return proposals

    def _detect_cover(
        self, pills: list[dict[str, Any]], address_maps: dict[str, list[dict[str, Any]]]
    ) -> list[dict[str, Any]]:
        """Address maps that have no pills referencing their doc_uuid."""
        proposals: list[dict[str, Any]] = []
        covered_docs: set[str] = set()
        for pill in pills:
            face = pill.get("face", pill)
            veins = pill.get("veins", {})
            source = face.get("source", {}) if isinstance(face.get("source"), dict) else {}
            if not source and isinstance(veins, dict):
                source = veins.get("source", {})
            doc_uuid = source.get("doc_uuid")
            if doc_uuid:
                covered_docs.add(doc_uuid)

        for doc_uuid in address_maps:
            if doc_uuid not in covered_docs:
                proposals.append(
                    self._make_proposal(
                        "cover",
                        [doc_uuid],
                        f"Document {doc_uuid} has address maps but no pills.",
                        0.3,
                    )
                )
        return proposals

    def _detect_diverge(self) -> list[dict[str, Any]]:
        """Identity-store divergences with no ruling."""
        proposals: list[dict[str, Any]] = []
        for divergence in self.identity_store.divergences:
            proposals.append(
                self._make_proposal(
                    "diverge",
                    [divergence.existing_identity_uuid, divergence.incoming_address_uuid],
                    f"Term {divergence.term!r} maps to multiple bodies; adjudicate meaning split or retirement.",
                    0.95,
                )
            )
        return proposals

    def _detect_test(self, pills: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Pills with kill conditions but no matching test receipt."""
        proposals: list[dict[str, Any]] = []
        for pill in pills:
            face = pill.get("face", pill)
            veins = pill.get("veins", {})
            pill_uuid = face.get("uuid")
            if not pill_uuid:
                continue

            kill_conditions: list[str] = []
            for key in self.config.falsification_keys:
                value = face.get(key) or (veins.get(key) if isinstance(veins, dict) else None)
                if value:
                    kill_conditions.append(str(value))

            if not kill_conditions:
                continue

            receipts = veins.get(self.config.test_receipt_key, []) if isinstance(veins, dict) else []
            if not receipts:
                proposals.append(
                    self._make_proposal(
                        "test",
                        [pill_uuid],
                        f"Pill {pill_uuid} has kill/falsification conditions but no test receipts.",
                        0.8,
                    )
                )
        return proposals

    def _detect_meta(self) -> list[dict[str, Any]]:
        """Recursive self-check: propose improvements if config is incomplete."""
        proposals: list[dict[str, Any]] = []
        config_dict = self.config.__dict__
        missing = [key for key in self.config.meta_required_keys if key not in config_dict]
        if missing:
            proposals.append(
                self._make_proposal(
                    "meta",
                    ["curator-pass"],
                    f"Curator configuration is missing required meta keys: {missing}.",
                    0.2,
                )
            )
        return proposals

    def run(self) -> list[dict[str, Any]]:
        """Run the full curator pass and return a ranked build_next queue."""
        pills = self._load_pills()
        address_maps = self._load_address_maps()

        proposals: list[dict[str, Any]] = []
        proposals.extend(self._detect_diverge())
        proposals.extend(self._detect_test(pills))
        proposals.extend(self._detect_extract(pills, address_maps))
        proposals.extend(self._detect_define(pills))
        proposals.extend(self._detect_link(pills, address_maps))
        proposals.extend(self._detect_cover(pills, address_maps))
        proposals.extend(self._detect_meta())

        # Rank: priority ascending, then expected_yield descending, then fewer targets first.
        def sort_key(p: dict[str, Any]) -> tuple[int, float, int]:
            yield_val = p["expected_yield"]
            yield_num = float(yield_val) if isinstance(yield_val, (int, float)) else 0.0
            return (p["priority"], -yield_num, len(p["targets"]))

        proposals.sort(key=sort_key)
        # Renumber proposal IDs after sorting.
        self._proposal_counter = 0
        for proposal in proposals:
            self._proposal_counter += 1
            proposal["proposal_id"] = f"PROP-{self._proposal_counter:04d}"

        return proposals
