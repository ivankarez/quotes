#!/usr/bin/env python3
"""Convert quotes.json into CSV files containing at most 200 quotes each."""

import csv
import json
from pathlib import Path


INPUT_FILE = Path("quotes.json")
BATCH_SIZE = 200
MAX_QUOTE_LENGTH = 200


def main():
    raw_json = INPUT_FILE.read_bytes()
    try:
        json_text = raw_json.decode("utf-8")
    except UnicodeDecodeError:
        json_text = raw_json.decode("cp1252")
    quotes = json.loads(json_text)

    rows = []
    for item in quotes:
        quote = item.get("quoteText", "")
        if not isinstance(quote, str) or len(quote) > MAX_QUOTE_LENGTH:
            continue

        author = item.get("quoteAuthor")
        if not isinstance(author, str) or not author.strip():
            author = "Unknown"

        rows.append((quote, author))

    for batch_number, start in enumerate(range(0, len(rows), BATCH_SIZE), start=1):
        output_file = Path(f"quotes_{batch_number}.csv")
        with output_file.open("w", encoding="utf-8", newline="") as destination:
            destination.write("Quote,Author\n")
            writer = csv.writer(destination, quoting=csv.QUOTE_ALL, lineterminator="\n")
            writer.writerows(rows[start : start + BATCH_SIZE])


if __name__ == "__main__":
    main()
