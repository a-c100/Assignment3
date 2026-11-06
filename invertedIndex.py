from stemming import Stemmer
from typing import NamedTuple

class Posting(NamedTuple):
    docID: int
    tokenCount: int


class InvertedIndex():
    def __init__(self):
        self._invertedIndex = dict()
        # self._docNameToID = dict()
        self._docIDtoName = dict()
        self._docNum = 1
        # self._stemmer = Stemmer()
    

    def assign_docID(self, doc) -> int:
        docName = doc #.name
        docID = self._docNum
        # self._docNameToID[docName] = self._docNum
        self._docIDtoName[self._docNum] = docName
        self._docNum +=1
        return docID


    def addWordToIndex(self, token, count, docID):
        if not token in self._invertedIndex:
            self._invertedIndex[token] = set()
    
        docInf = Posting(docID, count)
        self._invertedIndex[token].add(docInf)
    

    def getInvertedIndex(self) -> dict:
        return self._invertedIndex


    def getNumUniqueTokens(self) -> int:
        return len(self._invertedIndex)


    def indexDocument(self, doc):
        '''
        
        '''

        docID = self.assign_docID(doc)
        
        tokens_map = ...# = tokenize_and_stem(doc)
        for token in tokens_map:
            self.addWordToIndex(token, tokens_map[token], docID)





'''
data structure to map doc id back to doc blah blah blah baguette
'''