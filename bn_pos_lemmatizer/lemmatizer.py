from library.bn_pos_lemmatizer.base_file import BaseFile
from library.bn_pos_lemmatizer.word_lemma import WordLemma
from library.bn_pos_lemmatizer.utils.algorithms import calculate_minimum_distance

from library.bn_pos_lemmatizer.pos_rule import PosRule


class PosLemmatizer(BaseFile):
    def __init__(self, words_file=None, lookup_file=None, rules_file=None, stop_words=[]):
        super().__init__()

        default_lookup_file = lookup_file or self._get_default_file_path('lemma_lookup.json')
        self.lookup_map = self._read_data_from_json(default_lookup_file)

        stop_words_file = rules_file or self._get_default_file_path('stopwords.json')
        self.stop_words = stop_words or self._read_data_from_json(stop_words_file)
        # self.stop_words = stop_words

        self.lemma = WordLemma(words_file)
        self.pos_rule = PosRule(rules_file)

    def _replace_lookup(self, word):
        if word in self.lookup_map.keys():
            return self.lookup_map[word]
        return ""

    def _get_most_possible_word(self, word):
        longest_sub = self.lemma.longest_substring_search(word)
        root_word = self.lemma.search_dictionary(word)

        # some unicode differs
        nm_sub_w = self.normalize_word(longest_sub)
        nm_root_w = self.normalize_word(root_word)

        if longest_sub == root_word or nm_sub_w == nm_root_w:
            return longest_sub

        else:
            distance2 = calculate_minimum_distance(longest_sub, word)
            distance3 = calculate_minimum_distance(root_word, word)

            # difference between the longest sub to close distance word
            minimum_distance = min(distance2, distance3)
            if distance2 == minimum_distance:
                result_word = longest_sub
            else:
                result_word = root_word

            # we don't accept above 50% change of a world, using minimum distance
            calculated_percentage = (minimum_distance / len(word)) * 100
            if calculated_percentage > 50:
                return ""

            return result_word

    def lemmatize(self, text):
        cleaned_text = self.text_cleaner(text)
        words = self.tokenizer.tokenize(cleaned_text)
        tagged_word = self.pos_tagger.tagger(words)

        result_words = []
        for word, p_tag in tagged_word:
            parts_of_speech = self.pos_tagger.get_parts_of_speech_from_tag(p_tag)

            if word in self.stop_words:
                continue
            remove_inflection_func = self.pos_rule.get_modify_func(parts_of_speech)

            if parts_of_speech == "verb":
                possible_word = self._replace_lookup(word)
                if possible_word:
                    result_words.append(possible_word)
                    continue
            else:
                possible_word = self._get_most_possible_word(word)
                if possible_word:
                    result_words.append(possible_word)
                    continue

            possible_word = remove_inflection_func(word)
            result_words.append(possible_word)

        return " ".join(result_words)

        # return result_words

    def descriptive_lemmatize(self, text):
        cleaned_text = self.text_cleaner(text)
        words = self.tokenizer.tokenize(cleaned_text)
        tagged_word = self.pos_tagger.tagger(words)

        results = []
        for word, p_tag in tagged_word:
            parts_of_speech = self.pos_tagger.get_parts_of_speech_from_tag(p_tag)

            result = {
                "word": word,
                "pos": parts_of_speech,
                "is_stop": False,
                "is_rule": False,
                "lemma": ""
            }

            if word in self.stop_words:
                continue
            remove_inflection_func = self.pos_rule.get_modify_func(parts_of_speech)

            if parts_of_speech == "verb":
                possible_word = self._replace_lookup(word)
                if possible_word:
                    result["lemma"] = possible_word
                    results.append(result)
                    continue
            else:
                possible_word = self._get_most_possible_word(word)
                if possible_word:
                    result["lemma"] = possible_word
                    results.append(result)
                    continue

            possible_word = remove_inflection_func(word)
            result["lemma"] = possible_word
            result["is_rule"] = True

            results.append(result)

        return results


# document = """সরকারি চিকিৎসকদের অনীহার ফলে গ্রামের মানুষ অবিচারের শিকার হচ্ছে বলে মন্তব্য করেছেন পরিকল্পনামন্ত্রী এমএ মান্নান। চিকিৎসকদের গ্রামে গিয়ে সেবা দিতে অনীহার বিষয় উল্লেখ করে মন্ত্রী হতাশা প্রকাশ করেছেন
# """
# document1 = """
# আগামী ২৪ সেপ্টেম্বর দুপুর ২টায় ঢাকা শিক্ষা বোর্ডের সভাকক্ষে আলোচিত ওই বৈঠক অনুষ্ঠিত হবে।আন্তঃশিক্ষা বোর্ড সমন্বয় সাব-কমিটির সভাপতি অধ্যাপক মু. জিয়াউল হকের সভাপতিত্বে এ বৈঠক অনুষ্ঠিত হবে।কুমিল্লা শিক্ষা বোর্ডের চেয়ারম্যান মো. আবদুস ছালাম শুক্রবার সাংবাদিকদের এসব তথ্য জানান।তিনি বলেন, জেএসসি-জেডিসি পরীক্ষা না নেওয়ার সিদ্ধান্ত হওয়ায় কীভাবে অষ্টমের শিক্ষার্থীদের মূল্যায়ন করা হবে সে বিষয়েও একটি ইউনিক সিদ্ধান্ত হওয়ার কথা রয়েছে। আর এইচএসসি ও সমমানের পরীক্ষার বিষয়টি বৈঠকের আলোচসূচিতে রয়েছে।উল্লেখ্য, করোনার কারণে ইতোমধ্যে বাতিল করা হয়েছে এ বছরের প্রাথমিক শিক্ষা সমাপনী (পিইসি) ও জুনিয়র স্কুল সার্টিফিকেট (জেএসসি) পরীক্ষা। শিক্ষাপ্রতিষ্ঠান খুলে দিতে না পারলে বার্ষিক পরীক্ষা না নিয়ে পরবর্তী শ্রেণিতে শিক্ষার্থীদের উন্নীত করার চিন্তাভাবনাও চলছে। কিন্তু এ বছরের এইচএসসি পরীক্ষা গত এপ্রিলে নির্ধারিত থাকলেও তা নেয়া যায়নি।আর এই পরীক্ষা নেয়ার বাধ্যবাধকতা থাকায় তা বাতিলও করা হয়নি। ইতোমধ্যে এই পরীক্ষার প্রায় ১৪ লাখ শিক্ষার্থীর জীবন থেকে ঝরে গেছে সাড়ে ৫ মাস। যথাসময়ে পরীক্ষা হলে তারা এখন বিশ্ববিদ্যালয়ে লেখাপড়া করত। ঢাকা শিক্ষা বোর্ডের চেয়ারম্যান অধ্যাপক মু. জিয়াউল হক এ ব্যাপারে বলেন, এবারের এইচএসসি পরীক্ষা গ্রহণের সার্বিক প্রস্তুতি আমরা নিয়ে রেখেছি। সরকারি সিদ্ধান্ত পেলে রুটিন ঘোষণা করা হবে।
# """
# #

# document = "বলতে বলতে মুখস্থ হয়ে গিয়েছিল ওর।"
# pos_lemmatizer = PosLemmatizer()
# result = pos_lemmatizer.lemmatize(document)
# # print("result", result)
