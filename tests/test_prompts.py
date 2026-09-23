from canon_store.prompts import load_prompt, latest_version


def test_load_prompt():
    prompt = load_prompt("atoms", "extract-claims", "v1.0.0")
    assert "ATOMS Station Prompt" in prompt
    assert "claim atoms" in prompt.lower()


def test_latest_version():
    version = latest_version("atoms", "extract-claims")
    assert version == "v1.0.0"
