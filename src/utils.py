import json
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

from src.config import setup_logger

get_excel_df_logger = setup_logger("get_excel_df", "../logs/utils.log")
top_5_operations_logger = setup_logger("top_5_operations", "../logs/utils.log")
common_information_logger = setup_logger("common_information", "../logs/utils.log")
get_exchange_rate_logger = setup_logger("get_exchange_rate", "../logs/utils.log")
get_stock_price_logger = setup_logger("get_stock_price", "../logs/utils.log")


def get_excel_df(filename: str) -> list[dict]:
    """
    Считывает данные из внешнего файла Excel и возвращает их в формате DataFrame
    за период с начала месяца до заданной даты в формате YYYY-MM-DD HH:MM:SS
    """
    try:
        path = os.path.join("../data/", filename)
        excel_data = pd.read_excel(path)
        list_dict = excel_data.to_dict(orient="records")
        get_excel_df_logger.info(f"Успешное преобразование файла {filename} из объекта JSON в PYTHON")
        return list_dict
    except Exception as e:
        get_exchange_rate_logger.warning(
            f"Не удалось преобразовать файл {filename} из объекта json в python. Ошибка - {e}"
        )
        return []


def top_5_operations(list_dict: list[dict]) -> list:
    """Возвращает 5 самых крупных операции по столбцу 'Сумма операции'"""
    try:
        list_data = []
        df = pd.DataFrame(list_dict)
        df["datetime"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        df_sorted = df.sort_values(by="Сумма платежа", ascending=False, inplace=False).iloc[0:5, :]
        for _, row in df_sorted.iterrows():
            dic = {}
            dic["Дата операции"] = row["Дата операции"]
            dic["Номер карты"] = row["Номер карты"]
            dic["Сумма операции"] = row["Сумма операции"]
            dic["Категория"] = row["Категория"]
            dic["Описание"] = row["Описание"]
            list_data.append(dic)
        top_5_operations_logger.info("Успешно сформированы 5 самых доходных операций")
        return list_data[:6]
    except Exception as e:
        get_exchange_rate_logger.warning(
            f"Не удалось сформировать отчет проверьте поля списка {list_dict}. Ошибка - {e}"
        )
        return []


def common_information(list_dict: list[dict]) -> list:
    """Возвращает общую информацию по всем транзакциям"""
    try:
        list_data = []
        df = pd.DataFrame(list_dict)
        df["datetime"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        grouped_data = df.groupby("Номер карты").agg({"Сумма платежа": "sum", "Кэшбэк": "sum"}).reset_index()
        grouped_data["Сумма платежа"] = grouped_data["Сумма платежа"].abs()
        for _, row in grouped_data.iterrows():
            dic = {}
            dic["Номер карты"] = (row["Номер карты"])[-4:]
            dic["Сумма платежа"] = row["Сумма платежа"]
            dic["Кэшбэк"] = round((row["Кэшбэк"]) / (row["Сумма платежа"]) * 100, 2)
            list_data.append(dic)
        common_information_logger.info("Успешно сформированa общая информация по всем транзакциям")
        return list_data
    except Exception as e:
        get_exchange_rate_logger.warning(
            f"Не удалось сформировать отчет проверьте поля списка {list_dict}. Ошибка - {e}"
        )
        return []


def greetings() -> str:
    """Возвращает приветствие пользователю в зависимости от текущего времени суток"""
    date_obj = datetime.now()
    if 6 <= date_obj.hour < 12:
        return "Доброе утро!"
    elif 12 <= date_obj.hour < 18:
        return "Доброго дня!"
    elif 18 <= date_obj.hour < 24:
        return "Доброго вечера!"
    else:
        return "Доброй ночи!"


def get_exchange_rate(json_file: str) -> List[Dict[str, Any]]:
    """Получает JSON-файл с кодировкой иностранных валют и возвращает значения текущих котировок этих валют"""
    try:
        total_list = []
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)

        if response.status_code == 200:
            data_curr = response.json()

            file_path = os.path.join("../data/", json_file)
            with open(file_path, "r") as file:
                user_shares = json.load(file)

                if "user_currencies" not in user_shares:
                    raise KeyError("Ключ 'user_currencies' отсутствует в файле")

                for currency in user_shares["user_currencies"]:
                    if currency in data_curr["Valute"]:
                        dic = {"Валюта": currency, "Обменный курс": data_curr["Valute"][currency]["Value"]}
                        total_list.append(dic)
                    else:
                        get_exchange_rate_logger.warning(f"Валюта {currency} отсутствует.")

            get_exchange_rate_logger.info(
                f'Успешно сформированы котировки {", ".join(user_shares["user_currencies"])} к рублю'
            )
            return total_list

        else:
            raise ConnectionError(f"Ошибка при соединении с API: {response.status_code}")

    except Exception as e:
        get_exchange_rate_logger.warning(f"Не удалось отобразить котировки. Ошибка - {e}")
        return []


def get_stock_price(json_file: str) -> list:
    """Получает JSON-файл с наименованиями ценных бумаг и возвращает их текущие котировки"""
    try:
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("API_KEY не найдена в переменных окружения.")

        url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()

        stock_list = {stock["symbol"]: stock["price"] for stock in response.json()}

        with open(os.path.join("../data/", json_file), "r") as file:
            user_shares = json.load(file)

        total_list = []
        for symbol in user_shares.get("user_stocks", []):
            if symbol in stock_list:
                total_list.append({"Тикер": symbol, "Цена": stock_list[symbol]})
            else:
                get_stock_price_logger.warning(f"Котировка для акции {symbol} не найдена.")

        get_stock_price_logger.info(
            f"Успешно сформированы котировки акций: {', '.join(user_shares.get('user_stocks', []))}."
        )
        return total_list

    except Exception as e:
        get_stock_price_logger.warning(f"Не удалось отобразить котировки акций. Ошибка: {e}")
        return []
