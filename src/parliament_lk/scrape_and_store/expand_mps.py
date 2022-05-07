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
    matched_ed = search_ed(electoral_district)
    return matched_ed['ed_id'], matched_ed['name']


def parse_date_of_birth(date_of_birth):
    date_of_birth_ut = timex.parse_time(date_of_birth, '%d-%m-%Y')
    date_of_birth_norm = timex.format_time(date_of_birth_ut, '%Y-%m-%d')
    return date_of_birth_ut, date_of_birth_norm


def expand_single_mp(mp):
    name_cleaned = parse_name_cleaned(mp['name'])
    gender = parse_gender(mp['name'])
    first_names, last_name = parse_first_and_last_names(name_cleaned)
    party_short = parse_party_short(mp['party'])

    date_of_birth = mp['date_of_birth']
    if not date_of_birth:
        date_of_birth = {
            1575: "27-04-1951",  # Basil Rohana Rajapaksa
            3451: "01-10-1971",  # Jagath Kumara Sumithraarachchi
            3364: "07-10-1974",  # Lalith Varna Kumara
        }.get(mp['url_num'])

    if not date_of_birth:
        log.error(str(mp['url_num']) + ' ' + mp['name'])
    date_of_birth_ut, date_of_birth_norm = parse_date_of_birth(date_of_birth)

    if mp['electoral_district'] == 'National List':
        ed_id, ed_name = 'LK', 'National List'
    else:
        ed_id, ed_name = parse_ed_info(mp['electoral_district'])

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
        profession=mp['profession'],

        phone=mp['phone'],
        address=mp['address'],
        phone_sitting=mp['phone_sitting'],
        address_sitting=mp['address_sitting'],
        email=mp['email'],
        source_url=mp['source_url'],

        academic_qualifications=mp['academic_qualifications'],
        professional_qualifications=mp['professional_qualifications'],
    )


def expand_mps():
    # git = store_mps.git_download()
    mp_list = jsonx.read(store_mps.MP_LIST_JSON_FILE)
    expanded_mp_list = list(map(expand_single_mp, mp_list))

    # analysis only
    subset_list = sorted(list(map(
        lambda mp: [
            mp['date_of_birth_norm'],
            mp['date_of_birth_ut'],
            mp['date_of_birth'],
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
        print(x0)
        for x_rem in list(set(x_rem_list)):
            print('\t', x_rem)

    jsonx.write(EXPANDED_MP_LIST_JSON_FILE, expanded_mp_list)
    log.info(f'Wrote {EXPANDED_MP_LIST_JSON_FILE}')
    # git_upload(git)
