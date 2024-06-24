import unicodedata
from typing import List


class BanglaTokenizer:
    DUMMYTOKEN = 'XTEMPDOT'
    """Runs basic tokenization (punctuation splitting, lower casing, etc.)."""

    def __call__(self, text: str) -> List[str]:
        return self.tokenize(text)

    def tokenize(self, text: str) -> List[str]:
        """Tokenizes a piece of text."""
        text = self._convert_to_unicode(text)
        # handle (.) in bangla text
        text = text.replace('.', self.DUMMYTOKEN)
        orig_tokens = self._whitespace_tokenize(text)
        split_tokens = []
        for token in orig_tokens:
            split_tokens.extend(self._run_split_on_punc(token))

        output_tokens = self._whitespace_tokenize(" ".join(split_tokens))
        # get (.) back in output tokens
        output_tokens = [token.replace(self.DUMMYTOKEN, '.') for token in output_tokens]
        return output_tokens

    def _run_split_on_punc(self, text):
        """Splits punctuation on a piece of text."""
        chars = list(text)
        idx = 0
        start_new_word = True
        output = []
        while idx < len(chars):
            char = chars[idx]
            if self._is_punctuation(char):
                output.append([char])
                start_new_word = True
            else:
                if start_new_word:
                    output.append([])
                start_new_word = False
                output[-1].append(char)
            idx += 1

        return ["".join(x) for x in output]

    def _convert_to_unicode(self, text):
        """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return text.decode("utf-8", "ignore")
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))

    def _whitespace_tokenize(self, text):
        """Runs basic whitespace cleaning and splitting on a piece of text."""
        text = text.strip()
        if not text:
            return []
        tokens = text.split()
        return tokens

    def _is_punctuation(self, char):
        """Checks whether `chars` is a punctuation character."""
        cp = ord(char)
        # We treat all non-letter/number ASCII as punctuation.
        # Characters such as "^", "$", and "`" are not in the Unicode
        # Punctuation class but we treat them as punctuation anyways, for
        # consistency.

        if (33 <= cp <= 47) or (58 <= cp <= 64) or (91 <= cp <= 96) or (123 <= cp <= 126):
            return True

        cat = unicodedata.category(char)
        if cat.startswith("P"):
            return True
        return False
