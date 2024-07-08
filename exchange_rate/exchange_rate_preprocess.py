import os
from datetime import datetime, timedelta
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger
from . import *


class ExchangeRatePreProcessor:
    def __init__(self, json_data):
        """
        Initialize the ExchangeRatePreProcessor with Json Data containing exchange rates

        Sample Json expected structure
        {
            "success": true,
            "timeseries": true,
            "start_date": "2024-06-08",
            "end_date": "2024-07-08",
            "base": "AUD",
            "rates": {
                "2024-06-08": {
                    "NZD": 1.07895
            },
            "2024-06-09": {
                "NZD": 1.07808
            ...
            ...
        }
            """
        self.json_data = json_data['rates']

        # Generate the module configuration file name based on script name
        config_file = "config_" + os.path.splitext(os.path.basename(__file__))[0] + ".json"

        # Create a ConfigLoader instance and load module specific configurations
        config_loader = ConfigLoader(module_config_file=config_file)
        module_config = config_loader.get_module_config()

        # PLACEHOLDER - Assigning Variables from configurations
        self.place_holder_var1 = module_config.get("place_holder_var1")
        # self.place_holder_var2 = module_config.get("place_holder_var2")

    def process_data(self):
        """
        Preprocessing the data
        a. Fixes any missing dates (if any) in the last 30 days date range
        b. Interpolates missing values by taking average of previous and next values.
           In absence of either of them i.e. previous or next, then same value is used for both whichever is available
        """

        # Set up the logger for the script
        script_name = os.path.basename(__file__)
        logger = setup_logger(script_name, log_file)
        logger.info("Setting up Variables")

        # List of dates available in the json data
        existing_dates = list(self.json_data.keys())

        # List to hold all required dates
        required_dates = []

        # Converting start and end dates from string to date objects as date operation is required later
        iteration_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_dt = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Generating Required Dates Dict for comparison with extracted dates
        while iteration_date <= end_date_dt:
            iteration_date_str = iteration_date.strftime("%Y-%m-%d")
            required_dates.append(iteration_date_str)
            iteration_date += timedelta(days=1)

        # Interpolating missing data (required dates was already derived earlier)
        processed_data = {}
        for iteration_date in required_dates:
            if iteration_date not in existing_dates:
                processed_data[iteration_date] = self.interpolate_value(self.json_data, iteration_date)
            else:
                processed_data[iteration_date] = self.json_data[iteration_date][target_currency]

        # Returned data will be dict of a key value pair of date and exchange rate
        # example - { '2024-07-09' : 1.0789, '2024-07-08' : 1.0785, ... and so on }
        return processed_data

    def interpolate_value(self, rates_data, date):
        """
        Interpolates missing values by taking average of previous and next values.
        In absence of either of them i.e. previous or next, then same value is used for both whichever is available

        Returns: calculated value for interpolation (float)
        """
        prev_date, next_date = self.find_nearest_dates(rates_data, date)
        if not prev_date and not next_date:
            return None

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
        """
        Finds dates on the left/right side of the date passed as an argument inside the dictionary
        This also works if more than one date is missing

        Returns: two dates - previous date and next date available in dict
        """
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
