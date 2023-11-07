# Sportsbook Scraper 

A Python-based web spider using Scrapy to extract and store football 
match betting data, including team names, match date and time, odds, 
and more from the Caesars Sportsbook website

## Installation

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: Ensure you have Python installed. Install the required dependencies using the following commands:

    ```shell
    git clone https://github.com/arsenmakovei/sportsbook-scraper.git
    cd sportsbook_scraper
    python -m venv venv
    Windows: venv\Scripts\activate
    Linux, Unix: source venv/bin/activate
    pip install -r requirements.txt
    ```
   
## Usage

Running the Scraper

- To run the scraper manually, execute the following command:

   ```shell
   scrapy crawl football -O football.csv 
   ```
- You can use other file name or type, such as .json, .jl, .csv, etc.
- Use flag `-s LOG_LEVEL=INFO` to see logs in terminal for some log level. 
Also, you can use other log levels such as DEBUG, INFO, WARNING, ERROR, CRITICAL.
- Use flag `--logfile football.log` to save logs in file, or use other file name.
- Also you can see test scrapped data and logs in files football.csv and football.log