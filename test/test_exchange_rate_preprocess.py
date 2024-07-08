from unittest.mock import patch, Mock
from exchange_rate.exchange_rate_preprocess import ExchangeRatePreProcessor
import exchange_rate

"""
Test Case1: Check whether code fixes Missing date 2024-06-10 and value (interpolated) within the json
"""
@patch('exchange_rate.exchange_rate_preprocess.setup_logger')
def test_case1_exchange_rate_preprocess(mock_setup_logger):


        # Mock JSON data for testing
    mock_json_data = {"success":True,"timeseries":True,"start_date":"2024-06-09","end_date":"2024-07-09","base":"AUD","rates":{"2024-06-09":{"NZD":1.07808},"2024-06-11":{"NZD":1.075373},"2024-06-12":{"NZD":1.077024},"2024-06-13":{"NZD":1.076672},"2024-06-14":{"NZD":1.075134},"2024-06-15":{"NZD":1.073361},"2024-06-16":{"NZD":1.077516},"2024-06-17":{"NZD":1.079063},"2024-06-18":{"NZD":1.084816},"2024-06-19":{"NZD":1.087336},"2024-06-20":{"NZD":1.087845},"2024-06-21":{"NZD":1.08981},"2024-06-22":{"NZD":1.091934},"2024-06-23":{"NZD":1.08548},"2024-06-24":{"NZD":1.087334},"2024-06-25":{"NZD":1.085985},"2024-06-26":{"NZD":1.092889},"2024-06-27":{"NZD":1.09314},"2024-06-28":{"NZD":1.097649},"2024-06-29":{"NZD":1.097649},"2024-06-30":{"NZD":1.094296},"2024-07-01":{"NZD":1.097228},"2024-07-02":{"NZD":1.096445},"2024-07-03":{"NZD":1.098792},"2024-07-04":{"NZD":1.10017},"2024-07-05":{"NZD":1.098888},"2024-07-06":{"NZD":1.100644},"2024-07-07":{"NZD":1.098638},"2024-07-08":{"NZD":1.098292}}}

    # Initialize ExchangeRatePreProcessor with mock JSON data
    pre_processor = ExchangeRatePreProcessor(mock_json_data)

    # Mock interpolation for testing
    pre_processor.interpolate_value = Mock(return_value=1.078142)

    # Call process_data method
    processed_data = pre_processor.process_data()

    print(processed_data)
    # Assertions
    assert len(list(processed_data.keys())) == 31  # additional one day includes current date
    assert '2024-06-10' in processed_data  # Check interpolated date exists
    assert processed_data['2024-06-10'] == 1.078142 # Verify interpolated value

