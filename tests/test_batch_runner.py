import json
from pathlib import Path
import asyncio
from unittest.mock import patch, AsyncMock
import canon_store.paper as paper_module
import canon_store.prompts as prompts_module


def test_ingest_paper_from_inbox(monkeypatch, tmp_path):
    import batch_runner

    monkeypatch.setattr(paper_module, "CANON_STORE_ROOT", tmp_path)
    monkeypatch.setattr(prompts_module, "CANON_STORE_ROOT", tmp_path)

    inbox = tmp_path / "inbox"
    inbox.mkdir()
    source = inbox / "Sample Paper.md"
    source.write_text("# Sample Paper\n\nThis is the content.", encoding="utf-8")

    paper_uuid = batch_runner.ingest_source(source)

    assert (tmp_path / "sources" / f"{paper_uuid}.md").exists()
    record = paper_module.load_paper(paper_uuid)
    assert record["metadata"]["title"] == "Sample Paper"


def test_batch_run_atoms_on_ingested_paper(monkeypatch, tmp_path):
    import batch_runner

    monkeypatch.setattr(paper_module, "CANON_STORE_ROOT", tmp_path)
    monkeypatch.setattr(prompts_module, "CANON_STORE_ROOT", tmp_path)

    inbox = tmp_path / "inbox"
    inbox.mkdir()
    source = inbox / "Sample Paper.md"
    source.write_text("# Sample Paper\n\nThis is the content.", encoding="utf-8")

    prompt_dir = tmp_path / "prompts" / "atoms" / "extract-claims"
    prompt_dir.mkdir(parents=True)
    prompt_dir.joinpath("v1.0.0.md").write_text("# ATOMS prompt", encoding="utf-8")

    paper_uuid = batch_runner.ingest_source(source)

    fake_atoms = {
        "station": "atoms",
        "paper_uuid": paper_uuid,
        "atoms": [
            {"identity": {"object_type": "CLAIM"}, "provenance": {"raw_statement": "God is."}}
        ]
    }

    with patch("stations.atoms.run.complete", new=AsyncMock(return_value=(fake_atoms, {"status": "ok", "model": "deepseek-chat"}))):
        asyncio.run(batch_runner.run_station_on_paper(paper_uuid, "atoms", provider="deepseek"))

    record = paper_module.load_paper(paper_uuid)
    assert len(record["extracted"]["atoms"]) == 1
    assert record["runs"]
