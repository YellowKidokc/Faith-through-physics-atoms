"""Tests for the mothership prototype."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from mothership.address import Address, Resolution, resolve_address
from mothership.canon_engine import CanonEngine
from mothership.delta import compute_touched_addresses
from mothership.identity_store import Divergence, IdentityStore
from mothership.mothership import Mothership


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _address(exact: str, offsets: tuple[int, int] = (0, 0)) -> Address:
    return Address(
        uuid="addr-test",
        handle="TEST/CLAIM/§1",
        target_type="claim",
        section_path=(1,),
        offsets=offsets,
        exact=exact,
        prefix="prefix ",
        suffix=" suffix",
        sha256=_sha256(exact),
        doc_uuid="doc-test",
        doc_sha256="sha-test",
    )


class TestDedupe:
    def test_identical_exact_text_reuses_identity(self) -> None:
        store = IdentityStore()
        body = "Same body text."
        addr1 = _address(body, (0, len(body)))
        addr2 = _address(body, (0, len(body)))
        addr2 = addr2.with_locator((2,), (0, len(body)))

        uuid1 = store.ingest("term-a", addr1, body)
        uuid2 = store.ingest("term-a", addr2, body)

        assert uuid1 == uuid2
        assert len(store.identities) == 1
        assert len(store.occurrences) == 2

    def test_different_exact_text_creates_distinct_identities(self) -> None:
        store = IdentityStore()
        body_a = "Body A."
        body_b = "Body B."
        uuid_a = store.ingest("term-a", _address(body_a, (0, len(body_a))), body_a)
        uuid_b = store.ingest("term-b", _address(body_b, (0, len(body_b))), body_b)

        assert uuid_a != uuid_b
        assert len(store.identities) == 2


class TestDivergence:
    def test_same_term_different_sha256_raises_and_records(self) -> None:
        store = IdentityStore()
        body_a = "Alpha meaning."
        body_b = "Beta meaning."
        store.ingest("shared-term", _address(body_a), body_a)

        with pytest.raises(Divergence):
            store.ingest("shared-term", _address(body_b), body_b)

        assert len(store.divergences) == 1
        record = store.divergences[0]
        assert record.term == "shared-term"
        assert record.existing_sha256 == _sha256(body_a)
        assert record.incoming_sha256 == _sha256(body_b)


class TestResolutionWaterfall:
    def test_resolved_when_lasers_and_sha256_match(self) -> None:
        doc = "The universe is not a closed mechanical clock."
        addr = _address(doc, (0, len(doc)))
        result = resolve_address(addr, doc)
        assert result["status"] == Resolution.RESOLVED.value

    def test_re_aimed_when_offsets_drift(self) -> None:
        doc = "The universe is not a closed mechanical clock."
        # Original document had a leading space, new document does not.
        addr = _address(doc, (1, len(doc) + 1))
        result = resolve_address(addr, doc)
        assert result["status"] == Resolution.RE_AIMED.value
        assert result["address"].offsets == (0, len(doc))

    def test_lost_when_anchor_missing(self) -> None:
        doc = "Totally unrelated content."
        addr = _address("The universe is not a closed mechanical clock.", (0, 46))
        result = resolve_address(addr, doc)
        assert result["status"] == Resolution.LOST.value

    def test_moved_or_lost_status_exists(self) -> None:
        # The implementation classifies unrecoverable anchors as lost.
        assert Resolution.MOVED.value == "moved"
        assert Resolution.LOST.value == "lost"


class TestCanonEngine:
    def test_all_rules_pass(self) -> None:
        engine = CanonEngine()
        body = "Well-formed claim body."
        addr = _address(body, (0, len(body)))
        store = IdentityStore()
        identity_uuid = store.ingest("term", addr, body)
        identity = store.get_identity_by_uuid(identity_uuid)
        assert identity is not None

        receipt = engine.evaluate(identity, body)
        assert receipt["overall"] is True
        assert receipt["rule_version"]
        assert receipt["timestamp"]
        for rule_result in receipt["results"].values():
            assert rule_result["passed"] is True

    def test_missing_source_fails(self) -> None:
        engine = CanonEngine()
        body = "Body text."
        addr = Address(
            uuid="addr-test",
            handle="TEST",
            target_type="claim",
            section_path=(1,),
            offsets=(0, len(body)),
            exact=body,
            prefix="",
            suffix="",
            sha256=_sha256(body),
            doc_uuid="",
            doc_sha256="",
        )
        store = IdentityStore()
        identity_uuid = store.ingest("term", addr, body)
        identity = store.get_identity_by_uuid(identity_uuid)
        assert identity is not None

        receipt = engine.evaluate(identity, body)
        assert receipt["overall"] is False
        assert receipt["results"]["source_cited"]["passed"] is False


class TestDelta:
    def test_touches_address_in_changed_range(self) -> None:
        old = "The universe is not a closed mechanical clock."
        new = "The universe is not a closed mechanical watch."
        addr = _address("closed mechanical clock", (15, 38))
        touched = compute_touched_addresses(old, new, [addr])
        assert len(touched) == 1

    def test_ignores_unchanged_address(self) -> None:
        old = "First sentence. The universe is not a closed mechanical clock. Last sentence."
        new = "First sentence. The universe is not a closed mechanical watch. Last sentence."
        addr = _address("First sentence", (0, 14))
        touched = compute_touched_addresses(old, new, [addr])
        assert len(touched) == 0

    def test_prefix_expansion_catches_neighbor_changes(self) -> None:
        old = "We define coherence as parts fitting together."
        new = "We define coherence as parts fighting together."
        addr = _address("coherence as parts fitting together", (10, 43))
        touched = compute_touched_addresses(old, new, [addr])
        assert len(touched) == 1


class TestMothershipScan:
    def test_scan_produces_report(self) -> None:
        sample = Path(__file__).parent / "sample_data"
        mothership = Mothership()
        report = mothership.scan(sample, sample / "bodies")

        data = report.to_dict()
        assert data["linked_occurrences"] == 4
        # Four distinct bodies => four identities.
        assert len(data["new_identities"]) == 4
        # Three different grace-claim bodies => two divergences after first.
        assert len(data["divergences"]) == 2
        assert data["resolution_summary"][Resolution.RESOLVED.value] == 4

        pr_text = report.to_pr_text()
        assert "Mothership Nightly Report" in pr_text
        assert "Divergences requiring review" in pr_text

    def test_report_json_roundtrips(self) -> None:
        sample = Path(__file__).parent / "sample_data"
        report = Mothership().scan(sample, sample / "bodies")
        loaded = json.loads(report.to_json())
        assert loaded["linked_occurrences"] == report.linked_occurrences
        assert len(loaded["new_identities"]) == len(report.new_identities)
