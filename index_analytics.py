from inverted_index import *
from utils.constants import CORPUS_ROOT_PATH
import io
import pickle

def get_dict_disk_size_kb(mapping: dict) -> int:
    """
    Returns the disk size of a dict in kilobytes

    Args:
        mapping (dict): the dict to measure

    Returns:
        int: the disk size of mapping in kilobytes
    """
    # serialize dict into memory buffer using latest protocol
    buffer = io.BytesIO()
    pickle.dump(mapping, buffer, protocol=pickle.HIGHEST_PROTOCOL)
    
    # raw size in bytes
    bytes_size = buffer.tell()
    
    # bytes to kb
    size_in_kb = bytes_size / 1024
    return int(size_in_kb)


def analyzeInvertedIndex(root : str) -> None:
    """
    Creates the inverted index and outputs it to text files
     Args:
        None
    Returns:
        None
    """
    indexer = InvertedIndex()
    indexer.indexDirectory(root)
    index = indexer.getInvertedIndex()
    with open("outputs/invertedMatrix.txt", "w", encoding="utf-8") as f:
        for key in index:
            print(key, file=f)
            for tup in index[key]:
                print(f'\t{tup.docID} : {tup.tokenCount}', file=f)

    with open("outputs/matrixDetails.txt", "w", encoding="utf-8") as f:
        count = 0
        for key in index:
            count += 1
            print(f'{key} : {len(index[key])}', file=f)
        
        print(f'\nUnique Tokens: {count}', file=f)
        print(f'Number of Documents: {indexer.getNumDocs()}', file=f)
        print(f'Index size on disk : {get_dict_disk_size_kb(index)} kb', file=f)




if __name__ == '__main__':
    analyzeInvertedIndex(CORPUS_ROOT_PATH)
     