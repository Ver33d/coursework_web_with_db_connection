from pymysql import connect
from pymysql.err import OperationalError
from pymysql.err import InterfaceError,IntegrityError


class UserDatabase:
    """
        Класс для выполнения sql-запросов и получения данных из базы данных
    """
    def __init__(self, config: dict):
        """
        Создает все необходимые атрибуты для объекта конфигурации
        :конфигурация параметров: дикт. Содержит данные для подключения к базе данных
        """
        # создание объекта класса
        self.config = config

    def __enter__(self):
        """
        Выполнить подключение к базе данных, отловить ошибки
        :возвращение:
        """
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Неверный логин и пароль, повторите подключение')
                return None
            if err.args[0] == 2003:
                print('Неверно введен порт или хост для подключения к серверу')
                return None
            if err.args[0] == 1049:
                print('Такой базы данных не существует')
                return None
        except UnicodeEncodeError as err:
            print('Были введены символы на русском языке')
            return None
        except InterfaceError as err:
            print(err)
            return err

    def __exit__(self, exc_type, exc_value, exc_trace):
        """
        Перехватывать синтаксические ошибки sql
        : параметр exc_type: тип ошибки
        :параметр exc_val: значение ошибки
        :параметр exc_tb:
        :возвращение:
        """
        if exc_value:
            if exc_value == 'Курсор не был создан':
                print('Курсор не создан')
            elif exc_value.args[0] == 1064:
                print('Синтаксическая ошибка в запросе!')
            elif exc_value.args[0] == 1146:
                print('Ошибка в запросе! Такой таблицы не существует.')
            elif exc_value.args[0] == 1054:
                print('Ошибка в запросе! Такого поля не существует.')
            return False
        else:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            return True


def work_with_db(dbconfig, _SQL):
    """
    Выполняет sql-запрос и возвращает результат из базы данных
    :конфигурация параметров: дикт. Содержит данные для подключения к базе данных
    :параметр sql: str. Содержит sql-запрос в виде строки
    :возврат: список. Возвращает список диктовок в результате
    """
    result = []
    with UserDatabase(dbconfig) as cursor:
        cursor.execute(_SQL)
        schema = [column[0] for column in cursor.description]
        for item in cursor.fetchall():
            result.append(dict(zip(schema, item)))
    return result

def entry_db(dbconfig, _SQL):
    """
    Выполняет все sql-запросы, такие как вставка, удаление
    :конфигурация параметров: дикт. Содержит данные для подключения к базе данных
    :параметр sql: str. Содержит sql-запрос в виде строки
    """
    try:
        with UserDatabase(dbconfig) as cursor:
            cursor.execute(_SQL)
        return True

    except IntegrityError:
        return False



