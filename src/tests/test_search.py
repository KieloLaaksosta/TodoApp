import unittest
from repositories.reference_repository import format_like_pattern

class TestFormatLikePattern(unittest.TestCase):
    def test_single_word(self):
        self.assertEqual(format_like_pattern("Knuth"), "%Knuth%")

    def test_strips_outer_whitespace(self):
        self.assertEqual(format_like_pattern("    \t\n Knuth  \t\r\n "), "%Knuth%")

    def test_multiple_words(self):
        self.assertEqual(
            format_like_pattern("Donald Knuth 1968"),
            "%Donald%Knuth%1968%",
        )

    def test_collapses_mixed_inner_whitespace(self):
        self.assertEqual(
            format_like_pattern("Donald   Knuth\t\n1968"),
            "%Donald%Knuth%1968%",
        )

    def test_empty_string(self):
        self.assertEqual(format_like_pattern(""), "%%")

    def test_whitespace_only_string(self):
        self.assertEqual(format_like_pattern("    "), "%%")