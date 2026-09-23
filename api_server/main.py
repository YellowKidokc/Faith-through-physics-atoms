import os
import sys
import threading
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import canon_store.paper as paper_module
from canon_store.paper import load_paper
from api_server.runner import spawn_station, new_run_id, write_run_inputs

paper_module.CANON_STORE_ROOT = Path(os.environ.get("CANON_STORE_ROOT", "canon-store"))

app = FastAPI(title="Canon Workbench API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_runs: dict[str, dict[str, Any]] = {}
active_lock = threading.Lock()


class RunRequest(BaseModel):
    paper_uuid: str
    stations: list[str]
    provider: str = "deepseek"


def _run_worker(run_id: str, paper_uuid: str, stations: list[str], provider: str):
    try:
        for station in stations:
            with active_lock:
                if run_id not in active_runs:
                    return
                active_runs[run_id]["current_station"] = station
                active_runs[run_id]["status"] = "running"

            proc = spawn_station(project_root, run_id, paper_uuid, station, provider)
            with active_lock:
                if run_id in active_runs:
                    active_runs[run_id]["process"] = proc

            # Stream stdout until process exits
            if proc.stdout:
                for line in proc.stdout:
                    with active_lock:
                        if run_id in active_runs:
                            active_runs[run_id]["logs"].append(line.rstrip())

            proc.wait()

            with active_lock:
                if run_id not in active_runs:
                    return
                if proc.returncode != 0:
                    active_runs[run_id]["status"] = "failed"
                    active_runs[run_id]["exit_code"] = proc.returncode
                    return

        with active_lock:
            if run_id in active_runs:
                active_runs[run_id]["status"] = "completed"
    except Exception as e:
        with active_lock:
            if run_id in active_runs:
                active_runs[run_id]["status"] = "failed"
                active_runs[run_id]["error"] = str(e)


@app.get("/api/status")
def status():
    with active_lock:
        runs = [dict(run_id=k, **{key: v for key, v in v.items() if key != "process" and key != "logs"}) for k, v in active_runs.items()]
    return {"ok": True, "active_runs": runs}


@app.get("/api/papers")
def list_papers():
    papers_dir = paper_module.CANON_STORE_ROOT / "papers"
    papers = []
    if papers_dir.exists():
        for path in papers_dir.glob("*.json"):
            papers.append({"uuid": path.stem})
    return {"papers": papers}


@app.get("/api/paper/{paper_uuid}")
def get_paper(paper_uuid: str):
    try:
        return load_paper(paper_uuid)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="paper not found")


@app.post("/api/run")
def start_run(req: RunRequest):
    paper_uuid = req.paper_uuid
    stations = req.stations
    provider = req.provider

    if not paper_uuid or not stations:
        raise HTTPException(status_code=400, detail="paper_uuid and stations are required")

    run_id = new_run_id()
    write_run_inputs(paper_module.CANON_STORE_ROOT, run_id, paper_uuid, stations, provider)

    with active_lock:
        active_runs[run_id] = {
            "run_id": run_id,
            "paper_uuid": paper_uuid,
            "current_station": stations[0] if stations else "",
            "status": "queued",
            "provider": provider,
            "stations": stations,
            "logs": [],
        }

    thread = threading.Thread(
        target=_run_worker,
        args=(run_id, paper_uuid, stations, provider),
        daemon=True,
    )
    thread.start()

    return {
        "run_id": run_id,
        "status": "queued",
        "paper_uuid": paper_uuid,
        "stations": stations,
    }


@app.get("/api/run/{run_id}/status")
def run_status(run_id: str):
    with active_lock:
        run = active_runs.get(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="run not found")
        return {
            "run_id": run_id,
            "status": run["status"],
            "current_station": run["current_station"],
            "paper_uuid": run["paper_uuid"],
            "stations": run["stations"],
            "logs": run["logs"][-50:],
        }


@app.post("/api/run/{run_id}/stop")
def stop_run(run_id: str):
    with active_lock:
        run = active_runs.get(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="run not found")
        run["status"] = "cancelled"
        proc = run.get("process")
        if proc is not None and proc.poll() is None:
            proc.terminate()

    return {"run_id": run_id, "status": "cancelled"}


@app.get("/api/runs")
def list_runs():
    with active_lock:
        return {
            "runs": [
                {
                    "run_id": k,
                    "status": v["status"],
                    "current_station": v["current_station"],
                    "paper_uuid": v["paper_uuid"],
                    "stations": v["stations"],
                }
                for k, v in active_runs.items()
            ]
        }
