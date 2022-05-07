import os
import re

from gig import ents
from utils import jsonx, timex

from parliament_lk._utils import log
from parliament_lk.scrape_and_store import store_mps

EXPANDED_MP_LIST_JSON_FILE = os.path.join(
    store_mps.DIR_GIT_DATA, 'expanded_mp_list.json')

# {
#   "url_num": 3266,
#   "name": "Hon. A. Aravindh Kumar, M.P.",
#   "image_url": "https://www.parliament.lk/uploads
#   /images/members/profile_images/thumbs/3266.jpg",
#   "party": "Samagi Jana Balawegaya (SJB)",
#   "electoral_district": "Badulla",
#   "date_of_birth": "17-11-1954",
#   "civil_status": "Married",
#   "religion": "Hindu",
#   "profession": null,
#   "phone": "0777727472",
#   "address": "NO.19,Badulupitiya Road,Badulla.",
#   "phone_sitting": "0552231526",
#   "address_sitting": "NO.271/19, Resta Garden,
#   Muditha Mawatha, Kerawalapitiya, Hendala,Wattala.",
#   "email": "aravindh_k@parliament.lk",
#   "source_url": "https://www.parliament.lk/en/
#   members-of-parliament/directory-of-members/viewMember/3266",
#   "academic_qualifications": "G.C.E Advanced Level",
#   "professional_qualifications": "1. 20 Years
#   experience as an Executive in the Tea Plantation Sector.
#   2. 10 years experience as a Private Secretary to a
#   Cabinet Minister 3. 10 years as a Member of
#   Uva Provincial Council. 4. 4 1/2 years as a Member of Parliament."
# },


ED_INDEX = ents.get_entity_index('ed')


def git_upload(git):
    time_id = timex.get_time_id()
    message = f'[expand_mps] {time_id}'
    git.stage_commit_and_push(message)


def parse_name_cleaned(name):
    for k in [
        "Hon.",
        ", M.P.",
        "(Dr.)",
        "(Mrs.)",
        "(Major)",
        "Field Marshal",
        "(Ms.)",
        ", PC",
        "Thero",
        "(Ven.) ",
        "(Prof.)",
    ]:
        name = name.replace(k, ' ')
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def parse_gender(name):
    for k in ['Mrs.', 'Miss', 'Ms.']:
        if k in name:
            return 'Female'
    return 'Male'


def parse_first_and_last_names(name_cleaned):
    names = name_cleaned.split(' ')
    n_last_name_words = 1
    if names[-2].lower() in ['ali', 'de', 'bakeer']:
        n_last_name_words = 2

    return ' '.join(names[:-n_last_name_words]
                    ), ' '.join(names[-n_last_name_words:]).title()


def parse_party_short(party):
    return party.split('(')[1].split(')')[0]


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


def parse_ed_info(electoral_district):
    if electoral_district == 'National List':
        return 'LK', 'National List'

    matched_ed = search_ed(electoral_district)
    return matched_ed['ed_id'], matched_ed['name']


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


