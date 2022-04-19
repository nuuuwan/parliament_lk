
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
                image_url='https://www.parliament.lk'
                + '/uploads/images/members/profile_images/thumbs/1244.jpg',
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
            [1482, dict(
                name='Hon. (Mrs.) Thalatha Athukorala, M.P.',
                image_url='https://www.parliament.lk'
                + '/uploads/images/members/profile_images/thumbs/1482.jpg',
                party='Samagi Jana Balawegaya (SJB)',
                electoral_district='Ratnapura',

                date_of_birth='30-05-1963',
                civil_status='Married',
                religion='Buddhism',
                profession='Attorney-at-Law',

                phone='0452274287',
                address='No. 231/1,Stanley Tilekeratne Mawatha,Nugegoda.',
                phone_sitting='0452274287',
                address_sitting=None,
                email='atukorale_t@parliament.lk',
            )],
            [3179, dict(
                name='Hon. Namal Rajapaksa, M.P.',
                image_url='https://www.parliament.lk'
                + '/uploads/images/members/profile_images/thumbs/3179.jpg',
                party='Sri Lanka Podujana Peramuna (SLPP)',
                electoral_district='Hambantota',

                date_of_birth='10-04-1986',
                civil_status='Married',
                religion='Buddhism',
                profession=None,

                phone=None,
                address='Carlton House,Mahawela Road,Tangalle.',
                phone_sitting='0472240332',
                address_sitting='260/12,Torrington avenue,Colombo 05.',
                email='rajapaksa_n@parliament.lk',
            )],
            [3306, dict(
                name='Hon. Amarakeerthi Athukorala, M.P.',
                image_url='https://www.parliament.lk'
                + '/uploads/images/members/profile_images/thumbs/3306.jpg',
                party='Sri Lanka Podujana Peramuna (SLPP)',
                electoral_district='Polonnaruwa',

                date_of_birth='23-12-1964',
                civil_status='Married',
                religion='Buddhism',
                profession=None,

                phone='0773929655',
                address='D S Senanayake Road,New Town,Polonnaruwa.',
                phone_sitting='0272223282',
                address_sitting=None,
                email='amarakeerthi_a@parliament.lk',
            )],
            [3438, dict(
                name='Hon. Yadamini Gunawardena, M.P.',
                image_url='https://www.parliament.lk'
                + '/uploads/images/members/profile_images/thumbs/3438.jpg',
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
            )],
            [3449, dict(
                name='Hon. (Dr.) (Ms.) Harini Amarasuriya, M.P.',
                image_url='https://www.parliament.lk'
                + '/uploads/images/members/profile_images/thumbs/3449.jpg',
                party='Jathika Jana balawegaya (JJB)',
                electoral_district='National List',

                date_of_birth='06-03-1970',
                civil_status='Single',
                religion='Buddhism',
                profession=None,

                phone=None,
                address='No. 33B" Janatha Mawatha,Mirihana,Kotte.',
                phone_sitting='0112829722',
                address_sitting='No. 464/20, Pannipitiya Road,'
                + 'Pelawatte,Battaramulla.',
                email='harini_a@parliament.lk',
            )],
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
