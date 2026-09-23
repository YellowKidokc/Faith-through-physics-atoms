from pathlib import Path
import hashlib

CANON_STORE_ROOT = Path("canon-store")


def _prompt_dir(station: str, prompt_id: str) -> Path:
    return CANON_STORE_ROOT / "prompts" / station / prompt_id


def list_versions(station: str, prompt_id: str) -> list[str]:
    d = _prompt_dir(station, prompt_id)
    if not d.exists():
        return []
    return sorted(p.stem for p in d.glob("*.md"))


def latest_version(station: str, prompt_id: str) -> str | None:
    versions = list_versions(station, prompt_id)
    return versions[-1] if versions else None


def load_prompt(station: str, prompt_id: str, version: str | None = None) -> str:
    if version is None:
        version = latest_version(station, prompt_id)
        if version is None:
            raise FileNotFoundError(f"no prompt found for {station}/{prompt_id}")
    path = _prompt_dir(station, prompt_id) / f"{version}.md"
    if not path.exists():
        raise FileNotFoundError(f"prompt not found: {path}")
    return path.read_text(encoding="utf-8")


def prompt_hash(station: str, prompt_id: str, version: str | None = None) -> str:
    content = load_prompt(station, prompt_id, version)
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()
