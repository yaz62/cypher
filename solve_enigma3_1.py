from utils import *
from utils_enigma import Disc, Discs

cipher = "GYHRVFLRXY"

plugs = ['AB', 'SZ', 'UY', 'GH', 'LQ', 'EN']
scramble1 = "UWYGADFPVZBECKMTHXSLRINQOJ"
scramble2 = "AJPCZWRLFBDKOTYUQGENHXMIVS"
scramble3 = "TAGBPCSDQEUFVNZHYIXJWLRKOM"
reflect  = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
init_key = 'AEB'

# build swapper
P = {}
for p in plugs:
    key, val = p[0], p[1]
    P[key], P[val] = val, key
for a in ALPHABET:
    if a not in P.keys():
        P[a] = a

# build initial scramblers, order: 2 -> 1 -> 3
discs = Discs(
                    Disc(ALPHABET, scramble2),
                    Disc(ALPHABET, scramble1),
                    Disc(ALPHABET, scramble3),
                    init_key=init_key,
                )
print("Scrambler Setup:")
print('-' * len(ALPHABET))
discs.print()
print('-' * len(ALPHABET))

# build reflector
R = {k: v for k, v in zip(reflect, ALPHABET)}

rot_sgn = -1
plain = ""
for i, c in enumerate(cipher):
    # apply swapper
    x = P[c]

    # get rotated scramblers
    r1 = i + 1
    r2 = r1 // len(ALPHABET)
    r3 = r2 // len(ALPHABET)
    S, S_inv = discs.get_mappings([rot_sgn*r1, rot_sgn*r2, rot_sgn*r3])

    # apply scrambler
    for s in S:
        x = s[x]

    # apply reflector
    x = R[x]

    # apply inverse scramblers
    for s in S_inv[::-1]:
        x = s[x]

    # apply swapper
    x = P[x]

    plain += x

print(plain)