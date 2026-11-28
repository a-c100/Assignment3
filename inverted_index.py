import json
from typing import NamedTuple
from utils.extract_json import extract_and_read_json
from utils.constants import UNKNOWN_FILE_NAME, DOCS_PER_PARTIAL, PARTIAL_DIR
from math import log, log10
import os
import glob
import shutil

class Posting(NamedTuple):
    ''' stores the document ID and the number of times a token appears in that document '''
    docID: int
    tokenCount: int


class InvertedIndex():
    JSON_INDEX_NAME = 'invertedIndex.json'
    JSON_DOC_MAP_NAME = 'docMap.json'
    JSON_DOC_LENGTHS_NAME = 'docLengths.json'

    def __init__(self):
        self._invertedIndex = dict() # maps each token to its list of docs
        self._docIDtoURL = dict() # maps doc ID's to their page name
        self._docNum = 1 # keeping track of the
        self._docLengths = dict() # maps doc id to token count
        self._partialIndexCount = 0 # number of partial indexes
        self._partialDir = None

    def assign_docID(self, doc: str) -> int:
        """
        Assigns a unique integer to each indexed document

        Args:
            doc (string): The document's name
        Returns:
            int: the docID for this specific document
        """
        docID = self._docNum # assign doc number
        if doc == UNKNOWN_FILE_NAME: # unknown -> add docid to name for distinguishing
            doc += str(docID) 

        self._docIDtoURL[self._docNum] = doc # the mapping
        self._docNum +=1 # increment for new doc
        return docID


    def add_word_to_index(self, token: str, count: int, docID: int) -> None:
        """
        Appends a Posting object to the list of documents mapped to token

        Args:
            token (string): The word to index
            count (int): The frequency of token in the document
            docID (int): The unique number assigned to the document where token appears

        Returns:
            None
        """
        if not token in self._invertedIndex: # creates list for the tokens not already documented 
            self._invertedIndex[token] = list() 

        # add its docnum and its freq in doc to dict
        docInf = Posting(docID, count) 
        self._invertedIndex[token].append(docInf)
    

    def get_inverted_index(self) -> dict[str, list[Posting]]:
        """
        Returns the inverted index 

        Args:
            None

        Returns:
            dict: a mapping of tokens to a list of their Postings
        """
        return self._invertedIndex
    
    def get_document_map(self) -> dict[int, str]:
        """
        Returns the mapping of Document IDs to their respective URLs

        Args:
            None

        Returns:
            dict: a mapping of Document IDs to URLs
        """
        return self._docIDtoURL 


    def get_num_unique_tokens(self) -> int:
        """
        Returns the number of unique tokens indexed

        Args:
            None

        Returns:
            int: the number of unique tokens indexed
        """
        return len(self._invertedIndex)
    

    def get_num_docs(self) -> int:
        """
        Returns the number of unique documents indexed

        Args:
            None

        Returns:
            int: the number of unique documents indexed
        """
        return self._docNum - 1

    def index_document(self, doc: str, tokens_map: dict[str, int]) -> None:
        """
        Indexes a document, assigining doc an integer ID and extending the inverted index

        Args:
            doc (str): The name of the document being indexed
            tokens_map (dict[str, int]): A mapping of tokens to their frequency in doc

        Returns:
            None
        """
        # docid to name mapping 
        docID = self.assign_docID(doc)
        doc_length = sum(tokens_map.values())
        self._docLengths[docID] = doc_length
        for token in tokens_map:
            self.add_word_to_index(token, tokens_map[token], docID)

    def _write_partial(self, dir_path : str) -> None:
        """
        Writes the partial inverted index to disc and clears the inverted index in memory

        Args:
            dir_path (str): name of directory to save the partial index
        Returns:
            None
        """
        os.makedirs(dir_path, exist_ok=True)
        path : str = f"{dir_path}/partial_{self._partialIndexCount}.json"

        # sort index so it's easier to merge later
        sorted_index = dict(sorted(self._invertedIndex.items()))
        with open(path, "w") as f:
            json.dump(sorted_index, f, indent=2)

        self._partialIndexCount += 1

        # clear inverted index
        self._invertedIndex.clear()

    def _merge_partials(self, partial_dir, save_dir):
        os.makedirs(save_dir, exist_ok=True)
        buckets = ['_'] + list('abcdefghijklmnopqrstuvwxyz')

        for b in buckets:
            merged = {}
            for i in range(self._partialIndexCount):      # partial order preserved
                with open(f'{partial_dir}/partial_{i}.json') as f:
                    partial = json.load(f)
                for token, postings in partial.items():
                    if _bucket(token) == b:
                        merged.setdefault(token, []).extend(postings)

            if merged:
                with open(f'{save_dir}/index_{b}.json', 'w') as f:
                    json.dump(merged, f)

    def index_directory(self, root_path: str, save_dir_path: str = None) -> None:
        """
        Given a root directory, recursively iterates through all files and builds the inverted index
        Optionally saves the created inverted index to JSON files in a specified directory

        Args:
            root_path (str): The path to the root directory to index
            save_dir_path (str): Optional path to folder where to save the inverted index class to JSON files after processing

        Returns:
            None
        """
        if os.path.exists(PARTIAL_DIR):
            shutil.rmtree(PARTIAL_DIR)

        os.makedirs(PARTIAL_DIR, exist_ok=True)
        self._partialIndexCount = 0

        # creating index
        for page_name, stemmed_token_map in extract_and_read_json(root_path):
            self.index_document(page_name, stemmed_token_map)
            if self.get_num_docs() % DOCS_PER_PARTIAL == 0:
                self._write_partial(PARTIAL_DIR)

        # write leftover docs
        if self._invertedIndex:
            self._write_partial(PARTIAL_DIR)

        # merge partial docs
        self._merge_partials(PARTIAL_DIR, save_dir_path)

        #@TODO: Based on get_query_results implementation, see if this sorting is neccessary 
        # sort index for quick search lookup
        # for token in self._invertedIndex:
        #     self._invertedIndex[token] = sorted(self._invertedIndex[token], key = lambda posting: posting.tokenCount, reverse=True)
            
        # save directory to json
        if save_dir_path is None: save_dir_path = InvertedIndex.JSON_INDEX_NAME
        self.download_index_to_directory(save_dir_path)


    def download_index_to_directory(self, dir_path):
        os.makedirs(dir_path, exist_ok=True)
        """
        Given a path to a directory, saves the inverted index to a JSON file, then
        saves the mapping of document IDs to URLs to another JSON file 

        Args:
            dir_path (str): Path to the folder where to save the class attributes as JSON files

        Returns:
            None
        """
        with open(f'{dir_path}/{InvertedIndex.JSON_INDEX_NAME}', "w") as json_file:
            json.dump(self._invertedIndex, json_file, indent=4)
        with open(f'{dir_path}/{InvertedIndex.JSON_DOC_MAP_NAME}', "w") as json_file:
            json.dump(self._docIDtoURL, json_file, indent=4)
        with open(f'{dir_path}/{InvertedIndex.JSON_DOC_LENGTHS_NAME}', "w") as json_file:
            json.dump(self._docLengths, json_file, indent=4)
    

    def load_index_from_directory(self, dir_path) -> bool:
        """
        Given a path to a directory, loads the inverted index from a JSON file, then
        loads the mapping of document IDs to URLs to another JSON file

        Args:
            dir_path (str): Path to the folder where to load the class attributes from JSON files

        Returns:
            bool: Whether or not the files were found in the directory and processed successfully 
        """
        
        try:
            # doc map: JSON keys come back as strings, so convert to int
            with open(f'{dir_path}/{InvertedIndex.JSON_DOC_MAP_NAME}', "r") as f:
                self._docIDtoURL = {int(k): v for k, v in json.load(f).items()}

            # doc lengths: load from disk
            with open(f'{dir_path}/{InvertedIndex.JSON_DOC_LENGTHS_NAME}', "r") as f:
                self._docLengths = {int(k): v for k, v in json.load(f).items()}

            self._docNum = len(self._docIDtoURL) + 1

            # inverted index: merge every bucket file (buckets hold disjoint tokens)
            self._invertedIndex = {}
            bucket_files = glob.glob(f'{dir_path}/index_*.json')
            if not bucket_files:
                return False
            for path in bucket_files:
                with open(path, "r") as f:
                    self._invertedIndex.update(json.load(f))
        except FileNotFoundError: return False
        return True
    

    # @TODO Add logic for partial indexes here to return to query function
    def get_postings(self, search_terms: list[str]) -> list[list[Posting]]:
        postings = []
        if not search_terms: return []
        for term in search_terms:
            # function currently returns nothing if any search term in the list is invalid
            # potentially continue instead if we want best results in spite of a faulty query term
            if term not in self._invertedIndex:
                return []

            postings.append(self._invertedIndex[term])
        
        return postings


    def get_query_results(self, search_terms: list[str]) -> list[tuple[int, int]]:
        # retrieve postings for all query terms
        postings = self.get_postings(search_terms)

        # ensure valis postings
        if not postings or any(not p for p in postings): return []

        # process smallest posting lists first
        postings.sort(key=len)

        # shortest list provides our candidate documents
        candidates = postings[0]

        # one pointer for each remaining posting list
        pointers = [0] * len(postings)

        results = []

        # iterate through candidate documents
        for docid, tf in candidates:
            total_tf = tf
            matched = True

            # compare candidate against every other posting list
            for i in range(1, len(postings)):
                current_list = postings[i]
                pointer = pointers[i]

                # advance until we reach the candidate or pass it
                while (pointer < len(current_list) and
                    current_list[pointer][0] < docid):
                    pointer += 1

                pointers[i] = pointer

                # candidate is missing from this posting list
                if (pointer == len(current_list) or
                        current_list[pointer][0] != docid):
                    matched = False
                    break

                #@TODO: Adapt this for tf-idf scores
                # accumulate term frequency
                total_tf += current_list[pointer][1]

            if matched:
                results.append((docid, total_tf))

        # rank by accumulated term frequency
        results.sort(key=lambda item: item[1], reverse=True)

        return results

    #@TODO apply TF-IDF logic to post-processing of index creation, not in real-time querying
    def get_query_results_tf_idf(self, search_terms: list[str]) -> list[tuple[int, float]]:
        if not search_terms:
            return []

        term_data = []
        for term in search_terms:
            postings = self._invertedIndex.get(term)
            if not postings:
                return []

            # {doc ID: token count}
            doc_freqs = dict(postings)

            # calculate inverse document frequency - IDF(term, Document)
            idf = log((self.get_num_docs() + 1) / (len(postings) + 1)) + 1

            term_data.append((doc_freqs, idf))

        # retrieve first term's documents
        matching_docs = set(term_data[0][0])

        # use other term's documents to update the intersection
        for doc_freqs, _ in term_data[1:]:
            matching_docs.intersection_update(doc_freqs)
            if not matching_docs:
                return []

        # summation of scores of each document: TF * IDF
        scores = {
            doc_id: sum(
                (doc_freqs[doc_id] / self._docLengths[doc_id]) * idf
                # (1 + log10(doc_freqs[doc_id])) * idf
                for doc_freqs, idf in term_data
            )
            for doc_id in matching_docs
        }

        return sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
def _bucket(token):
    return token[0] if token[0].isalpha() else '_'   # digits/symbols together
