
import unittest
from unittest.mock import MagicMock

from bs4 import BeautifulSoup
from test_examples.mp import (TEST_HTML, TEST_HTML_CONTACT,
                              TEST_HTML_DATE_OF_BIRTH, TEST_HTML_DIV_CONTENT,
                              TEST_HTML_EMAIL, TEST_HTML_PARTY, TEST_URL,
                              TEST_URL_NUM)
from utils import www

from parliament_lk.scrape_and_store import scrape_mp


class TestCase(unittest.TestCase):
    def setUp(self):
        www.read = MagicMock(return_value=TEST_HTML)

    def test_get_url(self):
        self.assertEqual(
            TEST_URL,
            scrape_mp.get_url(TEST_URL_NUM)
        )

    def test_clean(self):
        for [s, expected_output] in [
            ['Colombo    ', 'Colombo'],
            [['Colombo    ', 'Kandy '], ['Colombo', 'Kandy']],
            ['Presidents House, Colombo 10', 'Presidents House, Colombo 10'],
            ['Colombo\n  Sri Lanka', 'Colombo Sri Lanka'],
        ]:
            self.assertEqual(expected_output, scrape_mp.clean(s))

    def test_clean_and_remove_empty(self):
        for [s, expected_output] in [
            [['Colombo    ', 'Kandy '], ['Colombo', 'Kandy']],
            [['Colombo    ', 'Kandy ', '  '], ['Colombo', 'Kandy']],
            [['Colombo    ', ''], ['Colombo']],
        ]:
            self.assertEqual(
                expected_output,
                scrape_mp.clean_and_remove_empty(s),
            )

    def test_scrape_html(self):
        self.assertEqual(
            [TEST_HTML, TEST_URL, TEST_URL_NUM],
            scrape_mp.scrape_html(TEST_URL_NUM),
        )

    def test_extract_name(self):
        div_content = BeautifulSoup(TEST_HTML_DIV_CONTENT, 'html.parser')
        self.assertEqual(
            'Albert Einstein',
            scrape_mp.extract_name(div_content),
        )

    def test_extract_image_url(self):
        div_content = BeautifulSoup(TEST_HTML_DIV_CONTENT, 'html.parser')
        self.assertEqual(
            'profile.png',
            scrape_mp.extract_image_url(div_content),
        )

    def test_extract_pic_kv(self):
        tr = BeautifulSoup(TEST_HTML_EMAIL, 'html.parser')
        self.assertEqual(
            (scrape_mp.IMG_SRC_EMAIL, 'albert@einstein.org'),
            scrape_mp.extract_pic_kv(tr),
        )

    def test_extract_table_kvs(self):
        table = BeautifulSoup(TEST_HTML_CONTACT, 'html.parser')
        self.assertEqual(
            {
                '0-/images/phone_ico.png': '0123456789',
                '0-/images/address.png': 'Princeton, NJ',
                '1-/images/phone_ico.png': '0149779419',
                '1-/images/address.png': '123 Home Street Princeton, NJ',
            },
            scrape_mp.extract_table_kvs(table),
        )

    def test_extract_two_line_kv(self):
        td = BeautifulSoup(TEST_HTML_PARTY, 'html.parser')
        self.assertEqual(
            ('Party', 'United National Party (UNP)'),
            scrape_mp.extract_two_line_kv(td),
        )

    def test_extract_one_line_kv(self):
        td = BeautifulSoup(TEST_HTML_DATE_OF_BIRTH, 'html.parser')
        self.assertEqual(
            ('Date of Birth', '1234-05-06'),
            scrape_mp.extract_one_line_kv(td),
        )

    def test_parse_html(self):
        self.assertEqual(
            dict(
                url_num=TEST_URL_NUM,
                name='Albert Einstein',
                image_url='profile.png',
                party='United National Party (UNP)',
                electoral_district='Colombo',

                date_of_birth='1234-05-06',
                civil_status='Married',
                religion='Catholic',
                profession='Physicist',

                phone='0123456789',
                address='Princeton, NJ',
                phone_sitting='0149779419',
                address_sitting='123 Home Street Princeton, NJ',
                email='albert@einstein.org',
                source_url='www.albert.com',
            ),
            scrape_mp.parse_html(TEST_HTML, 'www.albert.com', TEST_URL_NUM),
        )


if __name__ == '__main__':
    unittest.main()
