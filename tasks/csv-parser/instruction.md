# Fix the `csvmini` CSV parser

`csvmini.parse(text)` parses CSV text into a list of rows (each a list of string
fields). It should follow RFC-4180 conventions:

- Fields are comma-separated; rows are newline-separated.
- A field may be wrapped in double quotes, inside which commas and newlines are
  literal.
- Inside a quoted field, two double quotes (`""`) mean one literal `"`.
- Both `\n` and `\r\n` (CRLF) are valid line endings.
- A trailing newline does **not** produce an extra empty row.

The implementation in `/app/csvmini/` has bugs:

1. **Escaped quotes are mishandled** — `""` inside a quoted field is treated as
   closing-then-reopening instead of a single literal `"`, so `"a""b"` parses as
   `ab` instead of `a"b`.
2. **CRLF is mishandled** — a `\r\n` line ending produces a spurious empty row
   because the `\n` after `\r` isn't consumed.

Fix `/app/csvmini/` so parsing is correct. Keep the public API (`parse(text)`)
unchanged.
