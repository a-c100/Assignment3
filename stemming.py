VOWELS = set('a e i o u'.split())


class Stemmer():
    def __init__(self, stemmer = 'porter'):
        self.stemmers = {'porter': self.porterStem}
        self.stemmer_func = self.stemmers[stemmer]

    def stem(self, word: str) -> str:
        return self.stemmer_func(word)


    def is_vowel(self, letter: str):
        return letter in VOWELS

    def contains_vowel(self, word: str):
        for letter in word:
            if self.is_vowel(letter):
                return True
        return False

    def measure(self, word):
        count = 0
        prev_vowel = False

        for letter in word:
            current_vowel = self.is_vowel(letter)

            if prev_vowel and not current_vowel:
                count += 1

            prev_vowel = current_vowel

        return count


    def porterStem(self, word: str) -> str:
        # step 1a
        if word.endswith('sses'): #sses -> ss
            word = word[:-2]


        elif word.endswith(('ied', 'ies')):
            word = word[:-3]
            if len(word) > 1:
                word += 'i'
            else:
                word += 'ie'

        elif word.endswith('s') and len(word) > 2 and (not word.endswith(('ss','us'))):
            if self.contains_vowel(word[:-2]):
                word = word[:-1]

        # step 1b
        if word.endswith(('eed', 'eedly')):
            if word.endswith('eedly'):
                stem = word[:-5]
            else:
                stem = word[:-3]

            if self.measure(stem) > 0:
                word = stem + 'ee'

        # delete ed/edly/ing/ingly if preceding word part contains a vowel
        elif word.endswith(('ed', 'edly', 'ing', 'ingly')):

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







