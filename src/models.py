from dataclasses import dataclass
from datetime import date


@dataclass
class Paper:
    title: str
    link: str
    abstract_en: str
    abstract_zh: str
    updated_date: date
