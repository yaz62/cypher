from collections import deque
import numpy as np
import wordsegment as ws

_loaded = False

class TrieNode:
    """Trie node for storing words efficiently."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    """Trie data structure for fast prefix-based word lookup."""
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        """Returns True if the word exists in the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        """Returns True if any word in the Trie starts with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

def word_segment_dp(sentence, word_list):
    """
    Segments a sentence without spaces to maximize the number of valid characters in known words.
    Uses Trie for fast word lookups and BFS for efficient exploration.

    Args:
        sentence (str): The input string without spaces.
        word_list (list): A list of valid words.

    Returns:
        tuple: (max_valid_chars, list of all best segmentations)
    """
    # Step 1: Build the Trie
    trie = Trie()
    for word in word_list:
        trie.insert(word)

    n = len(sentence)
    queue = deque([(0, [], 0)])  # (current index, segmentation, valid_chars count)
    max_valid_chars = 0
    best_segmentations = []

    visited = np.full(n + 1, -1)  # Memoization table

    while queue:
        index, current_words, valid_chars = queue.popleft()

        # Prune paths that are worse than the best so far
        if visited[index] > valid_chars:
            continue
        visited[index] = valid_chars

        word = ""
        for end in range(index + 1, n + 1):
            word += sentence[end - 1]  # Extend substring dynamically

            if trie.search(word):  # Found a valid word
                new_valid_chars = valid_chars + len(word)
                new_segmentation = current_words + [word]

                if new_valid_chars > max_valid_chars:
                    max_valid_chars = new_valid_chars
                    best_segmentations = [new_segmentation]
                elif new_valid_chars == max_valid_chars:
                    best_segmentations.append(new_segmentation)

                queue.append((end, new_segmentation, new_valid_chars))

            elif not trie.starts_with(word):  # Stop early if no word starts with this prefix
                break

    return max_valid_chars, [" ".join(words) for words in best_segmentations]

def word_segment(sentence, join=False):
    global _loaded
    if not _loaded:
        ws.load()
        _loaded = not _loaded
    
    segmented_sentence = ws.segment(sentence)
    if join:
        return ' '.join(segmented_sentence)
    else:
        return segmented_sentence