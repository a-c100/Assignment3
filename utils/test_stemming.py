import stemming

def test_stemmer(word, expected):
    stemmer = stemming.Stemmer()
    actual = stemmer.stem(word)
    result = "PASS" if actual == expected else "FAIL"

    print(f"{result} | Input: {word:<18} Expected: {expected:<15} Actual: {actual}")

# examples from Lecture 13, slide 22
test_stemmer('stresses', 'stress')
test_stemmer('gaps', 'gap')
test_stemmer('gas', 'gas')
test_stemmer('ties', 'tie')
test_stemmer('cries', 'cri')
test_stemmer('falling', 'fall')
test_stemmer('stress', 'stress')
test_stemmer('agreed', 'agree')
test_stemmer('feed', 'feed')
test_stemmer('fished', 'fish')
test_stemmer('pirating', 'pirate')
test_stemmer('falling', 'fall')
test_stemmer('hoping', 'hope')