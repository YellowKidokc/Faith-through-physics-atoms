"""Tests for the CKG companion publisher."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

import pytest
import yaml

from tools.publish_companion import (
    PROJECT_NAMESPACE,
    STATUS_VOCABULARY,
    CompanionValidationError,
    _ensure_paper_uuid,
    _mint_claim_uuids,
    _sluggify,
    _split_front_matter,
    publish_companion,
)


def _make_minimal_front_matter(**overrides: object) -> dict[str, object]:
    """Return a valid minimal front matter dict for testing."""
    front_matter: dict[str, object] = {
        "type": "axiom_companion",
        "title": "The Temporal Direction Insight",
        "clean_title": "The Temporal Direction Insight",
        "paper_uuid": "16166191",
        "status": "CANDIDATE_DRAFT",
        "one_sentence_finding": "GR/QM unification requires a boundary operator.",
        "claim_ids": ["temporal_direction_breakthrough-C001"],
        "score_total": 71,
        "score_ceiling": 100,
        "score_class": "CANDIDATE",
        "build_next": "Formalize the Bool -> Hilbert bridge.",
    }
    for section in range(1, 11):
        front_matter[f"s{section:02d}_pos"] = 8
        front_matter[f"s{section:02d}_neg"] = 0
        front_matter[f"s{section:02d}_net"] = 8
        front_matter[f"s{section:02d}_ceiling"] = 10
    front_matter.update(overrides)
    return front_matter


def _write_companion(path: Path, front_matter: dict[str, object], body: str = "") -> None:
    """Write a companion file using fenced YAML front matter."""
    yaml_text = yaml.safe_dump(front_matter, sort_keys=False, allow_unicode=True)
    text = f"```yaml\n---\n{yaml_text}---\n```\n\n{body}"
    path.write_text(text, encoding="utf-8")


def test_split_front_matter_fenced(tmp_path: Path) -> None:
    source = tmp_path / "companion.md"
    _write_companion(source, {"title": "Test"}, "## Body\n\nHello.")

    front_matter, body = _split_front_matter(source.read_text(encoding="utf-8"))

    assert front_matter["title"] == "Test"
    assert "## Body" in body
    assert "Hello." in body


def test_split_front_matter_bare(tmp_path: Path) -> None:
    source = tmp_path / "companion.md"
    yaml_text = yaml.safe_dump({"title": "Bare"}, allow_unicode=True)
    source.write_text(f"---\n{yaml_text}---\n\n## Body\n", encoding="utf-8")

    front_matter, body = _split_front_matter(source.read_text(encoding="utf-8"))

    assert front_matter["title"] == "Bare"
    assert "## Body" in body


def test_sluggify() -> None:
    assert _sluggify("The Temporal Direction Insight") == "the_temporal_direction_insight"
    assert _sluggify("  What's   New? ") == "what_s_new"
    assert _sluggify("---leading---") == "leading"


def test_mint_claim_uuids_preserves_existing() -> None:
    existing_uuid = "existing-uuid-1234"
    front_matter = {
        "claim_ids": ["c1", "c2"],
        "claim_uuids": {"c1": existing_uuid},
    }
    claim_uuids, minted = _mint_claim_uuids(front_matter)

    assert minted == 1
    assert claim_uuids["c1"] == existing_uuid
    assert claim_uuids["c2"] == str(uuid.uuid5(PROJECT_NAMESPACE, "c2"))


def test_mint_claim_uuids_rejects_bad_types() -> None:
    with pytest.raises(CompanionValidationError):
        _mint_claim_uuids({"claim_ids": [1, 2, 3]})


def test_ensure_paper_uuid_existing() -> None:
    paper_uuid, minted = _ensure_paper_uuid({"paper_uuid": "abc123"}, Path("x.md"))
    assert paper_uuid == "abc123"
    assert not minted


def test_ensure_paper_uuid_mints_from_title_and_path(tmp_path: Path) -> None:
    source = tmp_path / "input.md"
    paper_uuid, minted = _ensure_paper_uuid({"title": "Test Title"}, source)
    assert minted
    expected = str(uuid.uuid5(PROJECT_NAMESPACE, f"Test Title:{source.resolve().as_posix()}"))
    assert paper_uuid == expected


def test_publish_companion_with_example(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "companions"
    input_dir.mkdir()

    front_matter = _make_minimal_front_matter()
    body = "## SCORECARD\n\n| S01 | ... |\n\n## S01 · Test\n"
    source = input_dir / "TEMPORAL_DIRECTION_BREAKTHROUGH.md"
    _write_companion(source, front_matter, body)

    result = publish_companion(source, output_dir)

    assert result.output_path.exists()
    assert result.paper_uuid == "16166191"
    assert result.title == "The Temporal Direction Insight"
    assert result.status == "CANDIDATE_DRAFT"
    assert len(result.claim_ids) == 1

    written_text = result.output_path.read_text(encoding="utf-8")
    assert written_text.startswith("---\n")
    written_front_matter, written_body = _split_front_matter(written_text)
    assert written_front_matter["paper_uuid"] == "16166191"
    assert "claim_uuids" in written_front_matter
    assert "_claim_uuids_minted" in written_front_matter
    assert "## SCORECARD" in written_body

    index_path = output_dir / "index.json"
    assert index_path.exists()
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert len(index) == 1
    assert index[0]["paper_uuid"] == "16166191"
    assert index[0]["path"] == "companions/16166191_the_temporal_direction_insight.md"


def test_publish_companion_mints_missing_paper_uuid(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "companions"
    input_dir.mkdir()

    front_matter = _make_minimal_front_matter()
    del front_matter["paper_uuid"]
    source = input_dir / "missing_uuid.md"
    _write_companion(source, front_matter, "## Body\n")

    result = publish_companion(source, output_dir)

    assert result.paper_uuid_minted
    assert result.output_path.name.startswith(result.paper_uuid)


def test_publish_companion_normalizes_filename(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "companions"
    input_dir.mkdir()

    front_matter = _make_minimal_front_matter(
        paper_uuid="999",
        clean_title="What's New?!",
    )
    source = input_dir / "source.md"
    _write_companion(source, front_matter, "## Body\n")

    result = publish_companion(source, output_dir)

    assert result.output_path.name == "999_what_s_new.md"


def test_publish_companion_rejects_missing_required_fields(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "companions"
    input_dir.mkdir()

    front_matter = _make_minimal_front_matter()
    del front_matter["score_total"]
    del front_matter["build_next"]
    source = input_dir / "bad.md"
    _write_companion(source, front_matter, "## Body\n")

    with pytest.raises(CompanionValidationError) as exc_info:
        publish_companion(source, output_dir)

    message = str(exc_info.value)
    assert "Missing required field: score_total" in message
    assert "Missing required field: build_next" in message


def test_publish_companion_rejects_invalid_status(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "companions"
    input_dir.mkdir()

    front_matter = _make_minimal_front_matter(status="NOT_A_STATUS")
    source = input_dir / "bad_status.md"
    _write_companion(source, front_matter, "## Body\n")

    with pytest.raises(CompanionValidationError) as exc_info:
        publish_companion(source, output_dir)

    assert "Invalid status 'NOT_A_STATUS'" in str(exc_info.value)
    assert all(s in str(exc_info.value) for s in STATUS_VOCABULARY)


def test_publish_companion_rejects_score_total_above_ceiling(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "companions"
    input_dir.mkdir()

    front_matter = _make_minimal_front_matter(score_total=101, score_ceiling=100)
    source = input_dir / "bad_score.md"
    _write_companion(source, front_matter, "## Body\n")

    with pytest.raises(CompanionValidationError) as exc_info:
        publish_companion(source, output_dir)

    assert "score_total cannot exceed score_ceiling" in str(exc_info.value)


def test_publish_companion_updates_existing_index(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "companions"
    input_dir.mkdir()
    output_dir.mkdir()

    existing_index = [{"paper_uuid": "old", "title": "Old"}]
    (output_dir / "index.json").write_text(json.dumps(existing_index), encoding="utf-8")

    front_matter = _make_minimal_front_matter(paper_uuid="16166191")
    source = input_dir / "companion.md"
    _write_companion(source, front_matter, "## Body\n")

    publish_companion(source, output_dir)

    index = json.loads((output_dir / "index.json").read_text(encoding="utf-8"))
    assert len(index) == 2
    assert any(e["paper_uuid"] == "old" for e in index)
    assert any(e["paper_uuid"] == "16166191" for e in index)


def test_publish_companion_does_not_modify_input(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "companions"
    input_dir.mkdir()

    front_matter = _make_minimal_front_matter()
    source = input_dir / "companion.md"
    _write_companion(source, front_matter, "## Body\n")
    original_text = source.read_text(encoding="utf-8")

    publish_companion(source, output_dir)

    assert source.read_text(encoding="utf-8") == original_text
