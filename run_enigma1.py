from utils import *
from utils_enigma import *
import json

cipher = "ZYDNI"

scramble = "UWYGADFPVZBECKMTHXSLRINQOJ"
reflect  = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# load dictionary
with open("words_dictionary.json", "r") as file:
    wordlist = json.load(file)
wordlist = set(wordlist.keys())

S = {k: v for k, v in zip(scramble, ALPHABET)}
R = {k: v for k, v in zip(reflect, ALPHABET)}

rot_sgn = -1
for init_n in range(26):
    Ss = [rotate_disc(S, int(rot_sgn * (n + init_n))) for n in range(len(cipher))]
    Ss_inv = [get_inv_map(s) for s in Ss]

    enig = lambda c, i: Ss_inv[i][ R[ Ss[i][c] ] ]

    plain = ""
    for i, c in enumerate(cipher):
        plain += enig(c, i)
    
    if plain.lower() in wordlist:
        plain += ' *'

    print(plain)
