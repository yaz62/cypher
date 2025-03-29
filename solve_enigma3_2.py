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

enig = build_enigma_func(S, R, P, init_key)
plain = ''.join([enig(c, i) for i, c in enumerate(cipher)])
print(plain)