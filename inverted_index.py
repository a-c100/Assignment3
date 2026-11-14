import json
from typing import NamedTuple
from utils.extract_json import extract_and_read_json
from utils.constants import UNKNOWN_FILE_NAME

class Posting(NamedTuple):
    ''' stores the document ID and the number of times a token appears in that document '''
    docID: int
    tokenCount: int


class InvertedIndex():
    JSON_INDEX_NAME = 'invertedIndex.json'
    JSON_DOC_MAP_NAME = 'docMap.json'



    def __init__(self):
        self._invertedIndex = dict() # maps each token to its list of docs
        self._docIDtoURL = dict() # maps doc ID's to their page name
        self._docNum = 1 # keeping track of the 
    

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
        return self._invertedIndex 


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
        for token in tokens_map:
            self.add_word_to_index(token, tokens_map[token], docID)


    def index_directory(self, root_path: str, save_dir_path: str | None = None) -> None:
        """
        Given a root directory, recursively iterates through all files and builds the inverted index
        Optionally saves the created inverted index to JSON files in a specified directory

        Args:
            root_path (str): The path to the root directory to index
            save_dir_path (str): Optional path to folder where to save the inverted index class to JSON files after processing

        Returns:
            None
        """
        # creating regular index
        for page_name, stemmed_token_map in extract_and_read_json(root_path):
            self.index_document(page_name, stemmed_token_map)

        #@TODO: Based on get_query_results implementation, see if this sorting is neccessary 
        # sort index for quick search lookup
        # for token in self._invertedIndex:
        #     self._invertedIndex[token] = sorted(self._invertedIndex[token], key = lambda posting: posting.tokenCount, reverse=True)
            
        # save directory to json
        if save_dir_path is None: return
        self.download_index_to_directory(save_dir_path)


    def download_index_to_directory(self, dir_path):
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
            with open(f'{dir_path}/{InvertedIndex.JSON_INDEX_NAME}', "r") as json_file:
                self._invertedIndex = json.load(json_file)
            with open(f'{dir_path}/{InvertedIndex.JSON_DOC_MAP_NAME}', "r") as json_file:
                self._docIDtoURL = json.load(json_file)
            self._docNum = len(self._docIDtoURL) + 1
        except FileNotFoundError: return False
        return True
    


    def get_query_results(self, search_terms: list[str]) -> list[tuple[int, int]]:
        if not search_terms:
            return []

        # retrieve postings for all query terms
        postings = []
        for term in search_terms:
            if term not in self._invertedIndex:
                return []

            postings.append(self._invertedIndex[term])

        # process smallest posting lists first
        postings.sort(key=len)

        # init with first/smallest posting list
        temp_dict = {
            docid: tf
            for docid, tf in postings[0]
        }

        # intersect with remaining posting lists and accumulate total frequency
        for term_list in postings[1:]:
            current_dict = dict(term_list)

            temp_dict = {
                docid: tf + current_dict[docid]
                for docid, tf in temp_dict.items() if docid in current_dict
            }

            if not temp_dict:
                break

        # sort by term frequency
        results = sorted(
            temp_dict.items(),
            key=lambda item: item[1],
            reverse=True
        )

        return results
    
