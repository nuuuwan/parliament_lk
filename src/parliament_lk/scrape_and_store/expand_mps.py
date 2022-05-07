import os
from utils import jsonx
from parliament_lk.scrape_and_store import store_mps
from parliament_lk._utils import log

EXPANDED_MP_LIST_JSON_FILE = os.path.join(
    store_mps.DIR_GIT_DATA, 'expanded_mp_list.json')

# {
#   "url_num": 3266,
#   "name": "Hon. A. Aravindh Kumar, M.P.",
#   "image_url": "https://www.parliament.lk/uploads/images/members/profile_images/thumbs/3266.jpg",
#   "party": "Samagi Jana Balawegaya (SJB)",
#   "electoral_district": "Badulla",
#   "date_of_birth": "17-11-1954",
#   "civil_status": "Married",
#   "religion": "Hindu",
#   "profession": null,
#   "phone": "0777727472",
#   "address": "NO.19,Badulupitiya Road,Badulla.",
#   "phone_sitting": "0552231526",
#   "address_sitting": "NO.271/19, Resta Garden,Muditha Mawatha, Kerawalapitiya, Hendala,Wattala.",
#   "email": "aravindh_k@parliament.lk",
#   "source_url": "https://www.parliament.lk/en/members-of-parliament/directory-of-members/viewMember/3266",
#   "academic_qualifications": "G.C.E Advanced Level",
#   "professional_qualifications": "1. 20 Years experience as an Executive in the Tea Plantation Sector. 2. 10 years experience as a Private Secretary to a Cabinet Minister 3. 10 years as a Member of Uva Provincial Council. 4. 4 1/2 years as a Member of Parliament."
# },


def git_upload(git):
    time_id = timex.get_time_id()
    message = f'[expand_mps] {time_id}'
    git.stage_commit_and_push(message)


def expand_single_mp(mp):
    return mp


def expand_mps():
    # git = store_mps.git_download()
    mp_list = jsonx.read(store_mps.MP_LIST_JSON_FILE)
    expanded_mp_list = list(map(expand_single_mp, mp_list))

    jsonx.write(EXPANDED_MP_LIST_JSON_FILE, expanded_mp_list)
    log.info(f'Wrote {EXPANDED_MP_LIST_JSON_FILE}')
    # git_upload(git)
