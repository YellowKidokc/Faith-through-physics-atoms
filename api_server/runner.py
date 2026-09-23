import json
import subprocess
import sys
import uuid
from pathlib import Path
from datetime import datetime, timezone

from stations.registry import get_station


def spawn_station(
    project_root: Path,
    run_id: str,
    paper_uuid: str,
    station: str,
    provider: str,
) -> subprocess.Popen:
    station_def = get_station(station)
    script = project_root / station_def["script"]
    if not script.exists():
        raise FileNotFoundError(f"station script not found: {script}")

    python = sys.executable
    cmd = [
        python,
        str(script),
        "--paper-uuid", paper_uuid,
        "--run-uuid", run_id,
        "--provider", provider,
    ]
    return subprocess.Popen(
        cmd,
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        creation_flags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
    )


def new_run_id() -> str:
    return f"run_{uuid.uuid4()}"


def write_run_inputs(
    canon_store_root: Path,
    run_id: str,
    paper_uuid: str,
    stations: list[str],
    provider: str,
) -> Path:
    run_dir = canon_store_root / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    inputs = {
        "run_id": run_id,
        "paper_uuid": paper_uuid,
        "stations": stations,
        "provider": provider,
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    (run_dir / "inputs.json").write_text(json.dumps(inputs, indent=2), encoding="utf-8")
    return run_dir
