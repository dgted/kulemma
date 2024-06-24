import pickle
from sklearn_crfsuite import CRF

from typing import List, Tuple

from library.bn_pos_tagger.utils.os_path import OSPathUtils


class BanglaPosTagger:
    def __init__(self, model_path: str = ""):
        self.current_folder_path = OSPathUtils.get_current_folder_path()

        if not model_path:
            model_path = OSPathUtils.join_path(self.current_folder_path, "default/bn_pos.pkl")
        self.model = self.load_pickle_model(model_path)

    def load_pickle_model(self, model_path: str) -> CRF:
        with open(model_path, "rb") as pkl_model:
            model = pickle.load(pkl_model)

        return model

    def tagger(self, tokens: List) -> List[Tuple[str, str]]:
        # remove punctuation from tokens
        sentence_features = [self.sentence_property(tokens, index) for index in range(len(tokens))]
        result = list(zip(tokens, self.model.predict([sentence_features])[0]))

        return result

    def get_parts_of_speech_from_tag(self, p_tag):
        noun_tags = ["NP", "NC", "NV"]
        adjective_tags = ["DAB", "JJ", "JQ"]
        pronoun_tags = ["PPR"]
        verb_tags = ["VM", "VAUX"]
        adverb_tags = ["AL", "ALC", "AMN"]

        conjunction_tags = ["LC", "CCD"]
        preposition_tags = ["PP"]

        if p_tag in noun_tags:
            return 'noun'
        elif p_tag in pronoun_tags:
            return 'pronoun'
        elif p_tag in adjective_tags:
            return 'adjective'
        elif p_tag in verb_tags:
            return 'verb'
        elif p_tag in adverb_tags:
            return 'adverb'
        elif p_tag in conjunction_tags:
            return 'conjunction'
        elif p_tag in preposition_tags:
            return 'preposition'
        else:
            return 'other'

    def sentence_property(self, sentence, index):
        """sentence: [w1, w2, ...], index: the index of the word"""
        return {
            "word": sentence[index],
            "is_first": index == 0,
            "is_last": index == len(sentence) - 1,
            "is_capitalized": sentence[index][0].upper() == sentence[index][0],
            "is_all_caps": sentence[index].upper() == sentence[index],
            "is_all_lower": sentence[index].lower() == sentence[index],
            "prefix-1": sentence[index][0],
            "prefix-2": sentence[index][:2],
            "prefix-3": sentence[index][:3],
            "suffix-1": sentence[index][-1],
            "suffix-2": sentence[index][-2:],
            "suffix-3": sentence[index][-3:],
            "prev_word": "" if index == 0 else sentence[index - 1],
            "next_word": "" if index == len(sentence) - 1 else sentence[index + 1],
            "has_hyphen": "-" in sentence[index],
            "is_numeric": sentence[index].isdigit(),
            "capitals_inside": sentence[index][1:].lower() != sentence[index][1:],
        }

#
# bn_pos = BanglaPosTagger()
# tokens = ['হাসান', 'ভাত', 'খাই']
# res = bn_pos.tagger(tokens)


# pos_mapping = {
#     "NP": "Noun Proper",
#     "NC": "Noun Common",
#     "NV": "Verb Main",
#     "JJ": "Adjective",
#     "DAB": "Demonstrative Adjective",
#     "CCD": "Coordinating Conjunction",
#     "PU": "Punctuation",
#     "VM": "Verb Main",
#     "VAUX": "Verb Auxiliary",
#     "PPR": "Personal Pronoun",
#     "AMN": "Adverb of Manner",
#     "JQ": "Question Word",
#     "PP": "Preposition",
#     "LC": "Subordinating Conjunction",
#     "ALC": "Adverb of Location",
#     "AL": "Adverb",
#     "RDF": "Numeral"
# }
