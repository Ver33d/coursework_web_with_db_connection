"""Главный модуль приложения"""

# стандартные модули
import json

# подгружаемые модули
from flask import Flask, render_template, session

# модули проекта
from DB.sql_provider import SQL_Provider
from auth_user.routes import login_app
from scenario_user.routes import user_app
from scenario_basket.routes import basket_app


app = Flask(__name__)
# регистрирую блюпринты
app.register_blueprint(user_app, url_prefix='/user')
app.register_blueprint(login_app, url_prefix='/auth')
app.register_blueprint(basket_app, url_prefix='/basket')

app.config['DB_CONFIG'] = json.load(open('configs/db.json', 'r'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json', 'r'))
app.config['SECRET_KEY'] = 'my_secret_key'


@app.route('/')

def index():
# Обработик главного меню
    return render_template('main.html')


@app.route('/clear-session')

def clear_session():
# очщение сесии
    session.clear()
    return render_template('end.html')

if (__name__ == "__main__"):
    app.run(host="127.0.0.1", port=3001)
