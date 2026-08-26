# Internal Research Runtime API

This repo uses `_scripts/research_runtime.py` as the local internal API layer for atoms, papers, stories, and topbar packets.

It is intentionally dependency-free. It can be called from shell scripts, local tools, future HTTP wrappers, or external model pipelines.

## Anchor-Line Compression

Purpose:

```text
Turn a chapter, article, or section into quotable anchor lines without rewriting the whole source.
```

Single file:

```powershell
python _scripts\research_runtime.py anchor "path\to\chapter.md"
```

Folder:

```powershell
python _scripts\research_runtime.py anchor-folder "path\to\folder" --pattern "CH*.md"
```

Include model-call prompts for a later external LLM pass:

```powershell
python _scripts\research_runtime.py anchor "path\to\chapter.md" --include-prompt
```

Outputs are written to:

```text
_runtime/anchor_lines/
```

Each report contains:

```json
{
  "documentAnchor": {
    "loadBearingMechanism": "...",
    "strongestSentenceAlreadyPresent": "...",
    "recommendedAnchorSentence": "...",
    "alternates": {
      "plain": "...",
      "poetic": "...",
      "brutal": "..."
    },
    "recommendation": "keep existing | add near ending | replace with new"
  },
  "sections": []
}
```

## Existing Runtime Calls

Build a source manifest:

```powershell
python _scripts\research_runtime.py manifest "path\to\source.md"
```

Show failure blast radius:

```powershell
python _scripts\research_runtime.py failure "claim-or-node-id"
```

Write the registry:

```powershell
python _scripts\research_runtime.py registry
```

## Contract

The anchor API is a compression pass, not a replacement for human editing.

It should preserve the mechanism, identify the strongest existing line, and produce one or two sentences the reader can remember. It should not turn technical claims into generic inspiration.

