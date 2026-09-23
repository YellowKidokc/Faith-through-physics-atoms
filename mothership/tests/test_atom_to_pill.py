"""Tests for the atom-to-pill converter."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

import yaml

from tools.atom_to_pill import (
    PROJECT_NAMESPACE,
    convert_atom,
    run_conversion,
)


def test_convert_atom_with_existing_uuid(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    atom = {
        "uuid": "existing-uuid-1234",
        "nodeID": "node-1",
        "claimID": "claim-1",
        "name": "Test Claim",
        "term": "test-term",
        "plain": "A plain statement.",
        "status": "candidate",
        "target_type": "claim",
        "extra_field": "should go to veins",
    }
    source = input_dir / "test.jsonld"
    source.write_text(json.dumps(atom), encoding="utf-8")

    output_path, was_minted, errors = convert_atom(source, input_dir, output_dir)

    assert not errors
    assert output_path is not None
    assert not was_minted
    assert output_path.exists()

    pill = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert pill["face"]["uuid"] == "existing-uuid-1234"
    assert pill["face"]["term"] == "test-term"
    assert pill["face"]["plain"] == "A plain statement."
    assert pill["veins"]["extra_field"] == "should go to veins"
    assert "_metadata" in pill
    assert pill["_metadata"]["source_path"] == "test.jsonld"
    assert "sha256" in pill["_metadata"]


def test_convert_atom_without_uuid_mints_stable_uuid(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    atom = {
        "nodeID": "stable-node-id",
        "name": "No UUID Atom",
        "target_type": "axiom",
    }
    source = input_dir / "no_uuid.jsonld"
    source.write_text(json.dumps(atom), encoding="utf-8")

    output_path, was_minted, errors = convert_atom(source, input_dir, output_dir)

    assert not errors
    assert output_path is not None
    assert was_minted

    pill = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    expected_uuid = str(uuid.uuid5(PROJECT_NAMESPACE, "stable-node-id"))
    assert pill["face"]["uuid"] == expected_uuid
    assert pill["face"]["target_type"] == "axiom"


def test_run_conversion_skips_forbidden_directories(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    (input_dir / "valid.jsonld").write_text(json.dumps({"uuid": "existing-uuid-a", "name": "Valid"}), encoding="utf-8")

    skip_dir = input_dir / "__pycache__"
    skip_dir.mkdir()
    (skip_dir / "hidden.jsonld").write_text(json.dumps({"uuid": "b", "name": "Hidden"}), encoding="utf-8")

    summary = run_conversion(input_dir, output_dir)

    assert summary["pills_created"] == 1
    assert summary["uuids_minted"] == 0
    assert not summary["errors"]


def test_run_conversion_preserves_directory_structure(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    sub = input_dir / "definitions" / "atoms"
    sub.mkdir(parents=True)

    (sub / "DEF-0001.jsonld").write_text(
        json.dumps({"uuid": "def-1", "canonical_term": "coherence", "plain_definition": "parts fit"}),
        encoding="utf-8",
    )

    summary = run_conversion(input_dir, output_dir)

    assert summary["pills_created"] == 1
    expected = output_dir / "definitions" / "atoms" / "DEF-0001.pill.yaml"
    assert expected.exists()

    pill = yaml.safe_load(expected.read_text(encoding="utf-8"))
    assert pill["face"]["term"] == "coherence"
    assert pill["face"]["plain"] == "parts fit"
