import unittest
from unittest.mock import Mock, patch
from sqlalchemy.exc import IntegrityError
from repositories.reference_repository import add_reference, update_reference


class TestReferenceRepository(unittest.TestCase):
    def setUp(self):
        self.fake_reference = Mock(
            key="jdsfjijff3842",
            type="book",
            title="The Heidelberg of Bringing",
            author="Bill Wat",
            year=1405,
            publisher="Otava",
        )

    @patch("repositories.reference_repository.db.session")
    def test_add_reference_success(self, fake_session):
        result = add_reference(self.fake_reference)

        fake_session.execute.assert_called_once()
        fake_session.commit.assert_called_once()
        fake_session.rollback.assert_not_called()
        self.assertIsNone(result)

    @patch("repositories.reference_repository.db.session")
    def test_add_reference_with_integrity_error(self, fake_session):
        fake_session.execute.side_effect = IntegrityError(None, None, None)

        with self.assertRaises(ValueError):
            add_reference(self.fake_reference)

        fake_session.rollback.assert_called_once()
        fake_session.commit.assert_not_called()

    @patch("repositories.reference_repository.db.session")
    def test_update_reference_success(self, fake_session):
        update_reference(self.fake_reference, "oldkey")

        self.assertEqual(fake_session.execute.call_args.args[1]["old_key"],1)

        fake_session.execute.assert_called_once()
        fake_session.commit.assert_called_once()
        fake_session.rollback.assert_not_called()


