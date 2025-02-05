from datetime import datetime
from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest

from src.utils import common_information, get_excel_df, get_exchange_rate, get_stock_price, greetings, top_5_operations


@pytest.fixture
def get_excel_return():
    return [
        {
            "Дата операции": "17.03.2023 15:48:14",
            "Дата платежа": "17.03.2023",
            "Номер карты": "*3047",
            "Статус": "OK",
            "Сумма операции": 200000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": 200000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "NaN",
            "Категория": "Пополнения",
            "MCC": "NaN",
            "Описание": "Внесение наличных через банкомат Тинькофф",
            "Бонусы (включая кэшбэк)": 0.0,
            "Округление на инвесткопилку": 0.0,
            "Сумма операции с округлением": 200000.0,
        },
        {
            "Дата операции": "20.12.2023 14:41:33",
            "Дата платежа": "20.12.2023",
            "Номер карты": "*4467",
            "Статус": "OK",
            "Сумма операции": 200000.00,
            "Валюта операции": "RUB",
            "Сумма платежа": 200000.00,
            "Валюта платежа": "RUB",
            "Кэшбэк": "NaN",
            "Категория": "Переводы",
            "MCC": "NaN",
            "Описание": "Анна А.",
            "Бонусы (включая кэшбэк)": 0.00,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 200000.0,
        },
        {
            "Дата операции": "27.12.2023 14:41:33",
            "Дата платежа": "27.12.2023",
            "Номер карты": "*4467",
            "Статус": "OK",
            "Сумма операции": 180000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": 180000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "NaN",
            "Категория": "Переводы",
            "MCC": "NaN",
            "Описание": "Андрей Г.",
            "Бонусы (включая кэшбэк)": 0.0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 180000.0,
        },
    ]


@patch("pandas.read_excel")
def test_get_excel_df_1(mock_get, get_excel_return):
    mock_get.return_value = pd.DataFrame(
        [
            {
                "Дата операции": "17.03.2023 15:48:14",
                "Дата платежа": "17.03.2023",
                "Номер карты": "*3047",
                "Статус": "OK",
                "Сумма операции": 200000.0,
                "Валюта операции": "RUB",
                "Сумма платежа": 200000.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": "NaN",
                "Категория": "Пополнения",
                "MCC": "NaN",
                "Описание": "Внесение наличных через банкомат Тинькофф",
                "Бонусы (включая кэшбэк)": 0.0,
                "Округление на инвесткопилку": 0.0,
                "Сумма операции с округлением": 200000.0,
            },
            {
                "Дата операции": "20.12.2023 14:41:33",
                "Дата платежа": "20.12.2023",
                "Номер карты": "*4467",
                "Статус": "OK",
                "Сумма операции": 200000.0,
                "Валюта операции": "RUB",
                "Сумма платежа": 200000.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": "NaN",
                "Категория": "Переводы",
                "MCC": "NaN",
                "Описание": "Анна А.",
                "Бонусы (включая кэшбэк)": 0.0,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 200000.0,
            },
            {
                "Дата операции": "27.12.2023 14:41:33",
                "Дата платежа": "27.12.2023",
                "Номер карты": "*4467",
                "Статус": "OK",
                "Сумма операции": 180000.0,
                "Валюта операции": "RUB",
                "Сумма платежа": 180000.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": "NaN",
                "Категория": "Переводы",
                "MCC": "NaN",
                "Описание": "Андрей Г.",
                "Бонусы (включая кэшбэк)": 0.0,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 180000.0,
            },
        ]
    )
    assert get_excel_df("filename.xlsx") == get_excel_return


@patch("pandas.read_excel")
def test_get_excel_df_2(mock_get):
    mock_get.return_value = pd.DataFrame({})
    assert get_excel_df("filename.xlsx") == []


@patch("os.path.join")
def test_get_excel_df_3(mock_path):
    mock_path.return_value = []
    assert get_excel_df("filename.xlsx") == []


def test_top_5_operations_1(get_excel_return):
    assert (
        top_5_operations(get_excel_return)
        == [
            {
                "Дата операции": "17.03.2023 15:48:14",
                "Категория": "Пополнения",
                "Номер карты": "*3047",
                "Описание": "Внесение наличных через банкомат Тинькофф",
                "Сумма операции": 200000.0,
            },
            {
                "Дата операции": "20.12.2023 14:41:33",
                "Категория": "Переводы",
                "Номер карты": "*4467",
                "Описание": "Анна А.",
                "Сумма операции": 200000.0,
            },
            {
                "Дата операции": "27.12.2023 14:41:33",
                "Категория": "Переводы",
                "Номер карты": "*4467",
                "Описание": "Андрей Г.",
                "Сумма операции": 180000.0,
            },
        ]
        != [
            {
                "Дата операции": "20.12.2023 14:41:33",
                "Категория": "Переводы",
                "Номер карты": "*4467",
                "Описание": "Анна А.",
                "Сумма операции": 200000.0,
            },
            {
                "Дата операции": "27.12.2023 14:41:33",
                "Категория": "Пополнения",
                "Номер карты": "*3047",
                "Описание": "Внесение наличных через банкомат Тинькофф",
                "Сумма операции": 200000.0,
            },
            {
                "Дата операции": "27.07.2024 09:09:00",
                "Категория": "Переводы",
                "Номер карты": "*4467",
                "Описание": "Андрей Г.",
                "Сумма операции": 180000.0,
            },
        ]
    )


def test_top_5_operations_2(get_excel_return):
    assert top_5_operations(None) == []


def test_common_information_1(get_excel_return):
    assert common_information(get_excel_return) == []


def test_common_information_2():
    assert common_information([]) == []


def test_common_information_3(get_excel_return):
    mock_get = Mock(return_value=get_excel_return)
    pd.DataFrame = mock_get
    assert common_information(get_excel_return) == []


@patch("src.utils.datetime")
def test_greetings_1(mock_datetime):
    mock_datetime.now.return_value = datetime(2022, 7, 12, 14, 26, 44)
    assert greetings() == "Доброго дня!"


@patch("src.utils.datetime")
def test_greetings_2(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 5, 15, 21, 55, 55)
    assert greetings() == "Доброго вечера!"


@patch("src.utils.datetime")
def test_greetings_3(mock_datetime):
    mock_datetime.now.return_value = datetime(2021, 1, 12, 2, 20, 46)
    assert greetings() == "Доброй ночи!"


@patch("src.utils.datetime")
def test_greetings_4(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 2, 2, 6, 20, 55)
    assert greetings() == "Доброе утро!"


def test_get_exchange_rate():
    assert get_exchange_rate("filename.json") == []


@patch("urllib.request")
def test_get_stock_price(mock_get):
    mock_get.return_value = [
        {"Тикер": "SADL", "Цена": 18.25},
        {"Тикер": "AMZN", "Цена": 227.03},
        {"Тикер": "IBACU", "Цена": 98.32},
    ]
    assert get_stock_price("None.json") == []


