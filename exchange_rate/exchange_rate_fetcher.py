import requests
import os
import sys

from utils.config_loader import ConfigLoader
from utils.logger import setup_logger
from . import *


class ExchangeRateFetcher:
    def __init__(self):
        """
        Initialize the ExchangeRateFetcher with module level variables
        """
        config_file = "config_" + os.path.splitext(os.path.basename(__file__))[0] + ".json"
        config_loader = ConfigLoader(module_config_file=config_file)
        module_config = config_loader.get_module_config()
        # Assigning Variables from configurations
        self.api_url = module_config.get("api_url")
        self.end_point = module_config.get("end_point")

    def get_exchange_rates(self):
        """
        Fetch exchange rates from an API using configured parameters

        Returns: JSON data containing exchange rates of between two currencies
        """

        # Setup Logger
        script_name = os.path.basename(__file__)
        logger = setup_logger(script_name, log_file)
        logger.info(f"Preparing Parameters for API request")

        # Prepare parameters for API request
        params = {
            "access_key": access_key,
            "start_date": start_date,
            "end_date": end_date,
            "base": base_currency,
            "symbols": target_currency
        }
        # Display parameters except for access_key
        params_for_log_display = dict(params)
        params_for_log_display.pop("access_key", None)
        logger.info(f"Parameters for API request: {params_for_log_display}")

        try:
            url = f"{self.api_url}/{self.end_point}"
            logger.info(f"Making GET request to the API - {url}")
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data: {e}")
            sys.exit(1)  # Exit with a non-zero status to indicate an error
