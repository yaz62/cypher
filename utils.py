import re
from collections import Counter


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def pattern_frequency(ciphertext: str, pattern: str, sort=True, cutoff=1, overlapping=True):
    """
    Finds all occurrences of the given pattern in the ciphertext and returns their frequency.
    
    Args:
        ciphertext (str): The encrypted text.
        pattern (str): The pattern to match (can include regex patterns).
        sort (bool): If True, sorts results by frequency in descending order.
        cutoff (int): Minimum frequency threshold for inclusion in the results.
        overlapping (bool): If True, captures overlapping matches.

    Returns:
        dict: A dictionary of matched patterns and their frequencies.
    """
    if overlapping and "." in pattern:  
        # Generate all overlapping substrings of the required length
        matches = [ciphertext[i:i+len(pattern)] for i in range(len(ciphertext) - len(pattern) + 1)]
        matches = [m for m in matches if re.fullmatch(pattern, m)]  # Filter with regex pattern if needed
    else:
        matches = re.findall(pattern, ciphertext)  # Non-overlapping default regex search

    freq_dict = Counter(matches)

    # Apply cutoff threshold
    if cutoff > 1:
        freq_dict = {k: v for k, v in freq_dict.items() if v >= cutoff}

    # Sort results by frequency in descending order
    if sort:
        freq_dict = dict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))

    return freq_dict


def patfreq(ciphertext: str, pattern: str, **kwargs):
    '''
        Wrapper of pattern_frequency with a shorter function name.
    '''
    return pattern_frequency(ciphertext, pattern, **kwargs)


def search_word(words, pattern: str):
    """
    Filters words that match the given regex pattern.

    Args:
        words (list): List of words to search.
        pattern (str): Regex pattern to match.

    Returns:
        list: Words that match the pattern.
    """
    return [word for word in words if re.fullmatch(pattern, word)]


def replace_char(ciphertext: str, mapdict: dict, gapchar='.'):
    text = ""
    for c in ciphertext:
        if c in mapdict.keys():
            text += mapdict[c]
        else:
            text += gapchar
    return text


def replchar(ciphertext: str, mapdict: dict, **kwargs):
    '''
        Wrapper of replace_char with a shorter function name.
    '''
    return replace_char(ciphertext, mapdict, **kwargs)


def is_symmetric(map_dict: dict):
    for k, v in map_dict.items():
        if k != map_dict[v]:
            return False
    return True


def vigenere_decrypt(ciphertext: str, key: str, offset=1) -> str:
    plaintext = []
    key = key.upper()
    ciphertext = ciphertext.upper()
    
    key_repeated = (key * ((len(ciphertext) // len(key)) + 1))[:len(ciphertext)]  # Repeat key

    for c, k in zip(ciphertext, key_repeated):
        if c in ALPHABET:
            shift = ALPHABET.index(k) + offset  # Get the shift value from the key
            original_index = (ALPHABET.index(c) - shift) % len(ALPHABET)  # Reverse the shift
            plaintext.append(ALPHABET[original_index])
        else:
            plaintext.append(c)  # Keep non-alphabetic characters unchanged

    return "".join(plaintext)


def get_vigenere_key(cipher: str, plain: str, offset=1):
    cipher, plain = cipher.upper(), plain.upper()

    key = ""
    for c, p in zip(cipher, plain):
        shift = (ALPHABET.index(c) - ALPHABET.index(p)) % len(ALPHABET) - offset
        key += ALPHABET[shift]
    return key


def count_valid_chars(sentence: str, wordlist, gapchar=' '):
    wordlist_ = set(wordlist)

    n = 0
    for w in sentence.split(gapchar):
        if w in wordlist_:
            n += len(w)
    return n


def repeat_distance(cipher: str, n: int):
    pattern = ''.join(['.'] * n)
    repeat_dict = pattern_frequency(cipher, pattern=pattern, sort=False, cutoff=2)

    dist = []
    for repeat in repeat_dict.keys():
        for i in range(len(cipher)):
            if cipher[i:i+n] == repeat:
                # Start counting distance
                for j in range(i+1, len(cipher)):
                    if cipher[j:j+n] == repeat:
                        dist.append(j - i)
    return Counter(dist)


def word_segment_dp(sentence, word_list):
    """
    Segments a sentence without spaces to maximize the number of valid characters in known words.
    Returns all possible segmentations that achieve the maximum valid character count.

    Args:
        sentence (str): The input string without spaces.
        word_list (set): A set of valid words.

    Returns:
        tuple: (max_valid_chars, set of all segmentations achieving that score)
    """
    n = len(sentence)
    word_list = set(word_list)  # Convert list to set for fast lookups

    # DP Table: dp[i] = (max_chars, set of segmentations)
    dp = [(-float('inf'), set()) for _ in range(n + 1)]
    dp[0] = (0, {""})  # Base case: empty string has 0 valid characters

    for i in range(1, n + 1):
        max_chars = -float('inf')
        best_segmentations = set()

        for j in range(i):  # Try splitting at every previous index j
            word = sentence[j:i]
            prev_chars, prev_segmentations = dp[j]

            if word in word_list:
                new_chars = prev_chars + len(word)  # Add word length
            else:
                new_chars = prev_chars  # No valid word found, keep previous count

            if new_chars > max_chars:
                max_chars = new_chars
                best_segmentations = {seg + (" " if seg else "") + word for seg in prev_segmentations}
            elif new_chars == max_chars:
                best_segmentations.update({seg + (" " if seg else "") + word for seg in prev_segmentations})

        dp[i] = (max_chars, best_segmentations)

    # Extract best solutions
    max_valid_chars, best_solutions = dp[n]
    return max_valid_chars, best_solutions