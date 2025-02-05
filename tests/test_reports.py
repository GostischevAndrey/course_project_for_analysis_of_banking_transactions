import pandas as pd
import pytest

from src.reports import spending_by_weekday


@pytest.fixture
def df_spending():
    return pd.DataFrame(
        {
            "Дата операции": ["31.01.2022 16:44:00", "30.12.2021 16:44:00", "24.12.2021 16:44:00"],
            "Дата платежа": ["31.12.2021", "30.12.2021", "24.12.2021"],
            "Сумма операции": [-160.89, -400, -900],
            "Сумма платежа": [-160.89, -400, -900],
        }
    )


def test_spending_by_weekday_1(df_spending):
    assert spending_by_weekday(df_spending, "2022-02-01") == '{"Friday":900.0,"Monday":160.89,"Thursday":400.0}'


def test_spending_by_weekday_2(df_spending):
    assert spending_by_weekday(df_spending) == "{}"
