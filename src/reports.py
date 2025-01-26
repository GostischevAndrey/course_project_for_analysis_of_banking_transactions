from datetime import datetime
from typing import Optional, Union

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.config import setup_logger

spending_by_weekday_logger = setup_logger("spending_by_weekday", "../logs/reports.log")


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> Union[str, list]:
    """Возвращает средние траты в каждом из дней недели за последние три месяца от переданной даты"""
    try:
        if date is None:
            date_value = datetime.now()
        else:
            date_value = datetime.strptime(date, "%Y-%m-%d")

        transactions["datetime"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        transactions["day_name"] = transactions["datetime"].dt.day_name()

        df = transactions[
            (transactions["datetime"] >= (date_value + relativedelta(months=-3)))
            & (transactions["datetime"] <= date_value)
        ].groupby(by="day_name")

        print(df.head(10))
        spending_by_weekday_logger.info("Успешное формирование отчета о средних тратах.")
        return (df["Сумма платежа"].mean().abs().round(2)).to_json()

    except Exception as e:
        spending_by_weekday_logger.warning(f"Неудачное формирование отчета. Ошибка - {e}")
        return []
