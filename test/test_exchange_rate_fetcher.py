from unittest.mock import patch
from exchange_rate.exchange_rate_fetcher import ExchangeRateFetcher

"""
Test Case1: Test whether data is retreived correctly by checking for four dates and their exchange rate values
"""
@patch('exchange_rate.exchange_rate_fetcher.ConfigLoader')
@patch('exchange_rate.exchange_rate_fetcher.setup_logger')
@patch('requests.get')
def test_case1_exchange_rate_fetcher(mock_requests_get, mock_setup_logger, mock_config_loader):
    # Mock ConfigLoader's return value
    mock_config_instance = mock_config_loader.return_value
    mock_config_instance.get_module_config.return_value = {
        "api_url": "https://api.exchangeratesapi.io",
        "end_point": "timeseries"
    }
    mock_config_instance.get_config_common.return_value = {
        "defaults_exchange_rate": {
            "days": 4,
            "base_currency": "AUD",
            "target_currency": "NZD"
        }
    }

    # Mock requests.get method
    mock_response = {
        "success": True,
        "timeseries": True,
        "start_date": "2024-07-06",
        "end_date": "2024-07-09",
        "base": "AUD",
        "rates": {
            "2024-07-06": {
                "NZD": 1.100644
            },
            "2024-07-07": {
                "NZD": 1.098638
            },
            "2024-07-08": {
                "NZD": 1.098625
            },
            "2024-07-09": {
                "NZD": 1.098625
            }
        }
    }
    mock_requests_get.return_value.json.return_value = mock_response

    # Initialize ExchangeRateFetcher
    exchange_rate_fetcher = ExchangeRateFetcher()

    # Calling the method under test (get_exchange_rates) without checking output
    result = exchange_rate_fetcher.get_exchange_rates()
    # Assertions to validate the result against the mock response
    assert result["success"] is True
    assert result["timeseries"] is True
    assert result["start_date"] == "2024-07-06"
    assert result["end_date"] == "2024-07-09"
    assert result["base"] == "AUD"
    assert "rates" in result
    assert "2024-07-06" in result["rates"]
    assert "NZD" in result["rates"]["2024-07-06"]
    assert result["rates"]["2024-07-06"]["NZD"] == 1.100644
    assert "2024-07-07" in result["rates"]
    assert "NZD" in result["rates"]["2024-07-07"]
    assert result["rates"]["2024-07-07"]["NZD"] == 1.098638
    assert "2024-07-08" in result["rates"]
    assert "NZD" in result["rates"]["2024-07-08"]
    assert result["rates"]["2024-07-08"]["NZD"] == 1.098625
    assert "2024-07-09" in result["rates"]
    assert "NZD" in result["rates"]["2024-07-09"]
    assert result["rates"]["2024-07-09"]["NZD"] == 1.098625

"""
Test Case2: Test if url can be used to fetch data for different end point and values match expectations
"""
@patch('exchange_rate.exchange_rate_fetcher.ConfigLoader')
@patch('exchange_rate.exchange_rate_fetcher.setup_logger')
@patch('requests.get')
def test_case2_exchange_rate_fetcher(mock_requests_get, mock_setup_logger, mock_config_loader):
    # Mock ConfigLoader's return value
    mock_config_instance = mock_config_loader.return_value
    mock_config_instance.get_module_config.return_value = {
        "api_url": "https://api.exchangeratesapi.io",
        "end_point": "latest"
    }

    # Mock requests.get method
    mock_response = {
        "success": True,
        "base": "AUD",
        "date": "2024-07-08",
        "rates": {
            "NZD": 1.098625
        }
    }
    mock_requests_get.return_value.json.return_value = mock_response

    # Initialize ExchangeRateFetcher
    exchange_rate_fetcher = ExchangeRateFetcher()

    # Calling the method under test (get_exchange_rates) without checking output
    result = exchange_rate_fetcher.get_exchange_rates()

    # Assertions to validate the result against the mock response
    assert result["success"] is True
    assert result["base"] == "AUD"
    assert result["date"] == "2024-07-08"
    assert "rates" in result
    assert "NZD" in result["rates"]
    assert result["rates"]["NZD"] == 1.098625


"""
Test Case3: Test if incorrect code returns error 404 when url is not reachable
"""
@patch('exchange_rate.exchange_rate_fetcher.ConfigLoader')
@patch('exchange_rate.exchange_rate_fetcher.setup_logger')
@patch('requests.get')
def test_case3_exchange_rate_fetcher(mock_requests_get, mock_setup_logger, mock_config_loader):

    # Mock ConfigLoader's return value
    mock_config_instance = mock_config_loader.return_value
    mock_config_instance.get_module_config.return_value = {
        "api_url": "https://somerandom.website",
        "end_point": "timeseries"
    }

    mock_config_instance.get_config_common.return_value = {
        "defaults_exchange_rate": {
            "days": 3,
            "base_currency": "AUD",
            "target_currency": "NZD"
        }
    }

    # Mock requests.get method
    mock_response = {
        "success": False,  # Indicating failure due to incorrect API URL
        "error": {
            "code": 404,
            "type": "not_found",
            "info": "Resource not found"
        }
    }
    mock_requests_get.return_value.json.return_value = mock_response

    # Initialize ExchangeRateFetcher
    exchange_rate_fetcher = ExchangeRateFetcher()


    # Calling the method under test (get_exchange_rates)
    result = exchange_rate_fetcher.get_exchange_rates()

    # Assertion to verify failure due to incorrect API URL
    assert result["success"] is False
    assert result["error"]["code"] == 404
    assert result["error"]["type"] == "not_found"
    assert result["error"]["info"] == "Resource not found"


# Running the test
test_case1_exchange_rate_fetcher()
test_case2_exchange_rate_fetcher()
test_case3_exchange_rate_fetcher()
