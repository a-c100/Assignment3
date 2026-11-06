import os
import json
import tokenizer
import stemming
from bs4 import BeautifulSoup

CORPUS_ROOT_PATH = "ANALYST"

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
def process_page(content):
    stemmer = stemming.Stemmer()
    # @TODO parse page
    soup = BeautifulSoup(content, "html.parser")
    
    # @TODO extract text and tokenize and stem
    raw_text = soup.get_text(separator=" ", strip=True)
    tokens = tokenizer.tokenize(raw_text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    return tokens




def extract_and_read_json():
    # key is a string, list containg strings pair
    index : dict[str, list[str]]= {}
    doc_map = {}    

    # extract from each JSON file
    for doc_id, path in enumerate(iter_json_files(CORPUS_ROOT_PATH)):
        with open(path, "r", encoding="utf-8") as f:
            page = json.load(f)
            stemmed_tokens = process_page(page["content"])
            # @TODO save frequency


            