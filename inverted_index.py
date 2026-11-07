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
    
    def assign_docID(self, doc) -> int:
        docID = self._docNum # assign doc number
        if doc == UNKNOWN_FILE_NAME: # unknown -> add docid to name for distinguishing
            doc += str(docID) 

        self._docIDtoName[self._docNum] = doc # the mapping
        self._docNum +=1 # increment for new doc
        return docID

    def addWordToIndex(self, token, count, docID) -> None:
        if not token in self._invertedIndex: # creates list for the tokens not already documented 
            self._invertedIndex[token] = list() 

        # add its docnum and its freq in doc to dict
        docInf = Posting(docID, count) 
        self._invertedIndex[token].append(docInf)
    
    def getInvertedIndex(self) -> dict:
        return self._invertedIndex

    def getNumUniqueTokens(self) -> int:
        return len(self._invertedIndex)
    
    def getNumDocs(self) -> int:
        return self._docNum - 1

    def indexDocument(self, doc, tokens_map) -> None:
        # docid to name mapping 
        docID = self.assign_docID(doc)
        
        for token in tokens_map:
            self.addWordToIndex(token, tokens_map[token], docID)


    def indexDirectory(self, root_path = CORPUS_ROOT_PATH) -> None:
        # creating regular index
        for page_name, stemmed_token_map in extract_and_read_json(root_path):
            self.indexDocument(page_name, stemmed_token_map)