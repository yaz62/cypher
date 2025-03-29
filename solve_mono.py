import json
from utils import *
from utils_adv import word_segment

cipher =  'AJLPNYRJZJFLZYASGSKQGSMME'
cipher += 'JKEJPFSVLPJLKKEJELNNSPZKY'
cipher += 'NNYGNSGASGYZJGAKEYZYGASVW'
cipher += 'NJKSWSKECNLUJZKEJZEYCYZWS'
cipher += 'VOEKLGAHYKKJAZEJNYJZLKLGU'
cipher += 'ESPPJLAFHSPZJLFSVGJRJPYTL'
cipher += 'OYGJALZMJJKJPZUESSGJPLUEY'
cipher += 'NATYOEKZLYNEJPKMSEVGAPJAK'
cipher += 'SGZGTJEYZCLGYSNL'

# load dictionary
with open("words_dictionary.json", "r") as file:
    wordlist = json.load(file)
wordlist = list(wordlist.keys())

# singleton frequencies
print(patfreq(cipher, '.'), '\n')

# doubleton frequencies
print(patfreq(cipher, '..', cutoff=2), '\n')

# tripleton frequencies
print(patfreq(cipher, '...', cutoff=2), '\n')

# the
print(patfreq(cipher, '.E.', cutoff=2), '\n')

# is/in
print(patfreq(cipher, 'Y.', cutoff=2), '\n')

# replace deciphered characters
mapdict = {
            'K': 't',
            'E': 'h',
            'J': 'e',
            'Y': 'i',
            'Z': 's',
            'A': 'd',
            'N': 'l',
            'C': 'p',
            'L': 'a',
            'G': 'n',
            'S': 'o',
            'M': 'w',
            'P': 'r',
            'Q': 'k',
            'V': 'u',
            'U': 'c',
            'H': 'f',
            'W': 'b',
            'O': 'g',
            'F': 'y',
            'R': 'v',
            'T': 'm'
        }
print(cipher)
decipher = replchar(cipher, mapdict)
print(decipher)

print('\n', '** Segmentation:')
print(' '.join(word_segment(decipher)))