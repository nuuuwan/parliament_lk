import os

from utils import jsonx

NA = "NA"

DIR_CABINETS = os.path.join(
    "src/parliament_lk",
    "scrape_and_store/expand_mps_helpers",
    "cabinets"
)


def read_cabinet(cabinet_id):
    return jsonx.read(
        os.path.join(DIR_CABINETS, f'{cabinet_id}.json'),
    )


CABINET_201911 = read_cabinet('201911')
CABINET_202008 = read_cabinet('202008')
CABINET_202204 = read_cabinet('202204')
CABINET_202205 = read_cabinet('202205')


def parse_cabinet_201911(name_cleaned):
    # Source: https://en.wikipedia.org/wiki/First_Gotabaya_Rajapaksa_cabinet
    return CABINET_201911.get(name_cleaned, NA)


def parse_cabinet_202008(name_cleaned):
    # Source: https://en.wikipedia.org/wiki/Second_Gotabaya_Rajapaksa_cabinet
    return CABINET_202008.get(name_cleaned, NA)


def parse_cabinet_202204(name_cleaned):
    # Source: https://en.wikipedia.org/wiki/Third_Gotabaya_Rajapaksa_cabinet
    return CABINET_202204.get(name_cleaned, NA)


def parse_cabinet_202205(name_cleaned):
    # Source:
    # https://www.newsfirst.lk/2022/05/23/sri-lanka-more-cabinet-ministers-appointed/
    return CABINET_202205.get(name_cleaned, NA)
