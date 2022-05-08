
from gig import ents

from parliament_lk._utils import log

ED_INDEX = ents.get_entity_index('ed')
PROVINCE_INDEX = ents.get_entity_index('province')


def search_ed(electoral_district):
    electoral_district = {
        'Nuwara - Eliya': 'Nuwara-Eliya',
        'Mahanuwara': 'Kandy',
        'Monaragala': 'Moneragala',
    }.get(electoral_district, electoral_district)

    for ed in ED_INDEX.values():
        if ed['name'] == electoral_district:
            return ed

    log.error('Can not find ed for: ' + electoral_district)
    return None


def parse_ed_info(electoral_district, name_cleaned):
    if electoral_district == 'National List' or name_cleaned in [
            'Ranil Wickremesinghe']:
        return 'LK', 'National List', 'LK', 'National List'

    matched_ed = search_ed(electoral_district)
    province = PROVINCE_INDEX[matched_ed['province_id']]
    return [
        matched_ed['ed_id'],
        matched_ed['name'],
        province['province_id'],
        province['name'],
    ]
