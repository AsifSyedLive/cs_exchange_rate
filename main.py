import os
from datetime import datetime
from utils.logger import setup_logger
from utils.config_loader import ConfigLoader
from exchange_rate.exchange_rate_fetcher import ExchangeRateFetcher
from exchange_rate.exchange_rate_preprocess import ExchangeRatePreProcessor


def init_variables():
    """
    Initialize environment variables

    Returns:
        dict: Environment variables loaded from configuration and other derived variables
    """
    config_loader = ConfigLoader()
    env_variables = config_loader.get_env_variables()
    current_datetime = datetime.now()
    log_file = env_variables.get('LOG_FILE') + "." + current_datetime.strftime('%Y-%m-%d') + ".log"

    config_dict = {
        'log_file': log_file,
        'current_datetime': current_datetime
    }
    return config_dict


# Main function to execute the script
def main():
    """
    Control Flow

    a. Fetch Exchange Rates
    b. Preprocess Exchange Rates data to fix date/rates anomalies
    c. Analyze Exchange Rate data
    """
    # Fetch Variables to configure
    config_dict = init_variables()
    print(config_dict['log_file'])
    # Set up logger
    script_name = os.path.basename(__file__)
    logger = setup_logger(script_name, config_dict['log_file'])

    # Log the start of the process
    logger.info("Initiating process to retrieve exchange rates")

    # Fetch exchange rates data
    fetcher = ExchangeRateFetcher()
    json_data_file = fetcher.get_exchange_rates()

    logger.info("Preprocess data to fix date/rates anomalies")
    processor = ExchangeRatePreProcessor(json_data_file)
    json_data_file_processed = processor.process_data()

    # Print processed data
    print(json_data_file_processed)

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
