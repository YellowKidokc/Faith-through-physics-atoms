"""Mothership API layer — one surface over pills, companions, addresses, and rules.

This module is the callable interface AI workers use to fetch faces, pull bodies,
resolve addresses, and ask the curator what to run next. It keeps the underlying
stores independent: callers do not need to know whether a pill is YAML, a body is
a file, or a companion is indexed.

USAGE
    from mothership.api import MothershipAPI
    api = MothershipAPI()

    pill = api.get_pill("fabe6192-d3e1-503e-9c00-f286a16deeed")
    companion = api.get_companion("16166191")
    proposals = api.curator_build_next()

The API is intentionally thin. Heavy logic lives in the dedicated modules:
address.py, identity_store.py, canon_engine.py, curator.py.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import hashlib

from mothership.address import Address, resolve_address
from mothership.canon_engine import CanonEngine
from mothership.curator import CuratorPass, IdentityStore
from mothership.identity_store import Identity, Occurrence

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


DEFAULT_ROOT = Path(__file__).resolve().parent.parent


class MothershipAPI:
    """Callable surface over the mothership stores."""

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root else DEFAULT_ROOT
        self.pills_dir = self.root / "pills"
        self.companions_dir = self.root / "companions"
        self.index_path = self.companions_dir / "index.json"
        self.address_maps_dir = self.root / "addresses"
        self.bodies_dir = self.root / "bodies"
        self._canon_engine: CanonEngine | None = None

    # ------------------------------------------------------------------ pills

    def _pill_files(self) -> list[Path]:
        if not self.pills_dir.exists():
            return []
        return sorted(self.pills_dir.rglob("*.pill.yaml"))

    def list_pills(self) -> list[dict[str, Any]]:
        """Return the face of every pill in the store."""
        if yaml is None:
            raise RuntimeError("PyYAML is required to load pills")
        faces: list[dict[str, Any]] = []
        for path in self._pill_files():
            pill = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(pill, dict):
                continue
            face = pill.get("face", pill)
            face["_path"] = str(path.relative_to(self.root).as_posix())
            faces.append(face)
        return faces

    def get_pill(self, uuid: str) -> dict[str, Any] | None:
        """Load a full pill by its UUID."""
        if yaml is None:
            raise RuntimeError("PyYAML is required to load pills")
        for path in self._pill_files():
            pill = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(pill, dict):
                continue
            face = pill.get("face", pill)
            if face.get("uuid") == uuid:
                pill["_path"] = str(path.relative_to(self.root).as_posix())
                return pill
        return None

    # -------------------------------------------------------------- companions

    def list_companions(self) -> list[dict[str, Any]]:
        """Return the companions index, or an empty list if none exists."""
        if not self.index_path.exists():
            return []
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def _companion_files(self) -> list[Path]:
        if not self.companions_dir.exists():
            return []
        return sorted(self.companions_dir.glob("*.md"))

    def get_companion(self, paper_uuid: str) -> dict[str, Any] | None:
        """Load a companion's front matter and body by paper_uuid."""
        if yaml is None:
            raise RuntimeError("PyYAML is required to load companions")
        for path in self._companion_files():
            text = path.read_text(encoding="utf-8")
            if not text.startswith("---"):
                continue
            end = text.find("\n---", 3)
            if end == -1:
                continue
            front_matter = yaml.safe_load(text[3:end])
            if not isinstance(front_matter, dict):
                continue
            if str(front_matter.get("paper_uuid")) == str(paper_uuid):
                return {
                    "paper_uuid": paper_uuid,
                    "front_matter": front_matter,
                    "body": text[end + 4 :].lstrip("\n"),
                    "path": str(path.relative_to(self.root).as_posix()),
                }
        return None

    # --------------------------------------------------------------- addresses

    def resolve_address(
        self, address_dict: dict[str, Any], document_text: str
    ) -> dict[str, Any]:
        """Resolve a universal address against a document string.

        Returns a dict with status, address, and reason per the address spec.
        """
        address = Address.from_dict(address_dict)
        result = resolve_address(address, document_text)
        return {
            "status": result["status"],
            "reason": result["reason"],
            "address": result["address"].to_dict(),
        }

    # ------------------------------------------------------------------ bodies

    def get_body(self, sha256: str) -> str | None:
        """Fetch a body by its sha256 hash, or None if absent."""
        body_path = self.bodies_dir / sha256
        if not body_path.exists():
            body_path = self.bodies_dir / (sha256 + ".txt")
        if not body_path.exists():
            return None
        return body_path.read_text(encoding="utf-8")

    # ------------------------------------------------------------------ curator

    def curator_build_next(
        self, identity_store: IdentityStore | None = None
    ) -> list[dict[str, Any]]:
        """Run the weekly curator pass and return the ranked proposal queue."""
        store = identity_store if identity_store is not None else IdentityStore()
        curator = CuratorPass(
            pills_dir=self.pills_dir,
            address_maps_dir=self.address_maps_dir,
            identity_store=store,
            bodies_dir=self.bodies_dir,
        )
        return curator.run()

    # ------------------------------------------------------------------ canon

    def canon_evaluate(self, pill: dict[str, Any]) -> dict[str, Any]:
        """Run the canon rule engine against a pill and return a receipt."""
        if self._canon_engine is None:
            self._canon_engine = CanonEngine()
        face = pill.get("face", pill)
        veins = pill.get("veins", {})
        body_text = json.dumps(veins, ensure_ascii=False, sort_keys=True)
        identity = Identity(
            uuid=face.get("uuid", ""),
            sha256=hashlib.sha256(body_text.encode("utf-8")).hexdigest(),
            body_text=body_text,
            term=face.get("term") or face.get("name"),
            occurrences=[],
        )
        receipt = self._canon_engine.evaluate(identity, body_text, occurrences=[])
        receipt["overall"] = "PASS" if receipt["overall"] else "FAIL"
        return receipt

    # ------------------------------------------------------------------ summary

    def status(self) -> dict[str, Any]:
        """Return a quick status snapshot of the mothership stores."""
        return {
            "root": str(self.root),
            "pills": len(self.list_pills()),
            "companions": len(self.list_companions()),
            "addresses_maps": len(list(self.address_maps_dir.rglob("*.jsonl")))
            if self.address_maps_dir.exists()
            else 0,
            "bodies": len(list(self.bodies_dir.iterdir()))
            if self.bodies_dir.exists()
            else 0,
        }


