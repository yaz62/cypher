from utils import ALPHABET
from utils_enigma import Disc, Discs

cipher = "QHSGUWIG"

scramble = "UWYGADFPVZBECKMTHXSLRINQOJ"
reflect  = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

R = {k: v for k, v in zip(reflect, ALPHABET)}   # Reflector

rot_sgn = -1    # in cypher, scramblers rotate leftwards
for init_n in range(26):
    # initialize scrambler array with different initial key positions
    discs = Discs(Disc(ALPHABET, scramble), init_key=ALPHABET[init_n])

    # decode using the prototype machine
    plain = ""
    for i, c in enumerate(cipher):
        # get input-to-scrambler, scrambler-to-reflector mappings
        Ss, Ss_inv = discs.get_mappings([rot_sgn * i])
        I, S = Ss[0], Ss[1]
        I_inv, S_inv = Ss_inv[0], Ss_inv[1]

        # decode
        plain += I_inv[ S_inv[ R[ S[ I[c] ] ] ] ]
    
    # if the plaintext startswith the Roman numeral XV (from hint), mark it
    if plain.startswith("XV"):
        # output initial scrambler position and plaintext
        print(f"{ALPHABET[init_n]} -", plain)

        # output machine setup
        print('\nMachine setup:')
        discs.print()
        print(reflect)
