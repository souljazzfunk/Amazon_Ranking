from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import io
from time import sleep
from PIL import Image

def fetch_data_with_requests(url):
    # Helper function to handle errors
    def exit_with_error(message):
        print(message)
        exit(1)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.3'}
    session = requests.Session()

    for retry_count in range(5):  # Maximum retries: 5
        response = session.get(url, headers=headers)
        status_code = response.status_code

        if status_code == 200:
            break
        elif status_code == 503:
            print(f"Failed to fetch the webpage. (Code: {status_code}) Attempt {retry_count + 1} of 5")
            sleep(60)
        else:
            return exit_with_error(f"Failed to fetch the webpage with an unhandled status code: {status_code}. Exiting.")
    else:
        return exit_with_error(f"Maximum retries reached for status code {status_code}. Exiting.")

    soup = BeautifulSoup(response.text, 'html.parser')
    ul_elems = soup.select('ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list')
    
    if not ul_elems or len(ul_elems) < 2:
        response.encoding = 'shift_jis'
        with open('error_log.html', 'w', encoding='shift_jis') as file:
            file.write(response.text)
        return exit_with_error(f"Could not find ranking data.\n{ul_elems}")
    
    ul_elem = ul_elems[1]

    ranking_data = {'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ranks = ul_elem.select('li > span > ul > li > span')
    screenshot_needed = False
    screenshot_links = []

    for rank in ranks:
        text = rank.get_text()
        num_rank, category = text.split('位', 1)
        num_rank = int(num_rank.replace(',','').strip(' -'))
        category = category.strip().split('(')[0]
        ranking_data[category] = num_rank

        if num_rank <= 9:
            screenshot_needed = True
            screenshot_links.append(rank.find('a', href=True)['href'])
    
    return screenshot_needed, screenshot_links, ranking_data

def save_screenshot(element, timestamp):
    img_binary = element.screenshot_as_png
    img = Image.open(io.BytesIO(img_binary))
    img.save(f'amazon_ranking_{timestamp.strftime("%Y-%m-%d_%H-%M-%S")}.png')

def take_screenshot_with_selenium(url, screenshot_links):
    chrome_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=2200,1600')
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=chrome_service, options=options)

    driver.get(url)
    sleep(2)
    div_elm = driver.find_element(By.CSS_SELECTOR, '#detailBulletsWrapper_feature_div')
    driver.execute_script("arguments[0].scrollIntoView();", div_elm)
    save_screenshot(div_elm, datetime.now())
    
    for link in screenshot_links:
        full_link = f'https://www.amazon.co.jp{link}'
        driver.get(full_link)
        sleep(2)

        body = driver.find_element(By.TAG_NAME, 'body')
        save_screenshot(body, datetime.now())
    
        div_elm = driver.find_element(By.CSS_SELECTOR, 'div#B0C6D2ZF8D')
        grandparent_elm = div_elm.find_element(By.XPATH, '../../..')
        driver.execute_script("arguments[0].scrollIntoView();", grandparent_elm)
        save_screenshot(grandparent_elm, datetime.now())
    
    driver.quit()


def main():
    url = 'https://www.amazon.co.jp/dp/B0C6D2ZF8D'
    screenshot_needed, screenshot_links, ranking_data = fetch_data_with_requests(url)

    if ranking_data:
        file_exists = False
        try:
            with open('amazon_ranking_data.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                if next(reader, None):
                    file_exists = True
        except FileNotFoundError:
            pass

        with open('amazon_ranking_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(ranking_data.keys()))
            if not file_exists:
                writer.writeheader()
            writer.writerow(ranking_data)

    if screenshot_needed:
        take_screenshot_with_selenium(url, screenshot_links)


if __name__ == '__main__':
    main()
