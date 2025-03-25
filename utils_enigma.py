from utils import ALPHABET


def get_inv_map(map_dict):
    inv_map = {v: k for k, v in map_dict.items()}
    return inv_map


def rotate_disc(disc_dict, n, alphabet=ALPHABET):
    rot_dict = {}

    for k, v in disc_dict.items():
        new_key = alphabet[(alphabet.index(k) + n) % len(alphabet)]
        new_val = alphabet[(alphabet.index(v) + n) % len(alphabet)]
        rot_dict[new_key] = new_val
    
    return rot_dict