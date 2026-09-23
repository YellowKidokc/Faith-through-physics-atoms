import json
from pathlib import Path

REGISTRY_PATH = Path("stations/stations.json")


def _registry() -> list[dict]:
    return json.loads(REGISTRY_PATH.read_text())


def list_stations() -> list[dict]:
    return _registry()


def get_station(station_id: str) -> dict:
    for s in _registry():
        if s["id"] == station_id:
            return s
    raise ValueError(f"unknown station: {station_id}")


def get_run_order(selected: list[str] | None = None) -> list[str]:
    stations = _registry()
    ids = selected or [s["id"] for s in stations]
    by_id = {s["id"]: s for s in stations}

    visited = set()
    order = []

    def visit(sid):
        if sid in visited or sid not in by_id:
            return
        visited.add(sid)
        for dep in by_id[sid].get("requires", []):
            if dep in by_id:
                visit(dep)
        order.append(sid)

    for sid in ids:
        visit(sid)
    return order
