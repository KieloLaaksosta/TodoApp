import unittest
from unittest.mock import patch
from entities.reference import Reference
from repositories.reference_repository import get_references, add_reference


class Test_reference_repository(unittest.TestCase):
    def setUp(self):
        self.reference=["jdsfjijff3842", "book", "The Heidelberg of Bringing", "Bill Wat", "1405", "Otava"]

    def test_add_reference_with_no_bibtex_key(self):
        ref=['']+self.reference[1:]
        result=add_reference(ref[0],ref[1],ref[2],ref[3],ref[4],ref[5])
        self.assertFalse(result)

    def test_add_reference_with_no_reference_type(self):
        ref=[self.reference[0]]+['']+self.reference[2:]
        result=add_reference(ref[0],ref[1],ref[2],ref[3],ref[4],ref[5])
        self.assertFalse(result)

    @patch("repositories.reference_repository.db.session")
    def test_add_reference_with_no_author(self,fake_session):
        ref=self.reference[:3]+['']+self.reference[4:]
        result=add_reference(ref[0],ref[1],ref[2],ref[3],ref[4],ref[5])
        self.assertTrue(result)

        args=fake_session.execute.call_args[0][1]
        self.assertIsNone(args["author"])

        fake_session.commit.assert_called_once()

    def test_add_reference_with_invalid_length(self):
        key_ref=[self.reference[0]*100]+self.reference[1:] # for bibtex_key
        result=add_reference(key_ref[0],key_ref[1],key_ref[2],key_ref[3],key_ref[4],key_ref[5])
        self.assertFalse(result)

        title_ref=self.reference[:2]+[self.reference[2]*1000]+self.reference[3:] # for title
        result=add_reference(title_ref[0],title_ref[1],title_ref[2],title_ref[3],title_ref[4],title_ref[5])
        self.assertFalse(result)

        author_ref=self.reference[:3]+[self.reference[3]*1000]+self.reference[4:] #for author
        result=add_reference(author_ref[0],author_ref[1],author_ref[2],author_ref[3],author_ref[4],author_ref[5])
        self.assertFalse(result)

        publisher_ref=self.reference[:5]+[self.reference[5]*1000] # for publisher
        result=add_reference(publisher_ref[0],publisher_ref[1],publisher_ref[2],publisher_ref[3],publisher_ref[4],publisher_ref[5])
        self.assertFalse(result)

    def test_add_reference_with_invalid_year(self):
        ref=self.reference[:4]+['abc']+[self.reference[5]] # not integer
        result=add_reference(ref[0],ref[1],ref[2],ref[3],ref[4],ref[5])
        self.assertFalse(result)

        ref=self.reference[:4]+['2200']+[self.reference[5]] # year > max_year
        result=add_reference(ref[0],ref[1],ref[2],ref[3],ref[4],ref[5])
        self.assertFalse(result)

        ref=self.reference[:4]+[0]+[self.reference[5]] # year < min_year
        result=add_reference(ref[0],ref[1],ref[2],ref[3],ref[4],ref[5])
        self.assertFalse(result)

    @patch("repositories.reference_repository.db.session")
    def test_add_reference(self, fake_session):
        ref=self.reference
        result=add_reference(ref[0],ref[1],ref[2],ref[3],ref[4],ref[5])

        args=fake_session.execute.call_args[0][1]
        self.assertEqual(args['bibtex_key'],"jdsfjijff3842")
        self.assertEqual(args['reference_type'],'book')
        self.assertEqual(args['title'],'The Heidelberg of Bringing')
        self.assertEqual(args['author'],'Bill Wat')
        self.assertEqual(args['year'],1405)
        self.assertEqual(args['publisher'],'Otava')


        fake_session.commit.assert_called_once()
        self.assertTrue(result)

    


        


if __name__ == "__main__":
    unittest.main()
