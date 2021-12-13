import os

from string import Template

class SQL_Provider:
    """
    Класс для получения sql-запроса в зависимости от параметрического пути
    """
    def __init__(self, file_path):
        """
        Инициализируйте дикт сценариев, ключ - имя файла, значение - содержимое sql-файла
        :параметр путь к файлу: str. Содержит путь к файлу sql-файла
        """
        self._scripts = {}

        for file in os.listdir(file_path):
            if file.endswith('.sql'):
                self._scripts[file] = Template(open(f'{file_path}/{file}','r').read())

    def get(self, file_name, **kwargs):
        return self._scripts[file_name].substitute(**kwargs)