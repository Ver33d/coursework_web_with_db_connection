"""В данном модуле содержится описание эндпоинтов для основного бизнесс-процесса"""

# сторонние пакеты
import os
from flask import Blueprint, request,render_template,current_app,session,redirect
from datetime import datetime

# модули проекта
from DB.sql_provider import SQL_Provider
from DB.database import work_with_db,entry_db
from .utils import add_to_basket,clear_basket, add_supplier, clear_suppliers
from access import group_permission_decorator


# ДЕКЛАРИРУЮ БЛЮПРИНТ
basket_app=Blueprint('basket', __name__, template_folder='templates')
# Получаем правильный путь к папке с запросами, принадлежащую данному каталогу
provider=SQL_Provider(os.path.join(os.path.dirname(__file__),'sql'))

@basket_app.route('/', methods=['GET', 'POST'])
@group_permission_decorator
def suppliers_list():
    # выдается список пользователей, для котрых требуется сделать заказ
    if request.method == 'GET':
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('sql_suppliers.sql'))
        return render_template('suppliers_list.html', items=items)
    else:
        # после выбора пользователей
        s_id = request.form['s_id']
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('sql_current_supplier.sql', s_id=s_id))
        # if not items:
        #     return 'Item not found'
        add_supplier(items)
        return redirect('/basket/basket_list')



@basket_app.route('/basket_list', methods=['GET','POST'])
def list_orders_handler():
    db_config=current_app.config['DB_CONFIG']
    # выдан ли список товаров
    if request.method == 'GET':
        # достаем товары
        basket = session.get('basket', [])
        # генерируем sql. Формируется изображение товаров в системе
        sql = provider.get('order_list.sql')
        items = work_with_db(db_config, sql)
        print(items)
        return render_template('basket_order_list.html', basket=basket, items=items)
    else:
        #Обновление корзины
        item_id=request.form['item_id']
        print(item_id)
        # sql при помощи которого мы кладем товар в корзину
        sql=provider.get('order_item.sql', item_id=item_id)
        print(sql)
        items=work_with_db(db_config, sql)

        if not items:
            return render_template('no_item.html')
        else:
            add_to_basket(items)
        return redirect('/basket/basket_list')

@basket_app.route('/clear-basket')
def clear_basket_handler():
    #очистка корзины
    clear_basket()
    return redirect('/basket/basket_list')

@basket_app.route('/buy')
def buy_basket_handler():
    #формирование итоговой таблицы, которую сделали для заказа
    db_config = current_app.config['DB_CONFIG']
    current_basket = session.get('basket', [])
    print('curr', current_basket)
    data=datetime.today().strftime('%Y-%m-%d')

    suppliers = session.get('suppliers', [])
    print(suppliers)
    sup_id = suppliers[0]['idexternal_users']

    # берем id заказа
    sql_ido = provider.get('select_basket_id.sql')
    value_id = work_with_db(current_app.config['DB_CONFIG'], sql_ido)
    # записываем айди если на 1 больше, если нет, то 1
    id_order = value_id[0]['id_order'] + 1 if value_id else 1
    # Заполняем корзину
    for item in current_basket:
        sql_add = provider.get('insert_order_desc_table.sql', id_order=id_order, id_tovar=item['item_id'], price=item['price_unit'])
        insert_val_desc = entry_db(db_config, sql_add)


    sql_add = provider.get('sql_insert_order.sql', date=data, s_id=sup_id, basket_id=id_order ) #
    entry_db(current_app.config['DB_CONFIG'], sql_add)
    print(sql_add)

    sql_add_lines = provider.get('sql_insert_for_lines.sql', price=item['price_unit'], date=data, order_id=id_order)
    entry_db(current_app.config['DB_CONFIG'], sql_add_lines)
    print(sql_add_lines)
    #clear_basket()

    sql_sel = provider.get('sql_current_order.sql', id_order=id_order)
    items_sel = work_with_db(current_app.config['DB_CONFIG'], sql_sel)

    clear_basket()
    clear_suppliers()
    name = ['Название товара' , 'Материал' , 'Стоимость']
    return render_template('order_done.html', items=items_sel, name=name)
