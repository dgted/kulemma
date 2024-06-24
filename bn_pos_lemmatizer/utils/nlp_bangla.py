import re


class NlpBangla:
    @staticmethod
    def sanitize_bangla_word(bangla_word=''):
        bangla_word = NlpBangla.modify_bangla_word(bangla_word)
        bangla_word = bangla_word.strip()

        has_english_letters = NlpBangla.has_english_letters(bangla_word)
        has_english_digits = NlpBangla.has_english_digits(bangla_word)
        has_special = NlpBangla.has_special_string(bangla_word)

        if has_english_letters or has_english_digits or has_special:
            return ""

        return bangla_word

    @staticmethod
    def has_english_letters(input_string):
        pattern = r'[a-zA-Z]'
        match = re.search(pattern, input_string)

        return bool(match)

    @staticmethod
    def extract_english_digits(input_string):
        pattern = r'\d+'
        return re.findall(pattern, input_string)[0]

    @staticmethod
    def has_english_digits(input_string):
        pattern = r'[0-9]'
        match = re.search(pattern, input_string)

        return bool(match)

    @staticmethod
    def has_special_string(input_string):
        pattern = r"[!@#$%:`~^&*()><{}[\]/\"?+=_]"
        return bool(re.search(pattern, input_string))

    @staticmethod
    def modify_bangla_word(bangla_word=''):

        special_strings = ['.', ';', '"', '|', '।']
        bn_numerics = ["১", "২", "৩", "৪", "৫", "৬", '৭', '৮', '৯', '০']

        special_characters = bn_numerics + special_strings
        for special_ch in special_characters:
            bangla_word = bangla_word.replace(special_ch, "")

        bangla_word = bangla_word.replace("  ", " ")

        if bangla_word.startswith("-"):
            bangla_word = bangla_word.replace("-", "")

        if bangla_word.startswith("_"):
            bangla_word = bangla_word.replace("_", "")

        if bangla_word.endswith("-"):
            bangla_word = bangla_word.replace("-", "")

        return bangla_word


    @staticmethod
    def get_first_and_second_split_word(split_words):
        if len(split_words) > 1:
            return split_words[0], split_words[1]
        return split_words[0], ""

    @staticmethod
    def get_words_split_by_digits(input_string):
        multi_words = []
        digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for digit in digits:
            split_words = input_string.split(digit)
            word, input_string = NlpBangla.get_first_and_second_split_word(split_words)
            multi_words.append(word)

        return multi_words