import os
import re

from bs4 import BeautifulSoup
from utils import www

from parliament_lk._utils import log

IMG_SRC_EMAIL = '/images/email_ico.png'
IMG_SRC_PHONE = '/images/phone_ico.png'
IMG_SRC_ADDRESS = '/images/address.png'


def clean(s):
    if isinstance(s, str):
        s = s.replace('\n', ' ')
        s = re.sub(r'\s+', ' ', s)
        s = s.strip()
        return s

    if isinstance(s, list):
        return list(map(clean, s))

    return clean(s.text)


def clean_and_remove_empty(s_list):
    return list(filter(lambda x: x, list(map(clean, s_list))))


def get_url(url_num):
    return os.path.join(
        'https://www.parliament.lk',
        'en',
        'members-of-parliament',
        'directory-of-members',
        'viewMember',
        f'{url_num}'
    )


def scrape_html(url_num):
    url = get_url(url_num)
    return www.read(url, use_selenium=True)


def extract_name(div_content):
    return div_content.find('h2').text


def extract_pic_kv(tr):
    tds = tr.find_all('td')
    if len(tds) != 2:
        return None
    img = tds[0].find('img')
    if not img:
        return None
    return (img.get('src'), clean(tds[1].text))


def extract_table_kvs(table):
    tables = table.find_all('table')
    if len(tables) != 2:
        return None
    d = {}
    for i, table in enumerate(tables):
        for tr1 in table.find_all('tr'):
            kv = extract_pic_kv(tr1)
            if kv:
                d[f'{i}-' + kv[0]] = kv[1]
    return d


def extract_two_line_kv(td):
    div = td.find('div')
    if not div:
        return None
    tokens = clean_and_remove_empty(td.find_all(text=True))
    if len(tokens) != 2:
        return None
    return (tokens[0], tokens[1])


def extract_one_line_kv(td):
    text = td.text.strip()
    tokens = clean_and_remove_empty(text.split(':'))
    if len(tokens) != 2:
        return None
    return (tokens[0], tokens[1])


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    div_content = soup.find('div', class_='components-wrapper')

    name = extract_name(div_content)

    d = {}
    for table in div_content.find_all('table'):
        kvs = extract_table_kvs(table)
        if kvs:
            d |= kvs
            continue

        for td in table.find_all('td'):
            kv = extract_two_line_kv(td)
            if kv:
                d |= dict([kv])
                continue

        for tr in div_content.find_all('tr'):
            kv = extract_pic_kv(tr)
            if kv:
                d |= dict([kv])
                continue

            for td in tr.find_all('td'):
                kv = extract_two_line_kv(td)
                if kv:
                    d |= dict([kv])
                    continue

                kv = extract_one_line_kv(td)
                if kv:
                    d |= dict([kv])

    return dict(
        name=name,
        party=d.get('Party'),
        electoral_district=d.get('Electoral District / National List'),
        date_of_birth=d.get('Date of Birth'),
        civil_status=d.get('Civil Status'),
        religion=d.get('Religion'),
        profession=d.get('Profession / Occupation'),

        phone=d.get('0-' + IMG_SRC_PHONE),
        address=d.get('0-' + IMG_SRC_ADDRESS),
        phone_sitting=d.get('1-' + IMG_SRC_PHONE),
        address_sitting=d.get('1-' + IMG_SRC_ADDRESS),
        email=d.get(IMG_SRC_EMAIL),
    )


def scrape(url_num):
    url = get_url(url_num)
    html = www.read(url, use_selenium=True)
    member_info = parse_html(html)
    name = member_info['name']
    log.debug(f'Scraped member_info for {name} ({url_num})')
    return member_info
