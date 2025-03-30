import argparse
import json
import os
from utils import ALPHABET, is_symmetric
from utils_enigma import build_enigma_func


parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Input file name")
parser.add_argument("-c", "--config", type=str, help="Enigma machine configuration file")
parser.add_argument("-o", "--outfile", type=str, help="Output file name")

args = parser.parse_args()

if os.path.exists(args.input):
    with open(args.input, 'r') as f:
        cipher = ''.join(f.readlines())
else:
    cipher = args.input

cipher = cipher.strip().upper().replace(" ", "")
for c in cipher:
    if c not in ALPHABET:
        raise Exception(f"Character {c} is not found in the alphabet.")

args.config = "enigma_default.json" if args.config is None else args.config
with open(args.config, "r") as f:
    cfg_dict = json.load(f)

# load alphabet
if "alphabet" in cfg_dict.keys():
    alphabet = cfg_dict["alphabet"]
else:
    alphabet = ALPHABET

# build swapper
if "swap" in cfg_dict.keys():
    plugs = cfg_dict["swap"]
else:
    plugs = {}

P = {}
for p in plugs:
    key, val = p[0], p[1]
    P[key], P[val] = val, key
for a in alphabet:
    if a not in P.keys():
        P[a] = a

# check if swapper is symmetric
if not is_symmetric(P):
    raise Exception(f"Swapper must be symmetric.")

# build scramblers
S = []
for scramble in cfg_dict["scramble"]:
    S.append({k: v for k, v in zip(scramble, alphabet)})

# build reflector
if type(cfg_dict["reflect"]) == str:
    R = {k: v for k, v in zip(cfg_dict["reflect"], alphabet)}
else:
    R = {}
    for p in cfg_dict["reflect"]:
        key, val = p[0], p[1]
        R[key], R[val] = val, key
    for a in alphabet:
        if a not in R.keys():
            R[a] = a

# check if reflector is symmetric
if not is_symmetric(R):
    raise Exception(f"Reflector must be symmetric.")

if "init_key" in cfg_dict.keys():
    init_key = cfg_dict['init_key']
else:
    init_key = [alphabet[0]] * len(S)

# build enigma and decode
enig = build_enigma_func(S, R, P, init_key)
plain = ''.join([enig(c, i) for i, c in enumerate(cipher)])

if args.outfile is None:
    print(plain)
else:
    with open(args.outfile, 'w') as f:
        f.write(plain)