import os


class OSPathUtils:
    @staticmethod
    def join_path(*args):
        return os.path.join(*args)

    @staticmethod
    def get_current_folder_path():
        current_file_path = os.path.abspath(__file__)
        current_folder_path = os.path.dirname(current_file_path)

        return os.path.dirname(current_folder_path)

    @staticmethod
    def get_file_extension_by_path(file_path):
        _, file_extension = os.path.splitext(os.path.basename(file_path))
        return file_extension

    @staticmethod
    def get_file_name_by_path(file_path):
        file_name, _ = os.path.splitext(os.path.basename(file_path))
        return file_name
