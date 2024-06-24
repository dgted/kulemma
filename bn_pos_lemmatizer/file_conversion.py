from library.bn_pos_lemmatizer.base_file import BaseFile


class FILE_CONVERTER(BaseFile):
    def __init__(self):
        super().__init__()

        default_words_file = self._get_default_file_path('root_words.json')
        self.json_root_words = self._read_data_from_json(default_words_file)

    def convert_json_to_yaml(self):
        yaml_path = self._get_default_file_path('root_words1.yaml')
        json_data = self.json_root_words
        self.save_yaml_by_data__path(json_data, yaml_path)

    def convert_yaml_to_json(self):
        json_path = self._get_default_file_path('root_words1.json')
        yaml_data = self.json_root_words
        self.save_json_by_data__path(yaml_data, json_path)

    def compare_data(self):
        words_not_in = []
        for word in []:
            if word not in self.json_root_words:
                words_not_in.append(word)

        return words_not_in


yaml_to_json = FILE_CONVERTER()
yaml_to_json.convert_json_to_yaml()
