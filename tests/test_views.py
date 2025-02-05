from datetime import datetime
from unittest.mock import patch

from src.views import get_monthly_transactions_info


@patch("src.utils.datetime")
def test_main(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 12, 10, 9, 20, 55)

    assert get_monthly_transactions_info("None") == ""
