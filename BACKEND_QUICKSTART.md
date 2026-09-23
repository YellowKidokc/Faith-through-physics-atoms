# Canon Workbench Backend — Quick Start

## What was built

A unified Python backend for the Faith Through Physics workbench:

- **Canon Store** (`canon-store/`) — git-backed single source of truth for sources, papers, runs, atoms, prompts, and templates.
- **Paper records** — schema-validated JSON records that aggregate every run against a source.
- **Prompt registry** — versioned prompts under `canon-store/prompts/<station>/<prompt_id>/<version>.md`.
- **API client** (`api_client/`) — provider-agnostic async client for DeepSeek/Kimi/OpenRouter/Ollama with receipts and cost tracking.
- **Station registry** (`stations/stations.json`) — declares CKG + 8 API_DEEP stations and their dependency order.
- **Generic station runner** (`stations/_base.py`) — one runner powers ATOMS, AXIOM_NODES, COHERENCE_SCORE, FRUITS, LEAN4, MASTER_EQUATION, PAPER_GRADER, and STORIES.
- **Local API server** (`api_server/`) — FastAPI on `http://127.0.0.1:8989` with endpoints for status, papers, runs, and stop.
- **Batch runner** (`batch_runner.py`) — ingest papers from an inbox, run stations concurrently, and move originals to `outbox/00_ORIGINAL_UNTOUCHED/`.

## Run the tests

```bash
pytest tests/ -v
```

All tests run without real API keys (mocked).

## Start the local API server

```bash
python run_api_server.py
```

Server listens on `http://127.0.0.1:8989`.

Check status:

```bash
curl http://127.0.0.1:8989/api/status
```

## Run a batch from inbox to outbox

```bash
python batch_runner.py \
  --inbox "path/to/inbox" \
  --outbox "path/to/outbox" \
  --stations atoms axiom_nodes coherence_score \
  --provider deepseek \
  --workers 5
```

The runner will:

1. Discover every `.md` file in the inbox.
2. Copy each to `canon-store/sources/<uuid>.md` and create a paper record.
3. Run the requested stations concurrently (up to `--workers`).
4. Update each paper record with extracted data.
5. Move the original file to `outbox/00_ORIGINAL_UNTOUCHED/`.

## Run a single station from the command line

```bash
python stations/atoms/run.py \
  --paper-uuid <uuid> \
  --run-uuid run_test_001 \
  --provider deepseek
```

Output lands in `canon-store/runs/run_test_001/outputs/atoms.json`.

## Trigger a run via the API

```bash
curl -X POST http://127.0.0.1:8989/api/run \
  -H "Content-Type: application/json" \
  -d '{"paper_uuid":"<uuid>","stations":["atoms"],"provider":"deepseek"}'
```

Check progress:

```bash
curl http://127.0.0.1:8989/api/run/<run_id>/status
```

## Environment variables

- `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY`, `OPENROUTER_API_KEY` — provider keys.
- `CANON_STORE_ROOT` — override the default `canon-store/` path.
- `API_HOST`, `API_PORT` — server bind address (default `127.0.0.1:8989`).

## Next steps

- Wire the React UI to the local API (`/api/papers`, `/api/run`, `/api/run/<id>/status`).
- Implement priority/series/general inbox folder sorting.
- Add paper title renaming with keyword tags in the outbox.
- Add real-time WebSocket log streaming.
