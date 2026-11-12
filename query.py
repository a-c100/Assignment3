from utils.tokenizer import tokenize
from utils.stemming import Stemmer
from inverted_index import InvertedIndex
from utils.constants import CORPUS_ROOT_PATH, JSON_DIRECTORY_NAME

# one shared stemmer so we don't rebuild it for every query
_stemmer = Stemmer()
_indexer = InvertedIndex()

def process_query(text: str) -> list[str]:
    # turns raw search query into same terms as index
    # removes duplicate terms (i.e. learn and learning)
    # tokenize -> lowercase -> step
    terms = [_stemmer.stem(token) for token in tokenize(text)]
    
    # returns unique stemmed query terms
    return list(dict.fromkeys(terms))



def query_user_input(num_results = 5) -> None:
    """
    Runs query handling and displays search results using standard input/output text stream

    Args:
        num_results (int): The number of returned search results to display

    Returns:
        None
    """
    while True:
        print("Enter your search query, or 'q' to exit:")
        query = input()
        search_terms = process_query(query)
        if search_terms[0] == 'q': break
        else: 
            results = _indexer.get_query_results(search_terms)
            for result in results[:num_results]:
                print(result)


def run_query_from_input(json_load_dir : str) -> None:
    """
    Runs query handling and index creation using standard input/output text stream

    Args:
        None

    Returns:
        None
    """
    success = _indexer.loadIndexFromDirectory(json_load_dir)
    if success:
        query_user_input()
    else: 
        print(f'No directory {json_load_dir} was found or load was unsuccessful')
        print('y/n to index CORPUS_ROOT_PATH')

        if input().lower() == 'y':
            print('Indexing in progress...')
            _indexer.indexDirectory(CORPUS_ROOT_PATH, JSON_DIRECTORY_NAME)
            print('\nIndexing complete!')
            query_user_input()
    

if __name__ == '__main__':
    run_query_from_input(JSON_DIRECTORY_NAME)