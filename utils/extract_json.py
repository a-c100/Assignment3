import os
import json

CORPUS_ROOT_PATH = "DEV"

def iter_json_files(root):
    for dirpath, _, filenames in os.walk(root):
        for name in sorted(filenames):
            yield os.path.join(dirpath, name)

# @TODO retrieve text, tokenize, and stem
def process_page(page : dict[str, str]):
    content = page["content"]


def extract_and_read_json():
    index : dict[str, list[str]]= {}
    doc_map = {}    

    # extract from each JSON file
    for doc_id, path in enumerate(iter_json_files(CORPUS_ROOT_PATH)):
        with open(path, "r", encoding="utf-8") as f:
            page = json.load(f)

            # @TODO parse page
            # @TODO extract text and tokenize and stem
            # @TODO save frequency
            process_page(page)

            