"Initializing variables to be used across modules"
from datetime import datetime, timedelta
from utils.config_loader import ConfigLoader

# Initialize configurations
config_loader=ConfigLoader()
env_variables = config_loader.get_env_variables()
common_config = config_loader.get_common_config()

current_datetime = datetime.now()


# Extract necessary variables
log_file = env_variables.get('LOG_FILE') + "." + current_datetime.strftime('%Y-%m-%d') + ".log"
access_key = env_variables.get('API_KEY')
defaults_exchange_rate = common_config.get('defaults_exchange_rate', {})
delta_days = defaults_exchange_rate.get('days')
base_currency = defaults_exchange_rate.get('base_currency')
target_currency = defaults_exchange_rate.get('target_currency')

# Calculate start and end dates for fetching data
start_date = (current_datetime - timedelta(days=delta_days)).strftime('%Y-%m-%d')
end_date = current_datetime.strftime('%Y-%m-%d')
current_date=end_date

# Make these variables available to other modules within the package
__all__ = ['log_file', 'access_key', 'start_date', 'end_date', 'current_date', 'delta_days', 'base_currency', 'target_currency']