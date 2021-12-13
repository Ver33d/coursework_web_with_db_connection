"""Данный модуль содержит вспомогательные функции для реализации бизнесс-процесса"""

from flask import session

def add_to_basket(items:dict)->None:
    # basket=session.get('basket',[])
    # basket.append(item)
    # session['basket'] = basket
    """
    Создает корзину ключей в текущем сеансе

    :параметры предметов:
    пункты: list of dicts

    """
    basket = session.get('basket', [])
    # count = 1
    # for item in items:
    #     item.update(dict(count=count))
    # for item in items:
    #     key = True
    #     for i in basket:
    #         if item['p_id'] == i['p_id']:
    #             i['count'] += 1
    #             key = False
    #     if key:
    for item in items:
        basket.append(item)
    session['basket'] = basket


def clear_basket()->None:
    """
    Удаляет последний dict корзины в текущем сеансе
    """
    if 'basket' in session:
        session.pop('basket')


def add_supplier(items):
    """
    Создаем список покупателей, которым
    требуется сделать заказ
    """
    suppliers = session.get('suppliers', [])
    print(session)
    for item in items:
        suppliers.append(item)

    session['suppliers'] = suppliers


def clear_suppliers():
    """
       Очищаем список покупателей
    """
    if 'suppliers' in session:
        session.pop('suppliers')