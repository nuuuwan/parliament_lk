import math
import os

from utils import timex, www

URL_RAW_DATA_BASE = os.path.join(
    'https://raw.githubusercontent.com/nuuuwan/parliament_lk/data'
)
URL_MP_IDX = os.path.join(URL_RAW_DATA_BASE, 'mp_list.tsv')
FORMAT_DATE_OF_BIRTH = '%d-%m-%Y'

ID_TO_DOB = {
    '3364': '01-10-1971',
    '1575': '27-04-1951',
    '3451': '07-10-1974',
}


class MP:
    def __init__(self, d):
        self.url_num = d['url_num']
        self.name = d['name']
        self.image_url = d['image_url']

        self.party = d['party']
        self.electoral_district = d['electoral_district']

        self.date_of_birth = d['date_of_birth']
        self.civil_status = d['civil_status']
        self.religion = d['religion']
        self.profession = d['profession']

        self.phone = d['phone']
        self.address = d['address']
        self.phone_sitting = d['phone_sitting']
        self.address_sitting = d['address_sitting']
        self.email = d['email']

        self.vote20A = d['vote_20th_amendment']

        self.source_url = d['source_url']

    @property
    def name_clean(self):
        return self.name.replace('Hon. ', '').replace(', M.P.', '')

    @property
    def party_short(self):
        return self.party.split('(')[-1][:-1]

    @property
    def date_of_birth_ut(self):
        date_of_birth = ID_TO_DOB.get(self.url_num, self.date_of_birth)
        try:
            return timex.parse_time(date_of_birth, FORMAT_DATE_OF_BIRTH)
        except ValueError:
            raise Exception('No date_of_birth for ' + str(self))

    @property
    def age(self):
        ut_now = timex.get_unixtime()
        return math.floor(
            (ut_now - self.date_of_birth_ut) / timex.SECONDS_IN.YEAR
        )

    def __str__(self):
        return f'[MP-{self.url_num}] {self.name_clean} ({self.party_short})'

    @staticmethod
    def loadMPs():
        mp_info_list = www.read_tsv(URL_MP_IDX)
        return list(
            map(
                lambda mp_info: MP(mp_info),
                mp_info_list,
            )
        )