def _cli() -> None:
    """Minimal command-line interface for quick inspections."""
    import argparse

    parser = argparse.ArgumentParser(description="Mothership API surface")
    parser.add_argument("--root", type=Path, default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status")
    list_pills = sub.add_parser("list-pills")
    list_pills.add_argument("--uuid", action="store_true", help="print only UUIDs")
    sub.add_parser("list-companions")
    get_pill = sub.add_parser("get-pill")
    get_pill.add_argument("uuid")
    get_comp = sub.add_parser("get-companion")
    get_comp.add_argument("paper_uuid")
    sub.add_parser("curator")

    args = parser.parse_args()
    api = MothershipAPI(args.root)

    if args.command == "status":
        print(json.dumps(api.status(), indent=2))
    elif args.command == "list-pills":
        pills = api.list_pills()
        if args.uuid:
            for p in pills:
                print(p.get("uuid"))
        else:
            print(json.dumps(pills, indent=2))
    elif args.command == "list-companions":
        print(json.dumps(api.list_companions(), indent=2))
    elif args.command == "get-pill":
        pill = api.get_pill(args.uuid)
        print(json.dumps(pill, indent=2) if pill else "null")
    elif args.command == "get-companion":
        comp = api.get_companion(args.paper_uuid)
        print(json.dumps(comp, indent=2) if comp else "null")
    elif args.command == "curator":
        proposals = api.curator_build_next()
        print(json.dumps(proposals, indent=2))


if __name__ == "__main__":
    _cli()
