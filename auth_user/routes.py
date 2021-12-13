"""В данном модуле описаны эндпоинты, описывающие вариант использования авторизация"""

# сторонние пакеты
from flask import Blueprint, session, render_template, request, current_app

# модули проекта
from DB.database import work_with_db
from DB.sql_provider import SQL_Provider
from access import group_permission_decorator, is_group_permission_valid


login_app = Blueprint('login_app', __name__, template_folder='templates')
provider = SQL_Provider('scenario_user/sql')

@login_app.route('/login', methods=['GET', 'POST'])
def login_page():
    # функция авторизации
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        sql = provider.get('sql_access.sql', gener1=login, gener2=password)
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        print(result)

        if result:
            if login == result[0]['login'] and password == result[0]['password']:
                session['group_name'] = result[0]['role']
                return render_template('main.html')
        return render_template('unlogged.html')

