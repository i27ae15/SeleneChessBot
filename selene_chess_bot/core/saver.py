import os
import uuid
import json


class FileSaver:

    @staticmethod
    def json_saver(
        data_to_save: dict,
        folder: str = None,
        file_name: str = None,
    ) -> str:

        if not folder:
            folder = 'errors'

        if not os.path.exists(folder):
            os.makedirs(folder)

        if not file_name:
            file_name = f'error_{str(uuid.uuid4()).split('-')[0]}'

        file_name = os.path.join(folder, f'{file_name}.json')

        with open(file_name, 'w') as file:
            json.dump(data_to_save, file, indent=4)
            file.write(data_to_save)

        return file_name
