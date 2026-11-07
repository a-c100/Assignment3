from typing import NamedTuple
from utils.extract_json import *

class Posting(NamedTuple):
    docID: int
    tokenCount: int


class InvertedIndex():
    def __init__(self):
        self._invertedIndex = dict()
        self._docIDtoName = dict()
        self._docNum = 1
    
    def assign_docID(self, doc) -> int:
        docID = self._docNum
        if doc == UNKNOWN_FILE_NAME:
            doc += str(docID)
        self._docIDtoName[self._docNum] = doc
        self._docNum +=1
        return docID

    def addWordToIndex(self, token, count, docID) -> None:
        if not token in self._invertedIndex:
            self._invertedIndex[token] = list()
    
        docInf = Posting(docID, count)
        self._invertedIndex[token].append(docInf)
    
    def getInvertedIndex(self) -> dict:
        return self._invertedIndex

    def getNumUniqueTokens(self) -> int:
        return len(self._invertedIndex)
    
    def getNumDocs(self) -> int:
        return self._docNum - 1

    def indexDocument(self, doc, tokens_map) -> None:
        docID = self.assign_docID(doc)
        
        for token in tokens_map:
            self.addWordToIndex(token, tokens_map[token], docID)


    def indexDirectory(self, root_path = CORPUS_ROOT_PATH) -> None:
        for page_name, stemmed_token_map in extract_and_read_json(root_path):
            self.indexDocument(page_name, stemmed_token_map)