import json
from pathlib import Path
import asyncio
from unittest.mock import patch, AsyncMock
import canon_store.paper as paper_module
import canon_store.prompts as prompts_module


def test_run_atoms_writes_output(tmp_path):
    paper_module.CANON_STORE_ROOT = tmp_path
    prompts_module.CANON_STORE_ROOT = tmp_path

    record = paper_module.create_paper("sources/sample.md", "sha256:abc", title="Sample")
    paper_uuid = record["address"]["uuid"]
    paper_module.save_paper(record)

    source_path = tmp_path / "sources" / "sample.md"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text("This is a sample paper.", encoding="utf-8")

    prompt_dir = tmp_path / "prompts" / "atoms" / "extract-claims"
    prompt_dir.mkdir(parents=True)
    prompt_dir.joinpath("v1.0.0.md").write_text("# ATOMS prompt", encoding="utf-8")

    fake_atoms = {
        "station": "atoms",
        "paper_uuid": paper_uuid,
        "atoms": [
            {
                "identity": {"object_type": "CLAIM"},
                "provenance": {"raw_statement": "God is.", "source_uri": paper_uuid}
            }
        ]
    }

    from stations.atoms.run import run_atoms
    with patch("stations.atoms.run.complete", new=AsyncMock(return_value=(fake_atoms, {"status": "ok", "model": "deepseek-chat"}))):
        run_uuid = "run-test-001"
        asyncio.run(run_atoms(paper_uuid, run_uuid))

    output_path = tmp_path / "runs" / run_uuid / "outputs" / "atoms.json"
    assert output_path.exists()
    data = json.loads(output_path.read_text())
    assert data["station"] == "atoms"
    assert len(data["atoms"]) == 1
