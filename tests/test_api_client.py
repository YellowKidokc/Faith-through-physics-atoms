import asyncio
import json
from unittest.mock import patch, AsyncMock, MagicMock
from api_client.completion import complete


def test_complete_returns_json_and_receipt():
    fake_response = {
        "choices": [{"message": {"content": json.dumps({"atoms": []})}}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50}
    }
    response_mock = MagicMock()
    response_mock.raise_for_status = MagicMock()
    response_mock.json = MagicMock(return_value=fake_response)

    with patch("api_client.completion.get_api_key", return_value="fake-key"), \
         patch("api_client.completion.httpx.AsyncClient") as mock_client:
        instance = mock_client.return_value.__aenter__.return_value
        instance.post = AsyncMock(return_value=response_mock)

        result, receipt = asyncio.run(complete(
            provider="deepseek",
            system="You are a classifier.",
            user="Extract atoms from this paper.",
            json_mode=True,
        ))

    assert result == {"atoms": []}
    assert receipt["provider"] == "deepseek"
    assert receipt["input_tokens"] == 100
    assert receipt["output_tokens"] == 50
    assert receipt["status"] == "ok"
