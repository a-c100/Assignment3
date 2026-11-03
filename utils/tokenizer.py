from pathlib import Path

"""
tokenize(path : str) -> list[str]

This function runs in O(n * m) time, where 
n is the number of lines in the file and m is the average
number of characters in each line. 

"""
def tokenize(path : str) -> list[str]:
    # list containing all resulting tokens
    tokens = []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                # tokenize curr line

                # to account for possessive/shortened words
                line = line.lower().replace("'", "") 

                # replace special characters with blank space
                cleaned = ''.join([c if c.isalnum() and c.isascii() else ' ' for c in line])

                # add tokens in the current line to tokens list
                tokens.extend(cleaned.split())

    except:
        raise FileNotFoundError("Could not find file")

    return tokens

"""
This function, computeWordFrequencies(), runs in O(n + m log m), where
n is the length of tokens and k is the number of unique tokens, and k <= n.
The for loop runs once for each token and sorting the dictionary 
takes O(k log k time). 

The function would be in its worst case if all tokens are unique, in 
which case k = n and the runtime would be O(n + nlogn).

"""
def computeWordFrequencies(tokens : list[str]) -> dict[str, int] :
    # resulting freq map
    result = {}

    # add tokens to frequency map
    for token in tokens:
        result[token] = result.get(token, 0) + 1

    # sort dictionary by value desc and alphabetically
    result = dict(sorted(result.items(), key=lambda item: (-item[1], item[0])))

    return result

"""
The function runs in O(n) time, where n is the number of key value pairs 
in the dictionary. It loops through each pair once to print out
its contents. 
"""
def print_map(map : dict[str, int]) -> None :
    for token, freq in map.items():
        print(token + "\t" + str(freq))