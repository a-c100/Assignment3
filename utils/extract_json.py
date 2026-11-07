import os
import json

from .tokenizer import *
from .stemming import Stemmer
from bs4 import BeautifulSoup

UNKNOWN_FILE_NAME = 'Untitled'
CORPUS_ROOT_PATH = 'Data_Sources/DEV'

def iter_json_files(root): 
    '''
    goes through the directory and its subdirectory to find the JSON files

    yield: pauses func and saves internal state, it sends value back back to caller. 
    when func is called again, it resumes where its internal state was.
    '''
    for dirpath, _, filenames in os.walk(root):
        for name in sorted(filenames):
            yield os.path.join(dirpath, name) 

# @TODO retrieve text, tokenize, and stem
def process_page(content) -> tuple[str, dict[str, int]]:
    stemmer = Stemmer()
    
    #parse page
    soup = BeautifulSoup(content, "html.parser")
    
    # @TODO extract text and tokenize and stem
    raw_text = soup.get_text(separator=" ", strip=True)
    tokens = tokenize(raw_text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    page_name = soup.title.get_text(strip=True) if soup.title else UNKNOWN_FILE_NAME

    # can be modified back later to return list if we care about token position
    return page_name, computeWordFrequencies(stemmed_tokens)

'''
    stemmed_token_map = dict()
    for token in tokens:
        if not token in stemmed_token_map:
            stemmed_token_map[token] = 0
        stemmed_token_map[token] += 1

    return stemmed_token_map'''


def extract_and_read_json(root_path = CORPUS_ROOT_PATH):
    # key is a string, list containg strings pair
    # index : dict[str, list[str]]= {}
    # doc_map = {}    

    # extract from each JSON file
    for path in iter_json_files(root_path):
        with open(path, "r", encoding="utf-8") as f:
            try: 
                page = json.load(f)
                page_name, stemmed_token_map = process_page(page["content"])
                yield page_name, stemmed_token_map
            except UnicodeDecodeError:
                continue
            # @TODO save frequency