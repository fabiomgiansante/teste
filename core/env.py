import os
import uuid
from pathlib import Path
from typing import Mapping

from dotenv import load_dotenv


SUPPORTED_SECRET_KEYS = (
    "OPENAI_API_KEY",
    "SERPER_API_KEY",
    "ANTHROPIC_API_KEY",
    "DEEPSEEK_API_KEY",
    "GOOGLE_API_KEY",
    "GROQ_API_KEY",
)


def _clean_secret(value: object) -> str:
    return str(value).strip().replace("\n", "").replace("\r", "")


def bootstrap_environment(secrets: Mapping[str, object] | None = None) -> dict[str, str]:
    """
    Load env vars with this priority:
    1) Streamlit secrets (if available)
    2) Existing process environment
    3) .env (local development fallback)
    """
    applied: dict[str, str] = {}

    if secrets:
        for key in SUPPORTED_SECRET_KEYS:
            value = None
            try:
                if key in secrets:
                    value = secrets[key]
                elif hasattr(secrets, "get"):
                    value = secrets.get(key)
            except Exception:
                value = None

            if value:
                clean_value = _clean_secret(value)
                os.environ[key] = clean_value
                applied[key] = clean_value

    if not os.getenv("OPENAI_API_KEY"):
        load_dotenv(override=False)

    if os.getenv("GOOGLE_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

    return applied


def validate_openai_api_key(api_key: str, min_length: int = 50) -> str:
    cleaned = _clean_secret(api_key)

    if not cleaned:
        raise ValueError("OPENAI_API_KEY nao encontrada.")

    if not cleaned.startswith("sk-"):
        raise ValueError("OPENAI_API_KEY invalida: deve comecar com 'sk-'.")

    if len(cleaned) < min_length:
        raise ValueError(
            f"OPENAI_API_KEY invalida: chave muito curta ({len(cleaned)} caracteres)."
        )

    return cleaned


def ensure_openai_api_key() -> str:
    return validate_openai_api_key(os.getenv("OPENAI_API_KEY", ""))


def build_temp_upload_path(temp_dir: str | Path, original_name: str) -> Path:
    temp_path = Path(temp_dir)
    temp_path.mkdir(parents=True, exist_ok=True)

    safe_name = Path(original_name).name.replace(" ", "_")
    unique_prefix = uuid.uuid4().hex[:12]
    return temp_path / f"{unique_prefix}_{safe_name}"
