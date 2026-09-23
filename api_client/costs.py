# Price per 1M tokens (input, output)
MODEL_COSTS = {
    "deepseek-chat": (0.14, 0.28),
    "kimi-k2-0905-preview": (1.00, 3.00),
    "openai/gpt-4o-mini": (0.15, 0.60),
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    in_price, out_price = MODEL_COSTS.get(model, (0.0, 0.0))
    return (input_tokens * in_price + output_tokens * out_price) / 1_000_000
