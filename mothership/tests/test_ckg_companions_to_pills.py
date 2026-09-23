"""Tests for tools/ckg_companions_to_pills.py."""

from pathlib import Path

import yaml

from tools.ckg_companions_to_pills import (
    _extract_sections,
    _parse_frontmatter,
    convert_companion,
    run_conversion,
)


SAMPLE_COMPANION = """---
paper_uuid: abc-123
source_path: \\\\server\\share\\paper.md
source_hash: deadbeef
model: deepseek-chat
provider: deepseek
grade: UNSCORED
---

# CKG Companion — abc-123

## Source

```yaml
claims:
  - "claim one"
  - "claim two"
domains:
  Physics: 50
```

## 1. FIRST SECTION

First body.

## 2. SECOND SECTION

Second body with **bold**.
"""


def test_parse_frontmatter():
    front, body = _parse_frontmatter(SAMPLE_COMPANION)
    assert front["paper_uuid"] == "abc-123"
    assert front["grade"] == "UNSCORED"
    assert "# CKG Companion" in body


def test_extract_sections():
    _, body = _parse_frontmatter(SAMPLE_COMPANION)
    sections = _extract_sections(body)
    assert "1. FIRST SECTION" in sections
    assert "2. SECOND SECTION" in sections
    assert "First body." in sections["1. FIRST SECTION"]
    assert "Second body" in sections["2. SECOND SECTION"]


def test_convert_companion(tmp_path: Path):
    input_root = tmp_path / "in"
    output_root = tmp_path / "out"
    input_root.mkdir()
    source = input_root / "abc123.md"
    source.write_text(SAMPLE_COMPANION, encoding="utf-8")

    output_path, errors = convert_companion(source, input_root, output_root)

    assert not errors
    assert output_path is not None
    assert output_path.exists()

    pill = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert pill["face"]["uuid"] == "abc-123"
    assert pill["face"]["target_type"] == "paper_companion"
    assert pill["face"]["status"] == "unscored"
    assert pill["veins"]["source_yaml"]["claims"] == ["claim one", "claim two"]
    assert "1. FIRST SECTION" in pill["veins"]["sections"]


def test_run_conversion(tmp_path: Path):
    input_root = tmp_path / "in"
    output_root = tmp_path / "out"
    input_root.mkdir()
    (input_root / "a.md").write_text(SAMPLE_COMPANION, encoding="utf-8")
    (input_root / "b.md").write_text(SAMPLE_COMPANION.replace("abc-123", "def-456"), encoding="utf-8")

    summary = run_conversion(input_root, output_root)

    assert summary["pills_created"] == 2
    assert not summary["errors"]
    assert (output_root / "a.pill.yaml").exists()
    assert (output_root / "b.pill.yaml").exists()
