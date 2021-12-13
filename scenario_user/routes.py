"""В данном модуле содержится описание эндпоинтов для варианта использования работа с запросами"""

# сторонние пакеты
from flask import Blueprint, render_template, current_app, request

# модули проекта
from DB.sql_provider import SQL_Provider
from DB.database import work_with_db
from access import group_permission_decorator


user_app = Blueprint('user_app', __name__, template_folder='templates')
provider = SQL_Provider('scenario_user/sql')


@user_app.route('/')
def user_index():
# меню запросов
    return render_template('menu.html')


@user_app.route('/sql1', methods=['GET', 'POST'])
@group_permission_decorator
def user_sql1():
    # Выполнение первого запроса
    if request.method == 'GET':
        return render_template('sql_1.html')
    else:
        value = request.form.get('value', None)
        if value is not None:
            sql = provider.get('sql1.sql', gener1=value)
            print(sql)
            result = work_with_db(current_app.config['DB_CONFIG'], sql)
            print(result)
            name = [" месяц ", " название товара ", " количество ", " стоимость " ]
            if not result:
                return render_template('error.html')
            return render_template('result_1.html', res=result, name=name)
        else:
            return 'Not found value'


@user_app.route('/sql2', methods=['GET', 'POST'])
@group_permission_decorator
def user_sql2():
    # Выполнение второго запроса
    if request.method == 'GET':
        return render_template('sql_2.html')
    else:
        value1 = request.form.get('value1', None)
        value2 = request.form.get('value2', None)
        name = ["дата ", "общая сумма оплаты"]
        if value1 is not None and value2 is not None:
            sql = provider.get('sql2.sql', gener1=value1, gener2=value2)
            result = work_with_db(current_app.config['DB_CONFIG'], sql)
            if not result:
                return render_template('error.html')
            return render_template('result_2.html', res=result, name=name)
        else:
            return 'Not found value'


@user_app.route('/sql3', methods=['GET', 'POST'])
@group_permission_decorator
def user_sql3():
    # Выполнение третьего запроса
    if request.method == 'GET':
        return render_template('sql_3.html')
    else:
        value1 = request.form.get('value1', None)
        value2 = request.form.get('value2', None)
        name = ["категория ", "материал", "товар ", "дата поставки ", "единица измерения ", "цена ", "количество товара "]
        if value1 is not None and value2 is not None:
            sql = provider.get('sql3.sql', gener1=value1, gener3=value2)
            result = work_with_db(current_app.config['DB_CONFIG'], sql)
            print(result)
            if not result:
                return render_template('error.html')
            print(name)
            return render_template('result_3.html', res=result, name=name)
        else:
            return 'Not found value'