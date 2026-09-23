import asyncio
import json
import os
import time
from datetime import datetime, timezone
import httpx
from .providers import get_provider, get_api_key
from .receipts import new_request_id, text_hash, write_receipt
from .costs import estimate_cost


async def complete(
    provider: str,
    system: str,
    user: str,
    json_mode: bool = False,
    model: str | None = None,
    temperature: float = 0.2,
    max_retries: int = 3,
    timeout: float = 120.0,
    run_uuid: str | None = None,
) -> tuple[dict | str, dict]:
    cfg = get_provider(provider)
    model = model or cfg["default_model"]
    key = get_api_key(provider)
    if cfg.get("key_env") and not key:
        raise RuntimeError(f"{cfg['key_env']} not set")

    request_id = new_request_id()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    body = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}

    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"

    last_error = None
    for attempt in range(max_retries):
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(cfg["url"], json=body, headers=headers)
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            last_error = e
            await asyncio.sleep(2 ** attempt)
            continue

        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        latency = time.time() - start

        receipt = {
            "request_id": request_id,
            "provider": provider,
            "model": model,
            "prompt_hash": text_hash(system + "\n" + user),
            "response_hash": text_hash(content),
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
            "cost_usd": estimate_cost(model, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)),
            "latency_seconds": latency,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "status": "ok",
        }
        if run_uuid:
            write_receipt(run_uuid, receipt)

        if json_mode:
            try:
                return json.loads(content), receipt
            except json.JSONDecodeError as e:
                receipt["status"] = "json_parse_error"
                receipt["parse_error"] = str(e)
                if run_uuid:
                    write_receipt(run_uuid, receipt)
                raise RuntimeError(f"LLM returned non-JSON: {e}")
        return content, receipt

    raise RuntimeError(f"API call failed after {max_retries} attempts: {last_error}")
