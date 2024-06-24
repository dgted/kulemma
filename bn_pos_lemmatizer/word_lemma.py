from library.bn_pos_lemmatizer.base_file import BaseFile
from library.bn_pos_lemmatizer.dictionary import Dictionary
from library.bn_pos_lemmatizer.utils.algorithms import longest_substring_search


class WordLemma(BaseFile):
    def __init__(self, words_file=None):
        super().__init__()

        self.dictionary = Dictionary()

        default_words_file = words_file or self._get_default_file_path('root_words.json')
        self.root_words = self._read_data_from_json(default_words_file)

        name_entity_file = self._get_default_file_path('name_entity.json')
        self.names_entity = self._read_data_from_json(name_entity_file)

        place_entity_file = self._get_default_file_path('place_entity.json')
        self.place_entity = self._read_data_from_json(place_entity_file)

        self.words_map = {}  # for longest substring
        for word in self.root_words:
            nm_word = self.normalize_word(word)
            self.words_map[nm_word] = 1  # just for faster searching
            self.dictionary.add(nm_word)

        for word in self.names_entity:
            nm_word = self.normalize_word(word)
            self.dictionary.add(nm_word)

        for word in self.place_entity:
            nm_word = self.normalize_word(word)
            self.dictionary.add(nm_word)

    def search_dictionary(self, word):
        return self.dictionary.search(word)

    def longest_substring_search(self, word):
        return longest_substring_search(word, self.words_map)

# lemma = WordLemma()
