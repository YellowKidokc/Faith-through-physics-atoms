import json
import uuid
from pathlib import Path
from jsonschema import validate

CANON_STORE_ROOT = Path("canon-store")
SCHEMA_PATH = Path("schemas/paper-record-v1.schema.json")


def _schema():
    return json.loads(SCHEMA_PATH.read_text())


def _paper_path(paper_uuid: str) -> Path:
    return CANON_STORE_ROOT / "papers" / f"{paper_uuid}.json"


def load_paper(paper_uuid: str) -> dict:
    path = _paper_path(paper_uuid)
    if not path.exists():
        raise FileNotFoundError(f"paper not found: {paper_uuid}")
    record = json.loads(path.read_text())
    validate(instance=record, schema=_schema())
    return record


def save_paper(record: dict) -> Path:
    validate(instance=record, schema=_schema())
    paper_uuid = record["address"]["uuid"]
    path = _paper_path(paper_uuid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return path


def create_paper(source_path: str, source_sha256: str, title: str = "", author: str = "") -> dict:
    paper_uuid = str(uuid.uuid4())
    return {
        "address": {"uuid": paper_uuid, "handle": f"paper/{Path(source_path).stem}", "type": "paper"},
        "source": {"path": source_path, "sha256": source_sha256},
        "metadata": {"title": title, "author": author, "domain": "", "series": ""},
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
