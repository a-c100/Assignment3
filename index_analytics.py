from inverted_index import *
import io
import pickle

def get_dict_disk_size_kb(my_dict) -> int:
    # serialize dict into memory buffer using latest protocol
    buffer = io.BytesIO()
    pickle.dump(my_dict, buffer, protocol=pickle.HIGHEST_PROTOCOL)
    
    # raw size in bytes
    bytes_size = buffer.tell()
    
    # bytes to kilobytes
    size_in_kb = bytes_size / 1024
    return int(size_in_kb)


def analyzeInvertedIndex():
    indexer = InvertedIndex()
    indexer.indexDirectory('Data_Sources/DEV')
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
        
        print(f'\nUnique tokens: {count}', file=f)
        print(f'Number of Documents: {indexer.getNumDocs()}', file=f)
        print(f'Index size on disk : {get_dict_disk_size_kb(index)}', file=f)




if __name__ == '__main__':
    analyzeInvertedIndex()
     