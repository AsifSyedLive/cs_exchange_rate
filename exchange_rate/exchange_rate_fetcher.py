import requests
import os
import configparser
from datetime import datetime, timedelta

from utils.config_loader import ConfigLoader

class ExchangeRateFetcher:
    def __init__(self):
        config_file = "config_"+os.path.splitext(os.path.basename(__file__))[0]+".json"
        self.config_loader = ConfigLoader(module_config_file=config_file)

        self.env_variables = self.config_loader.get_env_variables()
        self.common_config = self.config_loader.get_common_config()
        self.module_config = self.config_loader.get_module_config()
    def get_exchange_rates(self):
        # Extract variables from configurations
        log_file = self.env_variables.get('LOG_FILE')
        access_key = self.env_variables.get('API_KEY')

        base_url = self.module_config.get("url_exchange_rate")
        defaults_exchange_rate = self.common_config.get('defaults_exchange_rate', {})
        days = defaults_exchange_rate.get('days')
        base_currency = defaults_exchange_rate.get('base_currency')
        target_currency = defaults_exchange_rate.get('target_currency')

        # Calculate start and end dates
        current_datetime = datetime.now()
        start_date = (current_datetime - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = current_datetime.strftime('%Y-%m-%d')

        params = {
            "access_key": {access_key},
            "start_date":{start_date},
            "end_date":{end_date},
            "base":{base_currency},
            "symbols":{target_currency}
        }
        try:
            base_url="https://api.exchangeratesapi.io/v1/timeseries"
            #response = requests.get(base_url, params=params)
            #response.raise_for_status()
            #data = response.json()
            data = {'success': True, 'timeseries': True, 'start_date': '2024-06-06', 'end_date': '2024-07-06', 'base': 'AUD', 'rates': {'2024-06-06': {'NZD': 1.07631}, '2024-06-07': {'NZD': 1.074866}, '2024-06-08': {'NZD': 1.07895}, '2024-06-09': {'NZD': 1.07808}, '2024-06-10': {'NZD': 1.078204}, '2024-06-11': {'NZD': 1.075373}, '2024-06-12': {'NZD': 1.077024}, '2024-06-13': {'NZD': 1.076672}, '2024-06-14': {'NZD': 1.075134}, '2024-06-15': {'NZD': 1.073361}, '2024-06-16': {'NZD': 1.077516}, '2024-06-17': {'NZD': 1.079063}, '2024-06-18': {'NZD': 1.084816}, '2024-06-19': {'NZD': 1.087336}, '2024-06-20': {'NZD': 1.087845}, '2024-06-21': {'NZD': 1.08981}, '2024-06-22': {'NZD': 1.091934}, '2024-06-23': {'NZD': 1.08548}, '2024-06-24': {'NZD': 1.087334}, '2024-06-25': {'NZD': 1.085985}, '2024-06-26': {'NZD': 1.092889}, '2024-06-27': {'NZD': 1.09314}, '2024-06-28': {'NZD': 1.097649}, '2024-06-29': {'NZD': 1.097649}, '2024-06-30': {'NZD': 1.094296}, '2024-07-01': {'NZD': 1.097228}, '2024-07-02': {'NZD': 1.096445}, '2024-07-03': {'NZD': 1.098792}, '2024-07-04': {'NZD': 1.10017}, '2024-07-05': {'NZD': 1.098888}, '2024-07-06': {'NZD': 1.098888}}}
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None