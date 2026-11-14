from utils.tokenizer import tokenize
from utils.stemming import Stemmer

_stemmer = Stemmer()

def process_query(text: str) -> list[str]:
    # turns raw search query into same terms as index
    # removes duplicate terms (i.e. learn and learning)
    # tokenize -> lowercase -> step
    terms = [_stemmer.stem(token) for token in tokenize(text)]
    
    # returns unique stemmed query terms
    return list(dict.fromkeys(terms))

def calculate_term_frequency():
    """
    Measures word frequency in the document
    """
    pass

def calculate_inverse_doc_frequency():
    """
    Measure rarity of word across corpus
    """
    
    pass