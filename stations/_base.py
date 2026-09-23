import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import canon_store.paper
from canon_store.paper import load_paper
from canon_store.prompts import load_prompt, prompt_hash
from api_client.completion import complete
from stations.registry import get_station

CHARS_PER_TOKEN = 4
CONTEXT_WINDOW_TOKENS = 64000
TOKEN_BUDGET = int(CONTEXT_WINDOW_TOKENS * 0.8)


def _estimate_tokens(text: str) -> int:
    return len(text) // CHARS_PER_TOKEN


def _chunk_by_paragraphs(text: str, max_chunk_tokens: int) -> list[str]:
    max_chars = max_chunk_tokens * CHARS_PER_TOKEN
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = []
    current_len = 0
    for p in paragraphs:
        p_len = len(p)
        if current_len + p_len > max_chars and current:
            chunks.append("\n\n".join(current))
            current = [p]
            current_len = p_len
        else:
            current.append(p)
            current_len += p_len + 2
    if current:
        chunks.append("\n\n".join(current))
    return chunks if chunks else [text]


async def run_station(station_id: str, paper_uuid: str, run_uuid: str, provider: str = "deepseek") -> Path:
    station_def = get_station(station_id)
    prompt_cfg = station_def.get("prompt", {"station": station_id, "prompt_id": "extract"})

    paper = load_paper(paper_uuid)
    source_path = canon_store.paper.CANON_STORE_ROOT / paper["source"]["path"]
    source_text = source_path.read_text(encoding="utf-8") if source_path.exists() else ""

    system = load_prompt(prompt_cfg["station"], prompt_cfg["prompt_id"])
    user = f"PAPER TITLE: {paper['metadata'].get('title', '')}\n\nSOURCE TEXT:\n{source_text}"

    estimated_tokens = _estimate_tokens(user)
    chunks = [user]
    if estimated_tokens > TOKEN_BUDGET:
        chunks = _chunk_by_paragraphs(user, TOKEN_BUDGET)

    all_results = []
    receipts = []
    for chunk in chunks:
        result, receipt = await complete(
            provider=provider,
            system=system,
            user=chunk,
            json_mode=True,
            run_uuid=run_uuid,
        )
        all_results.append(result)
        receipts.append(receipt)

    output_dir = canon_store.paper.CANON_STORE_ROOT / "runs" / run_uuid / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{station_id}.json"

    payload = {
        "station": station_id,
        "paper_uuid": paper_uuid,
        "run_uuid": run_uuid,
        "prompt_hash": prompt_hash(prompt_cfg["station"], prompt_cfg["prompt_id"]),
        "provider": provider,
        "model": receipts[0]["model"] if receipts else None,
        "receipts": receipts,
        "results": all_results if len(all_results) > 1 else all_results[0],
        "chunk_count": len(chunks),
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def main(station_id: str):
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-uuid", required=True)
    parser.add_argument("--run-uuid", required=True)
    parser.add_argument("--provider", default="deepseek")
    args = parser.parse_args()
    asyncio.run(run_station(station_id, args.paper_uuid, args.run_uuid, args.provider))
