from datetime import date, datetime


def clean_text(text: str) -> str:
    return " ".join(text.split())


def parse_cli_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%y%m%d").date()
    except ValueError as exc:
        raise ValueError(
            f"Invalid --date value '{value}'. Expected YYMMDD, for example 260625."
        ) from exc


def format_date_for_filename(target_date: date) -> str:
    return f"{target_date.strftime('%y%m%d')}.md"


def format_date_for_display(target_date: date) -> str:
    return target_date.isoformat()
