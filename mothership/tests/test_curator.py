"""Tests for the CuratorPass proposal generator."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml

from mothership.address import Address
from mothership.curator import CURATOR_VERSION, RULE_VERSION, CuratorConfig, CuratorPass
from mothership.identity_store import IdentityStore


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _address(exact: str, doc_uuid: str, offsets: tuple[int, int]) -> Address:
    return Address(
        uuid=f"addr-{doc_uuid}-{hash(exact) & 0xffffffff}",
        handle="TEST",
        target_type="claim",
        section_path=(1,),
        offsets=offsets,
        exact=exact,
        prefix="",
        suffix="",
        sha256=_sha256(exact),
        doc_uuid=doc_uuid,
        doc_sha256="sha-test",
    )


@pytest.fixture
def sample_corpus(tmp_path: Path):
    """Build a minimal pill/address/body corpus for curator tests."""
    pills_dir = tmp_path / "pills"
    maps_dir = tmp_path / "maps"
    bodies_dir = tmp_path / "bodies"
    pills_dir.mkdir()
    maps_dir.mkdir()
    bodies_dir.mkdir()

    # Pill with a resolved address.
    grace_pill = {
        "face": {
            "uuid": "pill-grace",
            "term": "grace-claim",
            "target_type": "claim",
            "name": "Grace Claim",
            "source": {"doc_uuid": "doc-a", "doc_sha256": "sha-test"},
        },
        "veins": {"dependencies": ["pill-coherence"]},
    }
    # Definition pill.
    coherence_pill = {
        "face": {
            "uuid": "pill-coherence",
            "term": "coherence",
            "target_type": "definition",
            "name": "Coherence",
            "source": {"doc_uuid": "doc-a", "doc_sha256": "sha-test"},
        },
        "veins": {},
    }
    # Pill with no address -> extract.
    orphan_pill = {
        "face": {
            "uuid": "pill-orphan",
            "term": "orphan",
            "target_type": "claim",
        },
        "veins": {},
    }
    # Pill with kill condition -> test.
    kill_pill = {
        "face": {
            "uuid": "pill-kill",
            "term": "falsifiable",
            "target_type": "claim",
            "source": {"doc_uuid": "doc-b", "doc_sha256": "sha-test"},
        },
        "veins": {"falsificationCondition": "counter-example exists"},
    }

    for name, pill in [
        ("grace.pill.yaml", grace_pill),
        ("coherence.pill.yaml", coherence_pill),
        ("orphan.pill.yaml", orphan_pill),
        ("kill.pill.yaml", kill_pill),
    ]:
        with (pills_dir / name).open("w", encoding="utf-8") as fh:
            yaml.safe_dump(pill, fh)

    # Address maps.
    grace_addr = _address("The universe is not a closed mechanical clock.", "doc-a", (0, 46))
    coherence_addr = _address("Coherence means parts fit together.", "doc-a", (0, 35))
    with (maps_dir / "doc-a.jsonl").open("w", encoding="utf-8") as fh:
        fh.write(json.dumps(grace_addr.to_dict()) + "\n")
        fh.write(json.dumps(coherence_addr.to_dict()) + "\n")

    # doc-c has an address map but no pills -> cover.
    extra_addr = _address("Extra document content.", "doc-c", (0, 23))
    with (maps_dir / "doc-c.jsonl").open("w", encoding="utf-8") as fh:
        fh.write(json.dumps(extra_addr.to_dict()) + "\n")

    # Bodies.
    for addr in (grace_addr, coherence_addr, extra_addr):
        (bodies_dir / addr.sha256).write_text(addr.exact, encoding="utf-8")

    # Identity store with a divergence on grace-claim.
    store = IdentityStore()
    body_a = "The universe is not a closed mechanical clock."
    body_b = "A second occurrence of grace."
    store.ingest("grace-claim", _address(body_a, "doc-a", (0, len(body_a))), body_a)
    with pytest.raises(Exception):
        store.ingest("grace-claim", _address(body_b, "doc-b", (0, len(body_b))), body_b)

    return pills_dir, maps_dir, store, bodies_dir


class TestCuratorProposals:
    def test_diverge_proposal(self, sample_corpus):
        pills_dir, maps_dir, store, bodies_dir = sample_corpus
        curator = CuratorPass(pills_dir, maps_dir, store, bodies_dir)
        proposals = curator.run()

        diverge = [p for p in proposals if p["type"] == "diverge"]
        assert len(diverge) == 1
        assert diverge[0]["priority"] == 1
        assert diverge[0]["status"] == "proposed"
        assert diverge[0]["receipt"]["curator_version"] == CURATOR_VERSION
        assert diverge[0]["receipt"]["rule_version"] == RULE_VERSION

    def test_test_proposal(self, sample_corpus):
        pills_dir, maps_dir, store, bodies_dir = sample_corpus
        proposals = CuratorPass(pills_dir, maps_dir, store, bodies_dir).run()

        test = [p for p in proposals if p["type"] == "test"]
        assert len(test) == 1
        assert "pill-kill" in test[0]["targets"]
        assert test[0]["priority"] == 2

    def test_extract_proposal_for_orphan(self, sample_corpus):
        pills_dir, maps_dir, store, bodies_dir = sample_corpus
        proposals = CuratorPass(pills_dir, maps_dir, store, bodies_dir).run()

        extract = [p for p in proposals if p["type"] == "extract"]
        assert any("pill-orphan" in p["targets"] for p in extract)
        assert all(p["priority"] == 3 for p in extract)

    def test_define_proposal(self, sample_corpus):
        pills_dir, maps_dir, store, bodies_dir = sample_corpus
        proposals = CuratorPass(pills_dir, maps_dir, store, bodies_dir).run()

        define = [p for p in proposals if p["type"] == "define"]
        assert any(p["targets"] == ["pill-coherence"] for p in define)

    def test_link_proposal_from_shared_term(self, sample_corpus):
        pills_dir, maps_dir, store, bodies_dir = sample_corpus
        proposals = CuratorPass(pills_dir, maps_dir, store, bodies_dir).run()

        link = [p for p in proposals if p["type"] == "link"]
        # grace pill depends on coherence pill, but no explicit edge recorded.
        assert any("pill-grace" in p["targets"] and "pill-coherence" in p["targets"] for p in link)

    def test_cover_proposal(self, sample_corpus):
        pills_dir, maps_dir, store, bodies_dir = sample_corpus
        proposals = CuratorPass(pills_dir, maps_dir, store, bodies_dir).run()

        cover = [p for p in proposals if p["type"] == "cover"]
        assert any("doc-c" in p["targets"] for p in cover)

    def test_ranking_order(self, sample_corpus):
        pills_dir, maps_dir, store, bodies_dir = sample_corpus
        proposals = CuratorPass(pills_dir, maps_dir, store, bodies_dir).run()

        priorities = [p["priority"] for p in proposals]
        assert priorities == sorted(priorities)
        assert proposals[0]["type"] == "diverge"

    def test_proposal_ids_sequential(self, sample_corpus):
        pills_dir, maps_dir, store, bodies_dir = sample_corpus
        proposals = CuratorPass(pills_dir, maps_dir, store, bodies_dir).run()

        ids = [p["proposal_id"] for p in proposals]
        assert ids == sorted(ids)
        assert ids[0].startswith("PROP-")


class TestCuratorGuards:
    def test_no_writes_to_paper_files(self, tmp_path: Path, sample_corpus):
        pills_dir, maps_dir, store, bodies_dir = sample_corpus
        before = list(maps_dir.rglob("*"))
        CuratorPass(pills_dir, maps_dir, store, bodies_dir).run()
        after = list(maps_dir.rglob("*"))
        assert before == after

    def test_meta_proposal_when_config_incomplete(self, tmp_path: Path):
        pills_dir = tmp_path / "pills"
        maps_dir = tmp_path / "maps"
        bodies_dir = tmp_path / "bodies"
        pills_dir.mkdir()
        maps_dir.mkdir()
        bodies_dir.mkdir()

        config = CuratorConfig(meta_required_keys=("missing_key",))
        curator = CuratorPass(pills_dir, maps_dir, IdentityStore(), bodies_dir, config=config)
        proposals = curator.run()

        meta = [p for p in proposals if p["type"] == "meta"]
        assert len(meta) == 1
        assert "missing_key" in meta[0]["reason"]
