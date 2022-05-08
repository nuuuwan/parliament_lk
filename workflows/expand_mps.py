import argparse

from parliament_lk.scrape_and_store import expand_mps


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('prod_mode', type=bool)
    return parser.parse_args()


if __name__ == '__main__':
    options = get_options()
    expand_mps.expand_mps(options.prod_mode)