def parse_academic_highest_level(academic_qualifications):
    if not academic_qualifications:
        return '0 Unknown'

    LEVEL_TO_KEYWORDS = {
        '8 Doctorate': [
            'Doctor of Public Service',
            'PhD',
            'Ph.D',
            'Doctor of Philosophy',
            'M.D.',
            'Doctarate in Public Administration',
        ],
        '7 Masters': [
            'Msc',
            'MA ',
            'Mphil ',
            'M.Ed',
            'MBA',
            'M.Sc',
            'MSc',
            'M.Com.',
            'M.B.A',
            'LLM',
        ],
        '6 Bachelors': [
            'Postgraduate Degree In Business Management',
            'BSc',
            'MBBS',
            'M.B.B.S.',
            'B.A',
            'Business Management Degree',
            'BSc.',
            'B.Eng',
            'B.com',
            'B.A. ',
            'B.Com.',
            'B. Sc.',
            'BA',
            'B.B.A ',
            'B. Com',
            'B.Sc',
            'LLB',
            'Bachelor',
            'L.L.B.',
            'Attorney',
            'B.Ed',
            'LL. B',
            'Open University Degree',
            'B.B.A',
            'L.LB',
            'Sri Lanka Law College',
            'Electrical and Electronics Engineering',
        ],
        '5 Short-Tertiary': [],
        '4 Post-Secondary': ['Diploma', 'Dip.', 'HCIMA', 'Dip in'],
        '3 Upper Secondary (A. Levels)': [
            'G.C.E Advanced Level',
            'A/L',
            'Advanced level',
            'GCE Advanced Level',
            'Advance level',
            'advanced Level',
            'G.C.E. (Advanced Level)',
        ],
        '2 Lower Secondary (O. Levels)': [
            'O/L',
            'O /L',
            'upto Advanced Level',
            'Secondary Education',
            'Upto Advanced Level',
        ],
        '1 Primary': [''],
    }

    for level, keywords in LEVEL_TO_KEYWORDS.items():
        for k in keywords:
            if k and k in academic_qualifications:
                return level

    return '1 Primary'


def expand_single_mp(mp):
    name_cleaned = parse_name_cleaned(mp['name'])
    gender = parse_gender(mp['name'])
    first_names, last_name = parse_first_and_last_names(name_cleaned)
    party_short = parse_party_short(mp['party'])

    date_of_birth, date_of_birth_ut, date_of_birth_norm = parse_date_of_birth(
        mp['date_of_birth'], mp['url_num'])

    ed_id, ed_name = parse_ed_info(mp['electoral_district'])

    religion_cleaned = parse_religion_cleaned(mp['religion'])

    academic_highest_level = parse_academic_highest_level(
        mp['academic_qualifications'],
    )
    if (int)(academic_highest_level[0]) < 6 \
        and mp['profession'] in [
            'Attorney-at-Law',
            'Accountant',
    ]:
        academic_highest_level = '6 Bachelors'

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

        date_of_birth=date_of_birth,
        date_of_birth_ut=date_of_birth_ut,
        date_of_birth_norm=date_of_birth_norm,

        civil_status=mp['civil_status'],
        religion=mp['religion'],
        religion_cleaned=religion_cleaned,
        profession=mp['profession'],

        phone=mp['phone'],
        address=mp['address'],
        phone_sitting=mp['phone_sitting'],
        address_sitting=mp['address_sitting'],
        email=mp['email'],
        source_url=mp['source_url'],

        academic_qualifications=mp['academic_qualifications'],
        academic_highest_level=academic_highest_level,
        professional_qualifications=mp['professional_qualifications'],
    )


def validate(expanded_mp_list):
    subset_list = sorted(list(map(
        lambda mp: [
            mp['academic_highest_level'],
            mp['academic_qualifications'],
            mp['profession'],
        ],
        expanded_mp_list,
    )), key=lambda x: x[0])

    x0_to_list = {}
    for x in subset_list:
        x0 = x[0]
        if x0 not in x0_to_list:
            x0_to_list[x0] = []
        x0_to_list[x0].append(tuple(x[1:]))

    for x0, x_rem_list in sorted(x0_to_list.items(), key=lambda x: x[0]):
        print('-' * 32)
        print(x0, len(x_rem_list))
        for x_rem in list(set(x_rem_list)):
            print('\t', x_rem)


def expand_mps():
    # git = store_mps.git_download()
    mp_list = jsonx.read(store_mps.MP_LIST_JSON_FILE)
    expanded_mp_list = list(map(expand_single_mp, mp_list))

    validate(expanded_mp_list)

    jsonx.write(EXPANDED_MP_LIST_JSON_FILE, expanded_mp_list)
    log.info(f'Wrote {EXPANDED_MP_LIST_JSON_FILE}')
    # git_upload(git)
