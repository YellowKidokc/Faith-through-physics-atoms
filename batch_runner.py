import argparse
import asyncio
import hashlib
import re
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

import canon_store.paper as paper_module
from canon_store.paper import load_paper, save_paper, create_paper
from stations.atoms.run import run_atoms


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def extract_title(text: str, fallback: str) -> str:
    # First Markdown H1
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return fallback


def ingest_source(source_path: Path) -> str:
    canon_root = paper_module.CANON_STORE_ROOT
    sources_dir = canon_root / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    paper_uuid = str(uuid.uuid4())
    ext = source_path.suffix
    dest_name = f"{paper_uuid}{ext}"
    dest_path = sources_dir / dest_name
    shutil.copy2(source_path, dest_path)

    text = dest_path.read_text(encoding="utf-8")
    title = extract_title(text, source_path.stem)
    sha = sha256_file(dest_path)

    record = create_paper(
        source_path=f"sources/{dest_name}",
        source_sha256=sha,
        title=title,
        author="",
    )
    # Override the uuid so it matches our minted one
    record["address"]["uuid"] = paper_uuid
    record["address"]["handle"] = f"paper/{source_path.stem}"
    save_paper(record)
    return paper_uuid


def update_paper_with_run(paper_uuid: str, station_id: str, run_uuid: str):
    record = load_paper(paper_uuid)
    output_path = paper_module.CANON_STORE_ROOT / "runs" / run_uuid / "outputs" / f"{station_id}.json"
    if output_path.exists():
        import json
        data = json.loads(output_path.read_text())
        if station_id == "atoms":
            record["extracted"]["atoms"] = data.get("atoms", [])
        # Extend for other stations later
    if run_uuid not in record["runs"]:
        record["runs"].append(run_uuid)
    record["latest_run"] = run_uuid
    save_paper(record)


async def run_station_on_paper(paper_uuid: str, station_id: str, provider: str = "deepseek") -> str:
    run_uuid = f"run_{uuid.uuid4()}"
    if station_id == "atoms":
        await run_atoms(paper_uuid, run_uuid, provider)
    else:
        raise NotImplementedError(f"station {station_id} not yet implemented")
    update_paper_with_run(paper_uuid, station_id, run_uuid)
    return run_uuid


def discover_inbox_files(inbox_dir: Path) -> list[Path]:
    files = []
    if inbox_dir.exists():
        for path in inbox_dir.rglob("*.md"):
            files.append(path)
    return sorted(files)


def move_to_outbox(source_path: Path, outbox_dir: Path, renamed: bool = True) -> Path:
    outbox_dir.mkdir(parents=True, exist_ok=True)
    if renamed:
        # Title + keywords placeholder — for now just title-cased filename
        new_name = f"{source_path.stem}.md"
    else:
        new_name = source_path.name
    dest = outbox_dir / new_name
    counter = 1
    while dest.exists():
        dest = outbox_dir / f"{source_path.stem}_{counter}.md"
        counter += 1
    shutil.move(str(source_path), str(dest))
    return dest


def batch_run(
    inbox_dir: Path,
    outbox_dir: Path,
    stations: list[str],
    provider: str = "deepseek",
    keep_originals: bool = True,
):
    files = discover_inbox_files(inbox_dir)
    print(f"Discovered {len(files)} paper(s) in {inbox_dir}")

    for file_path in files:
        print(f"\nIngesting: {file_path}")
        paper_uuid = ingest_source(file_path)
        print(f"  -> paper uuid: {paper_uuid}")

        for station_id in stations:
            print(f"  -> running station: {station_id}")
            try:
                asyncio.run(run_station_on_paper(paper_uuid, station_id, provider))
                print(f"  -> station {station_id} completed")
            except Exception as e:
                print(f"  -> station {station_id} failed: {e}")

        if keep_originals:
            untouched_dir = outbox_dir / "00_ORIGINAL_UNTOUCHED"
            move_to_outbox(file_path, untouched_dir, renamed=False)
            print(f"  -> moved original to {untouched_dir}")

    print("\nBatch complete.")


def main():
    parser = argparse.ArgumentParser(description="Batch-run stations on inbox papers")
    parser.add_argument("--inbox", required=True, type=Path, help="Inbox directory")
    parser.add_argument("--outbox", required=True, type=Path, help="Outbox directory")
    parser.add_argument("--stations", nargs="+", default=["atoms"], help="Stations to run")
    parser.add_argument("--provider", default="deepseek", help="API provider")
    args = parser.parse_args()

    batch_run(args.inbox, args.outbox, args.stations, args.provider)


if __name__ == "__main__":
    main()
