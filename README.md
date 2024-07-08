# Exchange Rates API Integration for Historical Analysis

This project provides tools to fetch, preprocess, and analyze exchange rate data. These scripts are designed to address data challenges such as filling in missing dates and handling invalid values. Additionally, the project features robust logging and flexible configuration options to ensure seamless integration and ease of use.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Setup](#setup)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Configuration](#configuration)
   - [Common Configuration](#common-configuration)
   - [Script-specific Configuration](#script-specific-configuration)
   - [.env File](#env-file)
4. [Usage](#usage)
   - [Fetch Exchange Rates](#fetch-exchange-rates)
   - [Preprocess Exchange Rates](#preprocess-exchange-rates)
   - [Analyze Exchange Rates](#analyze-exchange-rates)
   - [Main Script](#main-script)
5. [Testing](#testing)
6. [Logging](#logging)
7. [Utilities](#utilities)
   - [Config Loader](#config-loader)
   - [Logger](#logger)
8. [Limitations](#limitations)
9. [Future Enhancements](#future-enhancements)
10. [License](#license)
11. [Contributing](#contributing)
12. [Contact](#contact)

## Project Structure
```bash
cs_exchange_rate-master/
├── config/                         
│   ├── config_common.json
│   ├── config_exchange_rate_analyze.json
│   ├── config_exchange_rate_fetcher.json
│   └── config_exchange_rate_preprocess.json
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
```json{
  "defaults_exchange_rate": {
    "days": 30,
    "base_currency": "AUD",
    "target_currency": "NZD"
  }
}
```
