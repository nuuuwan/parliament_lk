import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import filex

from parliament_lk.scrape_and_store import scrape_mp

TIME_WAIT = 10
DIR_EXAMPLES = 'tests/parliament_lk/scrape_and_store/test_examples/real_mps'
REAL_MP_URL_NUM_LIST = [
    1244,
    1482,
    3179,
    3306,
    3438,
    3449,
]


def download(driver, url_num):
    url = scrape_mp.get_url(url_num)
    driver.get(url)
    time.sleep(TIME_WAIT)
    html = driver.page_source

    html_file = os.path.join(
        DIR_EXAMPLES,
        f'{url_num}.html',
    )
    filex.write(html_file, html)
    n_html_k = len(html) / 1000
    print(f'Wrote {n_html_k}KB to {html_file}')
    os.system(f'open -a firefox "{url}"')


def main():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    for url_num in REAL_MP_URL_NUM_LIST:
        download(driver, url_num)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
