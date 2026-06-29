from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI

from config import DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, REQUEST_TIMEOUT
from src.logger import get_logger


class DeepSeekTranslator:
    def __init__(self) -> None:
        self.logger = get_logger(__name__)
        load_dotenv()

        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("Missing DEEPSEEK_API_KEY. Please set it in .env.")

        self.client = OpenAI(
            api_key=api_key,
            base_url=DEEPSEEK_BASE_URL,
            timeout=REQUEST_TIMEOUT,
        )

    def translate_abstract(self, abstract_en: str) -> str:
        if not abstract_en.strip():
            return "Translation failed."

        try:
            response = self.client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a precise academic translator. "
                            "Translate the user's English abstract into fluent "
                            "Simplified Chinese only."
                        ),
                    },
                    {"role": "user", "content": abstract_en},
                ],
                stream=False,
            )
            content = response.choices[0].message.content if response.choices else ""
            if not content:
                raise RuntimeError("DeepSeek returned an empty translation.")
            return content.strip()
        except Exception as exc:
            self.logger.error("Translation failed: %s", exc)
            return "Translation failed."
