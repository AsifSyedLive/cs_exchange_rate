import json
import os
import sys
from datetime import datetime, timedelta
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger


class ExchangeRatePreProcessor:
    def __init__(self, json_data):
        self.json_data = json_data['rates']
        config_file = "config_"+os.path.splitext(os.path.basename(__file__))[0]+".json"
        self.config_loader = ConfigLoader(module_config_file=config_file)

        self.env_variables = self.config_loader.get_env_variables()
        self.common_config = self.config_loader.get_common_config()
        self.module_config = self.config_loader.get_module_config()

    def process_data(self):

        # Extract variables from configurations
        script_name = os.path.basename(__file__)
        log_file = self.env_variables.get('LOG_FILE')
        logger = setup_logger(script_name, log_file)
        logger.info("Setting up Variables")

        # Assigning Variables

        defaults_exchange_rate = self.common_config.get('defaults_exchange_rate', {})
        days = defaults_exchange_rate.get('days')
        base_currency = defaults_exchange_rate.get('base_currency')
        target_currency = defaults_exchange_rate.get('target_currency')

        logger.info("Calculate dates to fetch the exchange rates")
        # Calculate start and end dates
        current_datetime = datetime.now()
        start_date = (current_datetime - timedelta(days=days))
        end_date = current_datetime

        existing_dates = list(self.json_data.keys())
        required_dates = []

        iteration_date = start_date
        while iteration_date <= end_date:
            iteration_date_str = iteration_date.strftime("%Y-%m-%d")
            required_dates.append(iteration_date_str)
            iteration_date += timedelta(days=1)

        processed_data={}
        for date in required_dates:
            if date not in existing_dates:
                processed_data[date] = self.interpolate_value(self.json_data, date)
            else:
                processed_data[date] = self.json_data[date][target_currency]

        print(processed_data)
        return self.json_data

    def interpolate_value(self, rates_data, date):
        prev_date, next_date = self.find_nearest_dates(rates_data, date)
        if not prev_date and not next_date:
            return None

        target_currency = self.common_config.get('defaults_exchange_rate', {}).get('target_currency')

        if prev_date is None:
            prev_rate = rates_data[next_date][target_currency]
        else:
            prev_rate = rates_data[prev_date][target_currency]

        if next_date is None:
            next_rate = rates_data[prev_date][target_currency]
        else:
            next_rate = rates_data[next_date][target_currency]
        interpolated_value = (prev_rate + next_rate) / 2
        return interpolated_value

    def find_nearest_dates(self, rates_data, date):
        dates = list(rates_data.keys())
        dates.sort()
        prev_date, next_date = None, None
        for iter in dates:
            if iter <= date:
                prev_date = iter
            if iter >= date:
                next_date = iter
                break
        return prev_date, next_date


