"""A small RFC-4180-style CSV parser.

parse(text) -> list of rows, each a list of string fields. Supports quoted
fields (which may contain commas and newlines), escaped quotes ("" -> a literal
"), and both LF and CRLF line endings. A trailing newline does not create an
empty final row.
"""
from __future__ import annotations


def parse(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    row: list[str] = []
    field = []
    i, n = 0, len(text)
    in_quotes = False

    while i < n:
        ch = text[i]
        if in_quotes:
            if ch == '"':
                in_quotes = False
                i += 1
                continue
            field.append(ch)
            i += 1
            continue

        if ch == '"':
            in_quotes = True
            i += 1
        elif ch == ',':
            row.append("".join(field))
            field = []
            i += 1
        elif ch == '\r':
            row.append("".join(field))
            rows.append(row)
            row, field = [], []
            i += 1
        elif ch == '\n':
            row.append("".join(field))
            rows.append(row)
            row, field = [], []
            i += 1
        else:
            field.append(ch)
            i += 1

    if field or row:
        row.append("".join(field))
        rows.append(row)
    return rows
