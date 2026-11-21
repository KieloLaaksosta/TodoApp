import unittest
from unittest.mock import patch
from entities.reference import Reference, ReferenceValidationError, get_year_int

def _create_form(
    bibtex_key="KEY_of:greate-people123",
    reference_type="book",
    title="The Heidelberg of Bringing",
    author="Bill Wat",
    year="1405",
    publisher="Otava",
):
    return {
        "bibtex_key": bibtex_key,
        "reference_type": reference_type,
        "title": title,
        "author": author,
        "year": year,
        "publisher": publisher,
    }

class TestReferenceValidation(unittest.TestCase):
    def test_from_form_valid(self):
        ref = Reference.from_form(_create_form())
        self.assertEqual(ref.key, "KEY_of:greate-people123")
        self.assertEqual(ref.type, "book")
        self.assertEqual(ref.title, "The Heidelberg of Bringing")
        self.assertEqual(ref.author, "Bill Wat")
        self.assertEqual(ref.year, 1405)
        self.assertEqual(ref.publisher, "Otava")
        
    def test_from_form_strips(self):
        ref = Reference.from_form(_create_form(bibtex_key="    \t\n KEY_of:greate-people123  \t\r\n "))
        self.assertEqual(ref.key, "KEY_of:greate-people123")

    def test_from_form_missing_fields(self):
        form = _create_form()
        del form["publisher"]
        with self.assertRaises(ReferenceValidationError):
            Reference.from_form(form)

    def test_from_form_empty_fields(self):
        for field in ("bibtex_key", "reference_type", "title", "author", "publisher"):
            with self.subTest(field=field):
                form = _create_form(**{field: "  "})
                with self.assertRaises(ReferenceValidationError):
                    Reference.from_form(form)

    def test_from_form_invalid_reference_type(self):
        for bad_type in ("", "DROP TABLE latex_references", "Book"):
            with self.subTest(reference_type=bad_type):
                form = _create_form(reference_type=bad_type)
                with self.assertRaises(ReferenceValidationError):
                    Reference.from_form(form)

    def test_from_form_invalid_key_chars(self):
        form = _create_form(bibtex_key="bad key!@#")
        with self.assertRaises(ReferenceValidationError):
            Reference.from_form(form)

    def test_from_form_invalid_length(self):
        cases = [
            {"bibtex_key": "a" * 101},
            {"title": "A" * 256},
            {"author": "A" * 256},
            {"publisher": "P" * 256},
        ]
        for kwargs in cases:
            with self.subTest(kwargs=kwargs):
                form = _create_form(**kwargs)
                with self.assertRaises(ReferenceValidationError):
                    Reference.from_form(form)

    @patch("entities.reference.current_year", return_value=2026)
    def test_get_year_int_valid_and_invalid(self, _mock_year):
        self.assertEqual(get_year_int("1405"), 1405)

        for bad_year in ("abc", 2200, 2027, 0, -5):
            with self.subTest(year=bad_year):
                with self.assertRaises(ReferenceValidationError):
                    get_year_int(bad_year)
