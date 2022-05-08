import os
import unittest
from unittest.mock import MagicMock

from utils import filex, www

from parliament_lk.scrape_and_store import scrape_mp

TEST_URL_NUMS = []


class TestCase(unittest.TestCase):
    maxDiff = None

    def test(self):
        for url_num, expected_info in [
            [1244, dict(
                url_num=1244,
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
                source_url='https://www.parliament.lk'
                + '/en/members-of-parliament'
                + '/directory-of-members/viewMember/1244',

                academic_qualifications='LLB.;',
                professional_qualifications='Attorney-at-Law; Advocate',

                attendance_9th_present=61,
                attendance_9th_absent=19,
                attendance_8th_present=208,
                attendance_8th_absent=44,

            )],
            [1482, dict(
                url_num=1482,
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
                source_url='https://www.parliament.lk'
                + '/en/members-of-parliament'
                + '/directory-of-members/viewMember/1482',

                academic_qualifications='Attorney-at-Law;'
                + ' G.C.E. (A/L); G.C.E. (O/L)',
                professional_qualifications='Attorney At Law',

                attendance_9th_present=97,
                attendance_9th_absent=62,
                attendance_8th_present=144,
                attendance_8th_absent=108,
            )],
            [3179, dict(
                url_num=3179,
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
                source_url='https://www.parliament.lk'
                + '/en/members-of-parliament'
                + '/directory-of-members/viewMember/3179',

                academic_qualifications='LLB, Attorney -at- Law',
                professional_qualifications='Attorney at Law',

                attendance_9th_present=106,
                attendance_9th_absent=53,
                attendance_8th_present=96,
                attendance_8th_absent=156,
            )],
            [3306, dict(
                url_num=3306,
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
                source_url='https://www.parliament.lk'
                + '/en/members-of-parliament'
                + '/directory-of-members/viewMember/3306',

                academic_qualifications='Open University Degree',
                professional_qualifications='2008 To 2017 North Central'
                + ' province Council Member',

                attendance_9th_present=147,
                attendance_9th_absent=12,
                attendance_8th_present=None,
                attendance_8th_absent=None,
            )],
            [3438, dict(
                url_num=3438,
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
                source_url='https://www.parliament.lk'
                + '/en/members-of-parliament'
                + '/directory-of-members/viewMember/3438',

                academic_qualifications=None,
                professional_qualifications=None,

                attendance_9th_present=158,
                attendance_9th_absent=1,
                attendance_8th_present=None,
                attendance_8th_absent=None,
            )],
            [3449, dict(
                url_num=3449,
                name='Hon. (Dr.) (Ms.) Harini Amarasuriya, M.P.',
                image_url='https://www.parliament.lk'
                + '/uploads/images/members/profile_images/thumbs/3449.jpg',
                party='Jathika Jana balawegaya (JJB)',
                electoral_district='National List',

                date_of_birth='06-03-1970',
                civil_status='Single',
                religion='Buddhism',
                profession='University Lecturer',

                phone=None,
                address='No. 33B" Janatha Mawatha,Mirihana,Kotte.',
                phone_sitting='0112829722',
                address_sitting='No. 464/20, Pannipitiya Road,'
                + 'Pelawatte,Battaramulla.',
                email='harini_a@parliament.lk',
                source_url='https://www.parliament.lk'
                + '/en/members-of-parliament'
                + '/directory-of-members/viewMember/3449',

                academic_qualifications='BA (Hons) Sociology;'
                + ' MA App. Anthropology & Development Studies;'
                + ' PHD, Social Anthropology',
                professional_qualifications='University Lecturer',

                attendance_9th_present=124,
                attendance_9th_absent=35,
                attendance_8th_present=None,
                attendance_8th_absent=None,
            )],
        ]:
            html_file = os.path.join(
                'tests/parliament_lk/scrape_and_store',
                'test_examples/real_mps',
                f'{url_num}.html',
            )
            html = filex.read(html_file)
            www.read = MagicMock(return_value=html)

            actual_info = scrape_mp.scrape(url_num)

            self.assertEqual(
                expected_info,
                actual_info,
            )


if __name__ == '__main__':
    unittest.main()
