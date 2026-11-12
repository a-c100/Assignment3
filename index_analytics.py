from inverted_index import *
from utils.constants import CORPUS_ROOT_PATH, JSON_DIRECTORY_NAME
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


def analyzeInvertedIndex(root : str, json_save_folder = None, write_to_txt_file = True) -> None:
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
    if write_to_txt_file:
        with open("outputs/invertedMatrix.txt", "w", encoding="utf-8") as f:
            for key in index:
                print(key, file=f)
                for tup in index[key]:
                    print(f'\t{tup.docID} : {tup.tokenCount}', file=f)

        with open("outputs/matrixDetails.txt", "w", encoding="utf-8") as f:
            for key in index:
                print(f'{key} : {len(index[key])}', file=f)

            print(f'\nUnique Tokens: {indexer.getNumUniqueTokens()}', file=f)
            print(f'Number of Documents: {indexer.getNumDocs()}', file=f)
            print(f'Index size on disk : {get_dict_disk_size_kb(index)} kb', file=f)

    if json_save_folder != None:
        indexer.downloadIndexToDirectory(json_save_folder)




if __name__ == '__main__':
    analyzeInvertedIndex(CORPUS_ROOT_PATH, JSON_DIRECTORY_NAME, write_to_txt_file=False)
     