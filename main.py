import os
from datetime import datetime
# Import project utilities to assist logging and loading configurations
from utils.logger import setup_logger
from utils.config_loader import ConfigLoader
# Import classes to be instantiated
from exchange_rate.exchange_rate_fetcher import ExchangeRateFetcher
from exchange_rate.exchange_rate_preprocess import ExchangeRatePreProcessor
from exchange_rate.exchange_rate_analyze import ExchangeRateAnalyzer


def init_variables():
    """
    Initialize environment variables

    Returns:
        dict: Environment variables loaded from environmental configuration file and  derived variables
    """
    config_loader = ConfigLoader()
    env_variables = config_loader.get_env_variables()
    current_datetime = datetime.now()

    # Create a log file name by appending the current date to the base file name
    log_file = env_variables.get('LOG_FILE') + "." + current_datetime.strftime('%Y-%m-%d') + ".log"

    # Construct a config (dictionary) for configuration settings that will be used by main function
    config_dict = {
        'log_file': log_file,
        'current_datetime': current_datetime
    }
    return config_dict


# Main function to run the script
def main():
    """
    Main control flow of the script.

    a. Fetch the exchange rates
    b. Preprocess exchange rates data to fix date/rates anomalies
    c. Analyze and visualize exchange rate data
    """
    # Fetch Variables to configure
    config_dict = init_variables()

    # Set up logger
    script_name = os.path.basename(__file__)
    logger = setup_logger(script_name, config_dict['log_file'])

    # Log the start of the process
    logger.info("Initiating process to retrieve exchange rates")

    # Fetch the exchange rates data
    fetcher = ExchangeRateFetcher()
    exchange_rate_json = fetcher.get_exchange_rates()

    logger.info("Preprocess data to fix date/rates anomalies")
    processor = ExchangeRatePreProcessor(exchange_rate_json)
    exchange_rate_processed = processor.process_data()

    # Create an instance of ExchangeRateAnalyzer
    analyzer = ExchangeRateAnalyzer(exchange_rate_processed)

    # Analyze and visualize data
    analyzer.visualize_data()


# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
