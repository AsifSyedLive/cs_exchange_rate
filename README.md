# Exchange Rates API Integration for Historical Analysis

This project provides tools to fetch, preprocess, and analyze exchange rate data. These scripts are designed to address data challenges such as filling in missing dates and handling invalid values. Additionally, the project features robust logging and flexible configuration options to ensure seamless integration and ease of use.

**Project Results**
![Alt text](https://github.com/AsifSyedLive/cs_exchange_rate/blob/master/docs/Results/results_exchange_rate_analyze_output.png)
## Table of Contents
1. [Project Structure](#project-structure)
2. [Setup](#setup)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Configuration](#configuration)
   - [Common Configuration](#common-configuration)
   - [Module-specific Configuration](#module-specific-configuration)
   - [.env File](#env-file)
4. [Usage](#usage)
   - [Fetch Exchange Rates](#fetch-exchange-rates)
   - [Preprocess Exchange Rates](#preprocess-exchange-rates)
   - [Analyze Exchange Rates](#analyze-exchange-rates)
   - [Main Script](#main-script)
5. [Testing](#testing)
6. [Utilities](#utilities)
   - [Config Loader](#config-loader)
   - [Logger](#logger)
7. [Limitations](#Limitations)
8. [Future Enhancements](#future-enhancements)
9. [License](#license)
10. [Contributing](#contributing)
11. [Contact](#contact)

## Project Structure
```bash
cs_exchange_rate-master/
├── config/                         
│   ├── config_common.json
│   ├── config_exchange_rate_analyze.json
│   ├── config_exchange_rate_fetcher.json
│   └── config_exchange_rate_preprocess.json
├── docs/                         
│   ├── Results/
├── exchange_rate/                  
│   ├── __init__.py
│   ├── exchange_rate_analyze.py
│   ├── exchange_rate_fetcher.py
│   └── exchange_rate_preprocess.py
├── test/                           
│   ├── test_exchange_rate_analyze.py
│   ├── test_exchange_rate_fetcher.py
│   └── test_exchange_rate_preprocess.py
├── utils/                          
│   ├── config_loader.py
│   └── logger.py
├── .gitignore
├── README.md
├── main.py                         
├── requirements.txt                
└── .env
```
## Setup

### Prerequisites
- Python 3.7 or later
- Virtual environment (or any other python interpreter)
- The current project requies access key (API Key) to https://api.exchangeratesapi.io

### Installation
Clone the repository:
```bash
git clone https://github.com/AsifSyedLive/cs_exchange_rate.git
```
Create and activate a virtual environment:
While creating the project in Pycharm or any other IDE, select to install venv.
There are other python interpreters as well and other ways to install venv as well
In this project venv was installed while creating project in Pycharm
```bash
source venv/bin/activate
# On Windows, within Project Directory execute  `venv\\Scripts\\activate`
```
Install the dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Common Configuration
The `config_common.json` file has settings shared across all modules like base currency and target currency, how many days from past data needs to be exchange rates needs to be fetched.
Example:
```json
{
  "defaults_exchange_rate": {
    "days": 30,
    "base_currency": "AUD",
    "target_currency": "NZD"
  }
}
```
### Module-specific Configuration
Each script has its own configuration file:

- config_exchange_rate_analyze.json: Configuration variables for the analysis script
- config_exchange_rate_fetcher.json: Configuration variables for the fetching script
- config_exchange_rate_preprocess.json: Configuration variables for the preprocessing script

Here is an example for config_exchange_rate_fetcher.json:
```json
{
  "api_url": "https://api.exchangeratesapi.io/v1",
  "end_point": "timeseries"
}
```
### .env File
The .env file contains environment variables used at PROJECT LEVEL, also SENSITIVE information.

**This file is not be included in version control as it contains sensitive information such as API keys**

Here is an example .env file:
```bash
PROJECT="cs_exchange_rate"
BASE_PATH="C:\\Users\\asifs\\${PROJECT}"
LOG_DIR="${BASE_PATH}\\log"
LOG_FILE="${LOG_DIR}\\exchange_rate"
API_KEY='xxxxxxxxxxxxxx'
```
## Usage
### Fetch Exchange Rates
To fetch exchange rates, run the exchange_rate_fetcher.py script
```bash
python exchange_rate/exchange_rate_fetcher.py
```
or it can be imported into another python script, later to call Classes/Functions from it.
```bash
from exchange_rate.exchange_rate_fetcher import *
```
This script retrieves exchange rate data from the specified API and returns json

### Preprocess Exchange Rates
To preprocess the fetched exchange rates i.e handle missing date entries and invalid rates (null), run the exchange_rate_preprocess.py script:

python exchange_rate/exchange_rate_preprocess.py
or it can be imported into another python script, later to call Classes/Functions from it.
```bash
from exchange_rate.exchange_rate_preprocess import *
```
This script ensures that there are no missing dates and interpolates any missing/invalid values. It returns a dictionary with dates and exchange rates.
Interpolation is average of nearby values (previous and next)
### Analyze Exchange Rates
To analyze the processed exchange rates, run the exchange_rate_analyze.py script:
```bash
python exchange_rate/exchange_rate_analyze.py
```
or it can be imported into another python script, later to call Classes/Functions from it.
```bash
from exchange_rate.exchange_rate_analyze import *
```
This script performs various analyses on the exchange rate data such as calculating statictics (mean, min, max), calculating moving averages.
It shows a visual report after execution.

![Alt text](https://github.com/AsifSyedLive/cs_exchange_rate/blob/master/docs/Results/results_exchange_rate_analyze_output.png)


### Main Script
The main.py script is the entry point to run the workflow. 
This script orchestrates fetching of exchange rates, preprocessing the data obtained from API, and analyzing the exchange rate data
```bash
python main.py
```

## Testing
Test files are located in the test directory
- **NOTE: These scripts show case how configuration files can be tapped and data can be mocked to verify results instead of changing the code or its configurations to test**
- **NOTE: There can be more test cases added**
- **NOTE: Test Cases can be made more robust so that it can be rerun for any date**
  
- test_exchange_rate_analyze.py
     -   test case 1: data retrieved correctly for configuration variable set to 4 days, AUD to NZD
     -   test case 2: whether code is flexible to fetch from different end point
     -   test case 3: whether code responds with error message when an invalid url is passed
- test_exchange_rate_fetcher.py
     -   test case 1: Check whether code fixes Missing date and interpolate corresponding value. This date is picked from middle of the list of dates.
     -   test case 2: Check whether code fixes Missing date and interpolate corresponding value. This date is picked from left end of the list of dates.
     -   test case 3: Check whether code fixes Missing date and interpolate corresponding value. This date is picked from right end of the list of dates.
- test_exchange_rate_preprocess.py
     -   test case 1: Validate whether analyze script is returning valid statistical results i.e. mean, min, max

## Utilities
### Config Loader
The utils/config_loader.py script provides utilities for loading configuration files. 
It provides centralized way of accessing the configuration. 
**We can have controls based on which script is fetching the configuration**

### Logger
The utils/logger.py script sets up the logging configuration. With this utility the loogs are written to a common file and can be configured for different log levels (DEBUG, INFO, ERROR, WARNINGS, CRITICAL, NOTSET).

## Limitations
- Data Quality: The accuracy of the analysis is dependent on the quality and completeness of the data fetched from the API. If the API provides incomplete or inaccurate data, it may affect the results.
- Performance: For large datasets i.e. if days more than 30 is configured, the performance may degrade.
- Error Handling and Logging: While basic error handling is implemented, more robust mechanisms can be added to handle unexpected scenarios.

## Future Enhancements
- The project incorporates code to manage logging of errors, warnings, and debug messages. While the logging mechanism is built and showcased, additional implementation within each component is still to be done for every scenario. 

- Module level configuation files allow overriding project level or across module configurations. The code can be updated to allow specific variables that can override all other configurations. 

- Currently, the code handles exchange rates for one currency to another. It can be updated to support one currency to multiple exchange rates.

- Python test scripts are provided to demonstrate test automation, but they need further development to be more robust.

- The analysis can be enhanced by incorporating a machine learning model, such as linear regression. Including additional variables like socio-economic factors, political conditions, and the CPI index could yield better results.
  
## License
This project is available for educational and reference purposes. Feel free to review and examine the code to gain a better understanding of its functionality. If you intend to use any part of this project in your own work, please reach out to me for permission.

For permission requests, please reach out to me at [asif.syed@live.com]

## Contributing
Thank you for considering contributing to this project! 

As the initial author, I have developed this code with the help of resources searched online. Your contributions are welcome to help improve and expand the project.

How to Contribute
Fork the Repository: Create a personal copy of the repository by clicking the "Fork" button on GitHub.
Clone the Repository: Clone your forked repository to your local machine.
```bash
git clone https://github.com/AsifSyedLive/cs_exchange_rate.git
```
Create a Branch: Create a new branch for your feature or bug fix.
```bash
git checkout -b feature-or-bugfix-name
```
Make Changes: Implement your changes and ensure your code follows the project's coding standards (PEP8 coding standards).
Commit and Push: Commit your changes to your branch and push them to your forked repository.
```bash
git commit -m "Description of your changes"
git push origin feature-or-bugfix-name
```
Open a Pull Request: Open a pull request from your branch to the main repository's main branch. Provide a clear and detailed description of your changes.

Be respectful and considerate in your communication.

## Contact
If you have any questions, suggestions, or would like to request permission to use this project, feel free to reach out to me:

- **Email**: asif.syed@live.com
