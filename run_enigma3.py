from utils import *
from utils_enigma import *

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

# build initial scrambles
S1 = {k: v for k, v in zip(scramble1, ALPHABET)}
S2 = {k: v for k, v in zip(scramble2, ALPHABET)}
S3 = {k: v for k, v in zip(scramble3, ALPHABET)}
S = [S2, S1, S3]

# build reflector
R = {k: v for k, v in zip(reflect, ALPHABET)}

# initial keys
I = [ALPHABET.index(k) for k in init_key]

rot_sgn = -1
plain = ""
for i, c in enumerate(cipher):
    # apply swapper
    x = P[c]

    # get rotated scramblers
    r1 = i + 1 + I[0]
    r2 = r1 // len(ALPHABET) + I[1]
    r3 = r2 // len(ALPHABET) + I[2]
    r = [r1, r2, r3]

    S_ = [rotate_scrambler(S[j], int(rot_sgn*r[j])) for j in range(len(S))]

    # apply scrambler
    for s in S_:
        x = s[x]

    # apply reflector
    x = R[x]

    # apply inverse scramblers
    for s in S_[::-1]:
        x = get_inv_map(s)[x]

    # apply swapper
    x = P[x]

    plain += x

print(plain)