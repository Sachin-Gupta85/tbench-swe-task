"""Hidden acceptance suite for the mini CSV parser."""
import unittest

from csvmini import parse


class TestCsvMini(unittest.TestCase):
    def test_simple_rows(self):
        self.assertEqual(parse("a,b,c\n1,2,3\n"), [["a", "b", "c"], ["1", "2", "3"]])

    def test_empty_fields(self):
        self.assertEqual(parse("a,,c"), [["a", "", "c"]])

    def test_quoted_comma(self):
        self.assertEqual(parse('x,"a,b",y'), [["x", "a,b", "y"]])

    def test_escaped_quote(self):
        # "" inside a quoted field is a single literal quote.
        self.assertEqual(parse('"a""b"'), [['a"b']])
        self.assertEqual(parse('"she said ""hi"""'), [['she said "hi"']])

    def test_quoted_newline(self):
        self.assertEqual(parse('"line1\nline2",next'), [["line1\nline2", "next"]])

    def test_crlf_line_endings(self):
        self.assertEqual(parse("a,b\r\nc,d"), [["a", "b"], ["c", "d"]])

    def test_crlf_matches_lf(self):
        self.assertEqual(parse("x,y\r\n1,2\r\n"), parse("x,y\n1,2\n"))

    def test_trailing_newline_no_empty_row(self):
        self.assertEqual(parse("a\n"), [["a"]])

    def test_empty_input(self):
        self.assertEqual(parse(""), [])


if __name__ == "__main__":
    unittest.main()
