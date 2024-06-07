import os


API_KEY = os.environ.get("API_KEY", "DEFAULT_API_KEY")
OFFSET = int(os.environ.get("OFFSET", 11111))
LETTERS = os.environ.get(
    "LETTERS",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
)
INV_LETTERS = {v: k for k, v in enumerate(LETTERS)}
