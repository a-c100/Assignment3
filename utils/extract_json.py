import os
import json

from .tokenizer import *
from .stemming import Stemmer
from bs4 import BeautifulSoup
from utils.constants import UNKNOWN_FILE_NAME

def iter_json_files(root): 
    '''
    goes through the directory and its subdirectory to find the JSON files

    yield: pauses func and saves internal state, it sends value back back to caller. 
    when func is called again, it resumes where its internal state was.
    '''
    for dirpath, _, filenames in os.walk(root):
        for name in sorted(filenames):
            yield os.path.join(dirpath, name) 


def process_page(content) -> tuple[str, dict[str, int]]:
    '''
    takes in the JSON file's content and parses it using BeautifulSoup
    with an HTML parser.

    extracts the text without the HTML tags, tokenizes it, and applies
    stemming to each token.

    returns a tuple containing the page_name as a string and a dictionary
    of tokens with their frequencies.
    '''
    stemmer = Stemmer()
    
    #parse page
    soup = BeautifulSoup(content, "html.parser")
    
    # extracts text and tokenize and stem
    raw_text = soup.get_text(separator=" ", strip=True)
    tokens = tokenize(raw_text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    page_name = soup.title.get_text(strip=True) if soup.title else UNKNOWN_FILE_NAME

    # can be modified back later to return list if we care about token position
    return page_name, computeWordFrequencies(stemmed_tokens)


def extract_and_read_json(root_path):
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