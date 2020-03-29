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
