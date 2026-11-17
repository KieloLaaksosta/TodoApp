import unittest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from repositories.reference_repository import add_reference


class Test_reference_repository(unittest.TestCase):
    def test_add_reference_with_no_bibtex_key(self):
        bibtex_key = ""
        reference_type = "book"
        title = "The Heidelberg of Bringing"
        author = "Bill Wat"
        year = 1405
        publisher = "Otava"

        result = add_reference(bibtex_key, reference_type, title, author, year, publisher)
        self.assertFalse(result)

    def test_add_reference_with_no_reference_type(self):
        bibtex_key = "jdsfjijff3842"
        reference_type = ""
        title = "The Heidelberg of Bringing"
        author = "Bill Wat"
        year = 1405
        publisher = "Otava"

        result = add_reference(bibtex_key, reference_type, title, author, year, publisher)
        self.assertFalse(result)

    def test_add_reference_with_no_author(self):
        bibtex_key = "jdsfjijff3842"
        reference_type = "book"
        title = "The Heidelberg of Bringing"
        author = "  "
        year = 1405
        publisher = "Otava"

        result = add_reference(bibtex_key, reference_type, title, author, year, publisher)
        self.assertFalse(result)

    def test_add_reference_with_invalid_length(self):
        result = add_reference(
            bibtex_key="a" * 101,
            reference_type="book",
            title="The Heidelberg of Bringing",
            author="Bill Wat",
            year_str="1405",
            publisher="Otava"
        )
        self.assertFalse(result)

        result = add_reference(
            bibtex_key="jdsfjijff3842",
            reference_type="book",
            title="A" * 256,
            author="Bill Wat",
            year_str="1405",
            publisher="Otava"
        )
        self.assertFalse(result)

        result = add_reference(
            bibtex_key="jdsfjijff3842",
            reference_type="book",
            title="The Heidelberg of Bringing",
            author="A" * 256,
            year_str="1405",
            publisher="Otava"
        )
        self.assertFalse(result)

        result = add_reference(
            bibtex_key="jdsfjijff3842",
            reference_type="book",
            title="The Heidelberg of Bringing",
            author="Bill Wat",
            year_str="1405",
            publisher="P" * 256
        )
        self.assertFalse(result)

    def test_add_reference_with_invalid_year(self):
        result = add_reference("jdsfjijff3842", "book", "The Heidelberg of Bringing", "Bill Wat", "abc", "Otava")
        self.assertFalse(result)

        result = add_reference("jdsfjijff3842", "book", "The Heidelberg of Bringing", "Bill Wat", 2200, "Otava")
        self.assertFalse(result)

        result = add_reference("jdsfjijff3842", "book", "The Heidelberg of Bringing", "Bill Wat", 0, "Otava")
        self.assertFalse(result)

    @patch("repositories.reference_repository.db.session")
    def test_add_reference(self, fake_session):
        bibtex_key = "jdsfjijff3842"
        reference_type = "book"
        title = "The Heidelberg of Bringing"
        author = "Bill Wat"
        year = "1405"
        publisher = "Otava"

        result = add_reference(bibtex_key, reference_type, title, author, year, publisher)

        fake_session.commit.assert_called_once()
        self.assertTrue(result)

    @patch("repositories.reference_repository.db.session")
    def test_add_reference_with_IntegrityError(self, fake_session):
        fake_session.execute.side_effect = IntegrityError(None, None, None)

        result = add_reference(
            bibtex_key="jdsfjijff3842",
            reference_type="book",
            title="The Heidelberg of Bringing",
            author="Bill Wat",
            year_str="1405",
            publisher="Otava"
        )

        fake_session.rollback.assert_called_once()
        self.assertFalse(result)