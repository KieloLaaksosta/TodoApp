from datetime import datetime; 

def current_year(): return datetime.now().year

def bibtex_proof(text: str): return text.replace('"', '{"}')
