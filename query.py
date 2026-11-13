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


def get_number_from_user_input() -> int:
    """
    Returns an integer from user input, or a default value on faulty input

    Args:
        None

    Returns:
        (int): The integer from user input, or a default value on failure
    """
    print('Enter number of search results to be displayed, or \'@\' for all:')
    inp = input()
    try:
        num = abs(int(inp))
        return num
    except ValueError:
        if inp == '@': return 100000
        print('Invalid number')
        return 5


def query_user_input(num_results = 5) -> None:
    """
    Runs query handling and displays search results using standard input/output text stream

    Args:
        num_results (int): The number of returned search results to display

    Returns:
        None
    """
    while True:
        print("Enter your search query, '#' to change number of displayed results, or 'q' to exit:")
        query = input()
        search_terms = process_query(query)
        if query[0].lower() == 'q': break
        elif (query[0] == '#'):
            num_results = get_number_from_user_input()
        else: 
            results = _indexer.get_query_results(search_terms)
            num_found = len(results)
            if num_found == 0: 
                print('No results found!')
                continue
            else: 
                print(f'{num_found} results found!')
            for result in results[:num_results]:
                print(_indexer._docIDtoURL[str(result[0])], result[1])


def run_query_from_input(json_load_dir : str) -> None:
    """
    Runs query handling and index creation using standard input/output text stream

    Args:
        None

    Returns:
        None
    """
    success = _indexer.load_index_from_directory(json_load_dir)
    if success:
        query_user_input()
    else: 
        print(f'No directory {json_load_dir} was found or load was unsuccessful')
        print('y/n to index CORPUS_ROOT_PATH')

        if input().lower() == 'y':
            print('Indexing in progress...')
            _indexer.index_directory(CORPUS_ROOT_PATH, JSON_DIRECTORY_NAME)
            print('\nIndexing complete!')
            query_user_input()
    

if __name__ == '__main__':
    run_query_from_input(JSON_DIRECTORY_NAME)