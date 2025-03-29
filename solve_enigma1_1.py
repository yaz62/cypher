from utils_enigma import *

cipher = "ZYDNI"

scramble = "UWYGADFPVZBECKMTHXSLRINQOJ"
reflect  = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# build scrambler
S = {k: v for k, v in zip(scramble, ALPHABET)}
# build reflector
R = {k: v for k, v in zip(reflect, ALPHABET)}

rot_sgn = -1
init_n = 1

# get scramblers for each rotation
Ss = [rotate_scrambler(S, int(rot_sgn * (n + init_n))) for n in range(len(cipher))]
# get inverse scramblers for each rotation
Ss_inv = [get_inv_map(s) for s in Ss]
# build enigma prototype, transformation: S^-1 R S
enig = lambda c, i: Ss_inv[i][ R[ Ss[i][c] ] ]

# decode using the prototype
plain = ""
for i, c in enumerate(cipher):
    plain += enig(c, i)

print(plain)
