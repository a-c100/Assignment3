# used for stemming
VOWELS = set('a e i o u'.split())


class Stemmer():
    def __init__(self, stemmer = 'porter'):
        self.stemmers = {'porter': self.porterStem} # storing available stemming methods
        self.stemmer_func = self.stemmers[stemmer] # selects which stemming method to use (porter)

    def stem(self, word: str) -> str:
        return self.stemmer_func(word) # return stemmed word w/ applied method


    def is_vowel(self, letter: str):
        # checks if letter is vowel
        return letter in VOWELS

    def contains_vowel(self, word: str):
        # checks if the word contains at least one vowel
        for letter in word:
            if self.is_vowel(letter):
                return True
        return False

    def measure(self, word):
        # counts vowel-to-consonant transitions
        count = 0
        prev_vowel = False

        for letter in word:
            current_vowel = self.is_vowel(letter)

            # increase count when a vowel is followed by a consonant
            if prev_vowel and not current_vowel:
                count += 1

            prev_vowel = current_vowel

        return count


    def porterStem(self, word: str) -> str:
        word = word.lower()

        # step 1a: handle plural endings
        if word.endswith('sses'): #sses -> ss
            word = word[:-2]


        elif word.endswith(('ied', 'ies')):
            # replace ending with i or ie depending on stem length
            word = word[:-3]
            if len(word) > 1:
                word += 'i'
            else:
                word += 'ie'

        elif word.endswith('s') and len(word) > 2 and (not word.endswith(('ss','us'))):
            # remove s if the preceding part contains a vowel
            if self.contains_vowel(word[:-2]):
                word = word[:-1]

        # step 1b: handle past tense and -ing endings
        if word.endswith(('eed', 'eedly')):
            # remove suffix to get the stem
            if word.endswith('eedly'):
                stem = word[:-5]
            else:
                stem = word[:-3]

            # replace ending with ee if vowel-to-consonant is greater than 0
            if self.measure(stem) > 0:
                word = stem + 'ee'

        # delete ed/edly/ing/ingly if preceding word part contains a vowel
        elif word.endswith(('ed', 'edly', 'ing', 'ingly')):

            # remove the matching suffix
            if word.endswith('edly'):
                stem = word[:-4]
            elif word.endswith('ingly'):
                stem = word[:-5]
            elif word.endswith('ed'):
                stem = word[:-2]
            else:
                stem = word[:-3]

            if self.contains_vowel(stem):
                word = stem

                # if ending is at, bl, or iz, add e
                if word.endswith(('at', 'bl', 'iz')):
                    word += 'e'

                # if ending is ll, ss, or zz, do nothing
                elif word.endswith(('ll', 'ss', 'zz')):
                    pass

                # word ends in double consonant, remove last letter
                elif len(word) >= 2 and word[-1] == word[-2] and not self.is_vowel(word[-1]):
                    word = word[:-1]

                # add e if short word
                elif len(word)<=3:
                    word += 'e'

        return word







