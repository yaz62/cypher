from utils_enigma import *
import json

cipher = "ZYDNI"

scramble = "UWYGADFPVZBECKMTHXSLRINQOJ"
reflect  = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# load dictionary
with open("words_dictionary.json", "r") as file:
    wordlist = json.load(file)
wordlist = set(wordlist.keys())

# build scrambler
S = {k: v for k, v in zip(scramble, ALPHABET)}
# build reflector
R = {k: v for k, v in zip(reflect, ALPHABET)}

rot_sgn = -1
for init_n in range(26):
    # get scramblers for each rotation
    Ss = [rotate_disc(S, int(rot_sgn * (n + init_n))) for n in range(len(cipher))]
    # get inverse scramblers for each rotation
    Ss_inv = [get_inv_map(s) for s in Ss]
    # build enigma prototype, transformation: S^-1 R S
    enig = lambda c, i: Ss_inv[i][ R[ Ss[i][c] ] ]

    # decode using the prototype
    plain = ""
    for i, c in enumerate(cipher):
        plain += enig(c, i)
    
    # if the plaintext means something, label it
    if plain.lower() in wordlist:
        plain += ' *'

    print(plain)
