"""Identity store: bodies by sha256, divergence detection, occurrence linking."""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from typing import Any

from mothership.address import Address


class Divergence(Exception):
    """Raised when the same term maps to a different sha256."""

    def __init__(
        self,
        term: str,
        existing_sha256: str,
        incoming_sha256: str,
        identity_uuid: str,
    ) -> None:
        super().__init__(
            f"Divergence for term {term!r}: "
            f"existing {existing_sha256[:16]}... vs incoming {incoming_sha256[:16]}..."
        )
        self.term = term
        self.existing_sha256 = existing_sha256
        self.incoming_sha256 = incoming_sha256
        self.identity_uuid = identity_uuid


@dataclass
class Occurrence:
    """One appearance of an identity inside a specific document version."""

    occurrence_uuid: str
    identity_uuid: str
    address: Address
    term: str


@dataclass
class Identity:
    """Canonical identity for a unit of content."""

    uuid: str
    sha256: str
    body_text: str
    term: str | None = None
    occurrences: list[Occurrence] = field(default_factory=list)


@dataclass
class DivergenceRecord:
    """Recorded divergence between two bodies claiming the same term."""

    term: str
    existing_identity_uuid: str
    existing_sha256: str
    incoming_sha256: str
    incoming_address_uuid: str


class IdentityStore:
    """Stores bodies keyed by sha256 and links occurrences to identity UUIDs.

    Identities are deduplicated by exact body text.  Divergences are raised/recorded
    when the same term maps to more than one sha256.
    """

    def __init__(self) -> None:
        self.identities: dict[str, Identity] = {}  # sha256 -> Identity
        self._by_uuid: dict[str, Identity] = {}
        self._term_to_sha256: dict[str, str] = {}
        self.divergences: list[DivergenceRecord] = []
        self.occurrences: list[Occurrence] = []

    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def ingest(self, term: str, address: Address, body_text: str) -> str:
        """Ingest an occurrence and return its identity UUID.

        If the exact body text has been seen before, the existing identity UUID is
        reused.  If `term` has previously mapped to a different sha256, a divergence
        is recorded (and raised) for human review.
        """
        body_hash = self._hash(body_text)

        if body_hash in self.identities:
            identity = self.identities[body_hash]
        else:
            identity = Identity(
                uuid=str(uuid.uuid4()),
                sha256=body_hash,
                body_text=body_text,
            )
            self.identities[body_hash] = identity
            self._by_uuid[identity.uuid] = identity

        # Enforce one term -> one meaning.  A term already mapped to a different
        # body means a semantic divergence that must be reviewed.
        if term in self._term_to_sha256:
            existing_sha256 = self._term_to_sha256[term]
            if existing_sha256 != body_hash:
                existing_identity = self.identities[existing_sha256]
                record = DivergenceRecord(
                    term=term,
                    existing_identity_uuid=existing_identity.uuid,
                    existing_sha256=existing_sha256,
                    incoming_sha256=body_hash,
                    incoming_address_uuid=address.uuid,
                )
                self.divergences.append(record)
                raise Divergence(
                    term=term,
                    existing_sha256=existing_sha256,
                    incoming_sha256=body_hash,
                    identity_uuid=existing_identity.uuid,
                )
        else:
            self._term_to_sha256[term] = body_hash

        if identity.term is None:
            identity.term = term

        occurrence = Occurrence(
            occurrence_uuid=str(uuid.uuid4()),
            identity_uuid=identity.uuid,
            address=address,
            term=term,
        )
        identity.occurrences.append(occurrence)
        self.occurrences.append(occurrence)
        return identity.uuid

    def get_identity_by_sha256(self, sha256: str) -> Identity | None:
        return self.identities.get(sha256)

    def get_identity_by_uuid(self, identity_uuid: str) -> Identity | None:
        return self._by_uuid.get(identity_uuid)

    def to_report(self) -> dict[str, Any]:
        return {
            "identities": [
                {
                    "uuid": i.uuid,
                    "sha256": i.sha256,
                    "term": i.term,
                    "occurrence_count": len(i.occurrences),
                }
                for i in self.identities.values()
            ],
            "occurrence_count": len(self.occurrences),
            "divergence_count": len(self.divergences),
            "divergences": [
                {
                    "term": d.term,
                    "existing_identity_uuid": d.existing_identity_uuid,
                    "existing_sha256": d.existing_sha256,
                    "incoming_sha256": d.incoming_sha256,
                    "incoming_address_uuid": d.incoming_address_uuid,
                }
                for d in self.divergences
            ],
        }
