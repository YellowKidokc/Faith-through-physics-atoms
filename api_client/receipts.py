import json
import hashlib
import uuid
from datetime import datetime, timezone
from pathlib import Path

RECEIPT_DIR = Path("canon-store/runs")


def write_receipt(run_uuid: str, receipt: dict) -> Path:
    path = RECEIPT_DIR / run_uuid / "receipts"
    path.mkdir(parents=True, exist_ok=True)
    filename = f"{receipt['request_id']}.json"
    (path / filename).write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return path / filename


def new_request_id() -> str:
    return str(uuid.uuid4())


def text_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