"""
Test Case2: Check whether code fixes Missing date and value at left boundary i.e. 2024-06-09 
"""
@patch('exchange_rate.exchange_rate_preprocess.setup_logger')
def test_case2_exchange_rate_preprocess(mock_setup_logger):
    # Mock JSON data for testing - missing 2024-06-09 date
    mock_json_data = {"success": True, "timeseries": True, "start_date": "2024-06-09", "end_date": "2024-07-09",
                              "base": "AUD", "rates": {"2024-06-10": {"NZD": 1.078204},
                                                       "2024-06-11": {"NZD": 1.075373}, "2024-06-12": {"NZD": 1.077024},
                                                       "2024-06-13": {"NZD": 1.076672}, "2024-06-14": {"NZD": 1.075134},
                                                       "2024-06-15": {"NZD": 1.073361}, "2024-06-16": {"NZD": 1.077516},
                                                       "2024-06-17": {"NZD": 1.079063}, "2024-06-18": {"NZD": 1.084816},
                                                       "2024-06-19": {"NZD": 1.087336}, "2024-06-20": {"NZD": 1.087845},
                                                       "2024-06-21": {"NZD": 1.08981}, "2024-06-22": {"NZD": 1.091934},
                                                       "2024-06-23": {"NZD": 1.08548}, "2024-06-24": {"NZD": 1.087334},
                                                       "2024-06-25": {"NZD": 1.085985}, "2024-06-26": {"NZD": 1.092889},
                                                       "2024-06-27": {"NZD": 1.09314}, "2024-06-28": {"NZD": 1.097649},
                                                       "2024-06-29": {"NZD": 1.097649}, "2024-06-30": {"NZD": 1.094296},
                                                       "2024-07-01": {"NZD": 1.097228}, "2024-07-02": {"NZD": 1.096445},
                                                       "2024-07-03": {"NZD": 1.098792}, "2024-07-04": {"NZD": 1.10017},
                                                       "2024-07-05": {"NZD": 1.098888}, "2024-07-06": {"NZD": 1.100644},
                                                       "2024-07-07": {"NZD": 1.098638},
                                                       "2024-07-08": {"NZD": 1.098292},
                                                       "2024-07-09": {"NZD": 1.098625}
                                                       }}

    # Initialize ExchangeRatePreProcessor with mock JSON data
    pre_processor = ExchangeRatePreProcessor(mock_json_data)

    # Mock interpolation for testing
    pre_processor.interpolate_value = Mock(return_value=1.07808)

    # Call process_data method
    processed_data = pre_processor.process_data()

    print(processed_data)
    # Assertions
    assert len(list(processed_data.keys())) == 31  #Includes current date
    assert '2024-06-09' in processed_data  # Check interpolated date exists
    assert processed_data['2024-06-09'] == 1.07808  # Verify interpolated value

"""
Test Case3: Check whether code fixes Missing date and value at left boundary i.e. 2024-07-09 
"""
@patch('exchange_rate.exchange_rate_preprocess.setup_logger')
def test_case3_exchange_rate_preprocess(mock_setup_logger):


    # Mock JSON data for testing
    mock_json_data = {"success":True,"timeseries":True,"start_date":"2024-06-09","end_date":"2024-07-09","base":"AUD","rates":{"2024-06-09":{"NZD":1.07808},"2024-06-10":{"NZD":1.078204},"2024-06-11":{"NZD":1.075373},"2024-06-12":{"NZD":1.077024},"2024-06-13":{"NZD":1.076672},"2024-06-14":{"NZD":1.075134},"2024-06-15":{"NZD":1.073361},"2024-06-16":{"NZD":1.077516},"2024-06-17":{"NZD":1.079063},"2024-06-18":{"NZD":1.084816},"2024-06-19":{"NZD":1.087336},"2024-06-20":{"NZD":1.087845},"2024-06-21":{"NZD":1.08981},"2024-06-22":{"NZD":1.091934},"2024-06-23":{"NZD":1.08548},"2024-06-24":{"NZD":1.087334},"2024-06-25":{"NZD":1.085985},"2024-06-26":{"NZD":1.092889},"2024-06-27":{"NZD":1.09314},"2024-06-28":{"NZD":1.097649},"2024-06-29":{"NZD":1.097649},"2024-06-30":{"NZD":1.094296},"2024-07-01":{"NZD":1.097228},"2024-07-02":{"NZD":1.096445},"2024-07-03":{"NZD":1.098792},"2024-07-04":{"NZD":1.10017},"2024-07-05":{"NZD":1.098888},"2024-07-06":{"NZD":1.100644},"2024-07-07":{"NZD":1.098638},"2024-07-08": {"NZD":1.098292}}}

    # Initialize ExchangeRatePreProcessor with mock JSON data
    pre_processor = ExchangeRatePreProcessor(mock_json_data)

    # Mock interpolation for testing
    pre_processor.interpolate_value = Mock(return_value=1.098292)

    # Call process_data method
    processed_data = pre_processor.process_data()

    print(processed_data)
    # Assertions
    assert len(list(processed_data.keys())) == 31  # Expected 8 days of data
    assert '2024-07-09' in processed_data  # Check interpolated date exists
    assert processed_data['2024-07-09'] == 1.098292  # Verify interpolated value


# Run the test function

test_case1_exchange_rate_preprocess()
test_case2_exchange_rate_preprocess()
test_case3_exchange_rate_preprocess()

