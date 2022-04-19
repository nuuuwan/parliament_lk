
import unittest
from unittest.mock import MagicMock

from utils import filex, www

from parliament_lk import scrape_mem

TEST_URL_NUMS = []


class TestCase(unittest.TestCase):
    def test(self):

        for url_num, expected_info in [
            [1244, dict(
                name='Hon. Ranil Wickremesinghe, M.P.',
                party='United National Party (UNP)',
                electoral_district='Colombo',

                date_of_birth='24-03-1949',
                civil_status='Married',
                religion='Buddhism',
                profession='Attorney-at-Law',

                phone='2573974',
                address='No. 117, 5th Lane,Colombo 03.',
                phone_sitting='0112573308',
                address_sitting=None,
                email='wickremesinghe_r@parliament.lk',
            )],
            [3438, dict(
                name='Hon. Yadamini Gunawardena, M.P.',
                party='Sri Lanka Podujana Peramuna (SLPP)',
                electoral_district='National List',

                date_of_birth='04-01-1981',
                civil_status=None,
                religion=None,
                profession=None,

                phone='0714311163',
                address='Boralugoda,Kosgama.',
                phone_sitting='0714311163',
                address_sitting='No. 84,Kirulapona Avenue,Colombo 05.',
                email='yadamini_g@parliament.lk',
            )]
        ]:
            html_file = f'tests/test_examples/mem_real/{url_num}.html'
            html = filex.read(html_file)
            www.read = MagicMock(return_value=html)

            actual_info = scrape_mem.scrape(url_num)
            print(actual_info)

            self.assertEqual(
                expected_info,
                actual_info,
            )


if __name__ == '__main__':
    unittest.main()
