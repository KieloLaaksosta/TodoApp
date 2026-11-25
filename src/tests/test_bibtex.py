import unittest
from entities.reference import Reference
from repositories.bibtex_repository import generate_bibtex
from utils import bibtex_proof

class Test_bibtex(unittest.TestCase):
    def setUp(self):
        self.ref = Reference("book", "ilkimys", """Itse "pahis" Ilkimys""", 
                             "näin olet pahis", 1950, "Paha Publishing")

    def test_bibtex_proof(self):
        text = bibtex_proof(self.ref.author)
        correct = """Itse {"}pahis{"} Ilkimys"""

        self.assertEqual(text, correct)
    
    def test_generate_bibtex(self):
        ref = [self.ref]
        generated = generate_bibtex(ref)
        correct = (
            '@book{ilkimys,\n'
            '    author = "Itse {"}pahis{"} Ilkimys",\n'
            '    title = "näin olet pahis",\n'
            '    year = "1950",\n'
            '    publisher = "Paha Publishing"\n'
            '}\n\n'
        )

        self.assertEqual(generated, correct)