import json
from datetime import datetime, timedelta

import pandas as pd

from src.utils import common_information, get_excel_df, get_exchange_rate, get_stock_price, greetings, top_5_operations


def get_monthly_transactions_info(str_time: str) -> str:
    """
    Принимает дату в формате строки YYYY-MM-DD HH:MM:SS и возвращает общую информацию в формате
    json о банковских транзакциях за период с начала месяца до этой даты
    """
    try:
        data = get_excel_df("operations.xlsx")
        data_df = pd.DataFrame(data)
        date_obj = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        data_df["datetime"] = pd.to_datetime(data_df["Дата операции"], dayfirst=True)

        json_data = data_df[
            (data_df["datetime"] >= (date_obj - timedelta(days=date_obj.day - 1))) & (data_df["datetime"] <= date_obj)
        ]

        agg_dict = {
            "Приветствие": greetings(),
            "Карта": common_information(json_data),
            "Топ 5 транзакций": top_5_operations(json_data),
            "Цена акций": get_stock_price("user_settings.json"),
            "Цена валют": get_exchange_rate("user_settings.json"),
        }
        return json.dumps(agg_dict, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Неудачное формирование отчета. Ошибка - {e}")
        return ""
