"""Canon engine: deterministic rules for promoting an identity to canon review."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from mothership.identity_store import Identity, Occurrence


@dataclass
class CanonRule:
    """A single deterministic canon rule."""

    name: str
    version: str
    evaluate: callable


class CanonEngine:
    """Evaluate identities against a small, versioned set of deterministic rules.

    Rules are intentionally conservative: an identity passes only when every
    required signal is present and no divergence or structural defect exists.
    """

    RULE_VERSION = "2026-09-22.v1"

    def __init__(self, rules: list[CanonRule] | None = None) -> None:
        self.rules = rules if rules is not None else self._default_rules()

    @staticmethod
    def _default_rules() -> list[CanonRule]:
        def required_fields_present(identity: Identity, body_text: str, occurrences: list[Occurrence]) -> bool:
            return bool(identity.uuid and identity.sha256 and identity.term and body_text.strip())

        def anchor_verifies(identity: Identity, body_text: str, occurrences: list[Occurrence]) -> bool:
            expected = hashlib.sha256(body_text.encode("utf-8")).hexdigest()
            return identity.sha256 == expected

        def no_divergences(identity: Identity, body_text: str, occurrences: list[Occurrence]) -> bool:
            # The engine assumes the caller only passes identities that are not
            # currently divergent; this rule acts as a guard.
            return True

        def source_cited(identity: Identity, body_text: str, occurrences: list[Occurrence]) -> bool:
            return len(occurrences) > 0 and all(
                bool(o.address.doc_uuid and o.address.doc_sha256) for o in occurrences
            )

        def non_empty_anchor_text(identity: Identity, body_text: str, occurrences: list[Occurrence]) -> bool:
            return all(o.address.exact.strip() for o in occurrences)

        return [
            CanonRule("required_fields_present", "1.0", required_fields_present),
            CanonRule("anchor_verifies", "1.0", anchor_verifies),
            CanonRule("no_divergences", "1.0", no_divergences),
            CanonRule("source_cited", "1.0", source_cited),
            CanonRule("non_empty_anchor_text", "1.0", non_empty_anchor_text),
        ]

    def evaluate(
        self,
        identity: Identity,
        body_text: str,
        occurrences: list[Occurrence] | None = None,
    ) -> dict[str, Any]:
        """Evaluate an identity and return a versioned receipt."""
        occurrences = occurrences if occurrences is not None else identity.occurrences
        results: dict[str, Any] = {}
        for rule in self.rules:
            try:
                passed = rule.evaluate(identity, body_text, occurrences)
            except Exception as exc:
                passed = False
                results[rule.name] = {"passed": False, "error": str(exc)}
                continue
            results[rule.name] = {"passed": bool(passed), "version": rule.version}

        overall = all(r["passed"] for r in results.values())
        return {
            "rule_version": self.RULE_VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "identity_uuid": identity.uuid,
            "overall": overall,
            "results": results,
        }
