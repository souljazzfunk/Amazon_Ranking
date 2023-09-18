# Amazon Product Ranking Scraper

This project is a Python script that scrapes Amazon product ranking data. It is capable of retrieving ranking data for specific categories and taking screenshots.

## Features

- Fetches Amazon product ranking data and stores them in a CSV file.
- Takes screenshots for products that are in the top 10 ranks (or within the range you like) in their categories.
- Resilient to network failures with retry mechanisms.

## Requirements

- Python 3.x
- Selenium
- Requests
- BeautifulSoup
- PIL (Pillow)
- WebDriver Manager

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/souljazzfunk/Amazon_Ranking.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Amazon_Ranking
    ```

## Usage

1. Run the script:
    ```bash
    python amazon_ranking.py
    ```

The script will create a CSV file named `amazon_ranking_data.csv` and save screenshots in the current directory.

## License

Distributed under the MIT License. 
