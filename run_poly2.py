import numpy as np

from utils import *
from utils_adv import word_segment
import itertools
import json

cipher =  'LAFLUIWOYWPADUFHSNBVSWVNDZQDUF'
cipher += 'RBPLUYQPLWLPHZRLUEDUBSYMIPRDIJ'
cipher += 'HTYQUCUZYLKFRSKHZBUHULUEKPQFOY'
cipher += 'LYSSAMWOCWHZOLGDTDDPPOFDDTGOPY'
cipher += 'UDGWOYOSDRYKVVDVLAULRZYGWPLJZY'
cipher += 'QKYPTWVLJIAFHHSWOMUVDDAPLMJLUE'
cipher += 'PVLRNPDWFXWMQAFHZSEQCFAGQDFLJF'
cipher += 'LHLDSWCLMQLFXUBULBDUBVPVWFQHWY'
cipher += 'UHRHJGSOCUZZXAGFVLILQVAFDARKPQ'
cipher += 'LZCQAGULJBUCZAMPL'

# load dictionary
with open("words_dictionary.json", "r") as file:
    wordlist = json.load(file)
wordlist = list(wordlist.keys())
wordset = set(wordlist)

# Kasiski examination
dist_dict = repeat_distance(cipher, 3)
dists = np.array(list(dist_dict.keys()))
key_len = np.gcd.reduce(dists)
print("Possible key length:", key_len)

# Separate ciphers in groups based on key length
cipher_groups = {}
for i in range(key_len):
    cipher_groups[i] = cipher[i::key_len]

freq_dict = {}
for i, grp in cipher_groups.items():
    freq_dict[i] = patfreq(grp, '.')
    print(freq_dict[i])

# Get top frequent letters from each group and try to get the key
tops = [list(freq)[:6] for freq in freq_dict.values()]

top_key = ""
top_triplet = ""
top_plain = ""
top_word_count = 0
with open('out_ps2.txt', 'w') as f:
    for triplet in itertools.product(*tops):
        key = get_vigenere_key(''.join(triplet), 'eee')
        if key.lower() in wordset:
            print(key, '*')
        else:
            print(key)
        
        plain = word_segment(vigenere_decrypt(cipher, key), join=True)
        word_count = count_valid_chars(plain, wordlist)
        f.write(f"{key}: {plain}\n")

        if word_count >= top_word_count:
            top_word_count = word_count
            top_plain = plain
            top_key = key
            top_triplet = triplet

print(top_plain)
print("valid char count:", top_word_count)
print("key:", top_key)
print("triplet:", top_triplet)