import json
from pathlib import Path

import pytest

from mothership.api import MothershipAPI


def test_status_counts(tmp_path: Path) -> None:
    api = MothershipAPI(tmp_path)
    (tmp_path / "pills").mkdir()
    (tmp_path / "pills" / "p1.pill.yaml").write_text(
        "---\nface:\n  uuid: u1\n  term: x\nveins: {}\n", encoding="utf-8"
    )
    (tmp_path / "companions").mkdir()
    (tmp_path / "companions" / "index.json").write_text(
        json.dumps([{"paper_uuid": "16166191"}]), encoding="utf-8"
    )
    status = api.status()
    assert status["pills"] == 1
    assert status["companions"] == 1


def test_list_and_get_pill(tmp_path: Path) -> None:
    api = MothershipAPI(tmp_path)
    (tmp_path / "pills" / "a").mkdir(parents=True)
    (tmp_path / "pills" / "a" / "p1.pill.yaml").write_text(
        "---\nface:\n  uuid: abc-123\n  term: coherence\nveins:\n  x: 1\n",
        encoding="utf-8",
    )
    faces = api.list_pills()
    assert len(faces) == 1
    assert faces[0]["uuid"] == "abc-123"

    pill = api.get_pill("abc-123")
    assert pill is not None
    assert pill["face"]["term"] == "coherence"
    assert pill["veins"]["x"] == 1

    assert api.get_pill("missing") is None


def test_list_and_get_companion(tmp_path: Path) -> None:
    api = MothershipAPI(tmp_path)
    (tmp_path / "companions").mkdir(parents=True)
    (tmp_path / "companions" / "16166191_test.md").write_text(
        "---\npaper_uuid: '16166191'\ntitle: Test\n---\n\n# Body\n", encoding="utf-8"
    )
    (tmp_path / "companions" / "index.json").write_text(
        json.dumps([{"paper_uuid": "16166191", "title": "Test"}]), encoding="utf-8"
    )

    index = api.list_companions()
    assert len(index) == 1
    assert index[0]["paper_uuid"] == "16166191"

    comp = api.get_companion("16166191")
    assert comp is not None
    assert comp["front_matter"]["title"] == "Test"
    assert "# Body" in comp["body"]

    assert api.get_companion("99999") is None


def test_resolve_address_resolved(tmp_path: Path) -> None:
    api = MothershipAPI(tmp_path)
    doc = "The wrapper is outside the product."
    import hashlib

    sha = hashlib.sha256("The wrapper is outside the product.".encode("utf-8")).hexdigest()
    addr = {
        "uuid": "u1",
        "target_type": "claim",
        "locator": {"section_path": [0], "offsets": [0, 35]},
        "anchor": {
            "exact": "The wrapper is outside the product.",
            "prefix": "",
            "suffix": "",
            "sha256": sha,
        },
        "source": {"doc_uuid": "d1", "doc_sha256": "h1"},
    }
    result = api.resolve_address(addr, doc)
    assert result["status"] == "resolved"


def test_resolve_address_lost(tmp_path: Path) -> None:
    api = MothershipAPI(tmp_path)
    addr = {
        "uuid": "u1",
        "target_type": "claim",
        "locator": {"section_path": [0], "offsets": [0, 10]},
        "anchor": {
            "exact": "missing text",
            "prefix": "",
            "suffix": "",
            "sha256": "badhash",
        },
        "source": {"doc_uuid": "d1", "doc_sha256": "h1"},
    }
    result = api.resolve_address(addr, "completely different content")
    assert result["status"] == "lost"


def test_get_body(tmp_path: Path) -> None:
    api = MothershipAPI(tmp_path)
    (tmp_path / "bodies").mkdir(parents=True)
    (tmp_path / "bodies" / "abc").write_text("body text", encoding="utf-8")
    assert api.get_body("abc") == "body text"
    assert api.get_body("missing") is None


def test_curator_build_next_runs(tmp_path: Path) -> None:
    api = MothershipAPI(tmp_path)
    (tmp_path / "pills").mkdir(parents=True)
    (tmp_path / "pills" / "p1.pill.yaml").write_text(
        "---\nface:\n  uuid: u1\n  target_type: definition\n  term: coherence\nveins: {}\n",
        encoding="utf-8",
    )
    # No address maps => extract + define proposals.
    proposals = api.curator_build_next()
    assert isinstance(proposals, list)
    types = {p["type"] for p in proposals}
    assert "extract" in types
    assert "define" in types


def test_canon_evaluate(tmp_path: Path) -> None:
    api = MothershipAPI(tmp_path)
    pill = {
        "face": {"uuid": "u1", "term": "x", "status": "candidate"},
        "veins": {"source": {"exactShortQuotation": "q", "authoritativeSourceURL": "http://x"}},
    }
    receipt = api.canon_evaluate(pill)
    assert receipt["overall"] in ("PASS", "FAIL")
    assert "results" in receipt
