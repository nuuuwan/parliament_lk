import os
from bs4 import BeautifulSoup
from utils import www

def get_url(url_num):
    return os.path.join(
        'https://www.parliament.lk',
        'en',
        'members-of-parliament',
        'directory-of-members',
        'viewMember',
        f'{url_num}'
    )

def scrape_mem(url_num):
    url = get_url(url_num)
    html = www.read(url, use_selenium=True)
    soup = BeautifulSoup(html, 'html.parser')

    div_content = soup.find('div', class_='components-wrapper')
    h2_title = div_content.find('h2')
    name = h2_title.text

    for td in div_content.find_all('td'):
        text = td.text
        if '\n' in text:
            tokens = text.split('\n')
        elif ':' in text:
            tokens = text.split(':')
        print(tokens)    

    return dict(
        name=name,
    )
