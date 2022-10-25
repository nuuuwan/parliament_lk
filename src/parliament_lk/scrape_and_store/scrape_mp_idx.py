import os
import string

from bs4 import BeautifulSoup
from utils import www

from parliament_lk._utils import log


def get_url(c):
    return os.path.join(
        'https://www.parliament.lk',
        'en',
        'members-of-parliament',
        'directory-of-members',
        f'?cletter={c}',
    )


def scrape_html(c):
    url = get_url(c)
    html = www.read(url, use_selenium=True)
    return html


def parse_li(li):
    name = li.get('id')
    a = li.find('a')
    url_num = (int)(a.get('href').split('/')[-1])
    return dict(
        name=name,
        url_num=url_num,
    )


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', {'id': 'listholder'})
    return list(map(parse_li, div.find_all('li')))


def scrape_all_indices():
    mp_idx_info_list = []
    for c in string.ascii_uppercase:
        html = scrape_html(c)
        mp_idx_info_list_for_letter = parse_html(html)
        n_members = len(mp_idx_info_list_for_letter)
        log.debug(f'Scraped {n_members} infos for {c}')
        mp_idx_info_list += mp_idx_info_list_for_letter

    # HACK!
    mp_idx_info_list.append(
        dict(
            name='Wijeyadasa Rajapakshe',
            url_num=1521,
        )
    )

    n_members = len(mp_idx_info_list)
    log.info(f'Scraped {n_members} infos in total')
    return mp_idx_info_list
