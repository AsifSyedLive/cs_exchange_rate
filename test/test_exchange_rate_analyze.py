from exchange_rate.exchange_rate_analyze import ExchangeRateAnalyzer

def test_case1_get_statistics():
    # Sample exchange rate data dictionary
    exchange_rate_dict = {
        '2024-07-01': 1.097228,
        '2024-07-02': 1.096445,
        '2024-07-03': 1.098792,
        '2024-07-04': 1.10017,
        '2024-07-05': 1.098888,
        '2024-07-06': 1.100644,
        '2024-07-07': 1.098638,
        '2024-07-08': 1.098268
    }

    # Initialize ExchangeRateAnalyzer
    analyzer = ExchangeRateAnalyzer(exchange_rate_dict)

    # Get statistics
    mean_rate, median_rate, std_dev, min_rate, max_rate = analyzer.get_statistics()

    # Assertions for Average, Min Rate and Max Rate
    assert round(mean_rate, 6) == round(1.098634125, 6)
    assert min_rate == 1.096445
    assert max_rate == 1.100644


test_case1_get_statistics()
