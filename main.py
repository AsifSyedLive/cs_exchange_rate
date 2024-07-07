import os
import sys
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
from utils.logger import setup_logger
from utils.config_loader import ConfigLoader
from exchange_rate.exchange_rate_fetcher import ExchangeRateFetcher
from exchange_rate.exchange_rate_preprocess import Preprocess
from exchange_rate.exchange_rate_analyzer import ExchangeRateAnalyzer

def init_variables():
    config_loader = ConfigLoader()
    env_variables = config_loader.get_env_variables()
    return env_variables

def main():
    env_variables = init_variables()
    log_file=env_variables['LOG_FILE']

    script_name = os.path.basename(__file__)
    logger=setup_logger(script_name,log_file)

    logger.info("Initiating process to retrieve exchange rates")
    fetcher = ExchangeRateFetcher()

    data = fetcher.get_exchange_rates()
    print(data)

    # Instantiate and preprocess JSON data
    #preprocessor = JsonPreprocess(json_data)
    #processed_data = preprocessor.preprocess()

    # Print processed data
    #print(json.dumps(processed_data, indent=2))

    #analyzer - ExchangeRate

    # Create an instance of ExchangeRateAnalyzer
    #analyzer = ExchangeRateAnalyzer(data_str)

    # Retrieve and print results
    #min_date, min_rate, max_date, max_rate = analyzer.find_min_max_rates()
    #average_rate = analyzer.calculate_average_rate()
    #change_percentages = analyzer.calculate_percentage_change()

    #print(f"Minimum rate on {min_date}: {min_rate}")
    #print(f"Maximum rate on {max_date}: {max_rate}")
    #print(f"Average rate: {average_rate}")

    #print("\nPercentage change each day:")
    #for date, change_percent in change_percentages.items():
    #    print(f"{date}: {change_percent:.2f}%")

if __name__ == "__main__":
    main()
