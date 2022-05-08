import os

from utils import jsonx, timex, tsv

from parliament_lk._utils import log
from parliament_lk.scrape_and_store import store_mps
from parliament_lk.scrape_and_store.expand_mps_helpers.academics import \
    parse_academic_highest_level
from parliament_lk.scrape_and_store.expand_mps_helpers.corruption import \
    parse_asset_declaration_years
from parliament_lk.scrape_and_store.expand_mps_helpers.name import (
    parse_first_and_last_names, parse_gender, parse_name_cleaned)
from parliament_lk.scrape_and_store.expand_mps_helpers.regions import \
    parse_ed_info
from parliament_lk.scrape_and_store.expand_mps_helpers.validate import validate
from parliament_lk.scrape_and_store.expand_mps_helpers.voting import \
    parse_vote_20th_amendment

EXPANDED_MP_LIST_JSON_FILE = os.path.join(
    store_mps.DIR_GIT_DATA, 'expanded_mp_list.json',
)
EXPANDED_MP_LIST_TSV_FILE = os.path.join(
    store_mps.DIR_GIT_DATA, 'expanded_mp_list.tsv',
)


def git_upload(git):
    time_id = timex.get_time_id()
    message = f'[expand_mps] {time_id}'
    git.stage_commit_and_push(message)


def parse_party_short(party):
    return party.split('(')[1].split(')')[0]


def parse_date_of_birth(date_of_birth, url_num):
    if not date_of_birth:
        date_of_birth = {
            1575: "27-04-1951",  # Basil Rohana Rajapaksa
            3451: "01-10-1971",  # Jagath Kumara Sumithraarachchi
            3364: "07-10-1974",  # Lalith Varna Kumara
        }.get(url_num)

    if not date_of_birth:
        log.error(url_num)

    date_of_birth_ut = timex.parse_time(date_of_birth, '%d-%m-%Y')
    date_of_birth_norm = timex.format_time(date_of_birth_ut, '%Y-%m-%d')
    return date_of_birth, date_of_birth_ut, date_of_birth_norm


def parse_religion_cleaned(religion):
    return {
        'Buddhism': 'Buddhism',
        'Islam': 'Islam',
        'Hindu': 'Hinduism',
        'Roman Catholicism': 'Christianity (All)',
        'Christianity': 'Christianity (All)',

    }.get(religion, 'Other or Unknown')


def parse_phone_norm(phone):
    if not phone:
        return None

    if len(phone) == 9:
        phone = '0' + phone
    if len(phone) == 7:
        phone = '011' + phone

    if len(phone) != 10:
        log.error(phone)

    return '-'.join([
        phone[:3],
        phone[3:6],
        phone[6:10],
    ])


def parse_civil_status_cleaned(civil_status):
    if not civil_status or civil_status in ['None', 'Unknown', 'null']:
        return 'Unknown'
    return civil_status


def expand_single_mp(mp):
    name_cleaned = parse_name_cleaned(mp['name'])
    gender = parse_gender(mp['name'])
    first_names, last_name = parse_first_and_last_names(name_cleaned)
    party_short = parse_party_short(mp['party'])

    date_of_birth, date_of_birth_ut, date_of_birth_norm = parse_date_of_birth(
        mp['date_of_birth'], mp['url_num'])

    ed_id, ed_name, province_id, province_name = parse_ed_info(
        mp['electoral_district'],
        name_cleaned,
    )

    civil_status_cleaned = parse_civil_status_cleaned(mp['civil_status'])

    religion_cleaned = parse_religion_cleaned(mp['religion'])

    phone_norm = parse_phone_norm(mp['phone'])
    phone_sitting_norm = parse_phone_norm(mp['phone_sitting'])

    academic_highest_level = parse_academic_highest_level(
        mp['academic_qualifications'],
        mp['professional_qualifications'],
    )

    if (int)(academic_highest_level[0]) < 6 \
        and mp['profession'] in [
            'Attorney-at-Law',
            'Accountant',
    ]:
        academic_highest_level = '6 Bachelors'

    vote_20th_amendment = parse_vote_20th_amendment(
        party_short,
        name_cleaned,
    )

    asset_declaration_years = parse_asset_declaration_years(name_cleaned)

    return dict(
        url_num=mp['url_num'],
        id=mp['url_num'],

        name=mp['name'],
        name_cleaned=name_cleaned,
        first_names=first_names,
        last_name=last_name,

        gender=gender,

        image_url=mp['image_url'],

        party=mp['party'],
        party_short=party_short,

        electoral_district=mp['electoral_district'],
        ed_id=ed_id,
        ed_name=ed_name,
        province_id=province_id,
        province_name=province_name,

        date_of_birth=date_of_birth,
        date_of_birth_ut=date_of_birth_ut,
        date_of_birth_norm=date_of_birth_norm,

        civil_status=mp['civil_status'],
        civil_status_cleaned=civil_status_cleaned,

        religion=mp['religion'],
        religion_cleaned=religion_cleaned,
        profession=mp['profession'],

        phone=mp['phone'],
        phone_norm=phone_norm,

        address=mp['address'],

        phone_sitting=mp['phone_sitting'],
        phone_sitting_norm=phone_sitting_norm,

        address_sitting=mp['address_sitting'],

        email=mp['email'],
        source_url=mp['source_url'],

        academic_qualifications=mp['academic_qualifications'],
        academic_highest_level=academic_highest_level,
        professional_qualifications=mp['professional_qualifications'],

        vote_20th_amendment=vote_20th_amendment,
        asset_declaration_years=asset_declaration_years,
    )


def expand_mps(prod_mode):
    if prod_mode:
        git = store_mps.git_download()
    mp_list = jsonx.read(store_mps.MP_LIST_JSON_FILE)
    expanded_mp_list = list(map(expand_single_mp, mp_list))

    if not prod_mode:
        validate(expanded_mp_list)

    jsonx.write(EXPANDED_MP_LIST_JSON_FILE, expanded_mp_list)
    log.info(f'Wrote {EXPANDED_MP_LIST_JSON_FILE}')

    tsv.write(EXPANDED_MP_LIST_TSV_FILE, expanded_mp_list)
    log.info(f'Wrote {EXPANDED_MP_LIST_TSV_FILE}')

    if prod_mode:
        git_upload(git)
        os.system('open "https://github.com/nuuuwan/parliament_lk/tree/data"')
