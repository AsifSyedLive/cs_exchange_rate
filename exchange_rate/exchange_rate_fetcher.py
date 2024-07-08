import requests
import os
import sys
from datetime import datetime, timedelta
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
            #response = requests.get(url, params=params)
            #response.raise_for_status()
            #data = response.json()

            data = {'success': True, 'timeseries': True, 'start_date': '2024-06-07', 'end_date': '2024-07-07', 'base': 'AUD',
             'rates': {
                       '2024-06-10': {'NZD': 1.078204}, '2024-06-11': {'NZD': 1.075373},
                       '2024-06-12': {'NZD': 1.077024}, '2024-06-13': {'NZD': 1.076672},
                       '2024-06-14': {'NZD': 1.075134}, '2024-06-15': {'NZD': 1.073361},
                       '2024-06-16': {'NZD': 1.077516}, '2024-06-17': {'NZD': 1.079063},
                       '2024-06-18': {'NZD': 1.084816}, '2024-06-19': {'NZD': 1.087336},
                       '2024-06-20': {'NZD': 1.087845}, '2024-06-21': {'NZD': 1.08981}, '2024-06-22': {'NZD': 1.091934},
                       '2024-06-23': {'NZD': 1.08548}, '2024-06-24': {'NZD': 1.087334}, '2024-06-25': {'NZD': 1.085985},
                       '2024-06-26': {'NZD': 1.092889}, '2024-06-27': {'NZD': 1.09314}, '2024-06-28': {'NZD': 1.097649},
                       '2024-06-29': {'NZD': 1.097649}, '2024-06-30': {'NZD': 1.094296},
                       '2024-07-01': {'NZD': 1.097228}, '2024-07-02': {'NZD': 1.096445},
                       '2024-07-03': {'NZD': 1.098792}, '2024-07-04': {'NZD': 1.10017}, '2024-07-05': {'NZD': 1.098888},
                       '2024-07-06': {'NZD': 1.100644}}}

            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data: {e}")
            sys.exit(1)  # Exit with a non-zero status to indicate an error
