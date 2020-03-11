import numpy as np
import pandas as pd
from datetime import datetime as dt

# Имеется табличка с портфелем:
#     id, - уникальный id строки
#     load_date, - дата загрузки данных
#     agr_cred_id, - уникальный id договора не на срез, надеюсь он не меняется
#     inn, - ИНН клиента на срез
#     signed_dt, - дата подписания договора на срез
#     credit_srok, - срок ссуды в днях на срез
#     issued_sum, - сумма ссуды на срез
#     product_type, тип ссуды на срез
#     default, - флаг нахождение в дефолте на срез
#     report_dt - дата среза, конец месяца
#     rating, - рейтинг на дату среза
#

# pd_data = pd.DataFrame(
#     np.random.rand(10*1000),
#     columns = ['id', 'load_date', 'agr_cred_id', 'inn', 'signed_dt', 'credit_srok', 'issued_sum', 'product_type', 'default', 'report_dt'])

navbar_labels = {'label': 'ОМОРК ММБ - Риск метрики портфеля'}
default_types = {
    'Просрочка 90+ 12 мес.': 'v1',
    'Банкротство': 'v2',
    'Ликвидация': 'v3',
    'Заражение': 'v4',
}
loan_types = {
    'Разовые кредиты': 'v1',
    'Возобновляемая кредитная линия': 'v2',
    'Невозобновляемая кредитная линия': 'v3',
    'Гарантии': 'v4',
}

signed_dt_filtration = {
    'start_date': dt(2015, 1, 1),
    'end_date': dt(2018, 10, 1),
    'label': 'Интервал дат подписания договора:',
    'html_for': "Минимальная и максимальная дата подписания договора для фильтрации выборки"
}

defaults_types_dropdown = {
    'options': [
        {'label': 'Просрочка 90+ 12 мес.', 'value': default_types['Просрочка 90+ 12 мес.']},
        {'label': 'Банкротство', 'value': default_types['Банкротство']},
        {'label': 'Ликвидация', 'value': default_types['Ликвидация']},
        {'label': 'Заражение', 'value': default_types['Заражение']}, ],
    'values': [*default_types.values()],
    'label': 'Виды дефолтов:',
    'html_for': "Выберите типы дефолтов для фильтрации выборки"
}

loans_types_dropdown = {
    'options': [
        {'label': 'Разовые кредиты', 'value': loan_types['Разовые кредиты']},
        {'label': 'Возобновляемая кредитная линия', 'value': loan_types['Возобновляемая кредитная линия']},
        {'label': 'Невозобновляемая кредитная линия', 'value': loan_types['Невозобновляемая кредитная линия']},
        {'label': 'Гарантии', 'value': loan_types['Гарантии']},],
    'values': [*loan_types.values()],
    'label': 'Типы ссуд:',
    'html_for': "Выберите типы ссуд для фильтрации выборки"
}

dates = [
    dt(2013, 1, 1), dt(2013, 2, 1), dt(2013, 3, 1), dt(2013, 4, 1), dt(2013, 5, 1), dt(2013, 6, 1), dt(2013, 7, 1), dt(2013, 8, 1), dt(2013, 9, 1), dt(2013, 10, 1), dt(2013, 11, 1), dt(2013, 12, 1),
    dt(2014, 1, 1), dt(2013, 2, 1), dt(2013, 3, 1), dt(2013, 4, 1), dt(2013, 5, 1), dt(2013, 6, 1), dt(2013, 7, 1), dt(2013, 8, 1), dt(2013, 9, 1), dt(2013, 10, 1), dt(2013, 11, 1), dt(2013, 12, 1),
    dt(2015, 1, 1), dt(2013, 2, 1), dt(2013, 3, 1), dt(2013, 4, 1), dt(2013, 5, 1), dt(2013, 6, 1), dt(2013, 7, 1), dt(2013, 8, 1), dt(2013, 9, 1), dt(2013, 10, 1), dt(2013, 11, 1), dt(2013, 12, 1),
    dt(2016, 1, 1), dt(2013, 2, 1), dt(2013, 3, 1), dt(2013, 4, 1), dt(2013, 5, 1), dt(2013, 6, 1), dt(2013, 7, 1), dt(2013, 8, 1), dt(2013, 9, 1), dt(2013, 10, 1), dt(2013, 11, 1), dt(2013, 12, 1),
    dt(2017, 1, 1), dt(2013, 2, 1), dt(2013, 3, 1), dt(2013, 4, 1), dt(2013, 5, 1), dt(2013, 6, 1), dt(2013, 7, 1), dt(2013, 8, 1), dt(2013, 9, 1), dt(2013, 10, 1), dt(2013, 11, 1), dt(2013, 12, 1),
    dt(2018, 1, 1), dt(2013, 2, 1), dt(2013, 3, 1), dt(2013, 4, 1), dt(2013, 5, 1), dt(2013, 6, 1), dt(2013, 7, 1), dt(2013, 8, 1), dt(2013, 9, 1), dt(2013, 10, 1), dt(2013, 11, 1), dt(2013, 12, 1),
    dt(2019, 1, 1), dt(2013, 2, 1), dt(2013, 3, 1), dt(2013, 4, 1), dt(2013, 5, 1), dt(2013, 6, 1), dt(2013, 7, 1), dt(2013, 8, 1), dt(2013, 9, 1), dt(2013, 10, 1), dt(2013, 11, 1), dt(2013, 12, 1),
    dt(2020, 1, 1), dt(2013, 2, 1), dt(2013, 3, 1), dt(2013, 4, 1), dt(2013, 5, 1), dt(2013, 6, 1), dt(2013, 7, 1), dt(2013, 8, 1), dt(2013, 9, 1), dt(2013, 10, 1), dt(2013, 11, 1), dt(2013, 12, 1),
]

graph_count_data = pd.DataFrame(index=pd.MultiIndex.from_product([loan_types.values(), default_types.values(), dates], names=["Тип продукта", 'Тип дефолта', "Дата"])).reset_index().sort_values('Дата')
graph_count_data['Количество'] = [np.random.rand() for x in range(graph_count_data.shape[0])]
graph_count_data['Дефолт'] = [int(np.random.rand() * 100) % 2 for x in range(graph_count_data.shape[0])]
graph_count_data['Тип дефолта'] = graph_count_data[['Тип дефолта', 'Дефолт']].apply(lambda x: None if (x[1] == 0) else x[0], axis=1)
graph_count_data['Рейтинг'] = [int(np.random.normal()) for x in range(graph_count_data.shape[0])]

