import os
from datetime import datetime, timedelta
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger


class ExchangeRatePreProcessor:
    def __init__(self, json_data):
        """
        Initialize the ExchangeRatePreProcessor
        """
        self.json_data = json_data['rates']
        config_file = "config_"+os.path.splitext(os.path.basename(__file__))[0]+".json"
        self.config_loader = ConfigLoader(module_config_file=config_file)

        self.env_variables = self.config_loader.get_env_variables()
        self.common_config = self.config_loader.get_common_config()
        self.module_config = self.config_loader.get_module_config()
        self.current_datetime = datetime.now()
        self._load_config()

    def _load_config(self):
        """
         Variables to be used in this script
        """
        # Assigning Variables from configurations
        self.log_file = self.env_variables.get('LOG_FILE')+"."+self.current_datetime.strftime('%Y-%m-%d')+".log"
        self.defaults_exchange_rate = self.common_config.get('defaults_exchange_rate', {})
        self.days = self.defaults_exchange_rate.get('days')
        self.base_currency = self.defaults_exchange_rate.get('base_currency')
        self.target_currency = self.defaults_exchange_rate.get('target_currency')

        # Calculate start and end dates for fetching data
        self.start_date = (self.current_datetime - timedelta(days=self.days)).strftime('%Y-%m-%d')
        self.end_date = self.current_datetime.strftime('%Y-%m-%d')

    def process_data(self):
        """
        Two preprocessing steps
        a. Fixes any missing dates (if any) in the last 30 days date range
        b. Interpolates missing values by taking average of previous and next values.
           In absence of either of them i.e. previous or next, then same value is used for both whichever is available
        """
        script_name = os.path.basename(__file__)
        logger = setup_logger(script_name, self.log_file)
        logger.info("Setting up Variables")

        existing_dates = list(self.json_data.keys())
        required_dates = []

        iteration_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
        end_date_dt = datetime.strptime(self.end_date, '%Y-%m-%d').date()

        while iteration_date <= end_date_dt:
            iteration_date_str = iteration_date.strftime("%Y-%m-%d")
            required_dates.append(iteration_date_str)
            iteration_date += timedelta(days=1)

        processed_data = {}
        for date in required_dates:
            if date not in existing_dates:
                processed_data[date] = self.interpolate_value(self.json_data, date)
            else:
                processed_data[date] = self.json_data[date][self.target_currency]

        print(processed_data)
        return self.json_data

    def interpolate_value(self, rates_data, date):
        prev_date, next_date = self.find_nearest_dates(rates_data, date)
        if not prev_date and not next_date:
            return None

        if prev_date is None:
            prev_rate = rates_data[next_date][self.target_currency]
        else:
            prev_rate = rates_data[prev_date][self.target_currency]

        if next_date is None:
            next_rate = rates_data[prev_date][self.target_currency]
        else:
            next_rate = rates_data[next_date][self.target_currency]
        interpolated_value = (prev_rate + next_rate) / 2
        return interpolated_value

    def find_nearest_dates(self, rates_data, date):
        dates = list(rates_data.keys())
        dates.sort()
        prev_date, next_date = None, None
        for iter_date in dates:
            if iter_date <= date:
                prev_date = iter_date
            if iter_date >= date:
                next_date = iter_date
                break
        return prev_date, next_date
