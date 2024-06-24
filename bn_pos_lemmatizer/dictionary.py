class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Dictionary:
    def __init__(self):
        self.root = TrieNode()

    def _insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def _get_word_with_prefix(self, node, prefix):
        if node.is_end_of_word:
            return prefix
        for char, child_node in node.children.items():
            return self._get_word_with_prefix(child_node, prefix + char)
        return ""

    def _word_with_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return ""
            node = node.children[char]
        return self._get_word_with_prefix(node, prefix)

    def add(self, word):
        self._insert(word)

    def search(self, word):
        prefix_match = self._word_with_prefix(word)
        return prefix_match
