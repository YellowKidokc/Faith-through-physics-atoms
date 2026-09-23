from pathlib import Path
import json
import canon_store.paper as paper_module


def test_canon_store_directories_exist():
    base = Path("canon-store")
    for sub in [
        "sources",
        "papers",
        "runs",
        "atoms/candidate",
        "atoms/admitted",
        "atoms/rejected",
        "atoms/predicate",
        "predicates",
        "prompts",
        "templates",
    ]:
        assert (base / sub).is_dir(), f"missing {sub}"


def test_load_and_save_paper_record(tmp_path, monkeypatch):
    monkeypatch.setattr(paper_module, "CANON_STORE_ROOT", tmp_path)

    record = {
        "address": {"uuid": "22222222-2222-2222-2222-222222222222", "handle": "paper/temp", "type": "paper"},
        "source": {"path": "sources/temp.md", "sha256": "sha256:abc"},
        "metadata": {"title": "Temp"},
        "runs": [],
        "latest_run": None,
        "extracted": {
            "ckg": {}, "atoms": [], "axiom_nodes": [], "coherence_score": {},
            "fruits": {}, "lean4": {}, "master_equation": {}, "paper_grader": {}, "stories": {}
        },
        "classification": {"type": [], "domain": [], "register": []},
        "canon_status": "candidate",
        "truth_predicates": [],
        "atoms_produced": []
    }

    paper_module.save_paper(record)
    loaded = paper_module.load_paper("22222222-2222-2222-2222-222222222222")
    assert loaded["address"]["uuid"] == record["address"]["uuid"]
    assert (tmp_path / "papers" / "22222222-2222-2222-2222-222222222222.json").exists()
