import unicodedata
import yaml
import json

from library.bn_pos_lemmatizer.utils.os_path import OSPathUtils
from library.bn_tokenizer import BanglaTokenizer, TextCleaner
from library.bn_pos_tagger import BanglaPosTagger


class BaseFile:
    def __init__(self):
        self.UNICODE_NORM_FORM = "NFKC"
        self.default_folder_path = 'default'
        self.current_folder_path = OSPathUtils.get_current_folder_path()

        self.pos_tagger = BanglaPosTagger()
        self.tokenizer = BanglaTokenizer()
        self.text_cleaner = TextCleaner(unicode_norm_form=self.UNICODE_NORM_FORM)

    def normalize_word(self, word):
        return unicodedata.normalize(self.UNICODE_NORM_FORM, word)

    def _get_default_file_path(self, file_path):
        return OSPathUtils.join_path(self.current_folder_path, self.default_folder_path, file_path)

    def _read_data_from_file(self, file_path):
        lines = []
        with open(file_path, 'r', encoding="utf-8") as file:
            lines = [data for line in file for data in line.split()]
        file.close()
        return lines

    def save_file_by_data__path(self, input_data, file_path):
        try:
            with open(file_path, 'w', encoding="utf-8") as json_file:
                json.dump(input_data, json_file, ensure_ascii=False)
        except IOError:
            print(f"Error while saving to file: {file_path}")

    def _read_data_from_yaml(self, file_path):
        lines = []
        with open(file_path, 'r', encoding='utf-8') as yaml_file:
            lines = yaml.safe_load(yaml_file)
        yaml_file.close()
        return lines

    def save_yaml_by_data__path(self, input_data, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as yaml_file:
                yaml.dump(input_data, yaml_file, default_flow_style=False)
        except IOError:
            print(f"Error while saving to YAML file: {file_path}")

    def _read_data_from_json(self, file_path):
        with open(file_path, 'r', encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        json_file.close()

        return json_data

    def save_json_by_data__path(self, input_data, file_path):
        try:
            with open(file_path, 'w', encoding="utf-8") as json_file:
                json.dump(input_data, json_file, ensure_ascii=False)
        except IOError:
            print(f"Error while saving to JSON file: {file_path}")
