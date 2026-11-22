import unittest
from entities.reference import generate_bibtex, Reference
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
        correct = """@book{ilkimys,
    author = "Itse {"}pahis{"} Ilkimys",
    title = "näin olet pahis",
    year = "1950",
    publisher = "Paha Publishing"
}

"""

        self.assertEqual(generated, correct)