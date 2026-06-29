from pathlib import Path


KEYWORDS = [
    "Vision Language Action",
    "world model",
    "world action model",
    "robot",
]

SEARCH_MAX_RESULTS_PER_KEYWORD = 50
SAVE_MAX_RESULTS_PER_KEYWORD = 15
OUTPUT_DIR = Path("outputs")
TARGET_PRIMARY_CATEGORIES = ["cs", "stat"]

ARXIV_BASE_URL = "https://export.arxiv.org/api/query"
REQUEST_TIMEOUT = 30
RETRY_TIMES = 3

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"
