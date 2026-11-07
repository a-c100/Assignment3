from pathlib import Path
import string
"""
tokenize(text: str) -> list[str]

Converts text to lowercase ASCII alphanumeric tokens.
Returns all tokens, including duplicates.

Time complexity: O(n), where n is the number
of characters in the input text.
"""

# def tokenize(text) -> list[str]:
#     # list containing all resulting tokens
#     tokens = []
    
#     # replace special characters with blank space
#     cleaned = ''.join([c if c.isalnum() and c.isascii() else ' ' for c in text])

#     # add tokens in the current line to tokens list
#     tokens.extend(cleaned.split())

#     return tokens

def tokenize(text) -> list[str]:
    """
    converts text into lower case tokens defined as alphanumeric sequences in the dataset. 
    
    makestrans() creates a transition table that replaces the character w/ a space if c isn't
    in allowed.  
    """
    allowed = string.ascii_letters + string.digits

    translator = str.maketrans({ 
        c: ' ' for c in set(text) if c not in allowed
    })

    return text.lower().translate(translator).split()

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