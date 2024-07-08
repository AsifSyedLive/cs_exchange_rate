import os
import pandas as pd
import matplotlib.pyplot as plt
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger
from . import *


class ExchangeRateAnalyzer:
    def __init__(self, exchange_rate_dict):
        """
        Initialize the ExchangeRateAnalyzer

        sample of argument - { '2024-07-09' : 1.0789, '2024-07-08' : 1.0785, ... and so on }
        """

        # Generate the module configuration file name based on script name
        config_file = "config_" + os.path.splitext(os.path.basename(__file__))[0] + ".json"

        # Create a ConfigLoader instance and load module specific configurations
        config_loader = ConfigLoader(module_config_file=config_file)
        module_config = config_loader.get_module_config()

        # Assigning Module Variables from configurations
        self.moving_average = module_config.get("moving_average")
        self.fig_width = module_config.get("fig_width")
        self.fig_height = module_config.get("fig_height")

        # Initialize DataFrame from exchange_rate_data_dict for ease in generating statistics later
        self.df = pd.DataFrame(list(exchange_rate_dict.items()), columns=['Date', 'Exchange Rate'])

        # Apply Data Type
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['Exchange Rate'] = pd.to_numeric(self.df['Exchange Rate'])

    def get_statistics(self):
        """
        Calculate statistics for the exchange rate data

        Returns:
            Mean, median, standard deviation, minimum, and maximum of the exchange rates
        """
        mean_rate = self.df['Exchange Rate'].mean()
        median_rate = self.df['Exchange Rate'].median()
        std_dev = self.df['Exchange Rate'].std()
        min_rate = self.df['Exchange Rate'].min()
        max_rate = self.df['Exchange Rate'].max()

        return mean_rate, median_rate, std_dev, min_rate, max_rate

    def trend_analysis(self):
        """
        Trend analysis on the exchange rate data
        """
        self.df['Moving Average'] = self.df['Exchange Rate'].rolling(window=self.moving_average).mean()
        self.df['Rate of Change'] = self.df['Exchange Rate'].diff()

    def visualize_data(self):
        """
        Visualization of Exchange Rate Data
        """

        # Set up the logger for the script
        script_name = os.path.basename(__file__)
        logger = setup_logger(script_name, log_file)
        logger.info(f"Subplot 1 - Generation")

        # Create a figure with specified dimensions
        plt.figure(figsize=(self.fig_width, self.fig_height))

        # Executing Trend Analysis and Statistics before generating plot
        self.trend_analysis()
        mean_rate, median_rate, std_dev, min_rate, max_rate = self.get_statistics()

        # Subplot 1: Exchange Rate and Moving Average
        plt.subplot(2, 1, 1)
        plt.plot(self.df['Date'], self.df['Exchange Rate'],
                 marker='o', linestyle='-', color='b', label='Exchange Rate')
        plt.plot(self.df['Date'], self.df['Moving Average'],
                 linestyle='--', color='r', label=f'{self.moving_average}-day Moving Average')
        plt.title(f'Exchange Rate and Moving Average ({self.moving_average} days)')
        plt.xlabel('Date')
        plt.ylabel('Exchange Rate')
        plt.xticks(rotation=45)  # Rotate x-axis labels by 45 degrees
        plt.legend()

        # Log the addition of statistical information to the plot
        logger.info(f"Adding statistics information to plot")
        logger.info(f'Standard Deviation: {std_dev:.4f}'
                    f'\nMin: {min_rate:.4f}\nMax: {max_rate:.4f}'
                    f'\nMean: {mean_rate:.4f}\nMedian: {median_rate:.4f}')

        # To display text outside the plot area at the bottom of the figure
        fig = plt.gcf()
        fig.text(0.9, 0.2,
                 f'Standard Deviation: {std_dev:.4f}'
                 f'\nMin: {min_rate:.4f}\nMax: {max_rate:.4f}'
                 f'\nMean: {mean_rate:.4f}\nMedian: {median_rate:.4f}',
                 verticalalignment='bottom', horizontalalignment='right', fontsize=12)

        # Adjust layout and display plots
        plt.tight_layout()
        plt.show()
