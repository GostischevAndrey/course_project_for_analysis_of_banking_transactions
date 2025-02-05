import json

import pandas as pd

from src.reports import spending_by_weekday
from src.services import invest_bank, most_profit_cashback
from src.utils import common_information, get_excel_df, get_exchange_rate, get_stock_price, greetings, top_5_operations
from src.views import get_monthly_transactions_info

data = get_excel_df(
    "operations.xlsx",
)
data_json = json.dumps(data, indent=4, ensure_ascii=False)
data_df = pd.DataFrame(data)
data_df["datetime"] = pd.to_datetime(data_df["Дата операции"], dayfirst=True)

print(data_json)
print(top_5_operations(data))
print(common_information(data))
print(greetings())
print(get_stock_price("user_settings.json"))
print(get_exchange_rate("user_settings.json"))
print(most_profit_cashback(data, 2022, 7))
print(invest_bank(data, "2022-07", 50))
print(spending_by_weekday(data_df, "2022-02-01"))
print(get_monthly_transactions_info(str_time="2022-02-10 16:22:56"))
