from library.bn_pos_lemmatizer.base_file import BaseFile


class PosRule(BaseFile):
    def __init__(self, rules_file=None):
        super().__init__()

        lemma_rule_file = rules_file or self._get_default_file_path('lemma_rules.json')
        self.rules_map = self._read_data_from_json(lemma_rule_file)

        self.vowel_sings = ['ং', 'ঃ', 'া', 'ি', 'ী', 'ু', 'ূ', 'ৃ', 'ে', 'ৈ', 'ো', 'ৌ', '্', 'ৗ']

    def __remove_suffixes(self, word, suffix_type, modify_func=None):
        suffix_matched = False
        max_suffix_len, max_suffix = -1, ""

        rule_suffix = self.rules_map[suffix_type]

        for suffix in rule_suffix:
            if word.endswith(suffix):
                suffix_matched = True
                temp_word = word[: -len(suffix)]
                if temp_word and temp_word[-1] == "্":
                    continue

                elif len(suffix) > max_suffix_len:
                    max_suffix = suffix
                    max_suffix_len = len(suffix)

        if max_suffix_len > 0:
            if modify_func:
                max_suffix = modify_func(word, max_suffix)
            word = word[: -len(max_suffix)]

            suffix_value = rule_suffix.get(max_suffix, '')
            if word and word[-1] not in self.vowel_sings:
                word += suffix_value

        return word, suffix_matched

    def __modify_noun_case_suffix(self, word, max_suffix):
        if max_suffix == "ের" and word.endswith("দের"):
            max_suffix = "দের"

        if max_suffix == "র":
            if word.endswith("দের"):
                max_suffix = "দের"
            elif word.endswith("্র"):
                max_suffix = ""
            elif word.endswith("নগর"):
                max_suffix = ""
        return max_suffix

    def __modify_pronoun_case_suffix(self, word, max_suffix):
        if max_suffix == "ের" and word.endswith("দের"):
            max_suffix = "দের"

        return max_suffix

    def _modify_noun(self, word):
        word, _ = self.__remove_suffixes(word, "emphasis")
        word, _ = self.__remove_suffixes(word, "case", self.__modify_noun_case_suffix)

        word, determiner_matched = self.__remove_suffixes(word, "determiner")
        if determiner_matched:
            word, _ = self.__remove_suffixes(word, "case")

        word, plural_matched = self.__remove_suffixes(word, "plural")
        if plural_matched:
            word, _ = self.__remove_suffixes(word, "case")

        return word

    def _modify_pronoun(self, word):
        word, _ = self.__remove_suffixes(word, "emphasis")
        word, _ = self.__remove_suffixes(word, "case", self.__modify_pronoun_case_suffix)

        word, determiner_matched = self.__remove_suffixes(word, "determiner")
        if determiner_matched:
            word, _ = self.__remove_suffixes(word, "case")

        return word

    def _modify_adjective(self, word):
        word, _ = self.__remove_suffixes(word, "emphasis")
        word, _ = self.__remove_suffixes(word, "degree")

        return word

    def _modify_verb(self, word):
        # for emphasis in ["ই", "ও", "ঃ"]:
        #     if word.endswith(emphasis):
        #         word = word[:-1]
        word, _ = self.__remove_suffixes(word, "emphasis")
        word, _ = self.__remove_suffixes(word, "verb")
        return word

    def _modify_adverb(self, word):
        word, _ = self.__remove_suffixes(word, "emphasis")
        return word

    def _modify_postposition(self, word):
        word, _ = self.__remove_suffixes(word, "emphasis")
        return word

    def get_modify_func(self, pats_of_speech):
        speech_function = {
            "noun": self._modify_noun,
            "pronoun": self._modify_pronoun,
            "adjective": self._modify_adjective,
            "adverb": self._modify_adverb,
            "verb": self._modify_verb,
            "preposition": self._modify_postposition,
            "conjunction": self._modify_postposition,
            "other": self._modify_postposition,
        }
        return speech_function[pats_of_speech]
