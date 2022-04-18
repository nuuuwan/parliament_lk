import os
import string

from bs4 import BeautifulSoup
from utils import www

from parliament_lk._utils import log


def get_url(c):
    return os.path.join(
        'https://www.parliament.lk',
        'en/members-of-parliament',
        'directory-of-members',
        f'?cletter={c}',
    )


def extract_list_div(c):
    html = www.read(get_url(c), use_selenium=True)
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('div', {'id': 'listholder'})


def parse_info(li):
    name = li.get('id')
    a = li.find('a')
    url_num = (int)(a.get('href').split('/')[-1])
    return dict(
        name=name,
        url_num=url_num,
    )


def scrape_mem_dir_for_letter(c):
    mem_dir_info_list = []
    div = extract_list_div(c)
    for li in div.find_all('li'):
        mem_dir_info_list.append(parse_info(li))

    n_mem_dir_info_list = len(mem_dir_info_list)
    log.debug(f'Scraped {n_mem_dir_info_list} members for {c}')
    return mem_dir_info_list


def scrape_mem_dir():
    mem_dir_info_list = []
    for c in string.ascii_uppercase:
        mem_dir_info_list += scrape_mem_dir_for_letter(c)
    return mem_dir_info_list
