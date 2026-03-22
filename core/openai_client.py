from functools import lru_cache

from langchain_openai import ChatOpenAI

from core.env import ensure_openai_api_key


@lru_cache(maxsize=8)
def get_openai_chat_model(
    model_name: str = "gpt-4o-mini",
    temperature: float = 0.7,
    timeout: int = 90,
    max_retries: int = 2,
) -> ChatOpenAI:
    api_key = ensure_openai_api_key()
    return ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        api_key=api_key,
        timeout=timeout,
        max_retries=max_retries,
    )
