from utils import *
from utils_enigma import *

cipher = "ZYDNI"

input = ALPHABET
scramble = "UWYGADFPVZBECKMTHXSLRINQOJ"
reflect  = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

I = {k: v for k, v in zip(ALPHABET, ALPHABET)}  # Input to Scrambler
S = {k: v for k, v in zip(scramble, ALPHABET)}  # Scrambler to Reflector
R = {k: v for k, v in zip(reflect, ALPHABET)}   # Reflector

rot_sgn = -1
init_n = 1

# For each scrambler rotation, rotate I forward...
Is = [rotate_dict(I, int(rot_sgn * (n + init_n))) for n in range(len(cipher))]
Is_inv = [get_inv_map(i) for i in Is]

# ...and S backward
Ss = [rotate_dict(S, int(-rot_sgn * (n + init_n))) for n in range(len(cipher))]
Ss_inv = [get_inv_map(s) for s in Ss]

# build enigma prototype, transformation: I^-1 S^-1 R S I
enig = lambda c, i: Is_inv[i][Ss_inv[i][ R[ Ss[i][ Is[i][c] ] ] ] ]

plain = ""
for i, c in enumerate(cipher):
    plain += enig(c, i)

print(plain)
