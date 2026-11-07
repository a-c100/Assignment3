from typing import NamedTuple
from utils.extract_json import *


class Posting(NamedTuple):
    ''' stores the document ID and the number of times a token appears in that document '''
    docID: int
    tokenCount: int


class InvertedIndex():
    def __init__(self):
        self._invertedIndex = dict() # maps each token to its list of docs
        self._docIDtoName = dict() # maps doc ID's to their page name
        self._docNum = 1 # keeping track of the 
    

    def assign_docID(self, doc: string) -> int:
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

        self._docIDtoName[self._docNum] = doc # the mapping
        self._docNum +=1 # increment for new doc
        return docID


    def addWordToIndex(self, token: str, count: int, docID: int) -> None:
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
    

    def getInvertedIndex(self) -> dict[str, list[Posting]]:
        """
        Returns the inverted index 

        Args:
            None

        Returns:
            dict: a mapping of tokens to a list of their Postings
        """
        return self._invertedIndex


    def getNumUniqueTokens(self) -> int:
        """
        Returns the number of unique tokens indexed

        Args:
            None

        Returns:
            int: the number of unique tokens indexed
        """
        return len(self._invertedIndex)
    

    def getNumDocs(self) -> int:
        """
        Returns the number of unique documents indexed

        Args:
            None

        Returns:
            int: the number of unique documents indexed
        """
        return self._docNum - 1


    def indexDocument(self, doc: str, tokens_map: dict[str, int]) -> None:
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
            self.addWordToIndex(token, tokens_map[token], docID)


    def indexDirectory(self, root_path : str = CORPUS_ROOT_PATH) -> None:
        """
        Given a root directory, recursively iterates through all files and, builds the inverted index

        Args:
            root_path (str): The path to the root directory to index

        Returns:
            None
        """
        # creating regular index
        for page_name, stemmed_token_map in extract_and_read_json(root_path):
            self.indexDocument(page_name, stemmed_token_map)
