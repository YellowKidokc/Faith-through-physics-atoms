import os

PROVIDERS = {
    "deepseek": {
        "url": "https://api.deepseek.com/chat/completions",
        "key_env": "DEEPSEEK_API_KEY",
        "default_model": "deepseek-chat",
    },
    "kimi": {
        "url": "https://api.moonshot.ai/v1/chat/completions",
        "key_env": "MOONSHOT_API_KEY",
        "default_model": "kimi-k2-0905-preview",
    },
    "openrouter": {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "default_model": "openai/gpt-4o-mini",
    },
    "ollama": {
        "url": "http://localhost:11434/api/chat",
        "key_env": None,
        "default_model": "llama3.2",
    },
}


def get_provider(name: str) -> dict:
    if name not in PROVIDERS:
        raise ValueError(f"unknown provider: {name}")
    return PROVIDERS[name]


def get_api_key(provider_name: str) -> str | None:
    cfg = get_provider(provider_name)
    env = cfg.get("key_env")
    return os.environ.get(env) if env else None
