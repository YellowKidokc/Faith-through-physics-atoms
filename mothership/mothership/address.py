"""Address resolution for the Universal Address Spec v1.0.

An Address is a thin, stable pointer to a unit of content.  Resolution follows a
strict waterfall: lasers (section_path + offsets), sha256 verification,
fingerprint re-acquisition, and finally moved/lost classification.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Resolution(Enum):
    """Resolution status for an occurrence."""

    RESOLVED = "resolved"
    RE_AIMED = "re-aimed"
    MOVED = "moved"
    LOST = "lost"


@dataclass(frozen=True)
class Address:
    """Universal address object.

    Matches the JSON schema in UNIVERSAL_ADDRESS_SPEC_v1.0.md.
    """

    uuid: str
    handle: str
    target_type: str
    section_path: tuple[int, ...]
    offsets: tuple[int, int]
    exact: str
    prefix: str
    suffix: str
    sha256: str
    doc_uuid: str
    doc_sha256: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Address":
        locator = data.get("locator", {})
        anchor = data.get("anchor", {})
        source = data.get("source", {})
        return cls(
            uuid=data["uuid"],
            handle=data.get("handle", ""),
            target_type=data["target_type"],
            section_path=tuple(locator.get("section_path", [])),
            offsets=tuple(locator.get("offsets", [0, 0])),
            exact=anchor.get("exact", ""),
            prefix=anchor.get("prefix", ""),
            suffix=anchor.get("suffix", ""),
            sha256=anchor.get("sha256", ""),
            doc_uuid=source.get("doc_uuid", ""),
            doc_sha256=source.get("doc_sha256", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "handle": self.handle,
            "target_type": self.target_type,
            "locator": {
                "section_path": list(self.section_path),
                "offsets": list(self.offsets),
            },
            "anchor": {
                "exact": self.exact,
                "prefix": self.prefix,
                "suffix": self.suffix,
                "sha256": self.sha256,
            },
            "source": {
                "doc_uuid": self.doc_uuid,
                "doc_sha256": self.doc_sha256,
            },
        }

    def with_locator(self, section_path: tuple[int, ...], offsets: tuple[int, int]) -> "Address":
        """Return a copy with updated locator values."""
        return Address(
            uuid=self.uuid,
            handle=self.handle,
            target_type=self.target_type,
            section_path=section_path,
            offsets=offsets,
            exact=self.exact,
            prefix=self.prefix,
            suffix=self.suffix,
            sha256=self.sha256,
            doc_uuid=self.doc_uuid,
            doc_sha256=self.doc_sha256,
        )


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _fingerprint_reacquire(address: Address, document_text: str) -> tuple[int, int] | None:
    """Re-acquire target using exact text + prefix/suffix fingerprint.

    Returns new (start, end) offsets if a unique match is found, else None.
    """
    needle = address.exact
    if not needle:
        return None

    candidates: list[tuple[int, int]] = []
    start = 0
    while True:
        idx = document_text.find(needle, start)
        if idx == -1:
            break
        candidates.append((idx, idx + len(needle)))
        start = idx + 1

    if not candidates:
        return None

    if len(candidates) == 1:
        return candidates[0]

    # Disambiguate by prefix + suffix fingerprint.
    def matches_context(start: int, end: int) -> bool:
        before = document_text[max(0, start - len(address.prefix)) : start]
        after = document_text[end : end + len(address.suffix)]
        return before.endswith(address.prefix) and after.startswith(address.suffix)

    matched = [c for c in candidates if matches_context(*c)]
    return matched[0] if len(matched) == 1 else None


def resolve_address(address: Address, document_text: str) -> dict[str, Any]:
    """Resolve an address against the current document text.

    Implements the waterfall from the Universal Address Spec:
      1. Lasers first (section_path + offsets)
      2. Verify sha256(exact)
      3. Fingerprint re-acquire (exact + prefix/suffix)
      4. Mark moved/lost if re-acquire fails

    Returns a dict with keys:
      - status: one of Resolution values
      - address: the original Address (or a re-aimed copy)
      - reason: human-readable explanation
    """
    start, end = address.offsets

    # 1. Lasers first.
    if 0 <= start < end <= len(document_text):
        candidate = document_text[start:end]
        # 2. Verify anchor.
        if _sha256(candidate) == address.sha256:
            return {
                "status": Resolution.RESOLVED.value,
                "address": address,
                "reason": "lasers hit and sha256 verified",
            }

    # 3. Fingerprint re-acquire.
    new_offsets = _fingerprint_reacquire(address, document_text)
    if new_offsets is not None:
        new_start, new_end = new_offsets
        re_aimed = address.with_locator(address.section_path, new_offsets)
        # Sanity check: re-acquired text must hash to the same value.
        if _sha256(document_text[new_start:new_end]) == address.sha256:
            return {
                "status": Resolution.RE_AIMED.value,
                "address": re_aimed,
                "reason": f"drift detected; re-aimed from {address.offsets} to {new_offsets}",
            }

    # 4. Moved or lost.
    # Spec distinguishes moved (found elsewhere with a forward pointer) from lost.
    # Without a forward pointer mechanism here we classify as lost.
    return {
        "status": Resolution.LOST.value,
        "address": address,
        "reason": "anchor unrecoverable in current document version",
    }
